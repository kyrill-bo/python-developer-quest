import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from inventory import scan_inventory


def test_basic_scan():
    result = scan_inventory([("SKU1", 10), ("SKU2", 2), ("SKU3", 50)])
    assert result["total_quantity"] == 62
    assert result["distinct_skus"] == 3
    assert result["low_stock_skus"] == ["SKU2"]


def test_duplicate_skus_are_aggregated():
    result = scan_inventory([("SKU1", 2), ("SKU1", 2), ("SKU2", 10)])
    assert result["total_quantity"] == 14
    assert result["distinct_skus"] == 2
    assert result["low_stock_skus"] == ["SKU1"]


def test_custom_threshold():
    result = scan_inventory([("SKU1", 20), ("SKU2", 30)], low_stock_threshold=25)
    assert result["low_stock_skus"] == ["SKU1"]


def test_empty_items_raises():
    with pytest.raises(ValueError):
        scan_inventory([])
