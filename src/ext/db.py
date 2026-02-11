"""
Async database adapter: engine and session factory from settings.

Uses get_settings().database_url by default; build_engine(url) for tests (e.g. in-memory).
"""

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.ext.settings import get_settings


def build_engine(database_url: str | None = None) -> AsyncEngine:
    """Build an async engine. If database_url is None, use get_settings().database_url."""
    url = database_url
    if url is None:
        _s = get_settings()
        url = _s.database_url
    return create_async_engine(
        url,
        echo=get_settings().sql_echo,
        future=True,
    )


# Default engine from settings. Used by get_session and by Alembic (env.py uses sync URL separately).
engine = build_engine()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Async generator yielding an AsyncSession. Caller must use within async context."""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


__all__ = ["build_engine", "engine", "get_session"]
