"""PostgreSQL tests for operational workflow and reconciliation tables."""
from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator
from datetime import date

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import NullPool, delete, text, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from school_accounting.infrastructure.db.models import Advance, AdvanceSettlement, AuditEvent, AuthorizationDecision, BankAccount, BankReconciliation, BankStatement, BankStatementLine, Deposit, DepositRefund, FinancialDocument, FiscalYear, LifecycleEvent, Party, PayrollRun, PayrollRunItem, School, SchoolMembership, StaffPerson, TravelClaim, TravelOrder, User

TEST_DATABASE_URL = os.environ.get("SCHOOL_ACCOUNTING_TEST_DATABASE_URL")

def config() -> Config:
    result = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini")); result.set_main_option("sqlalchemy.url", TEST_DATABASE_URL or ""); return result

@pytest.fixture(scope="module", autouse=True)
def migrated() -> Iterator[None]:
    if not TEST_DATABASE_URL: pytest.skip("SCHOOL_ACCOUNTING_TEST_DATABASE_URL is required")
    command.upgrade(config(), "head"); yield; command.downgrade(config(), "base")

@pytest.fixture
def sessions() -> Iterator[async_sessionmaker[AsyncSession]]:
    assert TEST_DATABASE_URL
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    async def reset() -> None:
        async with engine.begin() as connection: await connection.execute(text("TRUNCATE schools CASCADE"))
    asyncio.run(reset()); yield async_sessionmaker(engine, expire_on_commit=False); asyncio.run(engine.dispose())

async def setup(session: AsyncSession, slug: str) -> tuple[School, FiscalYear, FinancialDocument, BankAccount]:
    school = School(slug=slug, name=slug, status="active"); session.add(school); await session.flush()
    year = FiscalYear(school_id=school.id, code="2082/83", bs_start="2082-04-01", bs_end="2083-03-31", ad_start=date(2025, 7, 17), ad_end=date(2026, 7, 16), status="active"); session.add(year); await session.flush()
    document = FinancialDocument(school_id=school.id, fiscal_year_id=year.id, document_type="operational", document_number="1", accounting_date=date(2025, 8, 1), status="draft"); bank = BankAccount(school_id=school.id, account_name="Bank", account_identity_fingerprint=slug.encode(), status="active")
    session.add_all([document, bank]); await session.flush(); return school, year, document, bank

def test_cross_school_subtype_and_payroll_staff_links_fail(sessions: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with sessions() as s:
            first, fy, doc, _ = await setup(s, "operations-first"); second, _, other_doc, _ = await setup(s, "operations-second")
            staff = StaffPerson(school_id=second.id, name="Other", employment_status="active"); s.add(staff); await s.commit()
            ids = first.id, doc.id, second.id, other_doc.id, staff.id
            s.add(PayrollRun(school_id=ids[0], document_id=ids[3], period_start=date(2025, 7, 1), period_end=date(2025, 7, 31), status="draft"))
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
            run = PayrollRun(school_id=ids[0], document_id=ids[1], period_start=date(2025, 7, 1), period_end=date(2025, 7, 31), status="draft"); s.add(run); await s.flush()
            s.add(PayrollRunItem(school_id=ids[0], payroll_run_id=run.id, line_no=1, staff_person_id=ids[4], gross_amount=1))
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
    asyncio.run(scenario())

def test_settlement_refund_and_travel_tenant_links_fail(sessions: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with sessions() as s:
            first, _, doc, _ = await setup(s, "links-first"); second, _, other_doc, _ = await setup(s, "links-second")
            party = Party(school_id=second.id, party_type="person", name="Other", status="active"); s.add(party); await s.commit()
            first_id, doc_id, fiscal_year_id, other_doc_id, party_id = first.id, doc.id, doc.fiscal_year_id, other_doc.id, party.id
            advance = Advance(school_id=first_id, document_id=doc_id, amount=10, status="draft"); deposit = Deposit(school_id=first_id, document_id=doc_id, depositor_party_id=party_id, amount=10, status="active")
            s.add_all([advance, deposit])
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
            advance = Advance(school_id=first_id, document_id=doc_id, amount=10, status="draft"); s.add(advance); await s.flush(); advance_id = advance.id
            s.add(AdvanceSettlement(school_id=first_id, advance_id=advance_id, document_id=other_doc_id, amount=1, settled_on=date(2025, 8, 1)))
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
            order = TravelOrder(school_id=first_id, document_id=doc_id); s.add(order); await s.flush()
            s.add(TravelClaim(school_id=first_id, travel_order_id=order.id, document_id=other_doc_id, amount=1))
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
            deposit_document = FinancialDocument(school_id=first_id, fiscal_year_id=fiscal_year_id, document_type="deposit", document_number="deposit", accounting_date=date(2025, 8, 1), status="draft")
            local_party = Party(school_id=first_id, party_type="person", name="Local", status="active")
            s.add_all([deposit_document, local_party]); await s.flush()
            deposit = Deposit(school_id=first_id, document_id=deposit_document.id, depositor_party_id=local_party.id, amount=10, status="active"); s.add(deposit); await s.flush()
            s.add(DepositRefund(school_id=first_id, deposit_id=deposit.id, document_id=other_doc_id, amount=1))
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
    asyncio.run(scenario())

def test_bank_statement_and_reconciliation_isolation_and_verified_immutability(sessions: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with sessions() as s:
            first, fy, _, bank = await setup(s, "bank-first"); second, other_fy, _, other_bank = await setup(s, "bank-second"); await s.commit()
            first_id, fy_id, bank_id, other_fy_id, other_bank_id = first.id, fy.id, bank.id, other_fy.id, other_bank.id
            s.add(BankStatement(school_id=first_id, bank_account_id=other_bank_id, fiscal_year_id=fy_id, period_start=date(2025, 7, 1), period_end=date(2025, 7, 31), closing_balance=0, status="draft"))
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
            statement = BankStatement(school_id=first_id, bank_account_id=bank_id, fiscal_year_id=fy_id, period_start=date(2025, 7, 1), period_end=date(2025, 7, 31), closing_balance=0, status="draft"); s.add(statement); await s.flush()
            line = BankStatementLine(school_id=first_id, statement_id=statement.id, line_no=1, transaction_date=date(2025, 7, 2), amount=1, external_line_ref="x"); s.add(line); await s.commit()
            statement_id, line_id = statement.id, line.id
            s.add(BankStatementLine(school_id=first_id, statement_id=statement_id, line_no=1, transaction_date=date(2025, 7, 2), amount=1))
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
            await s.execute(update(BankStatement).where(BankStatement.id == statement_id).values(status="verified")); await s.commit()
            with pytest.raises(DBAPIError): await s.execute(update(BankStatementLine).where(BankStatementLine.id == line_id).values(description="changed"))
            await s.rollback()
            s.add(BankReconciliation(school_id=first_id, bank_account_id=bank_id, statement_id=statement_id, fiscal_year_id=other_fy_id, as_of_date=date(2025, 7, 31), status="draft"))
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
    asyncio.run(scenario())

def test_new_event_targets_and_unsupported_targets(sessions: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with sessions() as s:
            school, _, doc, _ = await setup(s, "events-operations")
            advance = Advance(school_id=school.id, document_id=doc.id, amount=1, status="draft"); user = User(email="operations-events@example.test", status="active"); s.add_all([advance, user]); await s.flush()
            membership = SchoolMembership(school_id=school.id, user_id=user.id, status="active"); s.add(membership); await s.flush()
            s.add_all([LifecycleEvent(school_id=school.id, entity_type="advance", entity_id=advance.id, to_status="approved"), AuthorizationDecision(school_id=school.id, actor_membership_id=membership.id, target_type="advance", target_id=advance.id, decision_type="approve", status="approved"), AuditEvent(school_id=school.id, action="advance.create", target_type="advance", target_id=advance.id)])
            await s.commit(); school_id = school.id
            s.add(AuditEvent(school_id=school_id, action="bad", target_type="unsupported", target_id=advance.id))
            with pytest.raises(IntegrityError): await s.commit()
            await s.rollback()
    asyncio.run(scenario())
