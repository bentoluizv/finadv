"""
Async database adapter: SQLite via aiosqlite.

Engine and session are created from settings (see settings.py; loads .env).
Use build_engine() to create an engine for a given URL (e.g. tests with :memory:).
Use get_session in routes; import all SQLModel table models here so Alembic can discover them.
"""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.ext.settings import get_settings


def build_engine(
    database_url: str | None = None,
    *,
    echo: bool | None = None,
    **kwargs: Any,
) -> AsyncEngine:
    """Factory: build an async engine. No args → use settings; pass url (and optional echo) for tests or custom DB."""
    s = get_settings()
    url = database_url if database_url is not None else s.database_url
    echo_val = echo if echo is not None else s.sql_echo
    connect_args: dict[str, Any] = (
        {"check_same_thread": False} if "sqlite" in url else {}
    )
    async_engine = create_async_engine(url, echo=echo_val, connect_args=connect_args, **kwargs)
    return async_engine


_settings = get_settings()
engine = build_engine()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields an async session per request. Repositories are responsible for commit/rollback."""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


# Alembic and app need metadata. Import all *table* models (table=True) here.
# _base.models.BaseTable is a mixin (no table); import concrete models from resources, e.g.:
# from src.resources.debts.models import Debt  # noqa: F401
# from src.resources.incomes.models import Income  # noqa: F401
__all__ = [
    "build_engine",
    "engine",
    "get_session",
    "AsyncSession",
    "SQLModel",
]
