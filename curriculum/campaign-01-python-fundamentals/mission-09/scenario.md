## Mission: API Response Normalizer

**Rank:** Python Apprentice
**Difficulty:** 3/5
**Estimated time:** 30 Minuten
**XP reward:** 25

### Prerequisites
- Sales Aggregator abgeschlossen.

### Scenario
Du integrierst zwei vorgelagerte Systeme, die beide "Bestellungen" liefern
-- aber mit unterschiedlichen Feldnamen (`order_id` vs. `orderId`) und
Datentypen (`amount` mal als String, mal als Zahl). Du baust die
Normalisierungsschicht, die beides auf ein einheitliches internes Format
abbildet.

### Objectives
- Mit JSON-artigen, inkonsistenten `dict`-Strukturen umgehen.
- `datetime.fromisoformat` aus der Standardbibliothek nutzen.

### Requirements
Implementiere in `workspace/normalizer.py`:

```
class NormalizationError(Exception): ...

def normalize_order(raw: dict) -> dict
```

- Akzeptiere sowohl `order_id` als auch `orderId` (snake_case hat Vorrang,
  wenn beide vorhanden sind).
- Akzeptiere `amount` als `str`, `int` oder `float`; konvertiere zu `float`.
- Akzeptiere sowohl `created_at` als auch `createdAt` als ISO-8601-String;
  parse zu `datetime` (oder `None`, wenn beides fehlt).
- Rueckgabe: `{"order_id": str, "amount": float, "created_at": datetime | None}`.

### Restrictions
- `raise NormalizationError(...)`, wenn keine ID vorhanden ist.
- `raise NormalizationError(...)`, wenn `amount` fehlt oder nicht
  konvertierbar ist.

### Acceptance Criteria
- Alle Tests in `tests/test_normalizer.py` bestehen.

### Submission
`workspace/normalizer.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-09`
