# Python Developer Quest

Ein gamifiziertes, lokal laufendes Lernsystem fuer Python-Backend- und
Microservices-Entwicklung. Inspiriert von Hack The Box (challenge-basierte
Progression) und RPGs (XP, Level, Skill-Tree, Achievements, Boss Fights) --
aber fachlich ein Software-Engineering-Bootcamp, kein Spiel fuer Kinder.

Du schreibst und debuggst den Code selbst. Die Plattform gibt Aufgaben,
progressive Hints, automatisierte Evaluierung und Fortschritts-Tracking --
keine fertigen Loesungen auf Zuruf. Jede Mission hat eine `solution/`
Referenzloesung -- schau sie dir erst an, nachdem du es selbst versucht
hast, sonst bringt dir die Mission nichts.

## Setup

Vorausgesetzt wird nur **Python 3.11 oder neuer** und **git**. Alles
andere (inkl. deiner eigenen virtuellen Umgebung) ist Teil von Campaign 0.

**macOS** (Homebrew):
```bash
brew install python@3.12 git
```

**Linux** (Debian/Ubuntu):
```bash
sudo apt update && sudo apt install -y python3 python3-venv git
```

**Windows** (PowerShell):
```powershell
winget install Python.Python.3.12 Git.Git
```
Danach in einem neuen Terminal `python --version` pruefen (ggf. `python`
statt `python3` verwenden -- unter Windows ist das die ueblichere Form).

**Klonen und starten** (alle Plattformen):
```bash
git clone <REPO-URL>
cd python-developer-quest
python3 -m quest status
```

Das `quest`-CLI selbst braucht **keine** Installation und **keine**
virtuelle Umgebung -- es nutzt nur die Standardbibliothek, lauft also
sofort nach dem Klonen. Das ist Absicht: Campaign 0 (Onboarding) bringt
dir bei, *selbst* eine `.venv` anzulegen und Dependencies zu
installieren -- plattformunabhaengig, die Mission fuehrt dich durch die
Befehle fuer dein jeweiliges Betriebssystem. Ab Mission 5 ("First Blood")
nutzt die Evaluierung dann deine eigene `.venv`.

## Schnellstart

```bash
python3 -m quest status   # dein aktueller Stand
python3 -m quest map      # Campaign-Uebersicht
python3 -m quest start    # naechste verfuegbare Mission anzeigen
python3 -m quest hint     # naechsten Hint fuer die aktive Mission
python3 -m quest check    # Mission evaluieren (XP, Achievements)
python3 -m quest progress # Completion % und Skill-Tree
python3 -m quest achievements
python3 -m quest review   # Staerken/Schwaechen-Zusammenfassung
python3 -m quest gui      # Web-Dashboard (Mission-Browser, Hints, Check-Button)
```

## Struktur

```
python-developer-quest/
├── quest/              CLI-Plattform (stdlib-only, siehe docs/progression-system.md)
├── curriculum/          15 Campaigns, je mit campaign.json + Missionen
│   └── campaign-XX/mission-YY/
│       ├── mission.json      Metadaten (XP, Prereqs, Hints, Check-Typ)
│       ├── scenario.md       Vollstaendiges Mission-Briefing (ohne Hints/Loesung)
│       ├── workspace/         Hier implementierst DU
│       ├── tests/             Automatisierte Tests (bei type=pytest)
│       └── solution/          Referenzloesung -- nur nach eigenem Versuch ansehen
├── state/               Dein Spielstand (player.json, history.json) -- wird beim ersten Lauf angelegt
├── docs/                 Learning Map, Progression-System, Troubleshooting
└── tests/                Tests fuer die Plattform selbst
```

## Status dieser Umgebung

- **Campaign 0 (Onboarding)** und **Campaign 1 (Python Fundamentals)** sind
  vollstaendig implementiert: 7 + 12 Missionen (inkl. Mini-Projekt und
  Boss Fight), alle mit Tests und gegen eine Referenzloesung verifiziert.
- **Campaign 2-14** sind als Metadaten (Themen, Skill-Tracks, Boss-Fight-
  Beschreibung, Voraussetzungen) angelegt und werden freigeschaltet bzw.
  inhaltlich ausgebaut, sobald du dort ankommst.
- Manche spaetere Campaigns (8, 11, 13, 14) setzen Docker voraus --
  installiere es erst, wenn du dort ankommst (siehe `docs/troubleshooting.md`).

## Fortsetzen nach einem Neustart

`python3 -m quest status` zeigt dir jederzeit, wo du stehst -- auch nach
Terminal-Neustart oder neuer Session. Siehe auch `SESSION.md`.
