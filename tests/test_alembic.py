"""
Alembic: tests that migrations run correctly.

All tests are atomic and use the migrated_db_path fixture or a fresh tmp_path.
No reliance on user action or existing DB state.
"""

import os
import subprocess
import sqlite3
import sys
from pathlib import Path

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory

ROOT = Path(__file__).resolve().parent.parent


def _get_head_revision() -> str:
    """Return the current Alembic head revision id (single head only)."""
    config = Config(ROOT / "alembic.ini")
    config.set_main_option("script_location", str(ROOT / "migrations"))
    script = ScriptDirectory.from_config(config)
    heads = script.get_heads()
    assert len(heads) == 1, f"Expected single head, got {heads}"
    return heads[0]


def _alembic(*args: str, url: str) -> subprocess.CompletedProcess[str]:
    """Run alembic with DATABASE_URL set. Returns completed process."""
    env = {**os.environ, "DATABASE_URL": url}
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_upgrade_head_creates_alembic_version(migrated_db_path: str) -> None:
    """After upgrade head, alembic_version table exists and has one row at current head."""
    conn = sqlite3.connect(migrated_db_path)
    cur = conn.execute(
        "SELECT version_num FROM alembic_version"
    )
    rows = cur.fetchall()
    conn.close()
    assert len(rows) == 1
    assert rows[0][0] == _get_head_revision()


def test_upgrade_head_idempotent(migrated_db_path: str) -> None:
    """Running upgrade head again on an already-migrated DB does not fail."""
    url = f"sqlite+aiosqlite:///{migrated_db_path}"
    result = _alembic("upgrade", "head", url=url)
    assert result.returncode == 0, (result.stdout or "") + (result.stderr or "")


def test_downgrade_base_then_upgrade_head(tmp_path: Path) -> None:
    """downgrade base then upgrade head leaves DB at head (atomic, no user action)."""
    db_file = tmp_path / "test.db"
    url = f"sqlite+aiosqlite:///{db_file}"

    r1 = _alembic("upgrade", "head", url=url)
    assert r1.returncode == 0, (r1.stdout or "") + (r1.stderr or "")

    r2 = _alembic("downgrade", "base", url=url)
    assert r2.returncode == 0, (r2.stdout or "") + (r2.stderr or "")

    conn = sqlite3.connect(str(db_file))
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version'")
    has_table = cur.fetchone() is not None
    if has_table:
        cur = conn.execute("SELECT version_num FROM alembic_version")
        assert len(cur.fetchall()) == 0
    conn.close()

    r3 = _alembic("upgrade", "head", url=url)
    assert r3.returncode == 0, (r3.stdout or "") + (r3.stderr or "")

    conn = sqlite3.connect(str(db_file))
    cur = conn.execute("SELECT version_num FROM alembic_version")
    rows = cur.fetchall()
    conn.close()
    assert len(rows) == 1 and rows[0][0] == _get_head_revision()
