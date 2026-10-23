## Mission: Onboarding Assessment

**Rank:** Python Initiate
**Difficulty:** 2/5
**Estimated time:** 20 Minuten
**XP reward:** 30

### Prerequisites
- Alle sechs Campaign-0-Missionen abgeschlossen.

### Scenario
Bevor du in Campaign 1 (Python Fundamentals) startest, schreibst du ein
kleines Diagnose-Skript, das deine eigene Umgebung zur Laufzeit beschreibt --
ohne die Antworten vorher in eine Datei zu schreiben. Das ist der
Unterschied zwischen "ich glaube, mein Setup stimmt" und "mein Code
verifiziert es".

### Objectives
- Laufzeit-Introspektion in Python (sys, importlib, shutil).
- Ein Skript bauen, das maschinenlesbaren JSON-Output auf stdout erzeugt.

### Requirements
Erstelle `workspace/onboarding_report.py`. Beim Ausfuehren mit dem
venv-Python muss das Skript **genau ein** JSON-Objekt auf stdout drucken
mit folgenden Feldern:

- `python_version` (string, `"MAJOR.MINOR"`)
- `venv_active` (bool): `True`, wenn das Skript tatsaechlich mit dem
  Interpreter aus `.venv` laeuft (nicht dem System-Python)
- `pytest_installed` (bool)
- `ruff_installed` (bool)

### Restrictions
- Keine hartcodierten Werte (`true` zu schreiben ohne echte Pruefung gilt
  nicht als Nachweis -- die Pruefung fuehrt dein Skript tatsaechlich aus).
- Nur eine Zeile JSON auf stdout, keine zusaetzlichen print()-Aufrufe.

### Acceptance Criteria
- Skript laeuft fehlerfrei (Exit-Code 0) mit dem venv-Python.
- stdout ist gueltiges JSON mit allen vier Feldern, alle Werte korrekt.

### Submission
`workspace/onboarding_report.py`

### Evaluation
`python -m quest check campaign-00-onboarding/assessment`

Nach Bestehen ist Campaign 0 abgeschlossen und Campaign 1 (Python
Fundamentals) ist freigeschaltet.
