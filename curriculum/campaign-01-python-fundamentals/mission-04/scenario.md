## Mission: Discount Engine

**Rank:** Code Explorer
**Difficulty:** 2/5
**Estimated time:** 20 Minuten
**XP reward:** 15

### Prerequisites
- Customer Deduplicator abgeschlossen.

### Scenario
Der Vertrieb will Mengenrabatte: je mehr Stueck bestellt werden, desto
hoeher der Rabatt in Prozent -- in festen Stufen.

### Objectives
- Bedingte Verzweigungen (`if`/`elif`/`else`) korrekt und grenzwertsicher
  einsetzen.

### Requirements
Implementiere in `workspace/discounts.py`:

```
def tiered_discount(quantity: int) -> float
```

Rabattstufen (Prozent):
| Menge         | Rabatt |
|---------------|--------|
| >= 100        | 20.0   |
| >= 50         | 15.0   |
| >= 20         | 10.0   |
| >= 10         | 5.0    |
| sonst         | 0.0    |

### Restrictions
- `raise ValueError(...)`, wenn `quantity < 0`.
- Die Grenzwerte selbst (z.B. genau 100, genau 50) gehoeren zur jeweils
  HOEHEREN Stufe.

### Acceptance Criteria
- Alle Tests in `tests/test_discounts.py` bestehen, inklusive der
  Grenzwert-Tests.

### Submission
`workspace/discounts.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-04`
