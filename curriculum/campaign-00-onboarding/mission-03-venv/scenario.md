## Mission: Isolation Protocol

**Rank:** Python Initiate
**Difficulty:** 1/5
**Estimated time:** 10 Minuten
**XP reward:** 15

### Prerequisites
- First Contact abgeschlossen.

### Scenario
Ohne Isolation landen irgendwann alle Projekt-Dependencies global im System-Python
und kollidieren miteinander. Das Python-Pendant zu einem projekt-lokalen
Gradle/Maven-Setup ist ein *virtual environment* (venv): ein eigener,
isolierter Python-Interpreter samt eigenem Package-Verzeichnis pro Projekt.

### Objectives
- Eine virtuelle Umgebung im Projekt-Root anlegen.

### Requirements
- Lege im Projekt-Root (dem Ordner mit `pyproject.toml`, NICHT in `curriculum/`)
  eine virtuelle Umgebung namens `.venv` an.
- Empfohlen: `uv venv` (schnell, nutzt dein installiertes `uv`).
- Alternative: `python3 -m venv .venv`.

### Restrictions
- Die venv muss `.venv` heissen und im Projekt-Root liegen -- die Pruefung
  sucht genau dort.

### Acceptance Criteria
- `.venv/bin/python3` (oder `.venv/bin/python`) existiert.

### Submission
Kein Code -- nur der Zustand des Dateisystems (`.venv/`).

### Evaluation
`python -m quest check campaign-00-onboarding/mission-03-venv`
