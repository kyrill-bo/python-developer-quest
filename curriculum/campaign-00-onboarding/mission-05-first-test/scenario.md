## Mission: First Blood: Automated Testing

**Rank:** Python Initiate
**Difficulty:** 1/5
**Estimated time:** 15 Minuten
**XP reward:** 15

### Prerequisites
- Dependency Lockdown abgeschlossen (pytest muss installiert sein).

### Scenario
Ab jetzt wird jede Mission in dieser Lernumgebung durch pytest evaluiert.
Diese Mission fuehrt den Workflow einmal bewusst langsam vor: ein fertiger
Test wartet auf deine Implementierung.

### Objectives
- Den Unterschied zwischen Testcode und Implementierungscode verstehen.
- Den ersten automatisierten Testlauf durchfuehren.

### Requirements
- Implementiere `add(a: int, b: int) -> int` in `workspace/calculator.py`,
  sodass alle Tests in `tests/test_calculator.py` bestehen.

### Restrictions
- Veraendere `tests/test_calculator.py` nicht -- die Pruefung nutzt eine
  eigene Kopie der Tests.

### Acceptance Criteria
- Alle Tests in `tests/` sind gruen.

### Submission
`workspace/calculator.py`

### Evaluation
`python -m quest check campaign-00-onboarding/mission-05-first-test`

(Dies fuehrt intern aus: `.venv/bin/python -m pytest tests/` im Missionsordner.)
