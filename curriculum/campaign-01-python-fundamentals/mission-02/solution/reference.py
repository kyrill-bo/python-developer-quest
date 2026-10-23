def scan_inventory(items: list[tuple[str, int]], low_stock_threshold: int = 5) -> dict:
    if not items:
        raise ValueError("items must not be empty")
    totals: dict[str, int] = {}
    for sku, qty in items:
        totals[sku] = totals.get(sku, 0) + qty
    low_stock = sorted(sku for sku, qty in totals.items() if qty < low_stock_threshold)
    return {
        "total_quantity": sum(totals.values()),
        "low_stock_skus": low_stock,
        "distinct_skus": len(totals),
    }
