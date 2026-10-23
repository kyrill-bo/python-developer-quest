"""Mini-Project: Sales Report Generator."""

import json
from pathlib import Path


def load_transactions(path: str) -> list[dict]:
    # TODO: read and parse the JSON file at `path`, return the list of
    # transaction dicts. Let FileNotFoundError propagate.
    raise NotImplementedError


def total_revenue(transactions: list[dict]) -> float:
    # TODO
    raise NotImplementedError


def revenue_by_category(transactions: list[dict]) -> dict[str, float]:
    # TODO
    raise NotImplementedError


def top_region(transactions: list[dict]) -> str:
    # TODO: raise ValueError if transactions is empty.
    raise NotImplementedError


def build_report(transactions: list[dict]) -> dict:
    # TODO: combine the functions above into one report dict,
    # rounding money values to 2 decimals.
    raise NotImplementedError


def write_report(report: dict, path: str) -> None:
    # TODO: serialize `report` as JSON to `path`.
    raise NotImplementedError


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent.parent / "data" / "transactions.json"
    transactions = load_transactions(str(data_path))
    report = build_report(transactions)
    print(json.dumps(report, indent=2))
