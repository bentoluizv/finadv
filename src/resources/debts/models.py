"""Debt model and PaymentMethod enum."""

from datetime import date
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import Boolean, Date, Numeric, String
from sqlmodel import Column, Field

from src.resources._base.models import BaseTable


class PaymentMethod(StrEnum):
    """Payment method: Pix, Credit, Debit, Cash."""

    PIX = 'Pix'
    CREDIT = 'Credit'
    DEBIT = 'Debit'
    CASH = 'Cash'


class Debt(BaseTable, table=True):
    """Debt: amount, payment_method, date, is_recurrent, due_date, paid, description."""

    __tablename__ = 'debt'  # pyright: ignore[reportAssignmentType]

    amount: Decimal = Field(sa_column=Column(Numeric(12, 2)))
    payment_method: PaymentMethod = Field(sa_column=Column(String(32)))
    entry_date: date = Field(sa_column=Column('date', Date()))
    is_recurrent: bool = Field(default=False, sa_column=Column(Boolean))
    due_date: date | None = Field(default=None)
    paid: bool = Field(default=False, sa_column=Column(Boolean))
    description: str = Field(default='', max_length=1024)


__all__ = ['Debt', 'PaymentMethod']
