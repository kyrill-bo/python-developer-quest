"""Mission: Safe Order Parser."""


class OrderValidationError(Exception):
    """Raised when a raw order dict fails validation."""


def parse_order(raw: dict) -> dict:
    # TODO: validate order_id, quantity, unit_price (in that order) and
    # raise OrderValidationError with a clear message on the first problem.
    raise NotImplementedError
