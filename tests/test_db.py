"""
Tests for the async database adapter (src.ext.db).
"""

import pytest

from sqlalchemy import select, text
from sqlmodel.ext.asyncio.session import AsyncSession

from src.ext.db import engine, get_session


@pytest.mark.asyncio
async def test_get_session_yields_async_session() -> None:
    """get_session is an async generator that yields an AsyncSession."""
    gen = get_session()
    session = await gen.__anext__()
    try:
        assert isinstance(session, AsyncSession)
    finally:
        await gen.aclose()


@pytest.mark.asyncio
async def test_session_executes_sql() -> None:
    """Session from get_session can run SQL (connection works)."""
    async for session in get_session():
        result = await session.exec(select(1))  # type: ignore[arg-type]
        value = result.one()[0]
        assert value == 1
        break


@pytest.mark.asyncio
async def test_engine_connect() -> None:
    """Engine can establish a connection (smoke test)."""
    async with engine.begin() as conn:
        result = await conn.run_sync(
            lambda sync_conn: sync_conn.execute(text("SELECT 1")).scalar()
        )
    assert result == 1
