## Mission: Price Tag Formatter

**Rank:** Code Explorer
**Difficulty:** 1/5
**Estimated time:** 20 Minuten
**XP reward:** 10

### Prerequisites
- Campaign 0 abgeschlossen (venv + pytest-Workflow).

### Scenario
Der Checkout-Service deines fiktiven E-Commerce-Backends braucht eine
Funktion, die einen Rabatt anwendet und den Preis als Anzeige-String
formatiert -- so wie du es aus deinem Spring-Boot-Checkout kennst, nur
jetzt in Python.

### Objectives
- String-Formatierung mit f-strings und Format-Specs.
- Einfache Eingabevalidierung mit Exceptions.

### Requirements
Implementiere in `workspace/pricing.py`:

```
def format_price(amount: float, currency: str = "EUR", discount_percent: float = 0.0) -> str
```

- Wendet den Rabatt an: `amount * (1 - discount_percent / 100)`.
- Gibt das Ergebnis als `"{wert}.{2 Nachkommastellen} {currency}"` zurueck,
  z.B. `"150.00 EUR"`.
- `currency` und `discount_percent` haben Defaultwerte (`"EUR"`, `0.0`).

### Restrictions
- `raise ValueError(...)`, wenn `amount < 0`.
- `raise ValueError(...)`, wenn `discount_percent` nicht in `[0, 100]` liegt.
- Keine rundungsbedingten Sonderfaelle behandeln -- die Format-Spec `:.2f`
  reicht.

### Acceptance Criteria
- Alle Tests in `tests/test_pricing.py` bestehen.

### Submission
`workspace/pricing.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-01`
