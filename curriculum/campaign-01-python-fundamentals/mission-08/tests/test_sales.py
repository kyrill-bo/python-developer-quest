import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from sales import filter_positive, top_categories

TRANSACTIONS = [
    {"category": "books", "amount": 10.0},
    {"category": "electronics", "amount": 500.0},
    {"category": "books", "amount": 15.0},
    {"category": "electronics", "amount": -50.0},
    {"category": "toys", "amount": 30.0},
]


def test_top_categories_aggregates_and_sorts():
    result = top_categories(TRANSACTIONS, n=2)
    assert result[0] == ("electronics", 450.0)
    assert result[1] == ("toys", 30.0)


def test_top_categories_respects_n():
    result = top_categories(TRANSACTIONS, n=1)
    assert len(result) == 1


def test_filter_positive_is_a_generator():
    gen = filter_positive(TRANSACTIONS)
    assert inspect.isgenerator(gen)


def test_filter_positive_only_yields_positive_amounts_in_order():
    result = list(filter_positive(TRANSACTIONS))
    assert all(t["amount"] > 0 for t in result)
    assert len(result) == 4
    assert result[0]["category"] == "books"
