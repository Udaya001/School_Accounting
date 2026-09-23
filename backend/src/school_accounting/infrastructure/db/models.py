"""Persistence models for the initial control-plane and tenant foundation slice."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, ForeignKeyConstraint, Index, String, Text, UniqueConstraint, func, text
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
