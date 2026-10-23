import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from customers import dedupe_customers


def test_no_duplicates():
    customers = [{"email": "a@example.com"}, {"email": "b@shop.io"}]
    deduped, domains = dedupe_customers(customers)
    assert len(deduped) == 2
    assert domains == {"example.com", "shop.io"}


def test_case_insensitive_duplicate_removed():
    customers = [
        {"email": "Alice@Example.com", "name": "Alice"},
        {"email": "alice@example.com", "name": "Alice Duplicate"},
    ]
    deduped, _ = dedupe_customers(customers)
    assert len(deduped) == 1
    assert deduped[0]["name"] == "Alice"


def test_order_preserved_first_occurrence_wins():
    customers = [{"email": "x@a.com"}, {"email": "y@b.com"}, {"email": "X@A.com"}]
    deduped, _ = dedupe_customers(customers)
    assert [c["email"] for c in deduped] == ["x@a.com", "y@b.com"]


def test_missing_email_raises():
    with pytest.raises(ValueError):
        dedupe_customers([{"name": "No Email"}])
