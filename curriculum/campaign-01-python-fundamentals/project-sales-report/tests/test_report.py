import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from report import (
    build_report,
    load_transactions,
    revenue_by_category,
    top_region,
    total_revenue,
    write_report,
)

SAMPLE = [
    {"category": "books", "amount": 10.0, "region": "EU"},
    {"category": "books", "amount": 5.0, "region": "US"},
    {"category": "toys", "amount": 100.0, "region": "EU"},
]

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "transactions.json"


def test_total_revenue():
    assert total_revenue(SAMPLE) == 115.0


def test_revenue_by_category():
    result = revenue_by_category(SAMPLE)
    assert result == {"books": 15.0, "toys": 100.0}


def test_top_region():
    assert top_region(SAMPLE) == "EU"


def test_top_region_empty_raises():
    with pytest.raises(ValueError):
        top_region([])


def test_build_report_shape():
    report = build_report(SAMPLE)
    assert report["total_revenue"] == 115.0
    assert report["top_region"] == "EU"
    assert report["by_category"] == {"books": 15.0, "toys": 100.0}


def test_write_report_roundtrip(tmp_path):
    report = build_report(SAMPLE)
    out_path = tmp_path / "report.json"
    write_report(report, str(out_path))
    assert json.loads(out_path.read_text(encoding="utf-8")) == report


def test_load_transactions_from_shipped_data():
    transactions = load_transactions(str(DATA_FILE))
    assert len(transactions) == 10
    report = build_report(transactions)
    assert report["total_revenue"] == pytest.approx(679.73)
    assert report["top_region"] == "EU"
