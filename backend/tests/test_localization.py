"""PostgreSQL tests for locale preferences and system reference translations."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator
from datetime import date

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import NullPool, func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from school_accounting.infrastructure.db.models import (
    AccountCodeVersion,
    AccountCodeVersionTranslation,
    LedgerAccountDefinition,
    LedgerAccountDefinitionTranslation,
    PermissionPreset,
    PermissionPresetTranslation,
    School,
    SchoolMembership,
    SchoolSettings,
    SupportedLocale,
    User,
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
            await connection.execute(text("TRUNCATE schools, users, account_code_versions, ledger_account_definitions, permission_presets CASCADE"))

    asyncio.run(reset())
    yield async_sessionmaker(engine, expire_on_commit=False)
    asyncio.run(engine.dispose())


async def school_and_user(session: AsyncSession, slug: str) -> tuple[School, User]:
    school = School(slug=slug, name=slug, status="active")
    user = User(email=f"{slug}@example.test", status="active")
    session.add_all([school, user])
    await session.flush()
    return school, user


def test_initial_locales_are_seeded(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            locales = set((await session.scalars(select(SupportedLocale.code).where(SupportedLocale.status == "active"))).all())
            assert {"en", "ne"} <= locales

    asyncio.run(scenario())


@pytest.mark.parametrize("locale", ["en", "ne"])
def test_school_default_locale_and_membership_override(
    session_factory: async_sessionmaker[AsyncSession], locale: str
) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, user = await school_and_user(session, f"school-locale-{locale}")
            settings = SchoolSettings(school_id=school.id, default_locale=locale)
            membership = SchoolMembership(school_id=school.id, user_id=user.id, status="active", preferred_locale="ne" if locale == "en" else "en")
            session.add_all([settings, membership])
            await session.commit()
            assert settings.default_locale == locale
            assert membership.preferred_locale == ("ne" if locale == "en" else "en")

    asyncio.run(scenario())


def test_unsupported_locale_references_are_rejected(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school, user = await school_and_user(session, "bad-locale")
            await session.commit()
            school_id, user_id = school.id, user.id
            session.add(SchoolSettings(school_id=school_id, default_locale="xx"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()
            session.add(SchoolMembership(school_id=school_id, user_id=user_id, status="active", preferred_locale="xx"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()
            code = AccountCodeVersion(code="T1", kind="income", title="Canonical", meaning="Canonical meaning", effective_from=date(2025, 1, 1), status="draft")
            session.add(code)
            await session.flush()
            session.add(AccountCodeVersionTranslation(account_code_version_id=code.id, locale="xx", title="Invalid", meaning="Invalid"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_one_canonical_reference_has_bilingual_translations_without_duplication(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            code = AccountCodeVersion(code="101", kind="income", title="Tuition", meaning="Canonical English source", effective_from=date(2025, 1, 1), status="published")
            ledger = LedgerAccountDefinition(semantic_key="cash", name="Cash", normal_side="debit", effective_from=date(2025, 1, 1), rule_context={}, status="draft")
            preset = PermissionPreset(code="accountant", name="Accountant", capabilities=[], status="active")
            session.add_all([code, ledger, preset])
            await session.flush()
            session.add_all(
                [
                    AccountCodeVersionTranslation(account_code_version_id=code.id, locale="en", title="Tuition", meaning="Tuition revenue"),
                    AccountCodeVersionTranslation(account_code_version_id=code.id, locale="ne", title="शिक्षण शुल्क", meaning="शिक्षण शुल्कबाट प्राप्त आम्दानी"),
                    LedgerAccountDefinitionTranslation(ledger_account_definition_id=ledger.id, locale="ne", name="नगद"),
                    PermissionPresetTranslation(permission_preset_id=preset.id, locale="ne", name="लेखापाल"),
                ]
            )
            await session.commit()
            code_id = code.id
            assert await session.scalar(select(func.count()).select_from(AccountCodeVersion).where(AccountCodeVersion.id == code_id)) == 1
            assert await session.scalar(select(func.count()).select_from(AccountCodeVersionTranslation).where(AccountCodeVersionTranslation.account_code_version_id == code_id)) == 2
            session.add(AccountCodeVersionTranslation(account_code_version_id=code_id, locale="en", title="Duplicate", meaning="Duplicate"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())
