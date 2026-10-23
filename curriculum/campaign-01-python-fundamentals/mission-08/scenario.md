## Mission: Sales Aggregator

**Rank:** Python Apprentice
**Difficulty:** 3/5
**Estimated time:** 30 Minuten
**XP reward:** 25

### Prerequisites
- Config Loader abgeschlossen.

### Scenario
Das Reporting-Team will wissen, welche Produktkategorien am meisten Umsatz
bringen -- und braucht eine Moeglichkeit, Transaktionen mit negativem
Betrag (Retouren) aus einem Datenstrom lazy herauszufiltern, ohne die
komplette Liste im Speicher zu duplizieren.

### Objectives
- List/Dict-Comprehensions bzw. Aggregation per Dictionary.
- Eine eigene Generator-Funktion mit `yield` schreiben.

### Requirements
Implementiere in `workspace/sales.py`:

```
def top_categories(transactions: list[dict], n: int = 3) -> list[tuple[str, float]]
def filter_positive(transactions: list[dict])
```

- `transactions`-Eintraege haben die Form `{"category": str, "amount": float}`.
- `top_categories` aggregiert den Gesamtumsatz pro Kategorie und gibt die
  `n` umsatzstaerksten als `(category, total)`-Tupel zurueck, absteigend
  sortiert.
- `filter_positive` ist ein **Generator** (kein `return` einer Liste!), der
  nur Transaktionen mit `amount > 0` liefert, in Originalreihenfolge.

### Restrictions
- `filter_positive` muss ein echter Generator sein (pruefbar via
  `inspect.isgenerator`).

### Acceptance Criteria
- Alle Tests in `tests/test_sales.py` bestehen.

### Submission
`workspace/sales.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-08`
