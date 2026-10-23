import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from normalizer import NormalizationError, normalize_order


def test_snake_case_input():
    result = normalize_order({"order_id": "A1", "amount": 19.99, "created_at": "2026-01-15T10:00:00"})
    assert result["order_id"] == "A1"
    assert result["amount"] == 19.99
    assert result["created_at"] == datetime(2026, 1, 15, 10, 0, 0)


def test_camel_case_input():
    result = normalize_order({"orderId": "B2", "amount": "42.5", "createdAt": "2026-02-01T08:30:00"})
    assert result["order_id"] == "B2"
    assert result["amount"] == 42.5


def test_amount_as_string_is_converted():
    result = normalize_order({"order_id": "C3", "amount": "100"})
    assert result["amount"] == 100.0
    assert isinstance(result["amount"], float)


def test_missing_created_at_is_none():
    result = normalize_order({"order_id": "D4", "amount": 5})
    assert result["created_at"] is None


def test_missing_id_raises():
    with pytest.raises(NormalizationError):
        normalize_order({"amount": 5})


def test_missing_amount_raises():
    with pytest.raises(NormalizationError):
        normalize_order({"order_id": "E5"})


def test_unconvertible_amount_raises():
    with pytest.raises(NormalizationError):
        normalize_order({"order_id": "F6", "amount": "not-a-number"})
