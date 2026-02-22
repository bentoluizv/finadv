"""
Shared pytest fixtures and test env.

Sets in-memory SQLite for tests so db adapter uses :memory: when tests import it.
"""

import os
import subprocess
import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from sqlmodel import SQLModel

# Use in-memory DB for tests; must be set before any import of src.ext.db
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

ROOT = Path(__file__).resolve().parent.parent


def _run_alembic(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """Run alembic in a subprocess with optional env. Returns completed process."""
    run_env = {**os.environ} if env is None else {**os.environ, **env}
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=ROOT,
        env=run_env,
        capture_output=True,
        text=True,
        timeout=30,
    )


@pytest.fixture
def migrated_db_path(tmp_path: Path) -> Generator[str, None, None]:
    """
    Run Alembic migrations against a temporary SQLite file and yield the file path.
    
    Parameters:
        tmp_path (Path): Temporary directory provided by pytest; a file named "test.db" will be created there.
    
    Returns:
        db_path (str): Filesystem path to the migrated SQLite database file.
    
    Raises:
        AssertionError: If the Alembic migration command exits with a non-zero status; the assertion message includes the command's stdout and stderr.
    """
    db_file = tmp_path / "test.db"
    url = f"sqlite+aiosqlite:///{db_file}"
    env = {"DATABASE_URL": url}
    result = _run_alembic("upgrade", "head", env=env)
    assert result.returncode == 0, (result.stdout or "") + (result.stderr or "")
    yield str(db_file)


@pytest.fixture
async def migrated_session(migrated_db_path: str):
    """
    Provide an AsyncSession connected to a migrated temporary SQLite database for use in async tests.
    
    Parameters:
        migrated_db_path (str): Filesystem path to the migrated SQLite database file.
    
    Returns:
        AsyncSession: The asynchronous SQLModel session bound to the temporary database file. The session is yielded for use in the test and the engine is disposed after use.
    """
    from sqlmodel.ext.asyncio.session import AsyncSession
    from src.ext.db import build_engine
    url = f"sqlite+aiosqlite:///{migrated_db_path}"
    engine = build_engine(database_url=url)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    await engine.dispose()


@pytest.fixture
def client():
    """
    Provide a TestClient instance for the FastAPI application.
    
    Creating the client may trigger application startup actions (for example, creating database tables on first use).
    
    Returns:
        TestClient: A TestClient bound to the application's ASGI app.
    """
    from fastapi.testclient import TestClient
    from src.main import app
    return TestClient(app)