"""Create tenant references, bank controls, and receipt controls.

Revision ID: 20260924_0003
Revises: 20260923_0002
Create Date: 2026-09-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260924_0003"
down_revision = "20260923_0002"
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
        "school_ledger_accounts",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("definition_id", UUID),
        sa.Column("account_code", sa.String(80), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date()),
        _created_at_column(),
        sa.CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_school_ledger_accounts_effective_range"),
        sa.CheckConstraint("status IN ('active', 'inactive')", name="ck_school_ledger_accounts_status"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["definition_id"], ["ledger_account_definitions.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_school_ledger_accounts_school_id_id"),
        sa.UniqueConstraint("school_id", "account_code", "effective_from", name="uq_school_ledger_accounts_code_effective_from"),
        postgresql.ExcludeConstraint(
            ("school_id", "="),
            ("account_code", "="),
            (sa.text("daterange(effective_from, effective_to, '[]')"), "&&"),
            where=sa.text("status = 'active'"),
            name="ex_school_ledger_accounts_active_effective_dates",
        ),
    )
    op.create_index("ix_school_ledger_accounts_school_status_effective", "school_ledger_accounts", ["school_id", "status", "effective_from"])

    op.create_table(
        "parties",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("party_type", sa.String(40), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("pan", sa.String(30)),
        sa.Column("external_ref", sa.String(255)),
        sa.Column("contact", postgresql.JSONB()),
        sa.Column("status", sa.String(30), nullable=False),
        _created_at_column(),
        sa.CheckConstraint("contact IS NULL OR jsonb_typeof(contact) = 'object'", name="ck_parties_contact_object"),
        sa.CheckConstraint("status IN ('active', 'inactive')", name="ck_parties_status"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_parties_school_id_id"),
    )
    op.create_index("uq_parties_school_type_external_ref", "parties", ["school_id", "party_type", "external_ref"], unique=True, postgresql_where=sa.text("external_ref IS NOT NULL"))
    op.create_index("ix_parties_school_type_name", "parties", ["school_id", "party_type", "name"])

    op.create_table(
        "student_accounts",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("external_ref", sa.String(255)),
        sa.Column("student_number", sa.String(80)),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        _created_at_column(),
        sa.CheckConstraint("status IN ('active', 'inactive')", name="ck_student_accounts_status"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_student_accounts_school_id_id"),
    )
    op.create_index("uq_student_accounts_school_external_ref", "student_accounts", ["school_id", "external_ref"], unique=True, postgresql_where=sa.text("external_ref IS NOT NULL"))
    op.create_index("uq_student_accounts_school_number", "student_accounts", ["school_id", "student_number"], unique=True, postgresql_where=sa.text("student_number IS NOT NULL"))

    op.create_table(
        "staff_people",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("external_ref", sa.String(255)),
        sa.Column("staff_number", sa.String(80)),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("employment_status", sa.String(30), nullable=False),
        sa.Column("tax_identifier", sa.String(80)),
        _created_at_column(),
        sa.CheckConstraint("employment_status IN ('active', 'inactive', 'terminated')", name="ck_staff_people_employment_status"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.UniqueConstraint("school_id", "id", name="uq_staff_people_school_id_id"),
    )
    op.create_index("uq_staff_people_school_external_ref", "staff_people", ["school_id", "external_ref"], unique=True, postgresql_where=sa.text("external_ref IS NOT NULL"))
    op.create_index("uq_staff_people_school_number", "staff_people", ["school_id", "staff_number"], unique=True, postgresql_where=sa.text("staff_number IS NOT NULL"))

    op.create_table(
        "bank_accounts",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("party_id", UUID),
        sa.Column("account_name", sa.Text(), nullable=False),
        sa.Column("account_number_masked", sa.String(80)),
        sa.Column("account_identity_fingerprint", sa.LargeBinary(), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False, server_default=sa.text("'NPR'")),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("opened_on", sa.Date()),
        sa.Column("closed_on", sa.Date()),
        _created_at_column(),
        sa.CheckConstraint("char_length(currency) = 3", name="ck_bank_accounts_currency_length"),
        sa.CheckConstraint("closed_on IS NULL OR opened_on IS NULL OR closed_on >= opened_on", name="ck_bank_accounts_date_range"),
        sa.CheckConstraint("status IN ('active', 'closed')", name="ck_bank_accounts_status"),
        sa.CheckConstraint("status <> 'closed' OR closed_on IS NOT NULL", name="ck_bank_accounts_closed_date"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "party_id"], ["parties.school_id", "parties.id"], name="fk_bank_accounts_party_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_bank_accounts_school_id_id"),
    )
    op.create_index("ix_bank_accounts_school_fingerprint", "bank_accounts", ["school_id", "account_identity_fingerprint"])
    op.execute(
        """
        CREATE FUNCTION validate_bank_account_lifecycle_bindings()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM bank_account_ledger_bindings binding
                WHERE binding.school_id = NEW.school_id
                  AND binding.bank_account_id = NEW.id
                  AND (
                    (NEW.opened_on IS NOT NULL AND binding.effective_from < NEW.opened_on)
                    OR (NEW.closed_on IS NOT NULL AND (binding.effective_to IS NULL OR binding.effective_to > NEW.closed_on))
                  )
            ) THEN
                RAISE EXCEPTION 'Bank account change would invalidate a ledger binding'
                    USING ERRCODE = '23514';
            END IF;
            RETURN NEW;
        END;
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_bank_accounts_validate_lifecycle_bindings
        BEFORE UPDATE OF opened_on, closed_on ON bank_accounts
        FOR EACH ROW EXECUTE FUNCTION validate_bank_account_lifecycle_bindings()
        """
    )

    op.create_table(
        "bank_account_ledger_bindings",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("bank_account_id", UUID, nullable=False),
        sa.Column("ledger_account_id", UUID, nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date()),
        _created_at_column(),
        sa.CheckConstraint("effective_to IS NULL OR effective_to >= effective_from", name="ck_bank_account_ledger_bindings_effective_range"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "bank_account_id"], ["bank_accounts.school_id", "bank_accounts.id"], name="fk_bank_account_ledger_bindings_bank_same_school"),
        sa.ForeignKeyConstraint(["school_id", "ledger_account_id"], ["school_ledger_accounts.school_id", "school_ledger_accounts.id"], name="fk_bank_account_ledger_bindings_ledger_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_bank_account_ledger_bindings_school_id_id"),
        postgresql.ExcludeConstraint(
            ("school_id", "="),
            ("bank_account_id", "="),
            (sa.text("daterange(effective_from, effective_to, '[]')"), "&&"),
            name="ex_bank_account_ledger_bindings_effective_dates",
        ),
    )
    op.create_index("ix_bank_account_ledger_bindings_school_ledger_dates", "bank_account_ledger_bindings", ["school_id", "ledger_account_id", "effective_from"])
    op.execute(
        """
        CREATE FUNCTION validate_bank_account_ledger_binding()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM bank_accounts bank
                JOIN school_ledger_accounts ledger
                  ON ledger.school_id = NEW.school_id
                 AND ledger.id = NEW.ledger_account_id
                WHERE bank.school_id = NEW.school_id
                  AND bank.id = NEW.bank_account_id
                  AND ledger.status = 'active'
                  AND ledger.effective_from <= NEW.effective_from
                  AND (ledger.effective_to IS NULL OR (NEW.effective_to IS NOT NULL AND ledger.effective_to >= NEW.effective_to))
                  AND (bank.opened_on IS NULL OR NEW.effective_from >= bank.opened_on)
                  AND (bank.closed_on IS NULL OR (NEW.effective_to IS NOT NULL AND NEW.effective_to <= bank.closed_on))
            ) THEN
                RAISE EXCEPTION 'Bank ledger binding is not applicable for its full effective period'
                    USING ERRCODE = '23514';
            END IF;
            RETURN NEW;
        END;
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_bank_account_ledger_bindings_validate_period
        BEFORE INSERT OR UPDATE ON bank_account_ledger_bindings
        FOR EACH ROW EXECUTE FUNCTION validate_bank_account_ledger_binding()
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_bank_account_ledger_bindings_immutable
        BEFORE UPDATE OR DELETE ON bank_account_ledger_bindings
        FOR EACH ROW EXECUTE FUNCTION reject_immutable_row_change()
        """
    )
    op.execute(
        """
        CREATE FUNCTION validate_ledger_account_bank_bindings()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM bank_account_ledger_bindings binding
                WHERE binding.school_id = NEW.school_id
                  AND binding.ledger_account_id = NEW.id
                  AND (
                    NEW.status <> 'active'
                    OR NEW.effective_from > binding.effective_from
                    OR (NEW.effective_to IS NOT NULL AND (binding.effective_to IS NULL OR NEW.effective_to < binding.effective_to))
                  )
            ) THEN
                RAISE EXCEPTION 'Ledger account change would invalidate a bank account binding'
                    USING ERRCODE = '23514';
            END IF;
            RETURN NEW;
        END;
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_school_ledger_accounts_validate_bank_bindings
        BEFORE UPDATE OF status, effective_from, effective_to ON school_ledger_accounts
        FOR EACH ROW EXECUTE FUNCTION validate_ledger_account_bank_bindings()
        """
    )

    op.create_table(
        "document_sequences",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("fiscal_year_id", UUID, nullable=False),
        sa.Column("sequence_key", sa.String(80), nullable=False),
        sa.Column("next_value", sa.BigInteger(), nullable=False),
        _created_at_column(),
        sa.Column("updated_at", TIMESTAMP, nullable=False, server_default=sa.text("now()")),
        sa.CheckConstraint("next_value > 0", name="ck_document_sequences_next_value_positive"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_document_sequences_fiscal_year_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_document_sequences_school_id_id"),
        sa.UniqueConstraint("school_id", "fiscal_year_id", "sequence_key", name="uq_document_sequences_school_fiscal_key"),
    )
    op.execute(
        """
        CREATE FUNCTION allocate_document_sequence(p_school_id uuid, p_fiscal_year_id uuid, p_sequence_key varchar)
        RETURNS bigint
        LANGUAGE plpgsql
        AS $$
        DECLARE allocated_value bigint;
        BEGIN
            UPDATE document_sequences
            SET next_value = next_value + 1, updated_at = now()
            WHERE school_id = p_school_id
              AND fiscal_year_id = p_fiscal_year_id
              AND sequence_key = p_sequence_key
            RETURNING next_value - 1 INTO allocated_value;
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Document sequence does not exist' USING ERRCODE = '23503';
            END IF;
            RETURN allocated_value;
        END;
        $$
        """
    )

    op.create_table(
        "receipt_books",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("fiscal_year_id", UUID, nullable=False),
        sa.Column("book_code", sa.String(80), nullable=False),
        sa.Column("first_number", sa.BigInteger()),
        sa.Column("last_number", sa.BigInteger()),
        sa.Column("status", sa.String(30), nullable=False),
        _created_at_column(),
        sa.CheckConstraint("first_number IS NULL OR first_number > 0", name="ck_receipt_books_first_number_positive"),
        sa.CheckConstraint("last_number IS NULL OR last_number > 0", name="ck_receipt_books_last_number_positive"),
        sa.CheckConstraint("first_number IS NULL OR last_number IS NULL OR last_number >= first_number", name="ck_receipt_books_range"),
        sa.CheckConstraint("status IN ('active', 'closed')", name="ck_receipt_books_status"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "fiscal_year_id"], ["fiscal_years.school_id", "fiscal_years.id"], name="fk_receipt_books_fiscal_year_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_receipt_books_school_id_id"),
        sa.UniqueConstraint("school_id", "fiscal_year_id", "book_code", name="uq_receipt_books_school_fiscal_code"),
    )
    op.create_index("ix_receipt_books_school_fiscal_status", "receipt_books", ["school_id", "fiscal_year_id", "status"])
    op.execute(
        """
        CREATE TRIGGER trg_receipt_books_no_delete
        BEFORE DELETE ON receipt_books
        FOR EACH ROW EXECUTE FUNCTION reject_immutable_row_change()
        """
    )

    op.create_table(
        "receipt_issues",
        _id_column(),
        sa.Column("school_id", UUID, nullable=False),
        sa.Column("receipt_book_id", UUID, nullable=False),
        sa.Column("receipt_number", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("issued_at", TIMESTAMP),
        sa.Column("cancel_reason", sa.Text()),
        sa.Column("replacement_issue_id", UUID),
        _created_at_column(),
        sa.CheckConstraint("receipt_number > 0", name="ck_receipt_issues_number_positive"),
        sa.CheckConstraint("status IN ('reserved', 'issued', 'cancelled', 'spoiled')", name="ck_receipt_issues_status"),
        sa.CheckConstraint("status NOT IN ('cancelled', 'spoiled') OR cancel_reason IS NOT NULL", name="ck_receipt_issues_terminal_reason"),
        sa.CheckConstraint("status <> 'issued' OR issued_at IS NOT NULL", name="ck_receipt_issues_issued_at"),
        sa.CheckConstraint("replacement_issue_id IS NULL OR replacement_issue_id <> id", name="ck_receipt_issues_not_self_replacement"),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["school_id", "receipt_book_id"], ["receipt_books.school_id", "receipt_books.id"], name="fk_receipt_issues_book_same_school"),
        sa.ForeignKeyConstraint(["school_id", "replacement_issue_id"], ["receipt_issues.school_id", "receipt_issues.id"], name="fk_receipt_issues_replacement_same_school"),
        sa.UniqueConstraint("school_id", "id", name="uq_receipt_issues_school_id_id"),
        sa.UniqueConstraint("school_id", "receipt_book_id", "receipt_number", name="uq_receipt_issues_school_book_number"),
    )
    op.create_index("ix_receipt_issues_school_status", "receipt_issues", ["school_id", "status"])
    op.execute(
        """
        CREATE FUNCTION validate_receipt_issue_book_range()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM receipt_books book
                WHERE book.school_id = NEW.school_id
                  AND book.id = NEW.receipt_book_id
                  AND (book.first_number IS NULL OR NEW.receipt_number >= book.first_number)
                  AND (book.last_number IS NULL OR NEW.receipt_number <= book.last_number)
            ) THEN
                RAISE EXCEPTION 'Receipt number is outside its receipt book range'
                    USING ERRCODE = '23514';
            END IF;
            RETURN NEW;
        END;
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_receipt_issues_validate_book_range
        BEFORE INSERT OR UPDATE OF school_id, receipt_book_id, receipt_number ON receipt_issues
        FOR EACH ROW EXECUTE FUNCTION validate_receipt_issue_book_range()
        """
    )
    op.execute(
        """
        CREATE FUNCTION validate_receipt_book_issue_ranges()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM receipt_issues issue
                WHERE issue.school_id = NEW.school_id
                  AND issue.receipt_book_id = NEW.id
                  AND (
                    (NEW.first_number IS NOT NULL AND issue.receipt_number < NEW.first_number)
                    OR (NEW.last_number IS NOT NULL AND issue.receipt_number > NEW.last_number)
                  )
            ) THEN
                RAISE EXCEPTION 'Receipt book range would invalidate an issued receipt number'
                    USING ERRCODE = '23514';
            END IF;
            RETURN NEW;
        END;
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_receipt_books_validate_issue_ranges
        BEFORE UPDATE OF first_number, last_number ON receipt_books
        FOR EACH ROW EXECUTE FUNCTION validate_receipt_book_issue_ranges()
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_receipt_issues_terminal_immutable
        BEFORE UPDATE OR DELETE ON receipt_issues
        FOR EACH ROW WHEN (OLD.status IN ('issued', 'cancelled', 'spoiled'))
        EXECUTE FUNCTION reject_immutable_row_change()
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_receipt_books_validate_issue_ranges ON receipt_books")
    op.execute("DROP TRIGGER IF EXISTS trg_receipt_issues_terminal_immutable ON receipt_issues")
    op.execute("DROP TRIGGER IF EXISTS trg_receipt_issues_validate_book_range ON receipt_issues")
    op.drop_index("ix_receipt_issues_school_status", table_name="receipt_issues")
    op.drop_table("receipt_issues")
    op.execute("DROP FUNCTION IF EXISTS validate_receipt_issue_book_range()")
    op.execute("DROP TRIGGER IF EXISTS trg_receipt_books_no_delete ON receipt_books")
    op.drop_index("ix_receipt_books_school_fiscal_status", table_name="receipt_books")
    op.drop_table("receipt_books")
    op.execute("DROP FUNCTION IF EXISTS validate_receipt_book_issue_ranges()")
    op.execute("DROP FUNCTION IF EXISTS allocate_document_sequence(uuid, uuid, varchar)")
    op.drop_table("document_sequences")
    op.execute("DROP TRIGGER IF EXISTS trg_bank_account_ledger_bindings_immutable ON bank_account_ledger_bindings")
    op.execute("DROP TRIGGER IF EXISTS trg_bank_account_ledger_bindings_validate_period ON bank_account_ledger_bindings")
    op.drop_index("ix_bank_account_ledger_bindings_school_ledger_dates", table_name="bank_account_ledger_bindings")
    op.drop_table("bank_account_ledger_bindings")
    op.execute("DROP FUNCTION IF EXISTS validate_bank_account_ledger_binding()")
    op.execute("DROP TRIGGER IF EXISTS trg_bank_accounts_validate_lifecycle_bindings ON bank_accounts")
    op.drop_index("ix_bank_accounts_school_fingerprint", table_name="bank_accounts")
    op.drop_table("bank_accounts")
    op.execute("DROP FUNCTION IF EXISTS validate_bank_account_lifecycle_bindings()")
    op.drop_index("uq_staff_people_school_number", table_name="staff_people")
    op.drop_index("uq_staff_people_school_external_ref", table_name="staff_people")
    op.drop_table("staff_people")
    op.drop_index("uq_student_accounts_school_number", table_name="student_accounts")
    op.drop_index("uq_student_accounts_school_external_ref", table_name="student_accounts")
    op.drop_table("student_accounts")
    op.drop_index("ix_parties_school_type_name", table_name="parties")
    op.drop_index("uq_parties_school_type_external_ref", table_name="parties")
    op.drop_table("parties")
    op.drop_index("ix_school_ledger_accounts_school_status_effective", table_name="school_ledger_accounts")
    op.execute("DROP TRIGGER IF EXISTS trg_school_ledger_accounts_validate_bank_bindings ON school_ledger_accounts")
    op.drop_table("school_ledger_accounts")
    op.execute("DROP FUNCTION IF EXISTS validate_ledger_account_bank_bindings()")
