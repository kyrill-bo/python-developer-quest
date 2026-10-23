def top_categories(transactions: list[dict], n: int = 3) -> list[tuple[str, float]]:
    totals: dict[str, float] = {}
    for t in transactions:
        totals[t["category"]] = totals.get(t["category"], 0.0) + t["amount"]
    return sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:n]


def filter_positive(transactions: list[dict]):
    for t in transactions:
        if t["amount"] > 0:
            yield t
