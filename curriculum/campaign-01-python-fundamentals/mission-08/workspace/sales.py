"""Mission: Sales Aggregator."""


def top_categories(transactions: list[dict], n: int = 3) -> list[tuple[str, float]]:
    # TODO: aggregate total amount per category, return top n descending.
    raise NotImplementedError


def filter_positive(transactions: list[dict]):
    # TODO: make this a generator (use yield) that only yields
    # transactions with amount > 0, preserving order.
    raise NotImplementedError
