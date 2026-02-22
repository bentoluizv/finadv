"""Incomes repository: list_by_month and base CRUD."""

from datetime import date, timedelta

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.resources._base.repository import add, delete_by_id, get_by_id, update
from src.resources.incomes.models import Income


def _month_range(year: int, month: int) -> tuple[date, date]:
    """Return (first_day, last_day) for the given calendar month."""
    first = date(year, month, 1)
    if month == 12:
        last = date(year, 12, 31)
    else:
        last = date(year, month + 1, 1) - timedelta(days=1)
    return first, last


async def list_by_month(
    session: AsyncSession, year: int, month: int
) -> list[Income]:
    """Return incomes whose entry_date falls in the given calendar month."""
    first_day, last_day = _month_range(year, month)
    statement = (
        select(Income)
        .where(Income.entry_date >= first_day, Income.entry_date <= last_day)
    )
    result = await session.exec(statement)
    return list(result.all())


__all__ = ['list_by_month', 'get_by_id', 'add', 'update', 'delete_by_id']
