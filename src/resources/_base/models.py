"""
Base table model: shared fields for all domain tables.

Inherit from BaseTable (without table=True on the base) and set table=True
on your resource model so it gets id, created_at, updated_at.
"""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel
from ulid import ULID


def _ulid_default() -> str:
    return str(ULID())


def _utc_now() -> datetime:
    return datetime.now(UTC)


class BaseTable(SQLModel):
    """Mixin: id (ULID), created_at, updated_at. Abstract so no table is created."""

    __abstract__ = True

    id: str = Field(primary_key=True, default_factory=_ulid_default)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)


__all__ = ["BaseTable"]
