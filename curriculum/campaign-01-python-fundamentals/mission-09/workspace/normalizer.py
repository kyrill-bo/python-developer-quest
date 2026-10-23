"""Mission: API Response Normalizer."""

from datetime import datetime  # noqa: F401 (used once you implement normalize_order)


class NormalizationError(Exception):
    """Raised when a raw order payload cannot be normalized."""


def normalize_order(raw: dict) -> dict:
    # TODO: accept order_id/orderId, amount as str|int|float,
    # created_at/createdAt as ISO string -> datetime.
    raise NotImplementedError
