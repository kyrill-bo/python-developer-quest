def format_price(amount: float, currency: str = "EUR", discount_percent: float = 0.0) -> str:
    if amount < 0:
        raise ValueError("amount must not be negative")
    if not (0 <= discount_percent <= 100):
        raise ValueError("discount_percent must be between 0 and 100")
    discounted = amount * (1 - discount_percent / 100)
    return f"{discounted:.2f} {currency}"
