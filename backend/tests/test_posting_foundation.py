"""PostgreSQL constraints for the immutable posting foundation."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator
from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import NullPool, delete, text, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from school_accounting.infrastructure.db.models import (
    BankAccount, BankAccountLedgerBinding, BankReconciliation, BankReconciliationItem,
    BankStatement, BankStatementLine, CorrectionLink, FinancialDocument, FiscalYear,
    IdempotencyRecord, JournalEntry, JournalLine, PostingRequest, PostingResult,
    RuleSetVersion, School, SchoolLedgerAccount,
)


TEST_DATABASE_URL = os.environ.get("SCHOOL_ACCOUNTING_TEST_DATABASE_URL")


def config() -> Config:
    result = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    result.set_main_option("sqlalchemy.url", TEST_DATABASE_URL or "")
    return result


@pytest.fixture(scope="module", autouse=True)
def migrated() -> Iterator[None]:
    if not TEST_DATABASE_URL:
        pytest.skip("SCHOOL_ACCOUNTING_TEST_DATABASE_URL is required")
    command.upgrade(config(), "head")
    yield
    command.downgrade(config(), "base")


@pytest.fixture
def sessions() -> Iterator[async_sessionmaker[AsyncSession]]:
    assert TEST_DATABASE_URL
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

    async def reset() -> None:
        async with engine.begin() as connection:
            await connection.execute(text("TRUNCATE schools CASCADE"))

    asyncio.run(reset())
    yield async_sessionmaker(engine, expire_on_commit=False)
    asyncio.run(engine.dispose())


async def setup(session: AsyncSession, slug: str) -> tuple[School, FiscalYear, FinancialDocument, RuleSetVersion, SchoolLedgerAccount, SchoolLedgerAccount]:
    school = School(slug=slug, name=slug, status="active")
    session.add(school)
    await session.flush()
    year = FiscalYear(school_id=school.id, code="2082/83", bs_start="2082-04-01", bs_end="2083-03-31", ad_start=date(2025, 7, 17), ad_end=date(2026, 7, 16), status="active")
    session.add(year)
    await session.flush()
    document = FinancialDocument(school_id=school.id, fiscal_year_id=year.id, document_type="payment", document_number="1", accounting_date=date(2025, 8, 1), status="approved", approved_at=datetime.now(timezone.utc))
    rule = RuleSetVersion(rule_key=f"posting.{slug}", version="1", effective_from=date(2025, 1, 1), context={}, status="published")
    cash = SchoolLedgerAccount(school_id=school.id, account_code="bank", name="Bank", status="active", effective_from=date(2025, 1, 1))
    expense = SchoolLedgerAccount(school_id=school.id, account_code="expense", name="Expense", status="active", effective_from=date(2025, 1, 1))
    session.add_all([document, rule, cash, expense])
    await session.flush()
    return school, year, document, rule, cash, expense


async def posted_entry(session: AsyncSession, school: School, year: FiscalYear, document: FinancialDocument, rule: RuleSetVersion, debit: SchoolLedgerAccount, credit: SchoolLedgerAccount, accounting_date: date = date(2025, 8, 1)) -> tuple[PostingRequest, JournalEntry, JournalLine]:
    request = PostingRequest(school_id=school.id, document_id=document.id, fiscal_year_id=year.id, accounting_date=accounting_date, rule_set_version_id=rule.id, idempotency_key=uuid4(), status="succeeded", finalized_at=datetime.now(timezone.utc))
    session.add(request)
    await session.flush()
    result = PostingResult(school_id=school.id, posting_request_id=request.id, rule_context={}, account_code_context={}, result_hash=b"result")
    session.add(result)
    await session.flush()
    entry = JournalEntry(school_id=school.id, posting_result_id=result.id, fiscal_year_id=year.id, accounting_date=accounting_date, entry_hash=b"entry")
    session.add(entry)
    await session.flush()
    first = JournalLine(school_id=school.id, journal_entry_id=entry.id, line_no=1, ledger_account_id=debit.id, debit_amount=Decimal("10.00"), credit_amount=Decimal("0"))
    second = JournalLine(school_id=school.id, journal_entry_id=entry.id, line_no=2, ledger_account_id=credit.id, debit_amount=Decimal("0"), credit_amount=Decimal("10.00"))
    session.add_all([first, second])
    document.status = "posted"
    document.posted_at = datetime.now(timezone.utc)
    return request, entry, first


def test_posting_tenant_references_duplicate_document_and_idempotency_scope(sessions: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with sessions() as session:
            first, first_year, first_doc, first_rule, _, _ = await setup(session, "posting-first")
            second, second_year, second_doc, second_rule, _, _ = await setup(session, "posting-second")
            await session.commit()
            first_id, second_id, first_year_id, first_doc_id, second_doc_id, first_rule_id = first.id, second.id, first_year.id, first_doc.id, second_doc.id, first_rule.id
            session.add(PostingRequest(school_id=first_id, document_id=second_doc_id, fiscal_year_id=first_year_id, accounting_date=date(2025, 8, 1), rule_set_version_id=first_rule_id, idempotency_key=uuid4(), status="pending"))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
            key = uuid4()
            session.add_all([IdempotencyRecord(school_id=first_id, operation_key=key, request_fingerprint=b"same", result_status="in_progress"), IdempotencyRecord(school_id=second_id, operation_key=key, request_fingerprint=b"same", result_status="in_progress")])
            await session.commit()
            session.add(IdempotencyRecord(school_id=first_id, operation_key=key, request_fingerprint=b"other", result_status="in_progress"))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
            request = PostingRequest(school_id=first_id, document_id=first_doc_id, fiscal_year_id=first_year_id, accounting_date=date(2025, 8, 1), rule_set_version_id=first_rule_id, idempotency_key=uuid4(), status="pending")
            session.add(request); await session.commit()
            session.add(PostingRequest(school_id=first_id, document_id=first_doc_id, fiscal_year_id=first_year_id, accounting_date=date(2025, 8, 1), rule_set_version_id=first_rule_id, idempotency_key=uuid4(), status="pending"))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
    asyncio.run(scenario())


def test_journal_constraints_balance_and_immutability(sessions: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with sessions() as session:
            school, year, document, rule, cash, expense = await setup(session, "journal")
            request, entry, line = await posted_entry(session, school, year, document, rule, expense, cash)
            await session.commit()
            school_id, year_id, rule_id, cash_id, line_id = school.id, year.id, rule.id, cash.id, line.id
            with pytest.raises(DBAPIError): await session.execute(update(JournalEntry).where(JournalEntry.id == entry.id).values(description="changed"))
            await session.rollback()
            with pytest.raises(DBAPIError): await session.execute(delete(JournalLine).where(JournalLine.id == line_id))
            await session.rollback()
            bad_doc = FinancialDocument(school_id=school_id, fiscal_year_id=year_id, document_type="payment", document_number="2", accounting_date=date(2025, 8, 1), status="approved", approved_at=datetime.now(timezone.utc)); session.add(bad_doc); await session.flush()
            request = PostingRequest(school_id=school_id, document_id=bad_doc.id, fiscal_year_id=year_id, accounting_date=date(2025, 8, 1), rule_set_version_id=rule_id, idempotency_key=uuid4(), status="succeeded", finalized_at=datetime.now(timezone.utc)); session.add(request); await session.flush()
            result = PostingResult(school_id=school_id, posting_request_id=request.id, rule_context={}, account_code_context={}, result_hash=b"bad"); session.add(result); await session.flush()
            bad = JournalEntry(school_id=school_id, posting_result_id=result.id, fiscal_year_id=year_id, accounting_date=date(2025, 8, 1), entry_hash=b"bad"); session.add(bad); await session.flush()
            session.add(JournalLine(school_id=school_id, journal_entry_id=bad.id, line_no=1, ledger_account_id=cash_id, debit_amount=Decimal("9"), credit_amount=Decimal("0")))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
            shape_doc = FinancialDocument(school_id=school_id, fiscal_year_id=year_id, document_type="payment", document_number="3", accounting_date=date(2025, 8, 1), status="approved", approved_at=datetime.now(timezone.utc)); session.add(shape_doc); await session.flush()
            request = PostingRequest(school_id=school_id, document_id=shape_doc.id, fiscal_year_id=year_id, accounting_date=date(2025, 8, 1), rule_set_version_id=rule_id, idempotency_key=uuid4(), status="succeeded", finalized_at=datetime.now(timezone.utc)); session.add(request); await session.flush()
            result = PostingResult(school_id=school_id, posting_request_id=request.id, rule_context={}, account_code_context={}, result_hash=b"shape"); session.add(result); await session.flush()
            shape = JournalEntry(school_id=school_id, posting_result_id=result.id, fiscal_year_id=year_id, accounting_date=date(2025, 8, 1), entry_hash=b"shape"); session.add(shape); await session.flush()
            session.add(JournalLine(school_id=school_id, journal_entry_id=shape.id, line_no=1, ledger_account_id=cash_id, debit_amount=Decimal("0"), credit_amount=Decimal("0")))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
    asyncio.run(scenario())


def test_journal_ledger_and_correction_links_are_tenant_safe(sessions: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with sessions() as session:
            first, year, doc, rule, cash, expense = await setup(session, "links-first")
            second, _, other_doc, _, other_cash, _ = await setup(session, "links-second")
            await session.commit()
            first_id, year_id, doc_id, rule_id, other_doc_id, other_cash_id = first.id, year.id, doc.id, rule.id, other_doc.id, other_cash.id
            request = PostingRequest(school_id=first_id, document_id=doc_id, fiscal_year_id=year_id, accounting_date=date(2025, 8, 1), rule_set_version_id=rule_id, idempotency_key=uuid4(), status="succeeded", finalized_at=datetime.now(timezone.utc)); session.add(request); await session.flush()
            result = PostingResult(school_id=first_id, posting_request_id=request.id, rule_context={}, account_code_context={}, result_hash=b"x"); session.add(result); await session.flush()
            entry = JournalEntry(school_id=first_id, posting_result_id=result.id, fiscal_year_id=year_id, accounting_date=date(2025, 8, 1), entry_hash=b"x"); session.add(entry); await session.flush()
            session.add(JournalLine(school_id=first_id, journal_entry_id=entry.id, line_no=1, ledger_account_id=other_cash_id, debit_amount=Decimal("1"), credit_amount=Decimal("0")))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
            session.add(CorrectionLink(school_id=first_id, original_document_id=doc_id, correcting_document_id=other_doc_id, correction_type="reversal", reason="x"))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
            session.add(CorrectionLink(school_id=first_id, original_document_id=doc_id, correcting_document_id=doc_id, correction_type="reversal", reason="x"))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
    asyncio.run(scenario())


def test_reconciliation_requires_effective_bank_journal_line(sessions: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with sessions() as session:
            school, year, document, rule, old_bank_ledger, new_bank_ledger = await setup(session, "reconciliation")
            bank = BankAccount(school_id=school.id, account_name="Bank", account_identity_fingerprint=b"bank", status="active")
            session.add(bank); await session.flush()
            session.add_all([BankAccountLedgerBinding(school_id=school.id, bank_account_id=bank.id, ledger_account_id=old_bank_ledger.id, effective_from=date(2025, 1, 1), effective_to=date(2025, 7, 31)), BankAccountLedgerBinding(school_id=school.id, bank_account_id=bank.id, ledger_account_id=new_bank_ledger.id, effective_from=date(2025, 8, 1))])
            statement = BankStatement(school_id=school.id, bank_account_id=bank.id, fiscal_year_id=year.id, period_start=date(2025, 8, 1), period_end=date(2025, 8, 31), closing_balance=0, status="draft"); session.add(statement); await session.flush()
            statement_line = BankStatementLine(school_id=school.id, statement_id=statement.id, line_no=1, transaction_date=date(2025, 8, 2), amount=10); session.add(statement_line); await session.flush()
            reconciliation = BankReconciliation(school_id=school.id, bank_account_id=bank.id, statement_id=statement.id, fiscal_year_id=year.id, as_of_date=date(2025, 8, 31), status="draft"); session.add(reconciliation)
            _, entry, line = await posted_entry(session, school, year, document, rule, new_bank_ledger, old_bank_ledger)
            await session.commit()
            session.add(BankReconciliationItem(school_id=school.id, reconciliation_id=reconciliation.id, statement_line_id=statement_line.id, journal_line_id=line.id, difference_amount=0, status="confirmed")); await session.commit()
            bad_doc = FinancialDocument(school_id=school.id, fiscal_year_id=year.id, document_type="payment", document_number="later", accounting_date=date(2025, 8, 2), status="approved", approved_at=datetime.now(timezone.utc)); session.add(bad_doc); await session.flush()
            _, _, old_line = await posted_entry(session, school, year, bad_doc, rule, old_bank_ledger, new_bank_ledger, date(2025, 8, 2))
            session.add(BankReconciliationItem(school_id=school.id, reconciliation_id=reconciliation.id, statement_line_id=statement_line.id, journal_line_id=old_line.id, difference_amount=0, status="confirmed"))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
    asyncio.run(scenario())
