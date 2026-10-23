"""BOSS FIGHT: Order Processing CLI."""

import sys


class OrderValidationError(Exception):
    """Raised when a raw order dict fails validation."""


def validate_order(raw: dict) -> dict:
    # TODO: validate order_id, quantity, unit_price (see Safe Order Parser).
    raise NotImplementedError


def discount_percent(quantity: int) -> float:
    # TODO: same tiers as Discount Engine.
    raise NotImplementedError


def order_total(order: dict) -> float:
    # TODO: quantity * unit_price, discount applied, rounded to 2 decimals.
    raise NotImplementedError


def process_orders(raw_orders: list[dict]) -> dict:
    # TODO: validate each order independently (quarantine pattern),
    # compute totals for valid ones, and a grand_total.
    raise NotImplementedError


def load_orders(path: str) -> list[dict]:
    # TODO: read and parse the JSON file at `path`.
    raise NotImplementedError


def main(argv: list[str]) -> int:
    # TODO: argv[1] is the file path. Exit 2 on missing arg/file, else
    # print process_orders(...) as JSON and return 0.
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main(sys.argv))
