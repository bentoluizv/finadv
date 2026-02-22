"""Income model and IncomeType enum."""

from datetime import date
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import Date, Numeric, String
from sqlmodel import Column, Field

from src.resources._base.models import BaseTable


class IncomeType(StrEnum):
    """Fixed (predictable) or Variable (one-off or irregular)."""

    FIXED = 'Fixed'
    VARIABLE = 'Variable'


class Income(BaseTable, table=True):
    """Income: source, type, amount, date, description."""

    __tablename__ = 'income'  # pyright: ignore[reportAssignmentType]

    source: str = Field(max_length=255)
    income_type: IncomeType = Field(sa_column=Column('type', String(32)))
    amount: Decimal = Field(sa_column=Column(Numeric(12, 2)))
    entry_date: date = Field(sa_column=Column('date', Date()))
    description: str = Field(default='', max_length=1024)


__all__ = ['Income', 'IncomeType']
