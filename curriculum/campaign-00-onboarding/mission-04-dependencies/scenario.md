## Mission: Dependency Lockdown

**Rank:** Python Initiate
**Difficulty:** 2/5
**Estimated time:** 15 Minuten
**XP reward:** 15

### Prerequisites
- Isolation Protocol abgeschlossen.

### Scenario
Eine venv ohne Pakete ist nutzlos. Du installierst jetzt die Tools, die der
Rest dieser Lernumgebung voraussetzt: `pytest` (Testframework, Python-Pendant
zu JUnit) und `ruff` (Linter/Formatter, schneller Ersatz fuer mehrere
klassische Tools wie flake8/black/isort in einem).

### Objectives
- Dev-Dependencies in die `.venv` installieren.

### Requirements
- Installiere `pytest` und `ruff` in die `.venv` im Projekt-Root.
- Nutze dafuer die bereits vorhandene `pyproject.toml` (`dev`-Extra) oder
  installiere die Pakete direkt.

### Restrictions
- Keine globale Installation ausserhalb der `.venv`.

### Acceptance Criteria
- `.venv/bin/pytest --version` laeuft erfolgreich.
- `.venv/bin/ruff --version` laeuft erfolgreich.

### Submission
Kein Code -- Zustand der `.venv`.

### Evaluation
`python -m quest check campaign-00-onboarding/mission-04-dependencies`
