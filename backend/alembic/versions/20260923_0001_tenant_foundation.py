"""Create the control-plane and tenant-foundation schema slice.

Revision ID: 20260923_0001
Revises:
Create Date: 2026-09-23
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260923_0001"
down_revision = None
branch_labels = None
depends_on = None


UUID = postgresql.UUID(as_uuid=True)
TIMESTAMP = sa.DateTime(timezone=True)


def _id_column() -> sa.Column:
    return sa.Column("id", UUID, primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()"))


def _created_at_column() -> sa.Column:
    return sa.Column("created_at", TIMESTAMP, nullable=False, server_default=sa.text("now()"))


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    op.create_table(
        "schools",
        _id_column(),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        _created_at_column(),
        sa.Column("provisioned_at", TIMESTAMP),
        sa.CheckConstraint("status IN ('active', 'suspended', 'archived')", name="ck_schools_status"),
        sa.UniqueConstraint("slug", name="uq_schools_slug"),
    )
    op.create_index("ix_schools_status", "schools", ["status"])

    op.create_table(
        "users",
        _id_column(),
        sa.Column("external_subject", sa.String(255)),
        sa.Column("email", postgresql.CITEXT()),
        sa.Column("display_name", sa.Text()),
        sa.Column("status", sa.String(30), nullable=False),
        _created_at_column(),
        sa.Column("last_seen_at", TIMESTAMP),
        sa.UniqueConstraint("external_subject", name="uq_users_external_subject"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_status", "users", ["status"])

    op.create_table(
        "permission_presets",
        _id_column(),
        sa.Column("code", sa.String(80), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("capabilities", postgresql.JSONB(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        _created_at_column(),
        sa.CheckConstraint("jsonb_typeof(capabilities) = 'array'", name="ck_permission_presets_capabilities_array"),
        sa.UniqueConstraint("code", name="uq_permission_presets_code"),
    )
    op.create_index("ix_permission_presets_status", "permission_presets", ["status"])

    op.create_table(
        "platform_administrator_grants",
        _id_column(),
        sa.Column("user_id", UUID, nullable=False),
        sa.Column("scope", sa.String(50), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("granted_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")),
        sa.Column("revoked_at", TIMESTAMP),
        sa.CheckConstraint("status IN ('active', 'revoked')", name="ck_platform_admin_grants_status"),
        sa.CheckConstraint(
            "(status = 'active' AND revoked_at IS NULL) OR "
            "(status = 'revoked' AND revoked_at IS NOT NULL)",
            name="ck_platform_admin_grants_revocation_consistency",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index(
        "uq_platform_admin_grants_active_user_scope", "platform_administrator_grants", ["user_id", "scope"],
        unique=True, postgresql_where=sa.text("status = 'active'"),
    )

    op.create_table(
        "platform_audit_events",
        _id_column(),
        sa.Column("actor_user_id", UUID),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("target_type", sa.String(80), nullable=False),
        sa.Column("target_id", UUID),
        sa.Column("metadata", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("occurred_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"]),
    )
    op.create_index("ix_platform_audit_events_occurred_at", "platform_audit_events", ["occurred_at"])
    op.create_index("ix_platform_audit_events_target", "platform_audit_events", ["target_type", "target_id"])
    op.execute(
        """
        CREATE OR REPLACE FUNCTION reject_immutable_row_change()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RAISE EXCEPTION 'Rows in % are append-only', TG_TABLE_NAME
                USING ERRCODE = '55000';
        END;
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_platform_audit_events_immutable
        BEFORE UPDATE OR DELETE ON platform_audit_events
        FOR EACH ROW EXECUTE FUNCTION reject_immutable_row_change()
        """
    )

    op.create_table(
        "school_memberships",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("user_id", UUID, nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        _created_at_column(),
        sa.Column("joined_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")),
        sa.Column("ended_at", TIMESTAMP),
        sa.CheckConstraint("ended_at IS NULL OR ended_at >= joined_at", name="ck_school_memberships_ended_after_joined"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_school_memberships_school_id_id"),
        sa.UniqueConstraint("school_id", "user_id", name="uq_school_memberships_school_id_user_id"),
    )
    op.create_index("ix_school_memberships_user_status", "school_memberships", ["user_id", "status"])

    op.create_table(
        "permission_assignments",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("membership_id", UUID, nullable=False),
        sa.Column("preset_id", UUID, nullable=False),
        _created_at_column(),
        sa.Column("assigned_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")),
        sa.Column("revoked_at", TIMESTAMP),
        sa.CheckConstraint("revoked_at IS NULL OR revoked_at >= assigned_at", name="ck_permission_assignments_revoked_after_assigned"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["preset_id"], ["permission_presets.id"]),
        sa.ForeignKeyConstraint(
            ["school_id", "membership_id"],
            ["school_memberships.school_id", "school_memberships.id"],
            name="fk_permission_assignments_membership_same_school",
        ),
        sa.UniqueConstraint("school_id", "id", name="uq_permission_assignments_school_id_id"),
    )
    op.create_index("ix_permission_assignments_school_membership", "permission_assignments", ["school_id", "membership_id"])
    op.create_index(
        "uq_permission_assignments_active_membership_preset", "permission_assignments",
        ["school_id", "membership_id", "preset_id"], unique=True, postgresql_where=sa.text("revoked_at IS NULL"),
    )

    op.create_table(
        "school_settings",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("settings", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        _created_at_column(),
        sa.Column("updated_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("jsonb_typeof(settings) = 'object'", name="ck_school_settings_object"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_school_settings_school_id_id"),
        sa.UniqueConstraint("school_id", name="uq_school_settings_school_id"),
    )

    op.create_table(
        "fiscal_years",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("bs_start", sa.String(16), nullable=False),
        sa.Column("bs_end", sa.String(16), nullable=False),
        sa.Column("ad_start", sa.Date(), nullable=False),
        sa.Column("ad_end", sa.Date(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        _created_at_column(),
        sa.Column("closed_at", TIMESTAMP),
        sa.CheckConstraint("ad_end >= ad_start", name="ck_fiscal_years_ad_range"),
        sa.CheckConstraint("status IN ('planned', 'active', 'closed')", name="ck_fiscal_years_status"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_fiscal_years_school_id_id"),
        sa.UniqueConstraint("school_id", "code", name="uq_fiscal_years_school_id_code"),
        postgresql.ExcludeConstraint(
            ("school_id", "="),
            (sa.text("daterange(ad_start, ad_end, '[]')"), "&&"),
            where=sa.text("status IN ('active', 'closed')"),
            name="ex_fiscal_years_school_active_closed_dates",
        ),
    )
    op.create_index("ix_fiscal_years_school_dates", "fiscal_years", ["school_id", "ad_start", "ad_end"])

    op.create_table(
        "school_funds",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        _created_at_column(),
        sa.CheckConstraint("status IN ('active', 'inactive')", name="ck_school_funds_status"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_school_funds_school_id_id"),
        sa.UniqueConstraint("school_id", name="uq_school_funds_school_id"),
    )


def downgrade() -> None:
    op.drop_table("school_funds")
    op.drop_index("ix_fiscal_years_school_dates", table_name="fiscal_years")
    op.drop_table("fiscal_years")
    op.drop_table("school_settings")
    op.drop_index("uq_permission_assignments_active_membership_preset", table_name="permission_assignments")
    op.drop_index("ix_permission_assignments_school_membership", table_name="permission_assignments")
    op.drop_table("permission_assignments")
    op.drop_index("ix_school_memberships_user_status", table_name="school_memberships")
    op.drop_table("school_memberships")
    op.execute("DROP TRIGGER IF EXISTS trg_platform_audit_events_immutable ON platform_audit_events")
    op.drop_index("ix_platform_audit_events_target", table_name="platform_audit_events")
    op.drop_index("ix_platform_audit_events_occurred_at", table_name="platform_audit_events")
    op.drop_table("platform_audit_events")
    op.execute("DROP FUNCTION IF EXISTS reject_immutable_row_change()")
    op.drop_index("uq_platform_admin_grants_active_user_scope", table_name="platform_administrator_grants")
    op.drop_table("platform_administrator_grants")
    op.drop_index("ix_permission_presets_status", table_name="permission_presets")
    op.drop_table("permission_presets")
    op.drop_index("ix_users_status", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_schools_status", table_name="schools")
    op.drop_table("schools")
