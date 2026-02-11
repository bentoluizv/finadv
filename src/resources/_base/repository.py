"""
Generic async repository helpers: get_by_id, list_all, add, delete_by_id.

Resource repositories call these and add only domain-specific queries.
"""

from typing import TypeVar

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T", bound=SQLModel)


async def get_by_id(session: AsyncSession, model: type[T], id: str) -> T | None:
    """Fetch one entity by primary key."""
    entity = await session.get(model, id)
    return entity


async def list_all(session: AsyncSession, model: type[T]) -> list[T]:
    """Fetch all rows for the model."""
    statement = select(model)
    result = await session.exec(statement)
    rows = result.all()
    return list(rows)


async def add(session: AsyncSession, entity: T) -> T:
    """Persist entity, commit, refresh, and return it."""
    session.add(entity)
    await session.commit()
    await session.refresh(entity)
    return entity


async def delete_by_id(session: AsyncSession, model: type[T], id: str) -> T | None:
    """Delete entity by id; return the deleted entity or None if not found."""
    entity = await session.get(model, id)
    if entity is None:
        return None
    await session.delete(entity)
    await session.commit()
    return entity
