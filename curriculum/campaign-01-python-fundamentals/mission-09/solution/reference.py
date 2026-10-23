from datetime import datetime


class NormalizationError(Exception):
    """Raised when a raw order payload cannot be normalized."""


def normalize_order(raw: dict) -> dict:
    order_id = raw.get("order_id") or raw.get("orderId")
    if not order_id:
        raise NormalizationError("missing order id")

    raw_amount = raw.get("amount")
    if raw_amount is None:
        raise NormalizationError("missing amount")
    try:
        amount = float(raw_amount)
    except (TypeError, ValueError) as exc:
        raise NormalizationError("amount is not numeric") from exc

    created_raw = raw.get("created_at") or raw.get("createdAt")
    created_at = datetime.fromisoformat(created_raw) if created_raw else None

    return {"order_id": str(order_id), "amount": amount, "created_at": created_at}
