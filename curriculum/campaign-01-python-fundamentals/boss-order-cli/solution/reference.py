import json
import sys
from pathlib import Path


class OrderValidationError(Exception):
    """Raised when a raw order dict fails validation."""


def validate_order(raw: dict) -> dict:
    order_id = raw.get("order_id")
    if not isinstance(order_id, str) or not order_id:
        raise OrderValidationError("order_id must be a non-empty string")

    quantity = raw.get("quantity")
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        raise OrderValidationError("quantity must be a positive integer")

    try:
        unit_price = float(raw["unit_price"])
    except (KeyError, TypeError, ValueError) as exc:
        raise OrderValidationError("unit_price must be numeric") from exc
    if unit_price <= 0:
        raise OrderValidationError("unit_price must be positive")

    return {"order_id": order_id, "quantity": quantity, "unit_price": unit_price}


def discount_percent(quantity: int) -> float:
    if quantity >= 100:
        return 20.0
    if quantity >= 50:
        return 15.0
    if quantity >= 20:
        return 10.0
    if quantity >= 10:
        return 5.0
    return 0.0


def order_total(order: dict) -> float:
    subtotal = order["quantity"] * order["unit_price"]
    discount = discount_percent(order["quantity"])
    return round(subtotal * (1 - discount / 100), 2)


def process_orders(raw_orders: list[dict]) -> dict:
    processed: list[dict] = []
    rejected: list[dict] = []
    for raw in raw_orders:
        try:
            order = validate_order(raw)
        except OrderValidationError as exc:
            rejected.append({"order": raw, "reason": str(exc)})
            continue
        order["total"] = order_total(order)
        processed.append(order)
    grand_total = round(sum(o["total"] for o in processed), 2)
    return {"processed": processed, "rejected": rejected, "grand_total": grand_total}


def load_orders(path: str) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: order_cli.py <orders.json>", file=sys.stderr)
        return 2
    try:
        raw_orders = load_orders(argv[1])
    except FileNotFoundError:
        print(f"File not found: {argv[1]}", file=sys.stderr)
        return 2
    result = process_orders(raw_orders)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
