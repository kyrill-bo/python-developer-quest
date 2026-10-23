class OrderValidationError(Exception):
    """Raised when a raw order dict fails validation."""


def parse_order(raw: dict) -> dict:
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

    return {
        "order_id": order_id,
        "quantity": quantity,
        "unit_price": unit_price,
        "notes": raw.get("notes", ""),
    }
