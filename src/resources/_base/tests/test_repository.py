"""Tests for base repository helpers (get_by_id, list_all, add, delete_by_id)."""

import pytest
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.ext.db import build_engine
from src.resources._base import repository as base_repo
from src.resources._base.models import BaseTable


# Concrete table for tests only. Import registers it with SQLModel.metadata.
class _TestRow(BaseTable, table=True):
    __tablename__ = "test_base_row"  # pyright: ignore[reportAssignmentType]
    name: str = Field(max_length=255)


@pytest.fixture
async def session():
    """Async session with in-memory DB and test table created."""
    engine = build_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(engine, expire_on_commit=False) as s:
        yield s
    await engine.dispose()


async def test_add_and_get_by_id(session: AsyncSession) -> None:
    """add() then get_by_id() returns the same entity."""
    row = _TestRow(name="first")
    added = await base_repo.add(session, row)
    assert added.id is not None
    assert added.name == "first"

    found = await base_repo.get_by_id(session, _TestRow, added.id)
    assert found is not None
    assert found.id == added.id
    assert found.name == added.name


async def test_get_by_id_returns_none_when_missing(session: AsyncSession) -> None:
    """get_by_id() returns None for unknown id."""
    found = await base_repo.get_by_id(session, _TestRow, "01ARZ3NDEKTSV4RRFFQ69G5FAV")
    assert found is None


async def test_list_all_empty_then_after_add(session: AsyncSession) -> None:
    """list_all() returns empty list then items after add."""
    empty = await base_repo.list_all(session, _TestRow)
    assert empty == []

    await base_repo.add(session, _TestRow(name="a"))
    await base_repo.add(session, _TestRow(name="b"))
    rows = await base_repo.list_all(session, _TestRow)
    assert len(rows) == 2
    names = {r.name for r in rows}
    assert names == {"a", "b"}


async def test_delete_by_id_returns_entity_and_removes(session: AsyncSession) -> None:
    """delete_by_id() returns the deleted entity and it is gone."""
    added = await base_repo.add(session, _TestRow(name="to_delete"))
    id_ = added.id

    deleted = await base_repo.delete_by_id(session, _TestRow, id_)
    assert deleted is not None
    assert deleted.id == id_
    assert deleted.name == "to_delete"

    found = await base_repo.get_by_id(session, _TestRow, id_)
    assert found is None


async def test_delete_by_id_returns_none_when_missing(session: AsyncSession) -> None:
    """delete_by_id() returns None when id does not exist."""
    deleted = await base_repo.delete_by_id(
        session, _TestRow, "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    )
    assert deleted is None
