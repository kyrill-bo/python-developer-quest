## Mission: Diagnose: The Broken Environment

**Rank:** Python Initiate
**Difficulty:** 2/5
**Estimated time:** 20 Minuten
**XP reward:** 20

### Prerequisites
- First Blood: Automated Testing abgeschlossen.

### Scenario
Ein Kollege hat `workspace/app_config.json` "schnell von Hand" bearbeitet.
Seitdem crasht der Config-Loader. Das passiert in echten Projekten
staendig -- deine Aufgabe ist es, die Datei so zu reparieren, dass sie
sowohl syntaktisch gueltiges JSON ist als auch dem erwarteten Schema
entspricht.

### Objectives
- Eine kaputte JSON-Datei debuggen und reparieren.
- Ein einfaches Daten-Schema verstehen und durchsetzen.

### Requirements
Repariere `workspace/app_config.json` so, dass gilt:

- `app_name`: nicht-leerer String
- `debug`: JSON-Boolean (`true`/`false`), kein String
- `max_connections`: Ganzzahl zwischen 1 und 1000
- `allowed_hosts`: nicht-leere Liste von Strings

### Restrictions
- Loesche keine Felder -- repariere die Werte/Syntax.
- Keine zusaetzliche Validierungs-Logik in Python noetig fuer diese Mission
  -- nur die JSON-Datei selbst muss stimmen.

### Acceptance Criteria
- `workspace/app_config.json` ist gueltiges JSON.
- Alle vier Felder erfuellen das Schema oben.

### Submission
`workspace/app_config.json`

### Evaluation
`python -m quest check campaign-00-onboarding/mission-06-broken-env`
