## Mission: Environment Recon

**Rank:** Python Initiate
**Difficulty:** 1/5
**Estimated time:** 15 Minuten
**XP reward:** 10

### Prerequisites
Keine. Dies ist die erste Mission.

### Scenario
Bevor ein Backend-Team auch nur eine Zeile Code schreibt, verifiziert es die
Zielumgebung. Fehlende oder falsche Toolchain-Versionen sind eine der
haeufigsten Ursachen fuer "works on my machine"-Bugs. Deine erste Aufgabe:
dokumentiere, was auf deinem System tatsaechlich installiert ist -- nicht,
was du vermutest.

### Objectives
- Ermittle deine Python-Version, ob pip verfuegbar ist, ob git verfuegbar ist
  und auf welcher Plattform du arbeitest.
- Dokumentiere die Befunde maschinenlesbar als JSON.

### Requirements
Lege die Datei `workspace/recon.json` mit genau diesen vier Feldern an:

- `python_version` (string): `"MAJOR.MINOR"`, z.B. `"3.14"`
- `pip_available` (bool): `true`, wenn `pip` bzw. `python3 -m pip` funktioniert
- `git_available` (bool): `true`, wenn `git --version` funktioniert
- `platform` (string): das Ergebnis von `platform.system()` (`Darwin` / `Linux` / `Windows`)

### Restrictions
- Keine erfundenen Werte -- die Pruefung vergleicht mit der echten Umgebung.
- Keine zusaetzlichen top-level Felder sind notwendig, aber auch nicht verboten.

### Acceptance Criteria
- `workspace/recon.json` existiert und ist gueltiges JSON.
- Alle vier Felder sind vorhanden und korrekt.

### Submission
`workspace/recon.json`

### Evaluation
`python -m quest check campaign-00-onboarding/mission-01-recon`
