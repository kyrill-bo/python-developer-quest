# Progression System

## XP und Ranks

10 Level, kumulative XP-Schwellen:

| Level | Rank | XP-Schwelle |
|---|---|---|
| 1 | Python Initiate | 0 |
| 2 | Code Explorer | 150 |
| 3 | Python Apprentice | 400 |
| 4 | Backend Builder | 800 |
| 5 | API Engineer | 1400 |
| 6 | Database Specialist | 2200 |
| 7 | Microservices Engineer | 3200 |
| 8 | Data Pipeline Engineer | 4500 |
| 9 | Production Engineer | 6200 |
| 10 | Senior Backend Candidate | 8500 |

Diese Ranks sind Fortschritts-Marker innerhalb der Lernumgebung, keine
Aussage ueber reale Jobqualifikation.

XP-Richtwerte pro Aufgabentyp (siehe `quest/model.py`, `mission.json` pro
Mission): kleine Exercise 10-15, mittlere Exercise 20-25, Mini-Projekt
~250, Boss Fight ~500, Capstone bis 1500.

Teil-XP: Bei einem ernsthaften, aber nicht vollstaendig bestandenen
Versuch (`score > 0`) gibt es die Haelfte von `xp_reward * score` als
Teil-XP -- einmalig, nicht bei jedem erneuten Versuch.

## Skill Tree

14 unabhaengige Tracks (`quest/model.py::SKILL_TRACKS`), je 0-5, alle 15
gesammelten Punkte ein Level hoeher. Jede Mission vergibt Punkte in
spezifische Tracks (`mission.json::skills`). Fortgeschrittene Missionen
koennen zusaetzlich einen Mindest-Skill-Level als Voraussetzung verlangen
(`mission.json::prerequisites.skills`) -- nicht nur eine Mission-ID.

## Achievements

Datengetrieben: eine Mission kann `grants_achievement` setzen
(`mission.json`). Beim ersten erfolgreichen Abschluss wird es
freigeschaltet (`quest/achievements.py`). Katalog mit Titel/Beschreibung:
`curriculum/achievements.json`.

## Freischaltung (Gating)

- Eine Mission ist gesperrt, bis alle `prerequisites.missions` abgeschlossen
  UND alle `prerequisites.skills`-Mindestlevel erreicht sind
  (`quest/progression.py::mission_is_unlocked`).
- Eine Campaign ist gesperrt, bis `status == "available"` UND alle
  Missionen jeder `prerequisite_campaigns`-Campaign abgeschlossen sind
  (`campaign_is_unlocked`). Campaigns ohne definierte Missionen (geplant,
  noch nicht ausgebaut) blockieren nicht.

## Evaluierung

Zwei Mission-Typen (`mission.json::type`):

- **check_script**: eine Python-Funktion in `quest/checks.py` prueft
  Datei-Inhalte oder fuehrt ein Skript des Spielers aus. Genutzt in
  Campaign 0, wo ggf. noch keine `.venv`/pytest existiert.
- **pytest**: `quest/evaluator.py` fuehrt die Mission-Tests mit dem
  Interpreter aus `.venv/bin/python` (Projekt-Root) aus und wertet die
  JUnit-XML-Ausgabe aus.

Scoring: `score` = Anteil bestandener Tests (0.0-1.0). Volle XP nur bei
`score >= min_pass_ratio` (Standard: 1.0, also 100%).

## Persistenz

`state/player.json` (Spielstand) und `state/history.json`
(Versuchsprotokoll) sind einfache JSON-Dateien, atomar geschrieben
(`quest/state.py`). Eine kaputte `player.json` wird als
`player.json.corrupt` gesichert; es wird automatisch ein neuer, leerer
Spielstand angelegt -- die CLI crasht dabei nie.

## CLI-Befehle

Siehe `README.md` fuer die Liste. Implementierung: `quest/cli.py`.
