import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from pricing import format_price


def test_default_currency():
    assert format_price(100.0) == "100.00 EUR"


def test_custom_currency():
    assert format_price(49.5, "USD") == "49.50 USD"


def test_discount_applied():
    assert format_price(200.0, "EUR", 25) == "150.00 EUR"


def test_negative_amount_raises():
    with pytest.raises(ValueError):
        format_price(-5.0)


def test_discount_out_of_range_raises():
    with pytest.raises(ValueError):
        format_price(10.0, "EUR", 150)
