"""Tests for base model (BaseTable)."""

from src.resources._base.models import BaseTable


def test_base_table_is_abstract_and_has_expected_fields() -> None:
    """BaseTable is abstract and defines id, created_at, updated_at."""
    assert getattr(BaseTable, "__abstract__", False) is True
    assert "id" in BaseTable.model_fields
    assert "created_at" in BaseTable.model_fields
    assert "updated_at" in BaseTable.model_fields
