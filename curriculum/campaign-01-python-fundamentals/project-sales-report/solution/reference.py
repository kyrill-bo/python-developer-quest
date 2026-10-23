import json
from pathlib import Path


def load_transactions(path: str) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def total_revenue(transactions: list[dict]) -> float:
    return sum(t["amount"] for t in transactions)


def revenue_by_category(transactions: list[dict]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for t in transactions:
        totals[t["category"]] = totals.get(t["category"], 0.0) + t["amount"]
    return totals


def top_region(transactions: list[dict]) -> str:
    if not transactions:
        raise ValueError("transactions must not be empty")
    totals: dict[str, float] = {}
    for t in transactions:
        totals[t["region"]] = totals.get(t["region"], 0.0) + t["amount"]
    return max(totals, key=totals.get)


def build_report(transactions: list[dict]) -> dict:
    return {
        "total_revenue": round(total_revenue(transactions), 2),
        "by_category": {k: round(v, 2) for k, v in revenue_by_category(transactions).items()},
        "top_region": top_region(transactions),
    }


def write_report(report: dict, path: str) -> None:
    Path(path).write_text(json.dumps(report, indent=2), encoding="utf-8")
