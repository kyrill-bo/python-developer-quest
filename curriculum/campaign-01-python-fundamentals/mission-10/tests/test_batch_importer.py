import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from batch_importer import import_batch


def test_all_valid():
    valid, invalid = import_batch([{"sku": "A", "qty": 1}, {"sku": "B", "qty": 2}])
    assert len(valid) == 2
    assert invalid == []


def test_mixed_batch_continues_past_errors():
    records = [
        {"sku": "A", "qty": 1},
        {"sku": "", "qty": 1},
        {"sku": "C", "qty": -5},
        {"sku": "D", "qty": 3},
    ]
    valid, invalid = import_batch(records)
    assert [v["sku"] for v in valid] == ["A", "D"]
    assert len(invalid) == 2
    assert invalid[0]["record"]["sku"] == ""
    assert "reason" in invalid[0]


def test_empty_batch():
    valid, invalid = import_batch([])
    assert valid == []
    assert invalid == []


def test_missing_fields_are_invalid():
    valid, invalid = import_batch([{"sku": "A"}, {"qty": 5}])
    assert valid == []
    assert len(invalid) == 2
