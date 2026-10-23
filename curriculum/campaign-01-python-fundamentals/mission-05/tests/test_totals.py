import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from totals import calculate_total


def test_simple_sum_no_tax():
    assert calculate_total(10.0, 20.0) == 30.0


def test_with_shipping_and_tax():
    assert calculate_total(100.0, shipping=10.0, tax_rate=10.0) == 121.0


def test_with_surcharges():
    assert calculate_total(50.0, gift_wrap=2.5, express=5.0) == 57.5


def test_negative_tax_raises():
    with pytest.raises(ValueError):
        calculate_total(10.0, tax_rate=-5.0)


def test_negative_item_price_raises():
    with pytest.raises(ValueError):
        calculate_total(-10.0, 20.0)


def test_negative_surcharge_raises():
    with pytest.raises(ValueError):
        calculate_total(10.0, gift_wrap=-1.0)
