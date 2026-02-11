"""
Shared pytest fixtures and test env.

Sets in-memory SQLite for tests so db adapter uses :memory: when tests import it.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

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
def migrated_db_path(tmp_path: Path) -> str:
    """
    Run Alembic migrations against a temporary SQLite file and yield its path.

    Atomic: uses a fresh temp dir per test, runs upgrade head, yields path.
    No reliance on user action or existing DB state.
    """
    db_file = tmp_path / "test.db"
    url = f"sqlite:///{db_file}"
    env = {"DATABASE_URL": url}
    result = _run_alembic("upgrade", "head", env=env)
    assert result.returncode == 0, (result.stdout or "") + (result.stderr or "")
    yield str(db_file)
