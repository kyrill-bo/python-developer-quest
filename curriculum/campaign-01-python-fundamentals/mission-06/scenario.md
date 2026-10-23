## Mission: Safe Order Parser

**Rank:** Python Apprentice
**Difficulty:** 3/5
**Estimated time:** 30 Minuten
**XP reward:** 25

### Prerequisites
- Order Total Calculator abgeschlossen.

### Scenario
Bestellungen kommen als rohe `dict`s von einem externen System -- Felder
koennen fehlen, falschen Typ haben oder leer sein. Dein Parser muss das
robust erkennen und mit einer **eigenen, aussagekraeftigen Exception**
abbrechen, statt mit einem kryptischen `KeyError` oder `TypeError`.

### Objectives
- Eigene Exception-Klassen definieren.
- Gezielt bestimmte Exceptions abfangen (nicht `except Exception` blind).
- Exception-Chaining mit `raise ... from exc`.

### Requirements
Implementiere in `workspace/order_parser.py`:

```
class OrderValidationError(Exception): ...

def parse_order(raw: dict) -> dict
```

Pruefreihenfolge (brich bei der ersten Verletzung ab):
1. `order_id`: muss ein nicht-leerer String sein.
2. `quantity`: muss ein positiver `int` sein (kein `bool`, kein Float).
3. `unit_price`: muss sich zu einem positiven `float` konvertieren lassen
   (auch wenn er z.B. als String `"19.99"` kommt).

Rueckgabe bei Erfolg: `{"order_id": ..., "quantity": ..., "unit_price": ..., "notes": raw.get("notes", "")}`.

### Restrictions
- Jede Verletzung fuehrt zu `raise OrderValidationError(...)` mit einer
  Message, die das betroffene Feld nennt.
- Beim Cast von `unit_price` darfst du `TypeError`/`ValueError`/`KeyError`
  gezielt abfangen und in `OrderValidationError` umwandeln (mit `from exc`)
  -- kein blindes `except Exception`.

### Acceptance Criteria
- Alle Tests in `tests/test_order_parser.py` bestehen.

### Submission
`workspace/order_parser.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-06`
