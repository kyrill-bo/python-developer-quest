# Session State -- Python Developer Quest

> Diese Datei wird nach jeder abgeschlossenen Mission aktualisiert. Sie ist
> eine lesbare Zusammenfassung von `state/player.json` -- die JSON-Datei
> ist die Quelle der Wahrheit, diese Datei ist fuer schnelles Wiedereinsteigen
> gedacht ("wo haben wir aufgehoert?").

**Letztes Update:** 2026-10-23 (Initial-Setup)

## Wo wir stehen

- Level 1: Python Initiate, 0 XP.
- 0 Missionen abgeschlossen, 0 Achievements.
- Campaign 0 (Developer Onboarding) ist aktiv und vollstaendig
  implementiert (7 Missionen). Campaign 1 (Python Fundamentals) ist
  freigeschaltet, sobald Campaign 0 abgeschlossen ist.

## Naechster Schritt

**Aktive Mission:** `campaign-00-onboarding/mission-01-recon` ("Environment
Recon") -- siehe `python -m quest start`.

Aufgabe: `workspace/recon.json` mit echten Befunden zu Python-Version,
pip-Verfuegbarkeit, git-Verfuegbarkeit und Plattform anlegen.

## Bei Session-Neustart

1. `python3 -m quest status` -- zeigt Rank, XP, aktive Mission.
2. `python3 -m quest map` -- Campaign-Uebersicht mit Lock-Status.
3. Diese Datei (`SESSION.md`) fuer den narrativen Kontext.
4. Weitermachen mit `python3 -m quest start` / `hint` / `check`.

## Bekannte Umgebungs-Einschraenkung

Docker wird erst ab Campaign 8/11/13/14 benoetigt -- installiere es erst,
wenn du dort ankommst. Details: `docs/troubleshooting.md`.
