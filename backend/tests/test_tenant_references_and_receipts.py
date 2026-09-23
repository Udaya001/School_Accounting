"""PostgreSQL tests for tenant reference, bank binding, sequence, and receipt controls."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator
from datetime import date, datetime, timezone

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import NullPool, select, text, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from school_accounting.infrastructure.db.models import (
    BankAccount,
    BankAccountLedgerBinding,
    DocumentSequence,
    FiscalYear,
    LedgerAccountDefinition,
    Party,
    ReceiptBook,
    ReceiptIssue,
    School,
    SchoolLedgerAccount,
    StaffPerson,
    StudentAccount,
)


TEST_DATABASE_URL = os.environ.get("SCHOOL_ACCOUNTING_TEST_DATABASE_URL")


def _alembic_config() -> Config:
    config = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL or "")
    return config


@pytest.fixture(scope="module", autouse=True)
def migrated_database() -> Iterator[None]:
    if not TEST_DATABASE_URL:
        pytest.skip("SCHOOL_ACCOUNTING_TEST_DATABASE_URL is required for PostgreSQL constraint tests")
    command.upgrade(_alembic_config(), "head")
    yield
    command.downgrade(_alembic_config(), "base")


@pytest.fixture
def session_factory() -> Iterator[async_sessionmaker[AsyncSession]]:
    assert TEST_DATABASE_URL
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

    async def reset() -> None:
        async with engine.begin() as connection:
            await connection.execute(
                text(
                    "TRUNCATE receipt_issues, receipt_books, document_sequences, "
                    "bank_account_ledger_bindings, bank_accounts, school_ledger_accounts, "
                    "parties, student_accounts, staff_people CASCADE"
                )
            )

    asyncio.run(reset())
    yield async_sessionmaker(engine, expire_on_commit=False)
    asyncio.run(engine.dispose())


async def create_school_and_fiscal_year(session: AsyncSession, slug: str) -> tuple[School, FiscalYear]:
    school = School(slug=slug, name=slug, status="active")
    session.add(school)
    await session.flush()
    fiscal_year = FiscalYear(
        school_id=school.id,
        code="2082/83",
        bs_start="2082-04-01",
        bs_end="2083-03-31",
        ad_start=date(2025, 7, 17),
        ad_end=date(2026, 7, 16),
        status="active",
    )
    session.add(fiscal_year)
    await session.flush()
    return school, fiscal_year


async def create_ledger_account(
    session: AsyncSession,
    school: School,
    code: str = "BANK",
    effective_from: date = date(2025, 1, 1),
    effective_to: date | None = None,
) -> SchoolLedgerAccount:
    definition = LedgerAccountDefinition(
        semantic_key=f"{school.slug}.{code}.{effective_from.isoformat()}",
        name=code,
        normal_side="debit",
        effective_from=effective_from,
        rule_context={},
        status="draft",
    )
    session.add(definition)
    await session.flush()
    ledger = SchoolLedgerAccount(
        school_id=school.id,
        definition_id=definition.id,
        account_code=code,
        name=code,
        status="active",
        effective_from=effective_from,
        effective_to=effective_to,
    )
    session.add(ledger)
    await session.flush()
    return ledger


async def create_bank_account(session: AsyncSession, school: School, **values: object) -> BankAccount:
    defaults: dict[str, object] = {
        "school_id": school.id,
        "account_name": "Bank",
        "account_identity_fingerprint": b"fingerprint",
        "status": "active",
        "opened_on": date(2025, 1, 1),
    }
    defaults.update(values)
    bank = BankAccount(**defaults)
    session.add(bank)
    await session.flush()
    return bank


def test_historical_bank_ledger_bindings_are_sequential(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, _ = await create_school_and_fiscal_year(session, "binding-history")
            first = await create_ledger_account(session, school, effective_to=date(2025, 6, 30))
            second = await create_ledger_account(session, school, effective_from=date(2025, 7, 1))
            bank = await create_bank_account(session, school)
            session.add_all(
                [
                    BankAccountLedgerBinding(school_id=school.id, bank_account_id=bank.id, ledger_account_id=first.id, effective_from=date(2025, 1, 1), effective_to=date(2025, 6, 30)),
                    BankAccountLedgerBinding(school_id=school.id, bank_account_id=bank.id, ledger_account_id=second.id, effective_from=date(2025, 7, 1)),
                ]
            )
            await session.commit()

    asyncio.run(scenario())


def test_overlapping_bank_ledger_bindings_are_rejected(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, _ = await create_school_and_fiscal_year(session, "binding-overlap")
            ledger = await create_ledger_account(session, school)
            bank = await create_bank_account(session, school)
            session.add(BankAccountLedgerBinding(school_id=school.id, bank_account_id=bank.id, ledger_account_id=ledger.id, effective_from=date(2025, 1, 1), effective_to=date(2025, 6, 30)))
            await session.commit()
            session.add(BankAccountLedgerBinding(school_id=school.id, bank_account_id=bank.id, ledger_account_id=ledger.id, effective_from=date(2025, 6, 30), effective_to=date(2025, 12, 31)))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_cross_school_bank_binding_is_rejected(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            first, _ = await create_school_and_fiscal_year(session, "binding-first")
            second, _ = await create_school_and_fiscal_year(session, "binding-second")
            bank = await create_bank_account(session, first)
            ledger = await create_ledger_account(session, second)
            session.add(BankAccountLedgerBinding(school_id=first.id, bank_account_id=bank.id, ledger_account_id=ledger.id, effective_from=date(2025, 1, 1)))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_bank_binding_cannot_exceed_ledger_period(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, _ = await create_school_and_fiscal_year(session, "binding-period")
            ledger = await create_ledger_account(session, school, effective_to=date(2025, 6, 30))
            bank = await create_bank_account(session, school)
            session.add(BankAccountLedgerBinding(school_id=school.id, bank_account_id=bank.id, ledger_account_id=ledger.id, effective_from=date(2025, 1, 1), effective_to=date(2025, 7, 1)))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_ledger_and_bank_dates_cannot_invalidate_bindings(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, _ = await create_school_and_fiscal_year(session, "binding-dates")
            ledger = await create_ledger_account(session, school, effective_to=date(2025, 12, 31))
            bank = await create_bank_account(session, school, closed_on=date(2025, 12, 31), status="closed")
            session.add(BankAccountLedgerBinding(school_id=school.id, bank_account_id=bank.id, ledger_account_id=ledger.id, effective_from=date(2025, 2, 1), effective_to=date(2025, 6, 30)))
            await session.commit()
            ledger_id, bank_id = ledger.id, bank.id
            with pytest.raises(DBAPIError):
                await session.execute(update(SchoolLedgerAccount).where(SchoolLedgerAccount.id == ledger_id).values(effective_to=date(2025, 5, 31)))
            await session.rollback()
            with pytest.raises(DBAPIError):
                await session.execute(update(BankAccount).where(BankAccount.id == bank_id).values(opened_on=date(2025, 3, 1)))
            await session.rollback()
            with pytest.raises(DBAPIError):
                await session.execute(update(BankAccount).where(BankAccount.id == bank_id).values(closed_on=date(2025, 5, 31)))
            await session.rollback()

    asyncio.run(scenario())


def test_bank_fingerprint_detection_does_not_use_masked_number(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, _ = await create_school_and_fiscal_year(session, "bank-fingerprint")
            fingerprint = b"protected-fingerprint"
            await create_bank_account(session, school, account_name="Bank A", account_number_masked="***1234", account_identity_fingerprint=fingerprint)
            await create_bank_account(session, school, account_name="Bank B", account_number_masked="***9876", account_identity_fingerprint=fingerprint)
            await session.commit()
            matches = await session.scalars(select(BankAccount).where(BankAccount.school_id == school.id, BankAccount.account_identity_fingerprint == fingerprint))
            assert len(list(matches)) == 2

    asyncio.run(scenario())


def test_party_student_and_staff_references_are_isolated_by_school(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            first, _ = await create_school_and_fiscal_year(session, "people-first")
            second, _ = await create_school_and_fiscal_year(session, "people-second")
            session.add_all(
                [
                    Party(school_id=first.id, party_type="supplier", name="Supplier", external_ref="shared", status="active"),
                    Party(school_id=second.id, party_type="supplier", name="Supplier", external_ref="shared", status="active"),
                    StudentAccount(school_id=first.id, external_ref="student", student_number="S-1", name="Student", status="active"),
                    StudentAccount(school_id=second.id, external_ref="student", student_number="S-1", name="Student", status="active"),
                    StaffPerson(school_id=first.id, external_ref="staff", staff_number="T-1", name="Staff", employment_status="active"),
                    StaffPerson(school_id=second.id, external_ref="staff", staff_number="T-1", name="Staff", employment_status="active"),
                ]
            )
            await session.commit()

    asyncio.run(scenario())


def test_document_sequence_allocation_is_atomic_under_concurrency(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, fiscal_year = await create_school_and_fiscal_year(session, "sequence")
            session.add(DocumentSequence(school_id=school.id, fiscal_year_id=fiscal_year.id, sequence_key="voucher", next_value=1))
            await session.commit()

        async def allocate() -> int:
            async with session_factory() as allocation_session:
                value = await allocation_session.scalar(text("SELECT allocate_document_sequence(:school_id, :fiscal_year_id, :sequence_key)").bindparams(school_id=school.id, fiscal_year_id=fiscal_year.id, sequence_key="voucher"))
                await allocation_session.commit()
                assert value is not None
                return value

        allocated = await asyncio.gather(*(allocate() for _ in range(8)))
        assert sorted(allocated) == list(range(1, 9))

    asyncio.run(scenario())


async def create_receipt_book(session: AsyncSession, slug: str) -> tuple[School, ReceiptBook]:
    school, fiscal_year = await create_school_and_fiscal_year(session, slug)
    book = ReceiptBook(school_id=school.id, fiscal_year_id=fiscal_year.id, book_code="A", first_number=10, last_number=20, status="active")
    session.add(book)
    await session.flush()
    return school, book


def test_receipt_number_outside_book_bounds_is_rejected(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, book = await create_receipt_book(session, "receipt-bounds")
            session.add(ReceiptIssue(school_id=school.id, receipt_book_id=book.id, receipt_number=9, status="reserved"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_receipt_book_range_cannot_invalidate_existing_numbers(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, book = await create_receipt_book(session, "receipt-range-change")
            session.add_all(
                [
                    ReceiptIssue(school_id=school.id, receipt_book_id=book.id, receipt_number=10, status="reserved"),
                    ReceiptIssue(school_id=school.id, receipt_book_id=book.id, receipt_number=20, status="issued", issued_at=datetime.now(timezone.utc)),
                ]
            )
            await session.commit()
            book_id = book.id
            with pytest.raises(DBAPIError):
                await session.execute(update(ReceiptBook).where(ReceiptBook.id == book_id).values(first_number=11))
            await session.rollback()
            with pytest.raises(DBAPIError):
                await session.execute(update(ReceiptBook).where(ReceiptBook.id == book_id).values(last_number=19))
            await session.rollback()

    asyncio.run(scenario())


def test_issued_receipt_requires_issued_at_and_self_replacement_is_rejected(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, book = await create_receipt_book(session, "receipt-state")
            await session.commit()
            school_id, book_id = school.id, book.id
            session.add(ReceiptIssue(school_id=school.id, receipt_book_id=book.id, receipt_number=10, status="issued"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()
            issue = ReceiptIssue(school_id=school_id, receipt_book_id=book_id, receipt_number=10, status="reserved")
            session.add(issue)
            await session.commit()
            issue_id = issue.id
            with pytest.raises(IntegrityError):
                await session.execute(update(ReceiptIssue).where(ReceiptIssue.id == issue_id).values(replacement_issue_id=issue_id))
            await session.rollback()

    asyncio.run(scenario())


def test_cancelled_and_spoiled_receipt_numbers_are_retained(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, book = await create_receipt_book(session, "receipt-retention")
            issue = ReceiptIssue(school_id=school.id, receipt_book_id=book.id, receipt_number=10, status="reserved")
            spoiled = ReceiptIssue(school_id=school.id, receipt_book_id=book.id, receipt_number=11, status="reserved")
            session.add_all([issue, spoiled])
            await session.commit()
            issue_id, spoiled_id, school_id, book_id = issue.id, spoiled.id, school.id, book.id
            await session.execute(update(ReceiptIssue).where(ReceiptIssue.id == issue_id).values(status="cancelled", cancel_reason="Mistake"))
            await session.execute(update(ReceiptIssue).where(ReceiptIssue.id == spoiled_id).values(status="spoiled", cancel_reason="Damaged"))
            await session.commit()
            session.add(ReceiptIssue(school_id=school_id, receipt_book_id=book_id, receipt_number=10, status="reserved"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()
            with pytest.raises(DBAPIError):
                await session.execute(update(ReceiptIssue).where(ReceiptIssue.id == issue_id).values(cancel_reason="Changed"))
            await session.rollback()

    asyncio.run(scenario())
