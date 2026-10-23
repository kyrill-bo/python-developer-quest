def calculate_total(
    *item_prices: float, tax_rate: float = 0.0, shipping: float = 0.0, **surcharges: float
) -> float:
    if tax_rate < 0:
        raise ValueError("tax_rate must not be negative")
    if any(p < 0 for p in item_prices) or shipping < 0 or any(v < 0 for v in surcharges.values()):
        raise ValueError("prices must not be negative")
    subtotal = sum(item_prices) + sum(surcharges.values()) + shipping
    return round(subtotal * (1 + tax_rate / 100), 2)
