import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from order_parser import OrderValidationError, parse_order


def test_valid_order():
    result = parse_order({"order_id": "ORD-1", "quantity": 3, "unit_price": "19.99"})
    assert result["order_id"] == "ORD-1"
    assert result["quantity"] == 3
    assert result["unit_price"] == pytest.approx(19.99)
    assert result["notes"] == ""


def test_valid_order_with_notes():
    result = parse_order({"order_id": "ORD-2", "quantity": 1, "unit_price": 5.0, "notes": "gift"})
    assert result["notes"] == "gift"


def test_missing_order_id_raises():
    with pytest.raises(OrderValidationError, match="order_id"):
        parse_order({"quantity": 1, "unit_price": 1.0})


def test_zero_quantity_raises():
    with pytest.raises(OrderValidationError, match="quantity"):
        parse_order({"order_id": "ORD-3", "quantity": 0, "unit_price": 1.0})


def test_bool_quantity_raises():
    with pytest.raises(OrderValidationError, match="quantity"):
        parse_order({"order_id": "ORD-4", "quantity": True, "unit_price": 1.0})


def test_non_numeric_unit_price_raises():
    with pytest.raises(OrderValidationError, match="unit_price"):
        parse_order({"order_id": "ORD-5", "quantity": 1, "unit_price": "not-a-number"})


def test_negative_unit_price_raises():
    with pytest.raises(OrderValidationError, match="unit_price"):
        parse_order({"order_id": "ORD-6", "quantity": 1, "unit_price": -5.0})
