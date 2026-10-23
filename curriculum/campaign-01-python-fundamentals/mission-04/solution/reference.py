def tiered_discount(quantity: int) -> float:
    if quantity < 0:
        raise ValueError("quantity must not be negative")
    if quantity >= 100:
        return 20.0
    if quantity >= 50:
        return 15.0
    if quantity >= 20:
        return 10.0
    if quantity >= 10:
        return 5.0
    return 0.0
