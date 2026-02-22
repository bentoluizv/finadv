"""P1.2: Incomes repository — list_by_month."""

from datetime import date
from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.resources._base.repository import add
from src.resources.incomes.models import Income, IncomeType
from src.resources.incomes.repository import list_by_month


@pytest.mark.asyncio
async def test_list_by_month_returns_incomes_in_range(
    migrated_session: AsyncSession,
) -> None:
    """
    Verifies that querying incomes by year and month returns incomes whose entry_date falls within that month.
    
    Creates an Income with entry_date 2025-02-15, persists it, queries list_by_month for February 2025, and asserts the result contains that income with the expected source and entry_date.
    """
    income_feb = Income(
        source='Salary',
        income_type=IncomeType.FIXED,
        amount=Decimal('1000.00'),
        entry_date=date(2025, 2, 15),
        description='',
    )
    await add(migrated_session, income_feb)

    incomes = await list_by_month(migrated_session, 2025, 2)
    assert len(incomes) == 1
    assert incomes[0].source == 'Salary'
    assert incomes[0].entry_date == date(2025, 2, 15)


@pytest.mark.asyncio
async def test_list_by_month_returns_empty_outside_range(
    migrated_session: AsyncSession,
) -> None:
    """list_by_month for a month with no data returns empty list."""
    income_feb = Income(
        source='Salary',
        income_type=IncomeType.FIXED,
        amount=Decimal('1000.00'),
        entry_date=date(2025, 2, 15),
        description='',
    )
    await add(migrated_session, income_feb)

    incomes_jan = await list_by_month(migrated_session, 2025, 1)
    incomes_mar = await list_by_month(migrated_session, 2025, 3)
    assert incomes_jan == []
    assert incomes_mar == []