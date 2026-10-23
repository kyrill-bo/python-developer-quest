## Mission: Customer Deduplicator

**Rank:** Code Explorer
**Difficulty:** 2/5
**Estimated time:** 25 Minuten
**XP reward:** 15

### Prerequisites
- Inventory Scanner abgeschlossen.

### Scenario
Ein Import aus einem Legacy-CRM liefert Kundendatensaetze, von denen einige
doppelt vorkommen -- mit unterschiedlicher Gross-/Kleinschreibung der
E-Mail-Adresse. Ausserdem will das Marketing-Team wissen, aus welchen
E-Mail-Domains die Kunden kommen.

### Objectives
- Dictionaries als Lookup-Strukturen nutzen.
- Sets fuer eindeutige Werte nutzen.

### Requirements
Implementiere in `workspace/customers.py`:

```
def dedupe_customers(customers: list[dict]) -> tuple[list[dict], set[str]]
```

- Jeder Eintrag in `customers` hat mindestens das Feld `"email"`.
- Duplikate werden case-insensitiv anhand der E-Mail erkannt; der
  **erste** Eintrag gewinnt, spaetere Duplikate werden verworfen.
- Rueckgabe: `(deduplizierte_liste, domains)`, wobei `domains` die Menge
  aller (kleingeschriebenen) Domain-Teile der E-Mails ist.

### Restrictions
- `raise ValueError(...)`, wenn ein Eintrag kein `"email"`-Feld hat.
- Die Reihenfolge der deduplizierten Liste folgt der Reihenfolge des ersten
  Vorkommens.

### Acceptance Criteria
- Alle Tests in `tests/test_customers.py` bestehen.

### Submission
`workspace/customers.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-03`
