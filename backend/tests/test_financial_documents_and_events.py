"""PostgreSQL tests for financial documents and append-only tenant events."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator
from datetime import date, datetime, timezone

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import NullPool, delete, text, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from school_accounting.infrastructure.db.models import (
    AuditEvent, AuthorizationDecision, FinancialDocument, FinancialDocumentItem, FiscalYear,
    IncomeReceipt, LifecycleEvent, Party, ReceiptBook, ReceiptIssue, School, SchoolMembership,
    StaffPerson, StudentAccount, User,
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
            await connection.execute(text("TRUNCATE financial_documents, receipt_issues, receipt_books, parties, student_accounts, staff_people, school_memberships, users, fiscal_years, schools CASCADE"))

    asyncio.run(reset())
    yield async_sessionmaker(engine, expire_on_commit=False)
    asyncio.run(engine.dispose())


async def school_with_year(session: AsyncSession, slug: str, year: str = "2082/83") -> tuple[School, FiscalYear]:
    school = School(slug=slug, name=slug, status="active")
    session.add(school)
    await session.flush()
    fiscal_year = FiscalYear(school_id=school.id, code=year, bs_start="2082-04-01", bs_end="2083-03-31", ad_start=date(2025, 7, 17), ad_end=date(2026, 7, 16), status="active")
    session.add(fiscal_year)
    await session.flush()
    return school, fiscal_year


async def document(session: AsyncSession, school: School, fiscal_year: FiscalYear, number: str = "1", document_type: str = "income", status: str = "draft") -> FinancialDocument:
    now = datetime.now(timezone.utc)
    result = FinancialDocument(school_id=school.id, fiscal_year_id=fiscal_year.id, document_type=document_type, document_number=number, accounting_date=date(2025, 8, 1), status=status, approved_at=now if status in {"approved", "posted", "locked"} else None, posted_at=now if status in {"posted", "locked"} else None, locked_at=now if status == "locked" else None)
    session.add(result)
    await session.flush()
    return result


async def receipt_issue(session: AsyncSession, school: School, fiscal_year: FiscalYear, number: int) -> ReceiptIssue:
    book = ReceiptBook(school_id=school.id, fiscal_year_id=fiscal_year.id, book_code=f"B{number}", first_number=number, last_number=number, status="active")
    session.add(book)
    await session.flush()
    issue = ReceiptIssue(school_id=school.id, receipt_book_id=book.id, receipt_number=number, status="reserved")
    session.add(issue)
    await session.flush()
    return issue


def test_document_tenant_links_and_number_scope(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            first, first_year = await school_with_year(session, "document-first")
            second, second_year = await school_with_year(session, "document-second")
            await document(session, first, first_year, "42")
            await document(session, second, second_year, "42")
            await document(session, first, first_year, "42", "expense")
            other_year = FiscalYear(school_id=first.id, code="2083/84", bs_start="2083-04-01", bs_end="2084-03-31", ad_start=date(2026, 7, 17), ad_end=date(2027, 7, 16), status="planned")
            session.add(other_year)
            await session.flush()
            await document(session, first, other_year, "42")
            await session.commit()
            first_id, first_year_id, second_year_id = first.id, first_year.id, second_year.id

            session.add(FinancialDocument(school_id=first_id, fiscal_year_id=second_year_id, document_type="income", document_number="cross", accounting_date=date(2025, 8, 1), status="draft"))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
            session.add(FinancialDocument(school_id=first_id, fiscal_year_id=first_year_id, document_type="income", document_number="42", accounting_date=date(2025, 8, 1), status="draft"))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
    asyncio.run(scenario())


def test_document_items_and_income_receipts_are_tenant_safe(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            first, first_year = await school_with_year(session, "details-first")
            second, second_year = await school_with_year(session, "details-second")
            first_doc, second_doc = await document(session, first, first_year), await document(session, second, second_year)
            student = StudentAccount(school_id=second.id, name="Student", status="active")
            staff = StaffPerson(school_id=second.id, name="Staff", employment_status="active")
            party = Party(school_id=second.id, party_type="payer", name="Party", status="active")
            session.add_all([student, staff, party])
            issue = await receipt_issue(session, second, second_year, 1)
            first_issue = await receipt_issue(session, first, first_year, 2)
            await session.commit()
            first_id, first_doc_id, first_year_id = first.id, first_doc.id, first_year.id
            second_id, second_year_id = second.id, second_year.id
            student_id, staff_id, party_id = student.id, staff.id, party.id
            issue_id, first_issue_id = issue.id, first_issue.id
            for column, value in (("student_account_id", student_id), ("staff_person_id", staff_id), ("party_id", party_id)):
                session.add(FinancialDocumentItem(school_id=first_id, document_id=first_doc_id, line_no=1, amount=1, **{column: value}))
                with pytest.raises(IntegrityError): await session.commit()
                await session.rollback()
            session.add(IncomeReceipt(school_id=first_id, document_id=first_doc_id, receipt_issue_id=issue_id, receipt_date=date(2025, 8, 1)))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
            session.add(IncomeReceipt(school_id=first_id, document_id=first_doc_id, receipt_issue_id=first_issue_id, receipt_date=date(2025, 8, 1)))
            await session.commit()
            another_document = FinancialDocument(school_id=first_id, fiscal_year_id=first_year_id, document_type="income", document_number="2", accounting_date=date(2025, 8, 1), status="draft")
            session.add(another_document)
            await session.flush()
            session.add(IncomeReceipt(school_id=first_id, document_id=another_document.id, receipt_issue_id=first_issue_id, receipt_date=date(2025, 8, 1)))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
    asyncio.run(scenario())


def test_posted_documents_lock_and_drafts_remain_mutable(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, year = await school_with_year(session, "document-lock")
            draft = await document(session, school, year, "draft")
            posted = await document(session, school, year, "posted", status="posted")
            await session.commit()
            draft_id, posted_id = draft.id, posted.id
            await session.execute(update(FinancialDocument).where(FinancialDocument.id == draft_id).values(summary="changed"))
            await session.commit()
            with pytest.raises(DBAPIError): await session.execute(update(FinancialDocument).where(FinancialDocument.id == posted_id).values(summary="changed"))
            await session.rollback()
            with pytest.raises(DBAPIError): await session.execute(delete(FinancialDocument).where(FinancialDocument.id == posted_id))
            await session.rollback()
    asyncio.run(scenario())


def test_tenant_events_are_append_only_and_targets_are_school_validated(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, year = await school_with_year(session, "events-first")
            other, other_year = await school_with_year(session, "events-second")
            target, other_target = await document(session, school, year), await document(session, other, other_year)
            user = User(email="event@example.test", status="active")
            session.add(user)
            await session.flush()
            membership = SchoolMembership(school_id=school.id, user_id=user.id, status="active")
            session.add(membership)
            await session.flush()
            lifecycle = LifecycleEvent(school_id=school.id, entity_type="financial_document", entity_id=target.id, to_status="submitted")
            decision = AuthorizationDecision(school_id=school.id, actor_membership_id=membership.id, target_type="financial_document", target_id=target.id, decision_type="approval", status="approved")
            audit = AuditEvent(school_id=school.id, actor_membership_id=membership.id, action="document.submit", target_type="financial_document", target_id=target.id)
            session.add_all([lifecycle, decision, audit])
            await session.commit()
            event_ids = ((LifecycleEvent, lifecycle.id), (AuthorizationDecision, decision.id), (AuditEvent, audit.id))
            school_id, other_target_id = school.id, other_target.id
            for model, event_id in event_ids:
                with pytest.raises(DBAPIError): await session.execute(update(model).where(model.id == event_id).values(created_at=datetime.now(timezone.utc)))
                await session.rollback()
                with pytest.raises(DBAPIError): await session.execute(delete(model).where(model.id == event_id))
                await session.rollback()
            session.add(AuditEvent(school_id=school_id, action="cross", target_type="financial_document", target_id=other_target_id))
            with pytest.raises(IntegrityError): await session.commit()
            await session.rollback()
    asyncio.run(scenario())
