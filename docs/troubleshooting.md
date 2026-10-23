# Troubleshooting & Umgebungs-Einschraenkungen

Stand der Environment-Inspektion (Stage A), durchgefuehrt auf diesem
System:

| Tool | Status | Version |
|---|---|---|
| Python | OK | 3.14.6 (`/opt/homebrew/bin/python3`) |
| pip | OK | 26.1.2 |
| git | OK | 2.54.0 |
| uv | OK | 0.11.28 |
| **Docker** | **NICHT installiert** | -- |
| podman / colima / docker-compose | nicht installiert | -- |
| poetry | nicht installiert (nicht benoetigt, `uv` wird genutzt) | -- |
| ruff | nicht global installiert (wird projekt-lokal via `.venv` oder `pyproject.toml`-Extra `dev` installiert) | -- |

## Docker fehlt -- Auswirkung

Folgende Campaigns setzen Docker (bzw. Docker Compose) voraus:

- **Campaign 8** (RabbitMQ/Kafka-Labs via Docker Compose)
- **Campaign 11** (Docker, Kubernetes, CI/CD)
- **Campaign 13** (Boss Fight: containerisiertes System)
- **Campaign 14** (Capstone: Docker Compose, optional lokales Kubernetes)

Diese Campaigns sind aktuell als `status: "planned"` markiert und werden
erst inhaltlich ausgebaut, wenn du dort ankommst -- bis dahin genug Zeit,
Docker zu installieren.

**Empfehlung, wenn du so weit bist:** Docker Desktop fuer macOS
(https://www.docker.com/products/docker-desktop/) oder, falls du eine
leichtgewichtigere Alternative bevorzugst, Colima
(`brew install colima docker docker-compose`). Pruefe danach erneut mit
`docker --version`.

Dieses System wurde **nicht** automatisch modifiziert, um Docker zu
installieren -- das war ausserhalb des Scopes dieser Lernumgebung und
haette eine explizite Erlaubnis gebraucht.

## Haeufige Probleme

**`python -m quest check` sagt "Keine .venv gefunden"**
-> Du bist noch nicht bei Mission "Isolation Protocol" (Campaign 0,
Mission 3) angelangt bzw. hast sie noch nicht geloest. Lege im
Projekt-Root (`studyPython/`, nicht in `curriculum/...`) eine `.venv` an:
`uv venv`.

**pytest/ruff fehlen trotz `.venv`**
-> Mission "Dependency Lockdown" (Campaign 0, Mission 4) noch nicht
geloest. `uv pip install -e ".[dev]"` im Projekt-Root.

**`state/player.json` scheint kaputt / CLI zeigt eine Warnung beim Start**
-> Die Datei wurde automatisch nach `player.json.corrupt` gesichert und
ein frischer Spielstand angelegt (siehe `quest/state.py::load_player`).
Das ist Absicht (fail-safe), kein Datenverlust-Bug -- aber dein alter
Fortschritt ist weg. Pruefe `state/player.json.corrupt`, falls du ihn
retten willst.

**Ein Mission-Check haengt oder dauert sehr lange**
-> Pytest-Checks haben ein 60-Sekunden-Timeout
(`quest/evaluator.py::_run_pytest`), check_script-Skriptaufrufe 15
Sekunden (`run_script`). Eine Endlosschleife in deinem Code fuehrt zu
einem klaren Timeout-Fehler, keinem haengenden Terminal.
