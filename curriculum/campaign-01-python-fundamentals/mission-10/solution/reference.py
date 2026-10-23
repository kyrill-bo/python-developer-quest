def _validate(record: dict) -> dict:
    sku = record.get("sku")
    if not isinstance(sku, str) or not sku:
        raise ValueError("invalid or missing sku")
    qty = record.get("qty")
    if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
        raise ValueError("invalid or missing qty")
    return {"sku": sku, "qty": qty}


def import_batch(records: list[dict]) -> tuple[list[dict], list[dict]]:
    valid: list[dict] = []
    invalid: list[dict] = []
    for record in records:
        try:
            valid.append(_validate(record))
        except ValueError as exc:
            invalid.append({"record": record, "reason": str(exc)})
    return valid, invalid
