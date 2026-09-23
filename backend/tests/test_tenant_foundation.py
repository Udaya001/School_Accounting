"""PostgreSQL constraint tests for the first tenant-foundation migration."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import NullPool, delete, func, select, text, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from school_accounting.infrastructure.db.models import (
    PermissionAssignment,
    PermissionPreset,
    PlatformAdministratorGrant,
    PlatformAuditEvent,
    School,
    SchoolFund,
    SchoolMembership,
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
            await connection.execute(
                text(
                    "TRUNCATE permission_assignments, platform_administrator_grants, "
                    "school_funds, school_memberships, permission_presets, users, schools CASCADE"
                )
            )

    asyncio.run(reset())
    yield async_sessionmaker(engine, expire_on_commit=False)
    asyncio.run(engine.dispose())


def test_user_can_belong_to_two_schools(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            user = User(email="member@example.test", status="active")
            first = School(slug="first-school", name="First School", status="active")
            second = School(slug="second-school", name="Second School", status="active")
            session.add_all([user, first, second])
            await session.flush()
            session.add_all(
                [
                    SchoolMembership(school_id=first.id, user_id=user.id, status="active"),
                    SchoolMembership(school_id=second.id, user_id=user.id, status="active"),
                ]
            )
            await session.commit()

            memberships = await session.scalar(
                select(func.count()).select_from(SchoolMembership).where(SchoolMembership.user_id == user.id)
            )
            assert memberships == 2

    asyncio.run(scenario())


def test_duplicate_membership_in_one_school_is_rejected(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            user = User(email="duplicate@example.test", status="active")
            school = School(slug="duplicate-school", name="Duplicate School", status="active")
            session.add_all([user, school])
            await session.flush()
            session.add(SchoolMembership(school_id=school.id, user_id=user.id, status="active"))
            await session.commit()

            session.add(SchoolMembership(school_id=school.id, user_id=user.id, status="active"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_cross_school_permission_assignment_is_rejected_by_postgresql(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            user = User(email="assignment@example.test", status="active")
            first = School(slug="assignment-first", name="First School", status="active")
            second = School(slug="assignment-second", name="Second School", status="active")
            preset = PermissionPreset(code="accountant", name="Accountant", capabilities=[], status="active")
            session.add_all([user, first, second, preset])
            await session.flush()
            membership = SchoolMembership(school_id=first.id, user_id=user.id, status="active")
            session.add(membership)
            await session.commit()

            session.add(
                PermissionAssignment(
                    school_id=second.id,
                    membership_id=membership.id,
                    preset_id=preset.id,
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_only_one_school_fund_can_exist_per_school(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            school = School(slug="fund-school", name="Fund School", status="active")
            session.add(school)
            await session.flush()
            session.add(SchoolFund(school_id=school.id, name="School Fund", status="active"))
            await session.commit()

            session.add(SchoolFund(school_id=school.id, name="Another Fund", status="active"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_platform_authority_does_not_create_tenant_membership(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            user = User(email="platform@example.test", status="active")
            school = School(slug="platform-school", name="Platform School", status="active")
            session.add_all([user, school])
            await session.flush()
            session.add(PlatformAdministratorGrant(user_id=user.id, scope="platform", status="active"))
            await session.commit()

            memberships = await session.scalar(
                select(func.count()).select_from(SchoolMembership).where(SchoolMembership.user_id == user.id)
            )
            assert memberships == 0

    asyncio.run(scenario())


def test_platform_audit_events_cannot_be_updated(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            event = PlatformAuditEvent(action="school.provision", target_type="school")
            session.add(event)
            await session.commit()
            with pytest.raises(DBAPIError):
                await session.execute(update(PlatformAuditEvent).where(PlatformAuditEvent.id == event.id).values(action="changed"))
            await session.rollback()

    asyncio.run(scenario())


def test_platform_audit_events_cannot_be_deleted(session_factory: async_sessionmaker[AsyncSession]) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            event = PlatformAuditEvent(action="school.provision", target_type="school")
            session.add(event)
            await session.commit()
            with pytest.raises(DBAPIError):
                await session.execute(delete(PlatformAuditEvent).where(PlatformAuditEvent.id == event.id))
            await session.rollback()

    asyncio.run(scenario())


def test_platform_grant_status_must_match_revocation_timestamp(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            user = User(email="grant-check@example.test", status="active")
            session.add(user)
            await session.flush()
            session.add(
                PlatformAdministratorGrant(
                    user_id=user.id,
                    scope="platform",
                    status="active",
                    revoked_at=datetime.now(timezone.utc),
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

            session.add(PlatformAdministratorGrant(user_id=user.id, scope="platform", status="revoked"))
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()

    asyncio.run(scenario())


def test_revoked_grant_allows_a_new_active_grant_for_same_scope(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def scenario() -> None:
        async with session_factory() as session:
            user = User(email="grant-cycle@example.test", status="active")
            session.add(user)
            await session.flush()
            old_grant = PlatformAdministratorGrant(user_id=user.id, scope="platform", status="active")
            session.add(old_grant)
            await session.commit()

            await session.execute(
                update(PlatformAdministratorGrant)
                .where(PlatformAdministratorGrant.id == old_grant.id)
                .values(status="revoked", revoked_at=datetime.now(timezone.utc))
            )
            new_grant = PlatformAdministratorGrant(user_id=user.id, scope="platform", status="active")
            session.add(new_grant)
            await session.commit()

            count = await session.scalar(
                select(func.count())
                .select_from(PlatformAdministratorGrant)
                .where(PlatformAdministratorGrant.user_id == user.id, PlatformAdministratorGrant.scope == "platform")
            )
            assert count == 2

    asyncio.run(scenario())
