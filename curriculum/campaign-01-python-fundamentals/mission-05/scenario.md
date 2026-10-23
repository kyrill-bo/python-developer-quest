## Mission: Order Total Calculator

**Rank:** Python Apprentice
**Difficulty:** 2/5
**Estimated time:** 25 Minuten
**XP reward:** 15

### Prerequisites
- Discount Engine abgeschlossen.

### Scenario
Eine Bestellung besteht aus einer variablen Anzahl Artikelpreisen, optionalem
Versand, optionaler Steuer und einer variablen Anzahl benannter Zuschlaege
(z.B. `gift_wrap=2.50`, `express_handling=5.00`).

### Objectives
- `*args` fuer variable positionale Parameter.
- `**kwargs` fuer variable benannte Parameter.
- Parameter mit Default-Werten.

### Requirements
Implementiere in `workspace/totals.py`:

```
def calculate_total(*item_prices: float, tax_rate: float = 0.0, shipping: float = 0.0, **surcharges: float) -> float
```

- Zwischensumme = Summe aller `item_prices` + Summe aller `surcharges`-Werte + `shipping`.
- Endresultat = Zwischensumme mit `tax_rate` Prozent Steuer, auf 2 Nachkommastellen gerundet.

### Restrictions
- `raise ValueError(...)`, wenn `tax_rate` negativ ist.
- `raise ValueError(...)`, wenn irgendein Preis (Artikel, Versand oder
  Zuschlag) negativ ist.

### Acceptance Criteria
- Alle Tests in `tests/test_totals.py` bestehen.

### Submission
`workspace/totals.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-05`
