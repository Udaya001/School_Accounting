"""Create financial documents, income receipts, and tenant event history.

Revision ID: 20260924_0004
Revises: 20260924_0003
Create Date: 2026-09-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260924_0004"
down_revision = "20260924_0003"
branch_labels = None
depends_on = None

UUID = postgresql.UUID(as_uuid=True)
TIMESTAMP = sa.DateTime(timezone=True)


def _id_column() -> sa.Column:
    return sa.Column("id", UUID, primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()"))


def _created_at_column() -> sa.Column:
    return sa.Column("created_at", TIMESTAMP, nullable=False, server_default=sa.text("now()"))


def upgrade() -> None:
    op.create_table(
        "financial_documents", _id_column(), sa.Column("school_id", UUID, nullable=False),
        sa.Column("document_type", sa.String(50), nullable=False), sa.Column("document_number", sa.String(100)),
        sa.Column("fiscal_year_id", UUID, nullable=False), sa.Column("accounting_date", sa.Date(), nullable=False),
        sa.Column("entered_bs_date", sa.String(16)), sa.Column("status", sa.String(30), nullable=False),
        sa.Column("party_id", UUID), sa.Column("bank_account_id", UUID), sa.Column("summary", sa.Text()),
        sa.Column("approved_at", TIMESTAMP), sa.Column("posted_at", TIMESTAMP), sa.Column("locked_at", TIMESTAMP), _created_at_column(),
        sa.CheckConstraint("status IN ('draft', 'returned', 'submitted', 'verified', 'approved', 'posted', 'locked')", name="ck_financial_documents_status"),
        sa.CheckConstraint("status NOT IN ('approved', 'posted', 'locked') OR approved_at IS NOT NULL", name="ck_financial_documents_approved_at"),
        sa.CheckConstraint("status NOT IN ('posted', 'locked') OR posted_at IS NOT NULL", name="ck_financial_documents_posted_at"),
        sa.CheckConstraint("status <> 'locked' OR locked_at IS NOT NULL", name="ck_financial_documents_locked_at"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_financial_documents_fiscal_year_same_school"),
        sa.ForeignKeyConstraint(["school_id", "party_id"], ["parties.school_id", "parties.id"], name="fk_financial_documents_party_same_school"),
        sa.ForeignKeyConstraint(["school_id", "bank_account_id"], ["bank_accounts.school_id", "bank_accounts.id"], name="fk_financial_documents_bank_account_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_financial_documents_school_id_id"),
    )
    op.create_index("uq_financial_documents_school_fiscal_type_number", "financial_documents", ["school_id", "fiscal_year_id", "document_type", "document_number"], unique=True, postgresql_where=sa.text("document_number IS NOT NULL"))
    op.create_index("ix_financial_documents_school_status_date", "financial_documents", ["school_id", "status", "accounting_date"])
    op.create_index("ix_financial_documents_school_fiscal_type", "financial_documents", ["school_id", "fiscal_year_id", "document_type"])
    op.execute("""
        CREATE TRIGGER trg_financial_documents_terminal_immutable
        BEFORE UPDATE OR DELETE ON financial_documents
        FOR EACH ROW WHEN (OLD.status IN ('posted', 'locked'))
        EXECUTE FUNCTION reject_immutable_row_change()
    """)

    op.create_table(
        "financial_document_items", _id_column(), sa.Column("school_id", UUID, nullable=False), sa.Column("document_id", UUID, nullable=False),
        sa.Column("line_no", sa.Integer(), nullable=False), sa.Column("description", sa.Text()), sa.Column("amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("account_code_version_id", UUID), sa.Column("student_account_id", UUID), sa.Column("staff_person_id", UUID), sa.Column("party_id", UUID),
        sa.Column("facts", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")), _created_at_column(),
        sa.CheckConstraint("line_no > 0", name="ck_financial_document_items_line_no_positive"), sa.CheckConstraint("amount >= 0", name="ck_financial_document_items_amount_nonnegative"), sa.CheckConstraint("jsonb_typeof(facts) = 'object'", name="ck_financial_document_items_facts_object"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]), sa.ForeignKeyConstraint(["account_code_version_id"], ["account_code_versions.id"]),
        sa.ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_financial_document_items_document_same_school"),
        sa.ForeignKeyConstraint(["school_id", "student_account_id"], ["student_accounts.school_id", "student_accounts.id"], name="fk_financial_document_items_student_same_school"),
        sa.ForeignKeyConstraint(["school_id", "staff_person_id"], ["staff_people.school_id", "staff_people.id"], name="fk_financial_document_items_staff_same_school"),
        sa.ForeignKeyConstraint(["school_id", "party_id"], ["parties.school_id", "parties.id"], name="fk_financial_document_items_party_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_financial_document_items_school_id_id"), sa.UniqueConstraint("school_id", "document_id", "line_no", name="uq_financial_document_items_school_document_line"),
    )
    op.create_index("ix_financial_document_items_school_document", "financial_document_items", ["school_id", "document_id"])

    op.create_table(
        "income_receipts", _id_column(), sa.Column("school_id", UUID, nullable=False), sa.Column("document_id", UUID, nullable=False),
        sa.Column("receipt_issue_id", UUID, nullable=False), sa.Column("student_account_id", UUID), sa.Column("payer_party_id", UUID), sa.Column("receipt_date", sa.Date(), nullable=False), _created_at_column(),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_income_receipts_document_same_school"),
        sa.ForeignKeyConstraint(["school_id", "receipt_issue_id"], ["receipt_issues.school_id", "receipt_issues.id"], name="fk_income_receipts_receipt_issue_same_school"),
        sa.ForeignKeyConstraint(["school_id", "student_account_id"], ["student_accounts.school_id", "student_accounts.id"], name="fk_income_receipts_student_same_school"),
        sa.ForeignKeyConstraint(["school_id", "payer_party_id"], ["parties.school_id", "parties.id"], name="fk_income_receipts_payer_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_income_receipts_school_id_id"), sa.UniqueConstraint("school_id", "document_id", name="uq_income_receipts_school_document"), sa.UniqueConstraint("school_id", "receipt_issue_id", name="uq_income_receipts_school_receipt_issue"),
    )
    op.create_index("ix_income_receipts_school_student_date", "income_receipts", ["school_id", "student_account_id", "receipt_date"])
    op.execute("""
        CREATE FUNCTION reject_financial_document_detail_change()
        RETURNS trigger LANGUAGE plpgsql AS $$
        DECLARE detail_document_id uuid;
        BEGIN
            detail_document_id := CASE WHEN TG_OP = 'DELETE' THEN OLD.document_id ELSE NEW.document_id END;
            IF EXISTS (SELECT 1 FROM financial_documents WHERE school_id = CASE WHEN TG_OP = 'DELETE' THEN OLD.school_id ELSE NEW.school_id END AND id = detail_document_id AND status IN ('posted', 'locked')) THEN
                RAISE EXCEPTION 'Financial document details are immutable after posting' USING ERRCODE = '55000';
            END IF;
            RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
        END;
        $$
    """)
    for table in ("financial_document_items", "income_receipts"):
        op.execute(f"CREATE TRIGGER trg_{table}_document_terminal_immutable BEFORE INSERT OR UPDATE OR DELETE ON {table} FOR EACH ROW EXECUTE FUNCTION reject_financial_document_detail_change()")

    op.create_table(
        "lifecycle_events", _id_column(), sa.Column("school_id", UUID, nullable=False), sa.Column("entity_type", sa.String(80), nullable=False), sa.Column("entity_id", UUID, nullable=False),
        sa.Column("from_status", sa.String(30)), sa.Column("to_status", sa.String(30), nullable=False), sa.Column("reason", sa.Text()), sa.Column("occurred_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")), _created_at_column(),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]), sa.UniqueConstraint("school_id", "id", name="uq_lifecycle_events_school_id_id"),
    )
    op.create_index("ix_lifecycle_events_school_target_time", "lifecycle_events", ["school_id", "entity_type", "entity_id", "occurred_at"])

    op.create_table(
        "authorization_decisions", _id_column(), sa.Column("school_id", UUID, nullable=False), sa.Column("actor_membership_id", UUID, nullable=False),
        sa.Column("target_type", sa.String(80), nullable=False), sa.Column("target_id", UUID, nullable=False), sa.Column("decision_type", sa.String(50), nullable=False), sa.Column("status", sa.String(30), nullable=False),
        sa.Column("decided_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")), sa.Column("reason", sa.Text()), sa.Column("evidence_metadata", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")), _created_at_column(),
        sa.CheckConstraint("jsonb_typeof(evidence_metadata) = 'object'", name="ck_authorization_decisions_evidence_metadata_object"), sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "actor_membership_id"], ["school_memberships.school_id", "school_memberships.id"], name="fk_authorization_decisions_actor_same_school"), sa.UniqueConstraint("school_id", "id", name="uq_authorization_decisions_school_id_id"),
    )
    op.create_index("ix_authorization_decisions_school_target_time", "authorization_decisions", ["school_id", "target_type", "target_id", "decided_at"])
    op.create_index("ix_authorization_decisions_school_actor_time", "authorization_decisions", ["school_id", "actor_membership_id", "decided_at"])

    op.create_table(
        "audit_events", _id_column(), sa.Column("school_id", UUID, nullable=False), sa.Column("actor_membership_id", UUID), sa.Column("action", sa.String(100), nullable=False),
        sa.Column("target_type", sa.String(80), nullable=False), sa.Column("target_id", UUID, nullable=False), sa.Column("outcome", sa.String(30)), sa.Column("metadata", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("occurred_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")), _created_at_column(),
        sa.CheckConstraint("jsonb_typeof(metadata) = 'object'", name="ck_audit_events_metadata_object"), sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "actor_membership_id"], ["school_memberships.school_id", "school_memberships.id"], name="fk_audit_events_actor_same_school"), sa.UniqueConstraint("school_id", "id", name="uq_audit_events_school_id_id"),
    )
    op.create_index("ix_audit_events_school_target_time", "audit_events", ["school_id", "target_type", "target_id", "occurred_at"])
    op.create_index("ix_audit_events_school_actor_time", "audit_events", ["school_id", "actor_membership_id", "occurred_at"])
    op.create_index("ix_audit_events_school_action_time", "audit_events", ["school_id", "action", "occurred_at"])
    op.execute("""
        CREATE FUNCTION validate_tenant_event_target()
        RETURNS trigger LANGUAGE plpgsql AS $$
        DECLARE target_kind text;
        DECLARE target_uuid uuid;
        BEGIN
            IF TG_TABLE_NAME = 'lifecycle_events' THEN
                target_kind := NEW.entity_type;
                target_uuid := NEW.entity_id;
            ELSE
                target_kind := NEW.target_type;
                target_uuid := NEW.target_id;
            END IF;
            IF target_kind = 'financial_document' THEN
                IF NOT EXISTS (SELECT 1 FROM financial_documents WHERE school_id = NEW.school_id AND id = target_uuid) THEN RAISE EXCEPTION 'Event target is outside its school' USING ERRCODE = '23503'; END IF;
            ELSIF target_kind = 'financial_document_item' THEN
                IF NOT EXISTS (SELECT 1 FROM financial_document_items WHERE school_id = NEW.school_id AND id = target_uuid) THEN RAISE EXCEPTION 'Event target is outside its school' USING ERRCODE = '23503'; END IF;
            ELSIF target_kind = 'income_receipt' THEN
                IF NOT EXISTS (SELECT 1 FROM income_receipts WHERE school_id = NEW.school_id AND id = target_uuid) THEN RAISE EXCEPTION 'Event target is outside its school' USING ERRCODE = '23503'; END IF;
            ELSIF target_kind = 'receipt_issue' THEN
                IF NOT EXISTS (SELECT 1 FROM receipt_issues WHERE school_id = NEW.school_id AND id = target_uuid) THEN RAISE EXCEPTION 'Event target is outside its school' USING ERRCODE = '23503'; END IF;
            ELSE RAISE EXCEPTION 'Unsupported tenant event target type: %', target_kind USING ERRCODE = '23514';
            END IF;
            RETURN NEW;
        END;
        $$
    """)
    for table in ("lifecycle_events", "authorization_decisions", "audit_events"):
        op.execute(f"CREATE TRIGGER trg_{table}_validate_target BEFORE INSERT ON {table} FOR EACH ROW EXECUTE FUNCTION validate_tenant_event_target()")
        op.execute(f"CREATE TRIGGER trg_{table}_immutable BEFORE UPDATE OR DELETE ON {table} FOR EACH ROW EXECUTE FUNCTION reject_immutable_row_change()")


def downgrade() -> None:
    for table in ("audit_events", "authorization_decisions", "lifecycle_events"):
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_immutable ON {table}")
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_validate_target ON {table}")
    op.drop_index("ix_audit_events_school_action_time", table_name="audit_events")
    op.drop_index("ix_audit_events_school_actor_time", table_name="audit_events")
    op.drop_index("ix_audit_events_school_target_time", table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index("ix_authorization_decisions_school_actor_time", table_name="authorization_decisions")
    op.drop_index("ix_authorization_decisions_school_target_time", table_name="authorization_decisions")
    op.drop_table("authorization_decisions")
    op.drop_index("ix_lifecycle_events_school_target_time", table_name="lifecycle_events")
    op.drop_table("lifecycle_events")
    op.execute("DROP FUNCTION IF EXISTS validate_tenant_event_target()")
    for table in ("income_receipts", "financial_document_items"):
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_document_terminal_immutable ON {table}")
    op.drop_index("ix_income_receipts_school_student_date", table_name="income_receipts")
    op.drop_table("income_receipts")
    op.drop_index("ix_financial_document_items_school_document", table_name="financial_document_items")
    op.drop_table("financial_document_items")
    op.execute("DROP FUNCTION IF EXISTS reject_financial_document_detail_change()")
    op.execute("DROP TRIGGER IF EXISTS trg_financial_documents_terminal_immutable ON financial_documents")
    op.drop_index("ix_financial_documents_school_fiscal_type", table_name="financial_documents")
    op.drop_index("ix_financial_documents_school_status_date", table_name="financial_documents")
    op.drop_index("uq_financial_documents_school_fiscal_type_number", table_name="financial_documents")
    op.drop_table("financial_documents")
