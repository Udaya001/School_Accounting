"""Add locale preferences and system reference translations.

Revision ID: 20260924_0006
Revises: 20260924_0005
Create Date: 2026-09-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260924_0006"
down_revision = "20260924_0005"
branch_labels = None
depends_on = None

UUID = postgresql.UUID(as_uuid=True)


def _id() -> sa.Column:
    return sa.Column("id", UUID, primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()"))


def upgrade() -> None:
    locales = sa.table(
        "supported_locales",
        sa.column("code", sa.String(10)),
        sa.column("name", sa.Text()),
        sa.column("status", sa.String(30)),
    )
    op.get_bind().execute(
        postgresql.insert(locales).values(
            [
                {"code": "en", "name": "English", "status": "active"},
                {"code": "ne", "name": "नेपाली", "status": "active"},
            ]
        ).on_conflict_do_update(
            index_elements=["code"],
            set_={"name": postgresql.insert(locales).excluded.name, "status": "active"},
        )
    )

    op.add_column("school_settings", sa.Column("default_locale", sa.String(10), nullable=False, server_default=sa.text("'en'")))
    op.create_foreign_key("fk_school_settings_default_locale", "school_settings", "supported_locales", ["default_locale"], ["code"])
    op.add_column("school_memberships", sa.Column("preferred_locale", sa.String(10), nullable=True))
    op.create_foreign_key("fk_school_memberships_preferred_locale", "school_memberships", "supported_locales", ["preferred_locale"], ["code"])

    op.create_table(
        "account_code_version_translations",
        _id(),
        sa.Column("account_code_version_id", UUID, nullable=False),
        sa.Column("locale", sa.String(10), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("meaning", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["account_code_version_id"], ["account_code_versions.id"], name="fk_account_code_version_translations_canonical"),
        sa.ForeignKeyConstraint(["locale"], ["supported_locales.code"], name="fk_account_code_version_translations_locale"),
        sa.UniqueConstraint("account_code_version_id", "locale", name="uq_account_code_version_translations_record_locale"),
    )
    op.create_table(
        "ledger_account_definition_translations",
        _id(),
        sa.Column("ledger_account_definition_id", UUID, nullable=False),
        sa.Column("locale", sa.String(10), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["ledger_account_definition_id"], ["ledger_account_definitions.id"], name="fk_ledger_account_definition_translations_canonical"),
        sa.ForeignKeyConstraint(["locale"], ["supported_locales.code"], name="fk_ledger_account_definition_translations_locale"),
        sa.UniqueConstraint("ledger_account_definition_id", "locale", name="uq_ledger_account_definition_translations_record_locale"),
    )
    op.create_table(
        "permission_preset_translations",
        _id(),
        sa.Column("permission_preset_id", UUID, nullable=False),
        sa.Column("locale", sa.String(10), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["permission_preset_id"], ["permission_presets.id"], name="fk_permission_preset_translations_canonical"),
        sa.ForeignKeyConstraint(["locale"], ["supported_locales.code"], name="fk_permission_preset_translations_locale"),
        sa.UniqueConstraint("permission_preset_id", "locale", name="uq_permission_preset_translations_record_locale"),
    )


def downgrade() -> None:
    op.drop_table("permission_preset_translations")
    op.drop_table("ledger_account_definition_translations")
    op.drop_table("account_code_version_translations")
    op.drop_constraint("fk_school_memberships_preferred_locale", "school_memberships", type_="foreignkey")
    op.drop_column("school_memberships", "preferred_locale")
    op.drop_constraint("fk_school_settings_default_locale", "school_settings", type_="foreignkey")
    op.drop_column("school_settings", "default_locale")
