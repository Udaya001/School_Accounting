"""Persistence models for the initial control-plane and tenant foundation slice."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, CheckConstraint, Date, DateTime, ForeignKey, ForeignKeyConstraint, Index, LargeBinary, String, Text, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import CITEXT, JSONB, ExcludeConstraint, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from school_accounting.infrastructure.db.base import Base


def _uuid() -> UUID:
    return uuid4()


class IdMixin:
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=_uuid, server_default=text("gen_random_uuid()")
    )


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class School(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "schools"
    __table_args__ = (
        CheckConstraint("status IN ('active', 'suspended', 'archived')", name="ck_schools_status"),
        Index("ix_schools_status", "status"),
    )

    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    provisioned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class User(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "users"
    __table_args__ = (Index("ix_users_status", "status"),)

    external_subject: Mapped[str | None] = mapped_column(String(255), unique=True)
    email: Mapped[str | None] = mapped_column(CITEXT, unique=True)
    display_name: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PermissionPreset(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "permission_presets"
    __table_args__ = (
        CheckConstraint("jsonb_typeof(capabilities) = 'array'", name="ck_permission_presets_capabilities_array"),
        Index("ix_permission_presets_status", "status"),
    )

    code: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    capabilities: Mapped[list[object]] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class PlatformAdministratorGrant(IdMixin, Base):
    __tablename__ = "platform_administrator_grants"
    __table_args__ = (
        CheckConstraint("status IN ('active', 'revoked')", name="ck_platform_admin_grants_status"),
        CheckConstraint(
            "(status = 'active' AND revoked_at IS NULL) OR "
            "(status = 'revoked' AND revoked_at IS NOT NULL)",
            name="ck_platform_admin_grants_revocation_consistency",
        ),
        Index(
            "uq_platform_admin_grants_active_user_scope",
            "user_id",
            "scope",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
    )

    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    scope: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PlatformAuditEvent(IdMixin, Base):
    __tablename__ = "platform_audit_events"
    __table_args__ = (
        Index("ix_platform_audit_events_occurred_at", "occurred_at"),
        Index("ix_platform_audit_events_target", "target_type", "target_id"),
    )

    actor_user_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    target_type: Mapped[str] = mapped_column(String(80), nullable=False)
    target_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    metadata_: Mapped[dict[str, object]] = mapped_column("metadata", JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class SchoolMembership(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "school_memberships"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_school_memberships_school_id_id"),
        UniqueConstraint("school_id", "user_id", name="uq_school_memberships_school_id_user_id"),
        CheckConstraint("ended_at IS NULL OR ended_at >= joined_at", name="ck_school_memberships_ended_after_joined"),
        Index("ix_school_memberships_user_status", "user_id", "status"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PermissionAssignment(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "permission_assignments"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_permission_assignments_school_id_id"),
        ForeignKeyConstraint(
            ["school_id", "membership_id"],
            ["school_memberships.school_id", "school_memberships.id"],
            name="fk_permission_assignments_membership_same_school",
        ),
        CheckConstraint("revoked_at IS NULL OR revoked_at >= assigned_at", name="ck_permission_assignments_revoked_after_assigned"),
        Index("ix_permission_assignments_school_membership", "school_id", "membership_id"),
        Index(
            "uq_permission_assignments_active_membership_preset",
            "school_id",
            "membership_id",
            "preset_id",
            unique=True,
            postgresql_where=text("revoked_at IS NULL"),
        ),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    membership_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    preset_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("permission_presets.id"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SchoolSettings(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "school_settings"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_school_settings_school_id_id"),
        UniqueConstraint("school_id", name="uq_school_settings_school_id"),
        CheckConstraint("jsonb_typeof(settings) = 'object'", name="ck_school_settings_object"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    settings: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class FiscalYear(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "fiscal_years"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_fiscal_years_school_id_id"),
        UniqueConstraint("school_id", "code", name="uq_fiscal_years_school_id_code"),
        CheckConstraint("ad_end >= ad_start", name="ck_fiscal_years_ad_range"),
        CheckConstraint("status IN ('planned', 'active', 'closed')", name="ck_fiscal_years_status"),
        ExcludeConstraint(
            ("school_id", "="),
            (text("daterange(ad_start, ad_end, '[]')"), "&&"),
            where=text("status IN ('active', 'closed')"),
            name="ex_fiscal_years_school_active_closed_dates",
        ),
        Index("ix_fiscal_years_school_dates", "school_id", "ad_start", "ad_end"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    bs_start: Mapped[str] = mapped_column(String(16), nullable=False)
    bs_end: Mapped[str] = mapped_column(String(16), nullable=False)
    ad_start: Mapped[date] = mapped_column(Date, nullable=False)
    ad_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SchoolFund(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "school_funds"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_school_funds_school_id_id"),
        UniqueConstraint("school_id", name="uq_school_funds_school_id"),
        CheckConstraint("status IN ('active', 'inactive')", name="ck_school_funds_status"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class RuleSetVersion(IdMixin, Base):
    __tablename__ = "rule_set_versions"
    __table_args__ = (
        UniqueConstraint("rule_key", "version", name="uq_rule_set_versions_rule_key_version"),
        CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_rule_set_versions_effective_range"),
        CheckConstraint("jsonb_typeof(context) = 'object'", name="ck_rule_set_versions_context_object"),
        CheckConstraint("status IN ('draft', 'published', 'retired')", name="ck_rule_set_versions_status"),
        ExcludeConstraint(
            ("rule_key", "="),
            (text("daterange(effective_from, effective_to, '[]')"), "&&"),
            where=text("status = 'published'"),
            name="ex_rule_set_versions_published_effective_dates",
        ),
        Index("ix_rule_set_versions_rule_dates", "rule_key", "effective_from", "effective_to"),
        Index("ix_rule_set_versions_status", "status"),
    )

    rule_key: Mapped[str] = mapped_column(String(120), nullable=False)
    version: Mapped[str] = mapped_column(String(80), nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date)
    context: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    source_ref: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AccountCodeVersion(IdMixin, Base):
    __tablename__ = "account_code_versions"
    __table_args__ = (
        UniqueConstraint("code", "kind", "effective_from", name="uq_account_code_versions_code_kind_effective_from"),
        CheckConstraint("kind IN ('income', 'expense')", name="ck_account_code_versions_kind"),
        CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_account_code_versions_effective_range"),
        CheckConstraint("status IN ('draft', 'published', 'retired')", name="ck_account_code_versions_status"),
        ExcludeConstraint(
            ("code", "="),
            ("kind", "="),
            (text("daterange(effective_from, effective_to, '[]')"), "&&"),
            where=text("status = 'published'"),
            name="ex_account_code_versions_published_effective_dates",
        ),
        Index("ix_account_code_versions_kind_code_dates", "kind", "code", "effective_from"),
    )

    code: Mapped[str] = mapped_column(String(20), nullable=False)
    kind: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    meaning: Mapped[str] = mapped_column(Text, nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date)
    source_ref: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class LedgerAccountDefinition(IdMixin, Base):
    __tablename__ = "ledger_account_definitions"
    __table_args__ = (
        UniqueConstraint("semantic_key", "effective_from", name="uq_ledger_account_definitions_semantic_key_effective_from"),
        CheckConstraint("normal_side IN ('debit', 'credit')", name="ck_ledger_account_definitions_normal_side"),
        CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_ledger_account_definitions_effective_range"),
        CheckConstraint("jsonb_typeof(rule_context) = 'object'", name="ck_ledger_account_definitions_rule_context_object"),
        CheckConstraint("status IN ('draft', 'published', 'retired')", name="ck_ledger_account_definitions_status"),
        ExcludeConstraint(
            ("semantic_key", "="),
            (text("daterange(effective_from, effective_to, '[]')"), "&&"),
            where=text("status = 'published'"),
            name="ex_ledger_account_definitions_published_effective_dates",
        ),
        Index("ix_ledger_account_definitions_semantic_dates", "semantic_key", "effective_from", "effective_to"),
    )

    semantic_key: Mapped[str] = mapped_column(String(120), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    normal_side: Mapped[str] = mapped_column(String(6), nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date)
    rule_context: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class OfficialTemplateVersion(IdMixin, Base):
    __tablename__ = "official_template_versions"
    __table_args__ = (
        UniqueConstraint("template_key", "language", "version", name="uq_official_template_versions_key_language_version"),
        CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_official_template_versions_effective_range"),
        CheckConstraint("status IN ('draft', 'published', 'retired')", name="ck_official_template_versions_status"),
        Index("ix_official_template_versions_key_language_dates", "template_key", "language", "effective_from"),
    )

    template_key: Mapped[str] = mapped_column(String(80), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    version: Mapped[str] = mapped_column(String(80), nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date)
    renderer_ref: Mapped[str] = mapped_column(Text, nullable=False)
    source_ref: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class SupportedLocale(Base):
    __tablename__ = "supported_locales"
    __table_args__ = (CheckConstraint("status IN ('active', 'inactive')", name="ck_supported_locales_status"),)

    code: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class SchoolLedgerAccount(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "school_ledger_accounts"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_school_ledger_accounts_school_id_id"),
        UniqueConstraint("school_id", "account_code", "effective_from", name="uq_school_ledger_accounts_code_effective_from"),
        CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_school_ledger_accounts_effective_range"),
        CheckConstraint("status IN ('active', 'inactive')", name="ck_school_ledger_accounts_status"),
        ExcludeConstraint(
            ("school_id", "="),
            ("account_code", "="),
            (text("daterange(effective_from, effective_to, '[]')"), "&&"),
            where=text("status = 'active'"),
            name="ex_school_ledger_accounts_active_effective_dates",
        ),
        Index("ix_school_ledger_accounts_school_status_effective", "school_id", "status", "effective_from"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    definition_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("ledger_account_definitions.id"))
    account_code: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date)


class Party(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "parties"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_parties_school_id_id"),
        CheckConstraint("contact IS NULL OR jsonb_typeof(contact) = 'object'", name="ck_parties_contact_object"),
        CheckConstraint("status IN ('active', 'inactive')", name="ck_parties_status"),
        Index("uq_parties_school_type_external_ref", "school_id", "party_type", "external_ref", unique=True, postgresql_where=text("external_ref IS NOT NULL")),
        Index("ix_parties_school_type_name", "school_id", "party_type", "name"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    party_type: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    pan: Mapped[str | None] = mapped_column(String(30))
    external_ref: Mapped[str | None] = mapped_column(String(255))
    contact: Mapped[dict[str, object] | None] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class StudentAccount(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "student_accounts"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_student_accounts_school_id_id"),
        CheckConstraint("status IN ('active', 'inactive')", name="ck_student_accounts_status"),
        Index("uq_student_accounts_school_external_ref", "school_id", "external_ref", unique=True, postgresql_where=text("external_ref IS NOT NULL")),
        Index("uq_student_accounts_school_number", "school_id", "student_number", unique=True, postgresql_where=text("student_number IS NOT NULL")),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    external_ref: Mapped[str | None] = mapped_column(String(255))
    student_number: Mapped[str | None] = mapped_column(String(80))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class StaffPerson(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "staff_people"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_staff_people_school_id_id"),
        CheckConstraint("employment_status IN ('active', 'inactive', 'terminated')", name="ck_staff_people_employment_status"),
        Index("uq_staff_people_school_external_ref", "school_id", "external_ref", unique=True, postgresql_where=text("external_ref IS NOT NULL")),
        Index("uq_staff_people_school_number", "school_id", "staff_number", unique=True, postgresql_where=text("staff_number IS NOT NULL")),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    external_ref: Mapped[str | None] = mapped_column(String(255))
    staff_number: Mapped[str | None] = mapped_column(String(80))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    employment_status: Mapped[str] = mapped_column(String(30), nullable=False)
    tax_identifier: Mapped[str | None] = mapped_column(String(80))


class BankAccount(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "bank_accounts"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_bank_accounts_school_id_id"),
        ForeignKeyConstraint(
            ["school_id", "party_id"],
            ["parties.school_id", "parties.id"],
            name="fk_bank_accounts_party_same_school",
        ),
        CheckConstraint("char_length(currency) = 3", name="ck_bank_accounts_currency_length"),
        CheckConstraint("closed_on IS NULL OR opened_on IS NULL OR closed_on >= opened_on", name="ck_bank_accounts_date_range"),
        CheckConstraint("status IN ('active', 'closed')", name="ck_bank_accounts_status"),
        CheckConstraint("status <> 'closed' OR closed_on IS NOT NULL", name="ck_bank_accounts_closed_date"),
        Index("ix_bank_accounts_school_fingerprint", "school_id", "account_identity_fingerprint"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    party_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    account_name: Mapped[str] = mapped_column(Text, nullable=False)
    account_number_masked: Mapped[str | None] = mapped_column(String(80))
    account_identity_fingerprint: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, server_default=text("'NPR'"))
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    opened_on: Mapped[date | None] = mapped_column(Date)
    closed_on: Mapped[date | None] = mapped_column(Date)


class BankAccountLedgerBinding(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "bank_account_ledger_bindings"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_bank_account_ledger_bindings_school_id_id"),
        ForeignKeyConstraint(
            ["school_id", "bank_account_id"],
            ["bank_accounts.school_id", "bank_accounts.id"],
            name="fk_bank_account_ledger_bindings_bank_same_school",
        ),
        ForeignKeyConstraint(
            ["school_id", "ledger_account_id"],
            ["school_ledger_accounts.school_id", "school_ledger_accounts.id"],
            name="fk_bank_account_ledger_bindings_ledger_same_school",
        ),
        CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_bank_account_ledger_bindings_effective_range"),
        ExcludeConstraint(
            ("school_id", "="),
            ("bank_account_id", "="),
            (text("daterange(effective_from, effective_to, '[]')"), "&&"),
            name="ex_bank_account_ledger_bindings_effective_dates",
        ),
        Index("ix_bank_account_ledger_bindings_school_ledger_dates", "school_id", "ledger_account_id", "effective_from"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    bank_account_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    ledger_account_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date)


class DocumentSequence(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "document_sequences"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_document_sequences_school_id_id"),
        UniqueConstraint("school_id", "fiscal_year_id", "sequence_key", name="uq_document_sequences_school_fiscal_key"),
        ForeignKeyConstraint(
            ["school_id", "fiscal_year_id"],
            ["fiscal_years.school_id", "fiscal_years.id"],
            name="fk_document_sequences_fiscal_year_same_school",
        ),
        CheckConstraint("next_value > 0", name="ck_document_sequences_next_value_positive"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    fiscal_year_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    sequence_key: Mapped[str] = mapped_column(String(80), nullable=False)
    next_value: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class ReceiptBook(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "receipt_books"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_receipt_books_school_id_id"),
        UniqueConstraint("school_id", "fiscal_year_id", "book_code", name="uq_receipt_books_school_fiscal_code"),
        ForeignKeyConstraint(
            ["school_id", "fiscal_year_id"],
            ["fiscal_years.school_id", "fiscal_years.id"],
            name="fk_receipt_books_fiscal_year_same_school",
        ),
        CheckConstraint("first_number IS NULL OR first_number > 0", name="ck_receipt_books_first_number_positive"),
        CheckConstraint("last_number IS NULL OR last_number > 0", name="ck_receipt_books_last_number_positive"),
        CheckConstraint("first_number IS NULL OR last_number IS NULL OR last_number >= first_number", name="ck_receipt_books_range"),
        CheckConstraint("status IN ('active', 'closed')", name="ck_receipt_books_status"),
        Index("ix_receipt_books_school_fiscal_status", "school_id", "fiscal_year_id", "status"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    fiscal_year_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    book_code: Mapped[str] = mapped_column(String(80), nullable=False)
    first_number: Mapped[int | None] = mapped_column(BigInteger)
    last_number: Mapped[int | None] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class ReceiptIssue(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "receipt_issues"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_receipt_issues_school_id_id"),
        UniqueConstraint("school_id", "receipt_book_id", "receipt_number", name="uq_receipt_issues_school_book_number"),
        ForeignKeyConstraint(
            ["school_id", "receipt_book_id"],
            ["receipt_books.school_id", "receipt_books.id"],
            name="fk_receipt_issues_book_same_school",
        ),
        ForeignKeyConstraint(
            ["school_id", "replacement_issue_id"],
            ["receipt_issues.school_id", "receipt_issues.id"],
            name="fk_receipt_issues_replacement_same_school",
        ),
        CheckConstraint("receipt_number > 0", name="ck_receipt_issues_number_positive"),
        CheckConstraint("status IN ('reserved', 'issued', 'cancelled', 'spoiled')", name="ck_receipt_issues_status"),
        CheckConstraint("status NOT IN ('cancelled', 'spoiled') OR cancel_reason IS NOT NULL", name="ck_receipt_issues_terminal_reason"),
        CheckConstraint("status <> 'issued' OR issued_at IS NOT NULL", name="ck_receipt_issues_issued_at"),
        CheckConstraint("replacement_issue_id IS NULL OR replacement_issue_id <> id", name="ck_receipt_issues_not_self_replacement"),
        Index("ix_receipt_issues_school_status", "school_id", "status"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    receipt_book_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    receipt_number: Mapped[int] = mapped_column(BigInteger, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancel_reason: Mapped[str | None] = mapped_column(Text)
    replacement_issue_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
