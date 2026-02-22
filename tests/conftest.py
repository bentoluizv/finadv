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
    Run Alembic migrations against a temporary SQLite file and yield its path.

    Atomic: uses a fresh temp dir per test, runs upgrade head, yields path.
    No reliance on user action or existing DB state.
    """
    db_file = tmp_path / "test.db"
    url = f"sqlite+aiosqlite:///{db_file}"
    env = {"DATABASE_URL": url}
    result = _run_alembic("upgrade", "head", env=env)
    assert result.returncode == 0, (result.stdout or "") + (result.stderr or "")
    yield str(db_file)


@pytest.fixture
async def migrated_session(migrated_db_path: str):
    """AsyncSession bound to the migrated temp DB. For use in async tests."""
    from sqlmodel.ext.asyncio.session import AsyncSession
    from src.ext.db import build_engine
    url = f"sqlite+aiosqlite:///{migrated_db_path}"
    engine = build_engine(database_url=url)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    await engine.dispose()


@pytest.fixture
def client():
    """TestClient with app. Tables created on first use via create_all."""
    from fastapi.testclient import TestClient
    from src.main import app
    return TestClient(app)
