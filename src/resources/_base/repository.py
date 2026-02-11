"""
Base repository helpers: get_by_id, list_all, add, update, delete_by_id.

Pure functions taking AsyncSession and model/entity; no class.
"""

from typing import TypeVar

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.resources._base.models import BaseTable

M = TypeVar("M", bound=BaseTable)


async def get_by_id(session: AsyncSession, model: type[M], id: str) -> M | None:
    """Return the entity with the given id, or None."""
    return await session.get(model, id)


async def list_all(session: AsyncSession, model: type[M]) -> list[M]:
    """Return all rows for the model, no ordering."""
    statement = select(model)
    result = await session.exec(statement)
    return list(result.all())


async def add(session: AsyncSession, entity: M) -> M:
    """Persist entity, commit, refresh, return it."""
    session.add(entity)
    await session.commit()
    await session.refresh(entity)
    return entity


async def update(session: AsyncSession, entity: M) -> M:
    """Commit and refresh entity, return it."""
    session.add(entity)
    await session.commit()
    await session.refresh(entity)
    return entity


async def delete_by_id(session: AsyncSession, model: type[M], id: str) -> M | None:
    """Delete the entity with the given id. Return the deleted entity or None."""
    entity = await session.get(model, id)
    if entity is None:
        return None
    await session.delete(entity)
    await session.commit()
    return entity


__all__ = ["get_by_id", "list_all", "add", "update", "delete_by_id"]
