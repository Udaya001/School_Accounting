"""PostgreSQL tests for system-owned accounting/reference constraints."""

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

from school_accounting.infrastructure.db.models import (
    AccountCodeVersion,
    LedgerAccountDefinition,
    OfficialTemplateVersion,
    RuleSetVersion,
    SupportedLocale,
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
                    "TRUNCATE official_template_versions, ledger_account_definitions, "
                    "account_code_versions, rule_set_versions, supported_locales"
                )
            )

    asyncio.run(reset())
    yield async_sessionmaker(engine, expire_on_commit=False)
    asyncio.run(engine.dispose())


def test_sequential_published_rule_versions_are_accepted(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            session.add_all(
                [
                    RuleSetVersion(
                        rule_key="tax.rate", version="2025", effective_from=date(2025, 1, 1),
                        effective_to=date(2025, 12, 31), context={}, status="published",
                    ),
                    RuleSetVersion(
                        rule_key="tax.rate", version="2026", effective_from=date(2026, 1, 1),
                        effective_to=None, context={}, status="published",
                    ),
                ]
            )
            await session.commit()

    asyncio.run(scenario())


def test_overlapping_published_rule_versions_are_rejected(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            session.add(
                RuleSetVersion(
                    rule_key="tax.rate", version="2025", effective_from=date(2025, 1, 1),
                    effective_to=date(2025, 12, 31), context={}, status="published",
                )
            )
            await session.commit()
            session.add(
                RuleSetVersion(
                    rule_key="tax.rate", version="2025-revision", effective_from=date(2025, 6, 1),
                    effective_to=None, context={}, status="published",
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_same_annex_code_is_allowed_for_income_and_expense(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            session.add_all(
                [
                    AccountCodeVersion(
                        code="101", kind="income", title="Income title", meaning="Income meaning",
                        effective_from=date(2025, 1, 1), status="published",
                    ),
                    AccountCodeVersion(
                        code="101", kind="expense", title="Expense title", meaning="Expense meaning",
                        effective_from=date(2025, 1, 1), status="published",
                    ),
                ]
            )
            await session.commit()

    asyncio.run(scenario())


def test_published_reference_rows_are_immutable(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            rule = RuleSetVersion(rule_key="rule", version="1", effective_from=date(2025, 1, 1), context={}, status="published")
            code = AccountCodeVersion(code="101", kind="income", title="Title", meaning="Meaning", effective_from=date(2025, 1, 1), status="published")
            ledger = LedgerAccountDefinition(semantic_key="cash", name="Cash", normal_side="debit", effective_from=date(2025, 1, 1), rule_context={}, status="published")
            template = OfficialTemplateVersion(template_key="SAM-FORM-01", language="ne", version="1", effective_from=date(2025, 1, 1), renderer_ref="forms/form-01", status="published")
            session.add_all([rule, code, ledger, template])
            await session.commit()

            for model, row_id in ((RuleSetVersion, rule.id), (AccountCodeVersion, code.id), (LedgerAccountDefinition, ledger.id), (OfficialTemplateVersion, template.id)):
                with pytest.raises(DBAPIError):
                    await session.execute(update(model).where(model.id == row_id).values(status="retired"))
                await session.rollback()
                with pytest.raises(DBAPIError):
                    await session.execute(delete(model).where(model.id == row_id))
                await session.rollback()

    asyncio.run(scenario())


def test_classification_codes_and_ledger_definitions_are_separate(session_factory: async_sessionmaker[AsyncSession]) -> None:
    assert AccountCodeVersion.__tablename__ != LedgerAccountDefinition.__tablename__
    assert "code" in AccountCodeVersion.__table__.c
    assert "semantic_key" in LedgerAccountDefinition.__table__.c


def test_supported_locale_code_is_unique(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            session.add(SupportedLocale(code="ne", name="Nepali", status="active"))
            await session.commit()
            session.add(SupportedLocale(code="ne", name="Nepali", status="active"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())
