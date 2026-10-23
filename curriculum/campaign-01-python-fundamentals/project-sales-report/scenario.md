## Mini-Project: Sales Report Generator

**Rank:** Python Apprentice
**Difficulty:** 4/5
**Estimated time:** 90 Minuten
**XP reward:** 250

### Prerequisites
- Alle 10 Missionen von Campaign 1 abgeschlossen.

### Scenario
Du baust zum ersten Mal ein kleines, aber vollstaendiges Werkzeug, statt
einer einzelnen Funktion: einen Sales-Report-Generator, der Transaktionen
aus einer JSON-Datei liest, mehrere Kennzahlen berechnet und einen Report
als JSON-Datei schreibt. Das ist die Zusammenfuehrung aller bisherigen
Fundamentals-Themen in einem realistischen Mini-Tool.

### Objectives
- Mehrere kleine, einzeln testbare Funktionen zu einem Werkzeug komponieren.
- Datei-I/O, Aggregation und JSON-Serialisierung kombinieren.

### Requirements
Implementiere in `workspace/report.py`:

```
def load_transactions(path: str) -> list[dict]
def total_revenue(transactions: list[dict]) -> float
def revenue_by_category(transactions: list[dict]) -> dict[str, float]
def top_region(transactions: list[dict]) -> str
def build_report(transactions: list[dict]) -> dict
def write_report(report: dict, path: str) -> None
```

- `transactions`-Eintraege haben die Form
  `{"category": str, "amount": float, "region": str}`.
- `build_report` liefert `{"total_revenue": float, "by_category": dict, "top_region": str}`,
  alle Geldbetraege auf 2 Nachkommastellen gerundet.
- `write_report` schreibt das `report`-dict als JSON an `path`.
- Testdaten liegen bereits unter `data/transactions.json`.

### Restrictions
- `top_region` wirft `ValueError`, wenn `transactions` leer ist.
- Jede Funktion macht genau eine Sache (keine 80-Zeilen-Monsterfunktion).

### Acceptance Criteria
- Alle Tests in `tests/test_report.py` bestehen.

### Submission
`workspace/report.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/project-sales-report`
