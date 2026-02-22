"""
P1.1: Migration runs; can create and get Income and Debt.

Uses migrated_db_path (Alembic upgrade head on a temp DB), then creates one
Income and one Debt via repository and asserts they can be fetched by id.
"""

from datetime import date
from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.resources._base.repository import add, get_by_id
from src.resources.debts.models import Debt, PaymentMethod
from src.resources.incomes.models import Income, IncomeType


@pytest.mark.asyncio
async def test_migration_creates_income_and_debt_tables(
    migrated_db_path: str,
    migrated_session: AsyncSession,
) -> None:
    """After migration, we can create one Income and one Debt and fetch them by id."""
    income = Income(
        source='Salary',
        income_type=IncomeType.FIXED,
        amount=Decimal('1000.50'),
        entry_date=date(2025, 2, 15),
        description='Monthly',
    )
    added_income = await add(migrated_session, income)
    assert added_income.id

    debt = Debt(
        amount=Decimal('50.00'),
        payment_method=PaymentMethod.PIX,
        entry_date=date(2025, 2, 14),
        is_recurrent=False,
        due_date=None,
        paid=False,
        description='Lunch',
    )
    added_debt = await add(migrated_session, debt)
    assert added_debt.id

    fetched_income = await get_by_id(migrated_session, Income, added_income.id)
    assert fetched_income is not None
    assert fetched_income.source == 'Salary'
    assert fetched_income.amount == Decimal('1000.50')

    fetched_debt = await get_by_id(migrated_session, Debt, added_debt.id)
    assert fetched_debt is not None
    assert fetched_debt.amount == Decimal('50.00')
    assert fetched_debt.paid is False
