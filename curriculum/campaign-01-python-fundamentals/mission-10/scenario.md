## Mission: Resilient Batch Importer

**Rank:** Python Apprentice
**Difficulty:** 3/5
**Estimated time:** 30 Minuten
**XP reward:** 25

### Prerequisites
- API Response Normalizer abgeschlossen.

### Scenario
Ein naechtlicher Batch-Import verarbeitet hunderte Inventar-Datensaetze.
Ein einzelner kaputter Datensatz darf den gesamten Lauf nicht abbrechen --
er soll stattdessen "in Quarantaene" landen, mit Begruendung, waehrend die
guten Datensaetze normal weiterverarbeitet werden.

### Objectives
- Fehlerbehandlung PRO ITERATION statt fuer den gesamten Batch.
- Ein wiederkehrendes Resilienz-Pattern kennenlernen (wichtig fuer spaetere
  Data-Pipeline-Missionen).

### Requirements
Implementiere in `workspace/batch_importer.py`:

```
def import_batch(records: list[dict]) -> tuple[list[dict], list[dict]]
```

- Jeder `record` sollte die Felder `sku` (nicht-leerer String) und `qty`
  (positiver `int`) haben.
- Gueltige Records werden normalisiert (`{"sku": ..., "qty": ...}`) in die
  erste Liste gesammelt.
- Ungueltige Records werden als `{"record": <original>, "reason": <str>}`
  in die zweite Liste gesammelt.
- Die Reihenfolge innerhalb jeder Liste folgt der Eingabereihenfolge.

### Restrictions
- Ein fehlerhafter Datensatz darf die Verarbeitung der uebrigen Datensaetze
  NICHT abbrechen.
- Keine globalen Variablen fuer den Zwischenzustand.

### Acceptance Criteria
- Alle Tests in `tests/test_batch_importer.py` bestehen.

### Submission
`workspace/batch_importer.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-10`
