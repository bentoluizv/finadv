"""
Alembic environment: reads database URL from settings (env / .env), runs migrations.

- Uses sync SQLite URL for migrations (sqlite://) so no async engine in Alembic.
- Import all table models below so SQLModel.metadata includes them for autogenerate.
"""

from alembic import context
from sqlalchemy import create_engine

from sqlmodel import SQLModel

# Import all table models so they are registered with SQLModel.metadata
# before autogenerate or upgrade. Add new resources here when you add tables.
from src.resources._base.models import BaseTable  # noqa: F401

config = context.config
# Skip fileConfig: alembic.ini has no [loggers]/[handlers]/[formatters]; avoids KeyError in tests.
target_metadata = SQLModel.metadata


def get_sync_url() -> str:
    """Database URL from settings, as sync (sqlite://) for Alembic."""
    from src.ext.settings import get_settings
    s = get_settings()
    url = s.database_url
    if url.startswith("sqlite+aiosqlite"):
        return url.replace("sqlite+aiosqlite", "sqlite", 1)
    return url


def run_migrations_offline() -> None:
    """Run migrations in offline mode (generate SQL only)."""
    context.configure(
        url=get_sync_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode (connect to DB)."""
    engine = create_engine(get_sync_url())
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
