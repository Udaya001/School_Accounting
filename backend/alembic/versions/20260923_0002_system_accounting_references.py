"""Create system accounting and reference tables.

Revision ID: 20260923_0002
Revises: 20260923_0001
Create Date: 2026-09-23
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260923_0002"
down_revision = "20260923_0001"
branch_labels = None
depends_on = None


UUID = postgresql.UUID(as_uuid=True)


def _id_column() -> sa.Column:
    return sa.Column("id", UUID, primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()"))


def _published_immutable_trigger(table_name: str) -> None:
    op.execute(
        f"""
        CREATE TRIGGER trg_{table_name}_published_immutable
        BEFORE UPDATE OR DELETE ON {table_name}
        FOR EACH ROW WHEN (OLD.status = 'published')
        EXECUTE FUNCTION reject_immutable_row_change()
        """
    )


def upgrade() -> None:
    op.create_table(
        "rule_set_versions",
        _id_column(),
        sa.Column("rule_key", sa.String(120), nullable=False),
        sa.Column("version", sa.String(80), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date()),
        sa.Column("context", postgresql.JSONB(), nullable=False),
        sa.Column("source_ref", sa.Text()),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_rule_set_versions_effective_range"),
        sa.CheckConstraint("jsonb_typeof(context) = 'object'", name="ck_rule_set_versions_context_object"),
        sa.CheckConstraint("status IN ('draft', 'published', 'retired')", name="ck_rule_set_versions_status"),
        sa.UniqueConstraint("rule_key", "version", name="uq_rule_set_versions_rule_key_version"),
        postgresql.ExcludeConstraint(
            ("rule_key", "="),
            (sa.text("daterange(effective_from, effective_to, '[]')"), "&&"),
            where=sa.text("status = 'published'"),
            name="ex_rule_set_versions_published_effective_dates",
        ),
    )
    op.create_index("ix_rule_set_versions_rule_dates", "rule_set_versions", ["rule_key", "effective_from", "effective_to"])
    op.create_index("ix_rule_set_versions_status", "rule_set_versions", ["status"])
    _published_immutable_trigger("rule_set_versions")

    op.create_table(
        "account_code_versions",
        _id_column(),
        sa.Column("code", sa.String(20), nullable=False),
        sa.Column("kind", sa.String(10), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("meaning", sa.Text(), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date()),
        sa.Column("source_ref", sa.Text()),
        sa.Column("status", sa.String(30), nullable=False),
        sa.CheckConstraint("kind IN ('income', 'expense')", name="ck_account_code_versions_kind"),
        sa.CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_account_code_versions_effective_range"),
        sa.CheckConstraint("status IN ('draft', 'published', 'retired')", name="ck_account_code_versions_status"),
        sa.UniqueConstraint("code", "kind", "effective_from", name="uq_account_code_versions_code_kind_effective_from"),
        postgresql.ExcludeConstraint(
            ("code", "="),
            ("kind", "="),
            (sa.text("daterange(effective_from, effective_to, '[]')"), "&&"),
            where=sa.text("status = 'published'"),
            name="ex_account_code_versions_published_effective_dates",
        ),
    )
    op.create_index("ix_account_code_versions_kind_code_dates", "account_code_versions", ["kind", "code", "effective_from"])
    _published_immutable_trigger("account_code_versions")

    op.create_table(
        "ledger_account_definitions",
        _id_column(),
        sa.Column("semantic_key", sa.String(120), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("normal_side", sa.String(6), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date()),
        sa.Column("rule_context", postgresql.JSONB(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.CheckConstraint("normal_side IN ('debit', 'credit')", name="ck_ledger_account_definitions_normal_side"),
        sa.CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_ledger_account_definitions_effective_range"),
        sa.CheckConstraint("jsonb_typeof(rule_context) = 'object'", name="ck_ledger_account_definitions_rule_context_object"),
        sa.CheckConstraint("status IN ('draft', 'published', 'retired')", name="ck_ledger_account_definitions_status"),
        sa.UniqueConstraint("semantic_key", "effective_from", name="uq_ledger_account_definitions_semantic_key_effective_from"),
        postgresql.ExcludeConstraint(
            ("semantic_key", "="),
            (sa.text("daterange(effective_from, effective_to, '[]')"), "&&"),
            where=sa.text("status = 'published'"),
            name="ex_ledger_account_definitions_published_effective_dates",
        ),
    )
    op.create_index("ix_ledger_account_definitions_semantic_dates", "ledger_account_definitions", ["semantic_key", "effective_from", "effective_to"])
    _published_immutable_trigger("ledger_account_definitions")

    op.create_table(
        "official_template_versions",
        _id_column(),
        sa.Column("template_key", sa.String(80), nullable=False),
        sa.Column("language", sa.String(10), nullable=False),
        sa.Column("version", sa.String(80), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date()),
        sa.Column("renderer_ref", sa.Text(), nullable=False),
        sa.Column("source_ref", sa.Text()),
        sa.Column("status", sa.String(30), nullable=False),
        sa.CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_official_template_versions_effective_range"),
        sa.CheckConstraint("status IN ('draft', 'published', 'retired')", name="ck_official_template_versions_status"),
        sa.UniqueConstraint("template_key", "language", "version", name="uq_official_template_versions_key_language_version"),
    )
    op.create_index("ix_official_template_versions_key_language_dates", "official_template_versions", ["template_key", "language", "effective_from"])
    _published_immutable_trigger("official_template_versions")

    op.create_table(
        "supported_locales",
        sa.Column("code", sa.String(10), primary_key=True, nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.CheckConstraint("status IN ('active', 'inactive')", name="ck_supported_locales_status"),
    )


def downgrade() -> None:
    op.drop_table("supported_locales")
    op.execute("DROP TRIGGER IF EXISTS trg_official_template_versions_published_immutable ON official_template_versions")
    op.drop_index("ix_official_template_versions_key_language_dates", table_name="official_template_versions")
    op.drop_table("official_template_versions")
    op.execute("DROP TRIGGER IF EXISTS trg_ledger_account_definitions_published_immutable ON ledger_account_definitions")
    op.drop_index("ix_ledger_account_definitions_semantic_dates", table_name="ledger_account_definitions")
    op.drop_table("ledger_account_definitions")
    op.execute("DROP TRIGGER IF EXISTS trg_account_code_versions_published_immutable ON account_code_versions")
    op.drop_index("ix_account_code_versions_kind_code_dates", table_name="account_code_versions")
    op.drop_table("account_code_versions")
    op.execute("DROP TRIGGER IF EXISTS trg_rule_set_versions_published_immutable ON rule_set_versions")
    op.drop_index("ix_rule_set_versions_status", table_name="rule_set_versions")
    op.drop_index("ix_rule_set_versions_rule_dates", table_name="rule_set_versions")
    op.drop_table("rule_set_versions")
