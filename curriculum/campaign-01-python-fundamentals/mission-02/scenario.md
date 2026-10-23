## Mission: Inventory Scanner

**Rank:** Code Explorer
**Difficulty:** 1/5
**Estimated time:** 25 Minuten
**XP reward:** 10

### Prerequisites
- Price Tag Formatter abgeschlossen.

### Scenario
Das Warehouse-System liefert Bestandsdaten als Liste von `(sku, quantity)`-
Tupeln -- mehrfach vorkommende SKUs sind moeglich (z.B. aus verschiedenen
Lagerorten) und muessen aufsummiert werden.

### Objectives
- Mit Listen und Tupeln arbeiten, Tupel-Entpacken in Schleifen.
- Aggregation ueber ein dict.

### Requirements
Implementiere in `workspace/inventory.py`:

```
def scan_inventory(items: list[tuple[str, int]], low_stock_threshold: int = 5) -> dict
```

Rueckgabe-dict mit:
- `total_quantity`: Summe aller Mengen (nach Aggregation pro SKU).
- `low_stock_skus`: alphabetisch sortierte Liste der SKUs, deren
  **aggregierte** Menge unter `low_stock_threshold` liegt.
- `distinct_skus`: Anzahl unterschiedlicher SKUs.

### Restrictions
- `raise ValueError(...)`, wenn `items` leer ist.
- Mengen fuer dieselbe SKU muessen VOR der Low-Stock-Pruefung summiert werden.

### Acceptance Criteria
- Alle Tests in `tests/test_inventory.py` bestehen.

### Submission
`workspace/inventory.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-02`
