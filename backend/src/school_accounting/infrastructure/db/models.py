"""Persistence models for the initial control-plane and tenant foundation slice."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, CheckConstraint, Date, DateTime, ForeignKey, ForeignKeyConstraint, Index, LargeBinary, Numeric, String, Text, UniqueConstraint, func, text
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
    preferred_locale: Mapped[str | None] = mapped_column(String(10), ForeignKey("supported_locales.code"))
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
    default_locale: Mapped[str] = mapped_column(String(10), ForeignKey("supported_locales.code"), nullable=False, server_default=text("'en'"))
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


class AccountCodeVersionTranslation(IdMixin, Base):
    __tablename__ = "account_code_version_translations"
    __table_args__ = (
        UniqueConstraint("account_code_version_id", "locale", name="uq_account_code_version_translations_record_locale"),
    )

    account_code_version_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("account_code_versions.id"), nullable=False)
    locale: Mapped[str] = mapped_column(String(10), ForeignKey("supported_locales.code"), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    meaning: Mapped[str] = mapped_column(Text, nullable=False)


class LedgerAccountDefinitionTranslation(IdMixin, Base):
    __tablename__ = "ledger_account_definition_translations"
    __table_args__ = (
        UniqueConstraint("ledger_account_definition_id", "locale", name="uq_ledger_account_definition_translations_record_locale"),
    )

    ledger_account_definition_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("ledger_account_definitions.id"), nullable=False)
    locale: Mapped[str] = mapped_column(String(10), ForeignKey("supported_locales.code"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class PermissionPresetTranslation(IdMixin, Base):
    __tablename__ = "permission_preset_translations"
    __table_args__ = (
        UniqueConstraint("permission_preset_id", "locale", name="uq_permission_preset_translations_record_locale"),
    )

    permission_preset_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("permission_presets.id"), nullable=False)
    locale: Mapped[str] = mapped_column(String(10), ForeignKey("supported_locales.code"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)


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


class FinancialDocument(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "financial_documents"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_financial_documents_school_id_id"),
        ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_financial_documents_fiscal_year_same_school"),
        ForeignKeyConstraint(["school_id", "party_id"], ["parties.school_id", "parties.id"], name="fk_financial_documents_party_same_school"),
        ForeignKeyConstraint(["school_id", "bank_account_id"], ["bank_accounts.school_id", "bank_accounts.id"], name="fk_financial_documents_bank_account_same_school"),
        CheckConstraint("status IN ('draft', 'returned', 'submitted', 'verified', 'approved', 'posted', 'locked')", name="ck_financial_documents_status"),
        CheckConstraint("status NOT IN ('approved', 'posted', 'locked') OR approved_at IS NOT NULL", name="ck_financial_documents_approved_at"),
        CheckConstraint("status NOT IN ('posted', 'locked') OR posted_at IS NOT NULL", name="ck_financial_documents_posted_at"),
        CheckConstraint("status <> 'locked' OR locked_at IS NOT NULL", name="ck_financial_documents_locked_at"),
        Index("uq_financial_documents_school_fiscal_type_number", "school_id", "fiscal_year_id", "document_type", "document_number", unique=True, postgresql_where=text("document_number IS NOT NULL")),
        Index("ix_financial_documents_school_status_date", "school_id", "status", "accounting_date"),
        Index("ix_financial_documents_school_fiscal_type", "school_id", "fiscal_year_id", "document_type"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    document_number: Mapped[str | None] = mapped_column(String(100))
    fiscal_year_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    accounting_date: Mapped[date] = mapped_column(Date, nullable=False)
    entered_bs_date: Mapped[str | None] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    party_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    bank_account_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    summary: Mapped[str | None] = mapped_column(Text)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class FinancialDocumentItem(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "financial_document_items"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_financial_document_items_school_id_id"),
        UniqueConstraint("school_id", "document_id", "line_no", name="uq_financial_document_items_school_document_line"),
        ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_financial_document_items_document_same_school"),
        ForeignKeyConstraint(["school_id", "student_account_id"], ["student_accounts.school_id", "student_accounts.id"], name="fk_financial_document_items_student_same_school"),
        ForeignKeyConstraint(["school_id", "staff_person_id"], ["staff_people.school_id", "staff_people.id"], name="fk_financial_document_items_staff_same_school"),
        ForeignKeyConstraint(["school_id", "party_id"], ["parties.school_id", "parties.id"], name="fk_financial_document_items_party_same_school"),
        CheckConstraint("line_no > 0", name="ck_financial_document_items_line_no_positive"),
        CheckConstraint("amount >= 0", name="ck_financial_document_items_amount_nonnegative"),
        CheckConstraint("jsonb_typeof(facts) = 'object'", name="ck_financial_document_items_facts_object"),
        Index("ix_financial_document_items_school_document", "school_id", "document_id"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    line_no: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    account_code_version_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("account_code_versions.id"))
    student_account_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    staff_person_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    party_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    facts: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))


class IncomeReceipt(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "income_receipts"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_income_receipts_school_id_id"),
        UniqueConstraint("school_id", "document_id", name="uq_income_receipts_school_document"),
        UniqueConstraint("school_id", "receipt_issue_id", name="uq_income_receipts_school_receipt_issue"),
        ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_income_receipts_document_same_school"),
        ForeignKeyConstraint(["school_id", "receipt_issue_id"], ["receipt_issues.school_id", "receipt_issues.id"], name="fk_income_receipts_receipt_issue_same_school"),
        ForeignKeyConstraint(["school_id", "student_account_id"], ["student_accounts.school_id", "student_accounts.id"], name="fk_income_receipts_student_same_school"),
        ForeignKeyConstraint(["school_id", "payer_party_id"], ["parties.school_id", "parties.id"], name="fk_income_receipts_payer_same_school"),
        Index("ix_income_receipts_school_student_date", "school_id", "student_account_id", "receipt_date"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    receipt_issue_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    student_account_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    payer_party_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    receipt_date: Mapped[date] = mapped_column(Date, nullable=False)


class LifecycleEvent(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "lifecycle_events"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_lifecycle_events_school_id_id"),
        Index("ix_lifecycle_events_school_target_time", "school_id", "entity_type", "entity_id", "occurred_at"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    from_status: Mapped[str | None] = mapped_column(String(30))
    to_status: Mapped[str] = mapped_column(String(30), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class AuthorizationDecision(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "authorization_decisions"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_authorization_decisions_school_id_id"),
        ForeignKeyConstraint(["school_id", "actor_membership_id"], ["school_memberships.school_id", "school_memberships.id"], name="fk_authorization_decisions_actor_same_school"),
        CheckConstraint("jsonb_typeof(evidence_metadata) = 'object'", name="ck_authorization_decisions_evidence_metadata_object"),
        Index("ix_authorization_decisions_school_target_time", "school_id", "target_type", "target_id", "decided_at"),
        Index("ix_authorization_decisions_school_actor_time", "school_id", "actor_membership_id", "decided_at"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    actor_membership_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    target_type: Mapped[str] = mapped_column(String(80), nullable=False)
    target_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    decision_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    reason: Mapped[str | None] = mapped_column(Text)
    evidence_metadata: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))


class AuditEvent(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "audit_events"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_audit_events_school_id_id"),
        ForeignKeyConstraint(["school_id", "actor_membership_id"], ["school_memberships.school_id", "school_memberships.id"], name="fk_audit_events_actor_same_school"),
        CheckConstraint("jsonb_typeof(metadata) = 'object'", name="ck_audit_events_metadata_object"),
        Index("ix_audit_events_school_target_time", "school_id", "target_type", "target_id", "occurred_at"),
        Index("ix_audit_events_school_actor_time", "school_id", "actor_membership_id", "occurred_at"),
        Index("ix_audit_events_school_action_time", "school_id", "action", "occurred_at"),
    )

    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    actor_membership_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    target_type: Mapped[str] = mapped_column(String(80), nullable=False)
    target_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    outcome: Mapped[str | None] = mapped_column(String(30))
    metadata_: Mapped[dict[str, object]] = mapped_column("metadata", JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class PayrollRun(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "payroll_runs"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_payroll_runs_school_id_id"), UniqueConstraint("school_id", "document_id", name="uq_payroll_runs_school_document"), ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_payroll_runs_document_same_school"), CheckConstraint("period_end >= period_start", name="ck_payroll_runs_period_range"), CheckConstraint("status IN ('draft', 'verified', 'approved', 'posted')", name="ck_payroll_runs_status"), Index("ix_payroll_runs_school_period", "school_id", "period_start", "period_end"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class PayrollRunItem(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "payroll_run_items"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_payroll_run_items_school_id_id"), UniqueConstraint("school_id", "payroll_run_id", "line_no", name="uq_payroll_run_items_school_run_line"), ForeignKeyConstraint(["school_id", "payroll_run_id"], ["payroll_runs.school_id", "payroll_runs.id"], name="fk_payroll_run_items_run_same_school"), ForeignKeyConstraint(["school_id", "staff_person_id"], ["staff_people.school_id", "staff_people.id"], name="fk_payroll_run_items_staff_same_school"), CheckConstraint("line_no > 0", name="ck_payroll_run_items_line_no_positive"), CheckConstraint("gross_amount >= 0", name="ck_payroll_run_items_gross_nonnegative"), CheckConstraint("jsonb_typeof(deduction_facts) = 'object'", name="ck_payroll_run_items_deduction_facts_object"), Index("ix_payroll_run_items_school_staff", "school_id", "staff_person_id"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    payroll_run_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    line_no: Mapped[int] = mapped_column(nullable=False)
    staff_person_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    gross_amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    deduction_facts: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))


class Advance(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "advances"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_advances_school_id_id"), UniqueConstraint("school_id", "document_id", name="uq_advances_school_document"), ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_advances_document_same_school"), ForeignKeyConstraint(["school_id", "recipient_party_id"], ["parties.school_id", "parties.id"], name="fk_advances_recipient_same_school"), CheckConstraint("amount >= 0", name="ck_advances_amount_nonnegative"), CheckConstraint("status IN ('draft', 'approved', 'settled', 'cancelled')", name="ck_advances_status"), Index("ix_advances_school_status", "school_id", "status"), Index("ix_advances_school_recipient", "school_id", "recipient_party_id"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    recipient_party_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class AdvanceSettlement(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "advance_settlements"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_advance_settlements_school_id_id"), UniqueConstraint("school_id", "document_id", name="uq_advance_settlements_school_document"), ForeignKeyConstraint(["school_id", "advance_id"], ["advances.school_id", "advances.id"], name="fk_advance_settlements_advance_same_school"), ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_advance_settlements_document_same_school"), CheckConstraint("amount >= 0", name="ck_advance_settlements_amount_nonnegative"), Index("ix_advance_settlements_school_advance", "school_id", "advance_id"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    advance_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    settled_on: Mapped[date] = mapped_column(Date, nullable=False)


class Deposit(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "deposits"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_deposits_school_id_id"), UniqueConstraint("school_id", "document_id", name="uq_deposits_school_document"), ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_deposits_document_same_school"), ForeignKeyConstraint(["school_id", "depositor_party_id"], ["parties.school_id", "parties.id"], name="fk_deposits_depositor_same_school"), CheckConstraint("amount >= 0", name="ck_deposits_amount_nonnegative"), CheckConstraint("status IN ('active', 'refunded', 'forfeited')", name="ck_deposits_status"), Index("ix_deposits_school_status", "school_id", "status"), Index("ix_deposits_school_depositor", "school_id", "depositor_party_id"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    depositor_party_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class DepositRefund(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "deposit_refunds"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_deposit_refunds_school_id_id"), UniqueConstraint("school_id", "document_id", name="uq_deposit_refunds_school_document"), ForeignKeyConstraint(["school_id", "deposit_id"], ["deposits.school_id", "deposits.id"], name="fk_deposit_refunds_deposit_same_school"), ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_deposit_refunds_document_same_school"), CheckConstraint("amount >= 0", name="ck_deposit_refunds_amount_nonnegative"), Index("ix_deposit_refunds_school_deposit", "school_id", "deposit_id"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    deposit_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)


class TravelOrder(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "travel_orders"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_travel_orders_school_id_id"), UniqueConstraint("school_id", "document_id", name="uq_travel_orders_school_document"), ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_travel_orders_document_same_school"), ForeignKeyConstraint(["school_id", "traveller_party_id"], ["parties.school_id", "parties.id"], name="fk_travel_orders_traveller_same_school"), CheckConstraint("to_date IS NULL OR from_date IS NULL OR to_date >= from_date", name="ck_travel_orders_date_range"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    traveller_party_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    from_date: Mapped[date | None] = mapped_column(Date)
    to_date: Mapped[date | None] = mapped_column(Date)
    purpose: Mapped[str | None] = mapped_column(Text)


class TravelClaim(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "travel_claims"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_travel_claims_school_id_id"), UniqueConstraint("school_id", "document_id", name="uq_travel_claims_school_document"), ForeignKeyConstraint(["school_id", "travel_order_id"], ["travel_orders.school_id", "travel_orders.id"], name="fk_travel_claims_order_same_school"), ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_travel_claims_document_same_school"), CheckConstraint("amount >= 0", name="ck_travel_claims_amount_nonnegative"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    travel_order_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    report_submitted_on: Mapped[date | None] = mapped_column(Date)


class PettyCashEntry(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "petty_cash_entries"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_petty_cash_entries_school_id_id"), UniqueConstraint("school_id", "document_id", name="uq_petty_cash_entries_school_document"), ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_petty_cash_entries_document_same_school"), CheckConstraint("amount >= 0", name="ck_petty_cash_entries_amount_nonnegative"), CheckConstraint("entry_kind IN ('spending', 'replenishment')", name="ck_petty_cash_entries_kind"), Index("ix_petty_cash_entries_school_fund_date", "school_id", "fund_date"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    entry_kind: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    fund_date: Mapped[date] = mapped_column(Date, nullable=False)


class BankStatement(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "bank_statements"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_bank_statements_school_id_id"), UniqueConstraint("school_id", "bank_account_id", "period_start", "period_end", name="uq_bank_statements_school_account_period"), ForeignKeyConstraint(["school_id", "bank_account_id"], ["bank_accounts.school_id", "bank_accounts.id"], name="fk_bank_statements_account_same_school"), ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_bank_statements_fiscal_year_same_school"), CheckConstraint("period_end >= period_start", name="ck_bank_statements_period_range"), CheckConstraint("status IN ('draft', 'verified')", name="ck_bank_statements_status"), Index("ix_bank_statements_school_account_period", "school_id", "bank_account_id", "period_start", "period_end"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    bank_account_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    fiscal_year_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    closing_balance: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class BankStatementLine(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "bank_statement_lines"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_bank_statement_lines_school_id_id"), UniqueConstraint("school_id", "statement_id", "line_no", name="uq_bank_statement_lines_school_statement_line"), ForeignKeyConstraint(["school_id", "statement_id"], ["bank_statements.school_id", "bank_statements.id"], name="fk_bank_statement_lines_statement_same_school"), CheckConstraint("line_no > 0", name="ck_bank_statement_lines_line_no_positive"), Index("uq_bank_statement_lines_school_statement_external_ref", "school_id", "statement_id", "external_line_ref", unique=True, postgresql_where=text("external_line_ref IS NOT NULL")), Index("ix_bank_statement_lines_school_statement", "school_id", "statement_id"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    statement_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    line_no: Mapped[int] = mapped_column(nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    external_line_ref: Mapped[str | None] = mapped_column(String(160))


class BankReconciliation(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "bank_reconciliations"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_bank_reconciliations_school_id_id"), UniqueConstraint("school_id", "statement_id", name="uq_bank_reconciliations_school_statement"), ForeignKeyConstraint(["school_id", "bank_account_id"], ["bank_accounts.school_id", "bank_accounts.id"], name="fk_bank_reconciliations_account_same_school"), ForeignKeyConstraint(["school_id", "statement_id"], ["bank_statements.school_id", "bank_statements.id"], name="fk_bank_reconciliations_statement_same_school"), ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_bank_reconciliations_fiscal_year_same_school"), CheckConstraint("status IN ('draft', 'reconciled')", name="ck_bank_reconciliations_status"), Index("ix_bank_reconciliations_school_account_status", "school_id", "bank_account_id", "status"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    bank_account_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    statement_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    fiscal_year_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    as_of_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class BankReconciliationItem(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "bank_reconciliation_items"
    __table_args__ = (UniqueConstraint("school_id", "id", name="uq_bank_reconciliation_items_school_id_id"), ForeignKeyConstraint(["school_id", "reconciliation_id"], ["bank_reconciliations.school_id", "bank_reconciliations.id"], name="fk_bank_reconciliation_items_reconciliation_same_school"), ForeignKeyConstraint(["school_id", "statement_line_id"], ["bank_statement_lines.school_id", "bank_statement_lines.id"], name="fk_bank_reconciliation_items_statement_line_same_school"), ForeignKeyConstraint(["school_id", "journal_line_id"], ["journal_lines.school_id", "journal_lines.id"], name="fk_bank_reconciliation_items_journal_line_same_school"), ForeignKeyConstraint(["school_id", "source_document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_bank_reconciliation_items_source_document_same_school"), CheckConstraint("status IN ('unmatched', 'exception', 'confirmed')", name="ck_bank_reconciliation_items_status"), Index("ix_bank_reconciliation_items_school_reconciliation", "school_id", "reconciliation_id"))
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    reconciliation_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    statement_line_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    journal_line_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    source_document_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    difference_amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class PostingRequest(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "posting_requests"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_posting_requests_school_id_id"),
        UniqueConstraint("school_id", "idempotency_key", name="uq_posting_requests_school_idempotency_key"),
        ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_posting_requests_document_same_school"),
        ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_posting_requests_fiscal_year_same_school"),
        CheckConstraint("status IN ('pending', 'succeeded', 'failed')", name="ck_posting_requests_status"),
        CheckConstraint("(status = 'pending' AND finalized_at IS NULL) OR (status IN ('succeeded', 'failed') AND finalized_at IS NOT NULL)", name="ck_posting_requests_finalized_consistency"),
        Index("ix_posting_requests_school_status_requested", "school_id", "status", "requested_at"),
        Index("uq_posting_requests_school_document_active", "school_id", "document_id", unique=True, postgresql_where=text("status IN ('pending', 'succeeded')")),
    )
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    fiscal_year_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    accounting_date: Mapped[date] = mapped_column(Date, nullable=False)
    rule_set_version_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("rule_set_versions.id"), nullable=False)
    idempotency_key: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    finalized_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PostingResult(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "posting_results"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_posting_results_school_id_id"),
        UniqueConstraint("school_id", "posting_request_id", name="uq_posting_results_school_request"),
        ForeignKeyConstraint(["school_id", "posting_request_id"], ["posting_requests.school_id", "posting_requests.id"], name="fk_posting_results_request_same_school"),
        CheckConstraint("jsonb_typeof(rule_context) = 'object'", name="ck_posting_results_rule_context_object"),
        CheckConstraint("jsonb_typeof(account_code_context) = 'object'", name="ck_posting_results_account_code_context_object"),
        Index("ix_posting_results_school_result_hash", "school_id", "result_hash"),
        Index("ix_posting_results_derived_at", "derived_at"),
    )
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    posting_request_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    rule_context: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    account_code_context: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
    result_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    derived_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class JournalEntry(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "journal_entries"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_journal_entries_school_id_id"),
        UniqueConstraint("school_id", "posting_result_id", name="uq_journal_entries_school_result"),
        ForeignKeyConstraint(["school_id", "posting_result_id"], ["posting_results.school_id", "posting_results.id"], name="fk_journal_entries_result_same_school"),
        ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_journal_entries_fiscal_year_same_school"),
        Index("ix_journal_entries_school_fiscal_date", "school_id", "fiscal_year_id", "accounting_date"),
        Index("ix_journal_entries_posted_at", "posted_at"),
        Index("ix_journal_entries_school_entry_hash", "school_id", "entry_hash"),
    )
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    posting_result_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    fiscal_year_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    accounting_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    posted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    entry_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)


class JournalLine(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "journal_lines"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_journal_lines_school_id_id"),
        UniqueConstraint("school_id", "journal_entry_id", "line_no", name="uq_journal_lines_school_entry_line"),
        ForeignKeyConstraint(["school_id", "journal_entry_id"], ["journal_entries.school_id", "journal_entries.id"], name="fk_journal_lines_entry_same_school"),
        ForeignKeyConstraint(["school_id", "ledger_account_id"], ["school_ledger_accounts.school_id", "school_ledger_accounts.id"], name="fk_journal_lines_ledger_same_school"),
        CheckConstraint("line_no > 0", name="ck_journal_lines_line_no_positive"),
        CheckConstraint("(debit_amount > 0 AND credit_amount = 0) OR (credit_amount > 0 AND debit_amount = 0)", name="ck_journal_lines_exactly_one_positive_side"),
        CheckConstraint("jsonb_typeof(classification_context) = 'object'", name="ck_journal_lines_classification_context_object"),
        Index("ix_journal_lines_school_ledger", "school_id", "ledger_account_id"),
        Index("ix_journal_lines_account_code_version", "account_code_version_id"),
    )
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    journal_entry_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    line_no: Mapped[int] = mapped_column(nullable=False)
    ledger_account_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    account_code_version_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("account_code_versions.id"))
    debit_amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False, server_default=text("0"))
    credit_amount: Mapped[object] = mapped_column(Numeric(18, 2), nullable=False, server_default=text("0"))
    classification_context: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))


class CorrectionLink(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "correction_links"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_correction_links_school_id_id"),
        UniqueConstraint("school_id", "correcting_document_id", name="uq_correction_links_school_correcting_document"),
        ForeignKeyConstraint(["school_id", "original_document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_correction_links_original_document_same_school"),
        ForeignKeyConstraint(["school_id", "correcting_document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_correction_links_correcting_document_same_school"),
        ForeignKeyConstraint(["school_id", "original_entry_id"], ["journal_entries.school_id", "journal_entries.id"], name="fk_correction_links_original_entry_same_school"),
        ForeignKeyConstraint(["school_id", "correcting_entry_id"], ["journal_entries.school_id", "journal_entries.id"], name="fk_correction_links_correcting_entry_same_school"),
        CheckConstraint("original_document_id <> correcting_document_id", name="ck_correction_links_not_self_document"),
        CheckConstraint("original_entry_id IS NOT NULL AND correcting_entry_id IS NOT NULL AND original_entry_id <> correcting_entry_id", name="ck_correction_links_entries"),
        CheckConstraint("correction_type IN ('reversal', 'adjustment', 'replacement')", name="ck_correction_links_type"),
        Index("ix_correction_links_school_original_document", "school_id", "original_document_id"),
        Index("ix_correction_links_school_original_entry", "school_id", "original_entry_id"),
    )
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    original_document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    correcting_document_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    original_entry_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    correcting_entry_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    correction_type: Mapped[str] = mapped_column(String(30), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    linked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class IdempotencyRecord(IdMixin, CreatedAtMixin, Base):
    __tablename__ = "idempotency_records"
    __table_args__ = (
        UniqueConstraint("school_id", "id", name="uq_idempotency_records_school_id_id"),
        UniqueConstraint("school_id", "operation_key", name="uq_idempotency_records_school_operation_key"),
        ForeignKeyConstraint(["school_id", "posting_request_id"], ["posting_requests.school_id", "posting_requests.id"], name="fk_idempotency_records_request_same_school"),
        CheckConstraint("result_status IN ('in_progress', 'completed', 'failed')", name="ck_idempotency_records_status"),
        CheckConstraint("(result_status = 'in_progress' AND completed_at IS NULL) OR (result_status IN ('completed', 'failed') AND completed_at IS NOT NULL)", name="ck_idempotency_records_completion_consistency"),
        Index("ix_idempotency_records_school_fingerprint", "school_id", "request_fingerprint"),
        Index("ix_idempotency_records_completion", "completed_at"),
    )
    school_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    operation_key: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    request_fingerprint: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    posting_request_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    result_status: Mapped[str] = mapped_column(String(30), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
