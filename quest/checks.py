"""check_script functions for Campaign 0 (Developer Onboarding).

Each function takes the mission directory and returns an evaluator.CheckResult.
Referenced by name from each mission's mission.json (`check_function`).
"""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from quest.evaluator import CheckResult, run_script


def env_check_recon(mission_dir: Path) -> CheckResult:
    recon_path = mission_dir / "workspace" / "recon.json"
    if not recon_path.exists():
        return CheckResult(False, 0.0, "workspace/recon.json fehlt. Lege die Datei mit deinen Befundwerten an.")
    try:
        data = json.loads(recon_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return CheckResult(False, 0.0, f"recon.json ist kein gueltiges JSON: {exc}")

    required = {"python_version", "pip_available", "git_available", "platform"}
    missing = required - data.keys()
    if missing:
        return CheckResult(False, 0.3, f"Fehlende Felder: {sorted(missing)}")

    expected_prefix = f"{sys.version_info.major}.{sys.version_info.minor}"
    checks = {
        "python_version": str(data["python_version"]).startswith(expected_prefix),
        "pip_available": data["pip_available"] is True,
        "git_available": data["git_available"] is True,
        "platform": str(data["platform"]).lower() == platform.system().lower(),
    }
    passed_count = sum(checks.values())
    ratio = passed_count / len(checks)
    if ratio == 1.0:
        return CheckResult(True, 1.0, "Recon-Report korrekt: Python, pip, git und Plattform passen.")
    wrong = [k for k, ok in checks.items() if not ok]
    return CheckResult(False, ratio, f"Diese Felder stimmen nicht mit der echten Umgebung ueberein: {wrong}")


def first_script_contact(mission_dir: Path) -> CheckResult:
    script = mission_dir / "workspace" / "hello.py"
    if not script.exists():
        return CheckResult(False, 0.0, "workspace/hello.py fehlt.")

    try:
        default_run = run_script(script)
        named_run = run_script(script, ["World"])
    except Exception as exc:  # noqa: BLE001
        return CheckResult(False, 0.0, f"Skript konnte nicht ausgefuehrt werden: {exc!r}")

    checks = []
    if default_run.returncode != 0:
        checks.append(f"Aufruf ohne Argumente schlug fehl (exit {default_run.returncode}): {default_run.stderr[-500:]}")
    elif "World" not in default_run.stdout:
        checks.append("Ohne Argumente sollte der Default-Name 'World' begruesst werden.")

    if named_run.returncode != 0:
        checks.append(f"Aufruf mit Argument schlug fehl (exit {named_run.returncode}): {named_run.stderr[-500:]}")
    elif "World" not in named_run.stdout or "Hello" not in named_run.stdout:
        checks.append("Mit Argument 'World' sollte die Ausgabe 'Hello' und 'World' enthalten.")

    if checks:
        return CheckResult(False, 1 - len(checks) / 2, "\n".join(checks))
    return CheckResult(True, 1.0, "hello.py begruesst korrekt mit und ohne Argument.")


def isolation_protocol(mission_dir: Path) -> CheckResult:
    from quest.state import project_root

    venv_dir = project_root() / ".venv"
    if not venv_dir.exists():
        return CheckResult(False, 0.0, "Keine .venv im Projektroot gefunden. Nutze `uv venv` oder `python3 -m venv .venv`.")
    python_bin = venv_dir / "bin" / "python3"
    if not python_bin.exists():
        python_bin = venv_dir / "bin" / "python"
    if not python_bin.exists():
        return CheckResult(False, 0.3, ".venv existiert, aber kein python-Interpreter unter .venv/bin gefunden.")
    return CheckResult(True, 1.0, f".venv korrekt angelegt mit Interpreter unter {python_bin}.")


def dependency_lockdown(mission_dir: Path) -> CheckResult:
    import subprocess

    from quest.state import project_root

    venv_dir = project_root() / ".venv"
    missing = []
    for tool in ("pytest", "ruff"):
        tool_bin = venv_dir / "bin" / tool
        if not tool_bin.exists():
            missing.append(tool)
            continue
        try:
            proc = subprocess.run(
                [str(tool_bin), "--version"], capture_output=True, text=True, timeout=10, check=False
            )
            if proc.returncode != 0:
                missing.append(tool)
        except (OSError, subprocess.TimeoutExpired):
            missing.append(tool)

    if missing:
        return CheckResult(
            False,
            1 - len(missing) / 2,
            f"Diese Tools fehlen in der .venv oder laufen nicht: {missing}. "
            f"Installiere mit `uv pip install -e \".[dev]\"` (im Projektroot).",
        )
    return CheckResult(True, 1.0, "pytest und ruff sind in der .venv installiert und lauffaehig.")


def diagnose_broken_env(mission_dir: Path) -> CheckResult:
    config_path = mission_dir / "workspace" / "app_config.json"
    if not config_path.exists():
        return CheckResult(False, 0.0, "workspace/app_config.json fehlt.")
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return CheckResult(False, 0.0, f"app_config.json ist weiterhin kein gueltiges JSON: {exc}")

    errors = []
    if not isinstance(data.get("app_name"), str) or not data.get("app_name"):
        errors.append("app_name muss ein nicht-leerer String sein.")
    if not isinstance(data.get("debug"), bool):
        errors.append("debug muss ein JSON-Boolean (true/false) sein, kein String.")
    max_conn = data.get("max_connections")
    if not isinstance(max_conn, int) or isinstance(max_conn, bool) or not (1 <= max_conn <= 1000):
        errors.append("max_connections muss eine Ganzzahl zwischen 1 und 1000 sein.")
    hosts = data.get("allowed_hosts")
    if not isinstance(hosts, list) or not hosts or not all(isinstance(h, str) for h in hosts):
        errors.append("allowed_hosts muss eine nicht-leere Liste von Strings sein.")

    if errors:
        ratio = max(0.0, 1 - len(errors) / 4)
        return CheckResult(False, ratio, "\n".join(errors))
    return CheckResult(True, 1.0, "app_config.json ist jetzt valides JSON mit korrektem Schema.")


def onboarding_assessment(mission_dir: Path) -> CheckResult:
    script = mission_dir / "workspace" / "onboarding_report.py"
    if not script.exists():
        return CheckResult(False, 0.0, "workspace/onboarding_report.py fehlt.")
    try:
        proc = run_script(script)
    except Exception as exc:  # noqa: BLE001
        return CheckResult(False, 0.0, f"Skript ist abgestuerzt: {exc!r}")
    if proc.returncode != 0:
        return CheckResult(False, 0.0, f"Skript endete mit Fehler: {proc.stderr[-800:]}")
    try:
        report = json.loads(proc.stdout.strip())
    except json.JSONDecodeError:
        return CheckResult(False, 0.0, f"stdout ist kein gueltiges JSON:\n{proc.stdout[-500:]}")

    required = {"python_version", "venv_active", "pytest_installed", "ruff_installed"}
    missing = required - report.keys()
    if missing:
        return CheckResult(False, 0.3, f"Report fehlen Felder: {sorted(missing)}")

    issues = []
    if not report["venv_active"]:
        issues.append("venv_active ist False - stelle sicher, dass das Skript mit der .venv ausgefuehrt wird.")
    if not report["pytest_installed"]:
        issues.append("pytest_installed ist False.")
    if not report["ruff_installed"]:
        issues.append("ruff_installed ist False.")

    if issues:
        return CheckResult(False, 1 - len(issues) / 4, "\n".join(issues))
    return CheckResult(True, 1.0, "Onboarding-Report vollstaendig und korrekt. Campaign 0 abgeschlossen!")
