"""Create immutable posting and journal persistence foundations.

Revision ID: 20260926_0007
Revises: 20260924_0006
Create Date: 2026-09-26
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260926_0007"
down_revision = "20260924_0006"
branch_labels = None
depends_on = None

UUID = postgresql.UUID(as_uuid=True)
TIMESTAMP = sa.DateTime(timezone=True)


def _id() -> sa.Column:
    return sa.Column("id", UUID, primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()"))


def _school_columns() -> tuple[sa.Column, sa.Column]:
    return _id(), sa.Column("school_id", UUID, nullable=False)


def _created() -> sa.Column:
    return sa.Column("created_at", TIMESTAMP, nullable=False, server_default=sa.text("now()"))


def upgrade() -> None:
    op.create_table(
        "posting_requests", *_school_columns(), sa.Column("document_id", UUID, nullable=False),
        sa.Column("fiscal_year_id", UUID, nullable=False), sa.Column("accounting_date", sa.Date(), nullable=False),
        sa.Column("rule_set_version_id", UUID, nullable=False), sa.Column("idempotency_key", UUID, nullable=False),
        sa.Column("status", sa.String(30), nullable=False), sa.Column("requested_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")),
        sa.Column("finalized_at", TIMESTAMP), _created(),
        sa.CheckConstraint("status IN ('pending', 'succeeded', 'failed')", name="ck_posting_requests_status"),
        sa.CheckConstraint("(status = 'pending' AND finalized_at IS NULL) OR (status IN ('succeeded', 'failed') AND finalized_at IS NOT NULL)", name="ck_posting_requests_finalized_consistency"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_posting_requests_document_same_school"),
        sa.ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_posting_requests_fiscal_year_same_school"),
        sa.ForeignKeyConstraint(["rule_set_version_id"], ["rule_set_versions.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_posting_requests_school_id_id"),
        sa.UniqueConstraint("school_id", "idempotency_key", name="uq_posting_requests_school_idempotency_key"),
    )
    op.create_index("ix_posting_requests_school_status_requested", "posting_requests", ["school_id", "status", "requested_at"])
    op.create_index("uq_posting_requests_school_document_active", "posting_requests", ["school_id", "document_id"], unique=True, postgresql_where=sa.text("status IN ('pending', 'succeeded')"))
    op.execute("""
        CREATE FUNCTION validate_posting_request_document() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM financial_documents document
                WHERE document.school_id = NEW.school_id AND document.id = NEW.document_id
                  AND document.status = 'approved' AND document.fiscal_year_id = NEW.fiscal_year_id AND document.accounting_date = NEW.accounting_date
            ) OR NOT EXISTS (SELECT 1 FROM rule_set_versions rule WHERE rule.id=NEW.rule_set_version_id AND rule.status='published' AND rule.effective_from<=NEW.accounting_date AND (rule.effective_to IS NULL OR rule.effective_to>=NEW.accounting_date)) THEN
                RAISE EXCEPTION 'Posting requests require an approved document in the same fiscal year' USING ERRCODE = '23514';
            END IF;
            RETURN NEW;
        END;
        $$
    """)
    op.execute("CREATE TRIGGER trg_posting_requests_approved_document BEFORE INSERT ON posting_requests FOR EACH ROW EXECUTE FUNCTION validate_posting_request_document()")
    op.execute("""CREATE FUNCTION validate_posting_request_change() RETURNS trigger LANGUAGE plpgsql AS $$
    BEGIN
      IF (NEW.school_id, NEW.document_id, NEW.fiscal_year_id, NEW.accounting_date, NEW.rule_set_version_id, NEW.idempotency_key) IS DISTINCT FROM (OLD.school_id, OLD.document_id, OLD.fiscal_year_id, OLD.accounting_date, OLD.rule_set_version_id, OLD.idempotency_key) THEN RAISE EXCEPTION 'Posting request identity is immutable' USING ERRCODE='55000'; END IF;
      RETURN NEW;
    END; $$""")
    op.execute("CREATE TRIGGER trg_posting_requests_identity_immutable BEFORE UPDATE ON posting_requests FOR EACH ROW EXECUTE FUNCTION validate_posting_request_change()")
    op.execute("CREATE TRIGGER trg_posting_requests_terminal_immutable BEFORE UPDATE OR DELETE ON posting_requests FOR EACH ROW WHEN (OLD.status IN ('succeeded', 'failed')) EXECUTE FUNCTION reject_immutable_row_change()")

    op.create_table(
        "posting_results", *_school_columns(), sa.Column("posting_request_id", UUID, nullable=False),
        sa.Column("rule_context", postgresql.JSONB(), nullable=False), sa.Column("account_code_context", postgresql.JSONB(), nullable=False),
        sa.Column("result_hash", sa.LargeBinary(), nullable=False), sa.Column("derived_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")), _created(),
        sa.CheckConstraint("jsonb_typeof(rule_context) = 'object'", name="ck_posting_results_rule_context_object"),
        sa.CheckConstraint("jsonb_typeof(account_code_context) = 'object'", name="ck_posting_results_account_code_context_object"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "posting_request_id"], ["posting_requests.school_id", "posting_requests.id"], name="fk_posting_results_request_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_posting_results_school_id_id"), sa.UniqueConstraint("school_id", "posting_request_id", name="uq_posting_results_school_request"),
    )
    op.create_index("ix_posting_results_school_result_hash", "posting_results", ["school_id", "result_hash"])
    op.create_index("ix_posting_results_derived_at", "posting_results", ["derived_at"])

    op.create_table(
        "journal_entries", *_school_columns(), sa.Column("posting_result_id", UUID, nullable=False), sa.Column("fiscal_year_id", UUID, nullable=False),
        sa.Column("accounting_date", sa.Date(), nullable=False), sa.Column("description", sa.Text()), sa.Column("posted_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")), sa.Column("entry_hash", sa.LargeBinary(), nullable=False), _created(),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "posting_result_id"], ["posting_results.school_id", "posting_results.id"], name="fk_journal_entries_result_same_school"),
        sa.ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_journal_entries_fiscal_year_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_journal_entries_school_id_id"), sa.UniqueConstraint("school_id", "posting_result_id", name="uq_journal_entries_school_result"),
    )
    op.create_index("ix_journal_entries_school_fiscal_date", "journal_entries", ["school_id", "fiscal_year_id", "accounting_date"])
    op.create_index("ix_journal_entries_posted_at", "journal_entries", ["posted_at"])
    op.create_index("ix_journal_entries_school_entry_hash", "journal_entries", ["school_id", "entry_hash"])
    op.execute("""CREATE FUNCTION validate_journal_entry_request() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
      IF NOT EXISTS (SELECT 1 FROM posting_results result JOIN posting_requests request ON request.school_id=result.school_id AND request.id=result.posting_request_id WHERE result.school_id=NEW.school_id AND result.id=NEW.posting_result_id AND request.fiscal_year_id=NEW.fiscal_year_id AND request.accounting_date=NEW.accounting_date) THEN RAISE EXCEPTION 'Journal entry must match its posting request fiscal year and accounting date' USING ERRCODE='23514'; END IF; RETURN NEW; END; $$""")
    op.execute("CREATE TRIGGER trg_journal_entries_match_request BEFORE INSERT ON journal_entries FOR EACH ROW EXECUTE FUNCTION validate_journal_entry_request()")

    op.create_table(
        "journal_lines", *_school_columns(), sa.Column("journal_entry_id", UUID, nullable=False), sa.Column("line_no", sa.Integer(), nullable=False), sa.Column("ledger_account_id", UUID, nullable=False), sa.Column("account_code_version_id", UUID),
        sa.Column("debit_amount", sa.Numeric(18, 2), nullable=False, server_default=sa.text("0")), sa.Column("credit_amount", sa.Numeric(18, 2), nullable=False, server_default=sa.text("0")), sa.Column("classification_context", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")), _created(),
        sa.CheckConstraint("line_no > 0", name="ck_journal_lines_line_no_positive"),
        sa.CheckConstraint("(debit_amount > 0 AND credit_amount = 0) OR (credit_amount > 0 AND debit_amount = 0)", name="ck_journal_lines_exactly_one_positive_side"),
        sa.CheckConstraint("jsonb_typeof(classification_context) = 'object'", name="ck_journal_lines_classification_context_object"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "journal_entry_id"], ["journal_entries.school_id", "journal_entries.id"], name="fk_journal_lines_entry_same_school"),
        sa.ForeignKeyConstraint(["school_id", "ledger_account_id"], ["school_ledger_accounts.school_id", "school_ledger_accounts.id"], name="fk_journal_lines_ledger_same_school"),
        sa.ForeignKeyConstraint(["account_code_version_id"], ["account_code_versions.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_journal_lines_school_id_id"), sa.UniqueConstraint("school_id", "journal_entry_id", "line_no", name="uq_journal_lines_school_entry_line"),
    )
    op.create_index("ix_journal_lines_school_ledger", "journal_lines", ["school_id", "ledger_account_id"])
    op.create_index("ix_journal_lines_account_code_version", "journal_lines", ["account_code_version_id"])
    op.execute("""CREATE FUNCTION validate_journal_line_references() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
      IF NOT EXISTS (SELECT 1 FROM journal_entries entry JOIN school_ledger_accounts ledger ON ledger.school_id=NEW.school_id AND ledger.id=NEW.ledger_account_id WHERE entry.school_id=NEW.school_id AND entry.id=NEW.journal_entry_id AND ledger.status='active' AND ledger.effective_from<=entry.accounting_date AND (ledger.effective_to IS NULL OR ledger.effective_to>=entry.accounting_date)) THEN RAISE EXCEPTION 'Ledger account is not active for the journal accounting date' USING ERRCODE='23514'; END IF;
      IF NEW.account_code_version_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM journal_entries entry JOIN account_code_versions code ON code.id=NEW.account_code_version_id WHERE entry.school_id=NEW.school_id AND entry.id=NEW.journal_entry_id AND code.status='published' AND code.effective_from<=entry.accounting_date AND (code.effective_to IS NULL OR code.effective_to>=entry.accounting_date)) THEN RAISE EXCEPTION 'Account code version is not published for the journal accounting date' USING ERRCODE='23514'; END IF; RETURN NEW; END; $$""")
    op.execute("CREATE TRIGGER trg_journal_lines_effective_references BEFORE INSERT ON journal_lines FOR EACH ROW EXECUTE FUNCTION validate_journal_line_references()")
    op.execute("""
        CREATE FUNCTION validate_finalized_journal_entry() RETURNS trigger LANGUAGE plpgsql AS $$
        DECLARE entry_id uuid := COALESCE((to_jsonb(NEW)->>'journal_entry_id')::uuid, NEW.id);
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM journal_lines WHERE school_id = NEW.school_id AND journal_entry_id = entry_id) THEN
                RAISE EXCEPTION 'Finalized journal entries require at least one line' USING ERRCODE = '23514';
            END IF;
            IF (SELECT COALESCE(sum(debit_amount), 0) = COALESCE(sum(credit_amount), 0) FROM journal_lines WHERE school_id = NEW.school_id AND journal_entry_id = entry_id) IS NOT TRUE THEN
                RAISE EXCEPTION 'Finalized journal entries must balance' USING ERRCODE = '23514';
            END IF;
            RETURN NULL;
        END;
        $$
    """)
    op.execute("CREATE CONSTRAINT TRIGGER trg_journal_entries_balanced AFTER INSERT ON journal_entries DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION validate_finalized_journal_entry()")
    op.execute("CREATE CONSTRAINT TRIGGER trg_journal_lines_keep_entry_balanced AFTER INSERT ON journal_lines DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION validate_finalized_journal_entry()")
    op.execute("""
        CREATE FUNCTION reject_late_journal_line_insert() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM journal_entries entry
                WHERE entry.school_id = NEW.school_id AND entry.id = NEW.journal_entry_id
                  AND entry.xmin = txid_current()::text::xid
            ) THEN
                RAISE EXCEPTION 'Journal lines may only be inserted with their new journal entry' USING ERRCODE = '55000';
            END IF;
            RETURN NEW;
        END;
        $$
    """)
    op.execute("CREATE TRIGGER trg_journal_lines_no_late_insert BEFORE INSERT ON journal_lines FOR EACH ROW EXECUTE FUNCTION reject_late_journal_line_insert()")
    for table in ("posting_results", "journal_entries", "journal_lines"):
        op.execute(f"CREATE TRIGGER trg_{table}_immutable BEFORE UPDATE OR DELETE ON {table} FOR EACH ROW EXECUTE FUNCTION reject_immutable_row_change()")

    op.create_table(
        "correction_links", *_school_columns(), sa.Column("original_document_id", UUID, nullable=False), sa.Column("correcting_document_id", UUID, nullable=False), sa.Column("original_entry_id", UUID), sa.Column("correcting_entry_id", UUID), sa.Column("correction_type", sa.String(30), nullable=False), sa.Column("reason", sa.Text(), nullable=False), sa.Column("linked_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")), _created(),
        sa.CheckConstraint("original_document_id <> correcting_document_id", name="ck_correction_links_not_self_document"), sa.CheckConstraint("original_entry_id IS NOT NULL AND correcting_entry_id IS NOT NULL AND original_entry_id <> correcting_entry_id", name="ck_correction_links_entries"), sa.CheckConstraint("correction_type IN ('reversal', 'adjustment', 'replacement')", name="ck_correction_links_type"), sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "original_document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_correction_links_original_document_same_school"), sa.ForeignKeyConstraint(["school_id", "correcting_document_id"], ["financial_documents.school_id", "financial_documents.id"], name="fk_correction_links_correcting_document_same_school"),
        sa.ForeignKeyConstraint(["school_id", "original_entry_id"], ["journal_entries.school_id", "journal_entries.id"], name="fk_correction_links_original_entry_same_school"), sa.ForeignKeyConstraint(["school_id", "correcting_entry_id"], ["journal_entries.school_id", "journal_entries.id"], name="fk_correction_links_correcting_entry_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_correction_links_school_id_id"), sa.UniqueConstraint("school_id", "correcting_document_id", name="uq_correction_links_school_correcting_document"),
    )
    op.create_index("ix_correction_links_school_original_document", "correction_links", ["school_id", "original_document_id"])
    op.create_index("ix_correction_links_school_original_entry", "correction_links", ["school_id", "original_entry_id"])
    op.execute("CREATE TRIGGER trg_correction_links_immutable BEFORE UPDATE OR DELETE ON correction_links FOR EACH ROW EXECUTE FUNCTION reject_immutable_row_change()")

    op.create_table(
        "idempotency_records", *_school_columns(), sa.Column("operation_key", UUID, nullable=False), sa.Column("request_fingerprint", sa.LargeBinary(), nullable=False), sa.Column("posting_request_id", UUID), sa.Column("result_status", sa.String(30), nullable=False), sa.Column("completed_at", TIMESTAMP), _created(),
        sa.CheckConstraint("result_status IN ('in_progress', 'completed', 'failed')", name="ck_idempotency_records_status"), sa.CheckConstraint("(result_status = 'in_progress' AND completed_at IS NULL) OR (result_status IN ('completed', 'failed') AND completed_at IS NOT NULL)", name="ck_idempotency_records_completion_consistency"), sa.ForeignKeyConstraint(["school_id"], ["schools.id"]), sa.ForeignKeyConstraint(["school_id", "posting_request_id"], ["posting_requests.school_id", "posting_requests.id"], name="fk_idempotency_records_request_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_idempotency_records_school_id_id"), sa.UniqueConstraint("school_id", "operation_key", name="uq_idempotency_records_school_operation_key"),
    )
    op.create_index("ix_idempotency_records_school_fingerprint", "idempotency_records", ["school_id", "request_fingerprint"])
    op.create_index("ix_idempotency_records_completion", "idempotency_records", ["completed_at"])
    op.execute("CREATE TRIGGER trg_idempotency_records_terminal_immutable BEFORE UPDATE OR DELETE ON idempotency_records FOR EACH ROW WHEN (OLD.result_status IN ('completed', 'failed')) EXECUTE FUNCTION reject_immutable_row_change()")
    op.execute("""CREATE FUNCTION validate_posting_chain() RETURNS trigger LANGUAGE plpgsql AS $$ DECLARE request_id uuid := COALESCE((to_jsonb(NEW)->>'posting_request_id')::uuid, (to_jsonb(NEW)->>'id')::uuid); BEGIN
      IF TG_TABLE_NAME='journal_entries' THEN SELECT result.posting_request_id INTO request_id FROM posting_results result WHERE result.school_id=NEW.school_id AND result.id=NEW.posting_result_id; END IF;
      IF EXISTS (SELECT 1 FROM posting_requests request WHERE request.school_id=NEW.school_id AND request.id=request_id AND request.status='succeeded' AND (NOT EXISTS (SELECT 1 FROM posting_results result WHERE result.school_id=request.school_id AND result.posting_request_id=request.id) OR NOT EXISTS (SELECT 1 FROM posting_results result JOIN journal_entries entry ON entry.school_id=result.school_id AND entry.posting_result_id=result.id WHERE result.school_id=request.school_id AND result.posting_request_id=request.id) OR NOT EXISTS (SELECT 1 FROM financial_documents document WHERE document.school_id=request.school_id AND document.id=request.document_id AND document.status IN ('posted','locked')))) THEN RAISE EXCEPTION 'Succeeded posting request requires one result, one journal entry, and posted document' USING ERRCODE='23514'; END IF;
      IF EXISTS (SELECT 1 FROM posting_requests request WHERE request.school_id=NEW.school_id AND request.id=request_id AND request.status='failed' AND EXISTS (SELECT 1 FROM posting_results result WHERE result.school_id=request.school_id AND result.posting_request_id=request.id)) THEN RAISE EXCEPTION 'Failed posting request cannot own authoritative results' USING ERRCODE='23514'; END IF; RETURN NULL; END; $$""")
    for table, events in (("posting_requests", "INSERT OR UPDATE"), ("posting_results", "INSERT"), ("journal_entries", "INSERT")):
        op.execute(f"CREATE CONSTRAINT TRIGGER trg_{table}_posting_chain AFTER {events} ON {table} DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION validate_posting_chain()")
    op.execute("""CREATE FUNCTION validate_idempotency_completion() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN IF NEW.result_status='completed' AND NOT EXISTS (SELECT 1 FROM posting_requests request JOIN posting_results result ON result.school_id=request.school_id AND result.posting_request_id=request.id WHERE request.school_id=NEW.school_id AND request.id=NEW.posting_request_id AND request.status='succeeded' AND request.idempotency_key=NEW.operation_key) THEN RAISE EXCEPTION 'Completed idempotency record must resolve to its successful posting request and result' USING ERRCODE='23514'; END IF; IF NEW.posting_request_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM posting_requests request WHERE request.school_id=NEW.school_id AND request.id=NEW.posting_request_id AND request.idempotency_key=NEW.operation_key) THEN RAISE EXCEPTION 'Idempotency operation key must match posting request key' USING ERRCODE='23514'; END IF; RETURN NULL; END; $$""")
    op.execute("CREATE CONSTRAINT TRIGGER trg_idempotency_records_completion AFTER INSERT OR UPDATE ON idempotency_records DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION validate_idempotency_completion()")
    op.execute("""CREATE FUNCTION validate_correction_link() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN
      IF NOT EXISTS (SELECT 1 FROM journal_entries entry JOIN posting_results result ON result.school_id=entry.school_id AND result.id=entry.posting_result_id JOIN posting_requests request ON request.school_id=result.school_id AND request.id=result.posting_request_id WHERE entry.school_id=NEW.school_id AND entry.id=NEW.original_entry_id AND request.document_id=NEW.original_document_id) OR NOT EXISTS (SELECT 1 FROM journal_entries entry JOIN posting_results result ON result.school_id=entry.school_id AND result.id=entry.posting_result_id JOIN posting_requests request ON request.school_id=result.school_id AND request.id=result.posting_request_id WHERE entry.school_id=NEW.school_id AND entry.id=NEW.correcting_entry_id AND request.document_id=NEW.correcting_document_id) THEN RAISE EXCEPTION 'Correction entries must belong to their linked documents' USING ERRCODE='23514'; END IF;
      IF EXISTS (WITH RECURSIVE chain(document_id) AS (SELECT NEW.original_document_id UNION SELECT link.original_document_id FROM correction_links link JOIN chain ON link.correcting_document_id=chain.document_id WHERE link.school_id=NEW.school_id) SELECT 1 FROM chain WHERE document_id=NEW.correcting_document_id) THEN RAISE EXCEPTION 'Correction links cannot form cycles' USING ERRCODE='23514'; END IF; RETURN NULL; END; $$""")
    op.execute("CREATE CONSTRAINT TRIGGER trg_correction_links_valid AFTER INSERT ON correction_links DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION validate_correction_link()")

    op.drop_constraint("ck_bank_reconciliation_items_confirmed_deferred_until_journals", "bank_reconciliation_items", type_="check")
    op.create_foreign_key("fk_bank_reconciliation_items_journal_line_same_school", "bank_reconciliation_items", "journal_lines", ["school_id", "journal_line_id"], ["school_id", "id"])
    op.execute("""
        CREATE FUNCTION validate_confirmed_reconciliation_item() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
            IF NEW.status = 'confirmed' AND NOT EXISTS (
                SELECT 1 FROM bank_reconciliations reconciliation
                JOIN journal_lines line ON line.school_id = NEW.school_id AND line.id = NEW.journal_line_id
                JOIN journal_entries entry ON entry.school_id = line.school_id AND entry.id = line.journal_entry_id AND entry.posted_at IS NOT NULL
                JOIN bank_account_ledger_bindings binding ON binding.school_id = reconciliation.school_id
                    AND binding.bank_account_id = reconciliation.bank_account_id AND binding.ledger_account_id = line.ledger_account_id
                    AND entry.accounting_date >= binding.effective_from AND (binding.effective_to IS NULL OR entry.accounting_date <= binding.effective_to)
                WHERE reconciliation.school_id = NEW.school_id AND reconciliation.id = NEW.reconciliation_id
                  AND EXISTS (SELECT 1 FROM bank_statement_lines statement_line WHERE statement_line.school_id=NEW.school_id AND statement_line.id=NEW.statement_line_id AND statement_line.statement_id=reconciliation.statement_id)
                  AND NEW.statement_line_id IS NOT NULL AND NEW.journal_line_id IS NOT NULL
            ) THEN
                RAISE EXCEPTION 'Confirmed reconciliation requires a posted journal line on the bank ledger account effective on its accounting date' USING ERRCODE = '23514';
            END IF;
            RETURN NULL;
        END;
        $$
    """)
    op.execute("CREATE CONSTRAINT TRIGGER trg_bank_reconciliation_items_confirmed_match AFTER INSERT OR UPDATE ON bank_reconciliation_items DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION validate_confirmed_reconciliation_item()")


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_correction_links_valid ON correction_links")
    op.execute("DROP FUNCTION IF EXISTS validate_correction_link()")
    op.execute("DROP TRIGGER IF EXISTS trg_idempotency_records_completion ON idempotency_records")
    op.execute("DROP FUNCTION IF EXISTS validate_idempotency_completion()")
    for table in ("posting_requests", "posting_results", "journal_entries"):
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_posting_chain ON {table}")
    op.execute("DROP FUNCTION IF EXISTS validate_posting_chain()")
    op.execute("DROP TRIGGER IF EXISTS trg_bank_reconciliation_items_confirmed_match ON bank_reconciliation_items")
    op.execute("DROP FUNCTION IF EXISTS validate_confirmed_reconciliation_item()")
    op.drop_constraint("fk_bank_reconciliation_items_journal_line_same_school", "bank_reconciliation_items", type_="foreignkey")
    op.execute("ALTER TABLE bank_reconciliation_items ADD CONSTRAINT ck_bank_reconciliation_items_confirmed_deferred_until_journals CHECK (status <> 'confirmed') NOT VALID")
    op.execute("DROP TRIGGER IF EXISTS trg_idempotency_records_terminal_immutable ON idempotency_records")
    op.drop_index("ix_idempotency_records_completion", table_name="idempotency_records"); op.drop_index("ix_idempotency_records_school_fingerprint", table_name="idempotency_records"); op.drop_table("idempotency_records")
    op.execute("DROP TRIGGER IF EXISTS trg_correction_links_immutable ON correction_links")
    op.drop_index("ix_correction_links_school_original_entry", table_name="correction_links"); op.drop_index("ix_correction_links_school_original_document", table_name="correction_links"); op.drop_table("correction_links")
    for table in ("journal_lines", "journal_entries", "posting_results"):
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_immutable ON {table}")
    op.execute("DROP TRIGGER IF EXISTS trg_journal_lines_no_late_insert ON journal_lines")
    op.execute("DROP TRIGGER IF EXISTS trg_journal_lines_effective_references ON journal_lines")
    op.execute("DROP FUNCTION IF EXISTS validate_journal_line_references()")
    op.execute("DROP TRIGGER IF EXISTS trg_journal_lines_keep_entry_balanced ON journal_lines")
    op.execute("DROP TRIGGER IF EXISTS trg_journal_entries_balanced ON journal_entries")
    op.execute("DROP FUNCTION IF EXISTS validate_finalized_journal_entry()")
    op.execute("DROP FUNCTION IF EXISTS reject_late_journal_line_insert()")
    op.drop_index("ix_journal_lines_account_code_version", table_name="journal_lines"); op.drop_index("ix_journal_lines_school_ledger", table_name="journal_lines"); op.drop_table("journal_lines")
    op.execute("DROP TRIGGER IF EXISTS trg_journal_entries_match_request ON journal_entries")
    op.execute("DROP FUNCTION IF EXISTS validate_journal_entry_request()")
    op.drop_index("ix_journal_entries_school_entry_hash", table_name="journal_entries"); op.drop_index("ix_journal_entries_posted_at", table_name="journal_entries"); op.drop_index("ix_journal_entries_school_fiscal_date", table_name="journal_entries"); op.drop_table("journal_entries")
    op.drop_index("ix_posting_results_derived_at", table_name="posting_results"); op.drop_index("ix_posting_results_school_result_hash", table_name="posting_results"); op.drop_table("posting_results")
    op.execute("DROP TRIGGER IF EXISTS trg_posting_requests_terminal_immutable ON posting_requests")
    op.execute("DROP TRIGGER IF EXISTS trg_posting_requests_identity_immutable ON posting_requests")
    op.execute("DROP FUNCTION IF EXISTS validate_posting_request_change()")
    op.execute("DROP TRIGGER IF EXISTS trg_posting_requests_approved_document ON posting_requests")
    op.execute("DROP FUNCTION IF EXISTS validate_posting_request_document()")
    op.drop_index("uq_posting_requests_school_document_active", table_name="posting_requests"); op.drop_index("ix_posting_requests_school_status_requested", table_name="posting_requests"); op.drop_table("posting_requests")
