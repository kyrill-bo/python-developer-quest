import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from order_cli import (
    OrderValidationError,
    discount_percent,
    load_orders,
    main,
    order_total,
    process_orders,
    validate_order,
)

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


def test_validate_order_valid():
    result = validate_order({"order_id": "O1", "quantity": 5, "unit_price": 10.0})
    assert result == {"order_id": "O1", "quantity": 5, "unit_price": 10.0}


def test_validate_order_missing_id_raises():
    with pytest.raises(OrderValidationError):
        validate_order({"quantity": 5, "unit_price": 10.0})


def test_validate_order_bad_quantity_raises():
    with pytest.raises(OrderValidationError):
        validate_order({"order_id": "O1", "quantity": -1, "unit_price": 10.0})


def test_validate_order_bad_price_raises():
    with pytest.raises(OrderValidationError):
        validate_order({"order_id": "O1", "quantity": 1, "unit_price": "bad"})


@pytest.mark.parametrize(
    "quantity,expected",
    [(5, 0.0), (10, 5.0), (20, 10.0), (50, 15.0), (100, 20.0)],
)
def test_discount_tiers(quantity, expected):
    assert discount_percent(quantity) == expected


def test_order_total_applies_discount():
    order = {"order_id": "O1", "quantity": 15, "unit_price": 20.0}
    assert order_total(order) == 285.0


def test_process_orders_quarantines_invalid_without_stopping():
    raw_orders = [
        {"order_id": "O1", "quantity": 5, "unit_price": 10.0},
        {"order_id": "", "quantity": 1, "unit_price": 10.0},
        {"order_id": "O3", "quantity": 100, "unit_price": 5.0},
    ]
    result = process_orders(raw_orders)
    assert len(result["processed"]) == 2
    assert len(result["rejected"]) == 1
    assert result["processed"][0]["order_id"] == "O1"
    assert result["processed"][1]["order_id"] == "O3"


def test_process_orders_grand_total():
    raw_orders = [
        {"order_id": "O1", "quantity": 5, "unit_price": 10.0},
        {"order_id": "O3", "quantity": 100, "unit_price": 5.0},
    ]
    result = process_orders(raw_orders)
    assert result["grand_total"] == 450.0  # 50.0 + 400.0


def test_load_orders_reads_shipped_data():
    orders = load_orders(str(DATA_FILE))
    assert len(orders) == 6


def test_end_to_end_with_shipped_data():
    orders = load_orders(str(DATA_FILE))
    result = process_orders(orders)
    assert len(result["processed"]) == 3
    assert len(result["rejected"]) == 3
    assert result["grand_total"] == 735.0


def test_main_prints_json_and_returns_zero(capsys):
    exit_code = main(["order_cli.py", str(DATA_FILE)])
    assert exit_code == 0
    output = json.loads(capsys.readouterr().out)
    assert output["grand_total"] == 735.0


def test_main_missing_file_returns_two():
    exit_code = main(["order_cli.py", "/nonexistent/path/orders.json"])
    assert exit_code == 2


def test_main_missing_argument_returns_two():
    exit_code = main(["order_cli.py"])
    assert exit_code == 2
