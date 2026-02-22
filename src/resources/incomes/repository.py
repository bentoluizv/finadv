"""Incomes repository: list_by_month and base CRUD."""

from datetime import date, timedelta

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.resources._base.repository import add, delete_by_id, get_by_id, update
from src.resources.incomes.models import Income


def _month_range(year: int, month: int) -> tuple[date, date]:
    """
    Compute the first and last day of the specified calendar month.
    
    Parameters:
        year (int): The calendar year.
        month (int): The calendar month (1-12).
    
    Returns:
        tuple[date, date]: A tuple (first_day, last_day) where `first_day` is the first day of the month and `last_day` is the last day of the month (inclusive).
    """
    first = date(year, month, 1)
    if month == 12:
        last = date(year, 12, 31)
    else:
        last = date(year, month + 1, 1) - timedelta(days=1)
    return first, last


async def list_by_month(
    session: AsyncSession, year: int, month: int
) -> list[Income]:
    """
    List Income records whose `entry_date` falls within the specified calendar month.
    
    Parameters:
        year (int): Year of the month to filter.
        month (int): Month number (1-12) of the year to filter.
    
    Returns:
        list[Income]: Income objects with `entry_date` between the month's first and last day (inclusive).
    """
    first_day, last_day = _month_range(year, month)
    statement = (
        select(Income)
        .where(Income.entry_date >= first_day, Income.entry_date <= last_day)
    )
    result = await session.exec(statement)
    return list(result.all())


__all__ = ['list_by_month', 'get_by_id', 'add', 'update', 'delete_by_id']