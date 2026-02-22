import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 1. IMPORT SQLMODEL AND YOUR MODELS
from sqlmodel import SQLModel

from src.ext.settings import get_settings
from src.resources.debts.models import Debt  # noqa: F401
from src.resources.incomes.models import Income  # noqa: F401

# this is the Alembic Config object
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. LINK THE METADATA
target_metadata = SQLModel.metadata


def _get_url() -> str:
    """
    Retrieve the database connection URL from application settings.
    
    Returns:
        str: The database URL (for example `postgresql://...` or `sqlite:///...`) obtained from configured settings.
    """
    return get_settings().database_url


def run_migrations_offline() -> None:
    """
    Configure the Alembic context for offline (file-based) migrations and execute them.
    
    This resolves the database URL from the Alembic configuration or application settings, sets the migration context (including target metadata, literal binding of parameters, named paramstyle, and batch rendering for SQLite), begins a migration transaction, and runs the migrations.
    """
    url = config.get_main_option("sqlalchemy.url") or _get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,  # pyright: ignore[reportArgumentType]
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # 3. ADD BATCH MODE FOR SQLITE
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    # 3. ADD BATCH MODE HERE TOO
    """
    Configure the Alembic migration context with the provided database connection and execute migrations using batch rendering.
    
    This starts a migration transaction on the given SQLAlchemy Connection and runs pending migrations with render_as_batch=True (useful for databases like SQLite that require batch mode for certain schema changes).
    
    Parameters:
        connection (Connection): Active SQLAlchemy Connection to use for running the migrations.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """
    Run database migrations using an asynchronous SQLAlchemy engine.
    
    Builds an async engine from the Alembic configuration (using the runtime database URL),
    opens an async connection to execute migrations via `do_run_migrations`, and disposes
    the engine when finished.
    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = _get_url()
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """
    Run the application's online database migrations to apply schema changes.
    
    Blocks until the configured asynchronous migration routine completes.
    """
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()