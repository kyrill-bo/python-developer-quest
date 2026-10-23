## Mission: Config Loader

**Rank:** Python Apprentice
**Difficulty:** 3/5
**Estimated time:** 30 Minuten
**XP reward:** 25

### Prerequisites
- Safe Order Parser abgeschlossen.

### Scenario
Dein Service soll eine optionale JSON-Konfigurationsdatei laden. Fehlt die
Datei, greifen Defaults. Ist sie vorhanden aber kaputt, soll das klar als
Fehler sichtbar werden -- nicht stillschweigend ignoriert.

### Objectives
- Dateien lesen mit `pathlib`.
- Eigene Module schreiben und gegenseitig importieren.
- Mergen von Dictionaries (Defaults + Override).

### Requirements
Erstelle zwei Dateien in `workspace/`:

1. `errors.py` mit `class ConfigError(Exception): ...`
2. `config_loader.py` mit:

```
def load_config(path: str, defaults: dict) -> dict
```

- Existiert die Datei unter `path` nicht: gib eine Kopie von `defaults`
  zurueck.
- Existiert sie, aber ist kein gueltiges JSON: `raise ConfigError(...)`
  (mit `from exc`, unter Nennung des Pfads).
- Existiert sie und ist gueltig: gemergtes dict, wobei Werte aus der Datei
  die Defaults ueberschreiben.

### Restrictions
- `config_loader.py` muss `ConfigError` aus `errors.py` importieren (kein
  Duplikat der Klasse).
- Keine Mutation des `defaults`-dicts, das dir uebergeben wird.

### Acceptance Criteria
- Alle Tests in `tests/test_config_loader.py` bestehen.

### Submission
`workspace/errors.py`, `workspace/config_loader.py`

### Evaluation
`python -m quest check campaign-01-python-fundamentals/mission-07`
