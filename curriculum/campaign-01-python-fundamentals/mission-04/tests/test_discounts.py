import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from discounts import tiered_discount


@pytest.mark.parametrize(
    "quantity,expected",
    [
        (0, 0.0),
        (9, 0.0),
        (10, 5.0),
        (19, 5.0),
        (20, 10.0),
        (49, 10.0),
        (50, 15.0),
        (99, 15.0),
        (100, 20.0),
        (500, 20.0),
    ],
)
def test_tier_boundaries(quantity, expected):
    assert tiered_discount(quantity) == expected


def test_negative_quantity_raises():
    with pytest.raises(ValueError):
        tiered_discount(-1)
