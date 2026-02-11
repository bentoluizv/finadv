"""
Shared pytest fixtures and test env.

Sets in-memory SQLite for tests so db adapter uses :memory: when tests import it.
"""

import os

# Use in-memory DB for tests; must be set before any import of src.ext.db
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
