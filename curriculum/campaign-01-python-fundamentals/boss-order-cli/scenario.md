## BOSS FIGHT: Order Processing CLI

**Rank:** Backend Builder
**Difficulty:** 5/5
**Estimated time:** 120 Minuten
**XP reward:** 500

### Prerequisites
- Mini-Project "Sales Report Generator" abgeschlossen.
- Alle 10 Fundamentals-Missionen abgeschlossen.

### Scenario
Das ist der Campaign-1-Boss: Du baust ein eigenstaendiges CLI-Tool, das eine
Datei mit rohen Bestelldaten einliest, jede Order validiert, Mengenrabatte
anwendet, Summen berechnet und fehlerhafte Orders robust in Quarantaene
steckt -- ohne den gesamten Lauf abzubrechen. Das ist strukturell identisch
mit echten Batch-Verarbeitungs-Tools, die du spaeter in Campaign 9
(Data Engineering) in groesserem Rahmen wiedersiehst.

### Objectives
- Mehrere zuvor einzeln gelernte Patterns (Validierung, Rabattstufen,
  Aggregation, Quarantaene bei Fehlern) zu einem zusammenhaengenden Tool
  komponieren.
- Ein CLI-Einstiegspunkt mit sauberen Exit-Codes.

### Requirements
Implementiere in `workspace/order_cli.py`:

```
class OrderValidationError(Exception): ...

def validate_order(raw: dict) -> dict
def discount_percent(quantity: int) -> float
def order_total(order: dict) -> float
def process_orders(raw_orders: list[dict]) -> dict
def load_orders(path: str) -> list[dict]
def main(argv: list[str]) -> int
```

- `validate_order`: prueft `order_id` (nicht-leerer String), `quantity`
  (positiver int), `unit_price` (konvertierbar zu positivem float) --
  raise `OrderValidationError` mit sprechender Message bei Verstoss.
- `discount_percent`: gleiche Stufen wie in "Discount Engine"
  (>=100 -> 20%, >=50 -> 15%, >=20 -> 10%, >=10 -> 5%, sonst 0%).
- `order_total`: `quantity * unit_price`, Rabatt angewendet, auf 2
  Nachkommastellen gerundet.
- `process_orders`: verarbeitet eine Liste roher Orders, trennt
  `processed` (mit berechnetem `total`) von `rejected`
  (`{"order": ..., "reason": ...}`), berechnet `grand_total` ueber alle
  `processed`-Orders. Ein fehlerhafter Datensatz bricht die Verarbeitung
  NICHT ab.
- `load_orders`: liest eine JSON-Datei und gibt die Liste roher Orders
  zurueck.
- `main(argv)`: `argv[1]` ist der Dateipfad. Druckt das Ergebnis von
  `process_orders` als JSON auf stdout. Gibt `2` zurueck bei fehlender
  Datei oder fehlendem Argument, sonst `0`.

### Restrictions
- Kein `except Exception` -- fange gezielt `OrderValidationError` bzw.
  `FileNotFoundError`.
- `process_orders` darf bei einem ungueltigen Datensatz nicht abbrechen.

### Acceptance Criteria
- Alle Tests in `tests/test_order_cli.py` bestehen.
- Testdaten liegen bereits unter `data/orders.json` -- du kannst dein Tool
  manuell damit ausprobieren: `python3 workspace/order_cli.py data/orders.json`.

### Submission
`workspace/order_cli.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/boss-order-cli`

Nach Bestehen: Achievement "Test Master" und Freischaltung weiterer
Campaigns (siehe `python -m quest map`).
