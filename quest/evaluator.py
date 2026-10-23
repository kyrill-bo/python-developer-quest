"""Runs a mission's checks and produces a pass/fail score.

Two mission types:
  - "check_script": a hand-written Python check function (quest/checks.py)
    inspects files the player produced, or runs their script via subprocess.
    Used for Campaign 0, where a venv/pytest may not exist yet.
  - "pytest": the player edits a submission file; we run the mission's
    pytest suite against it using the project's .venv interpreter.
"""
from __future__ import annotations

import json
import os
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from quest.model import Mission
from quest.state import project_root


@dataclass
class CheckResult:
    passed: bool
    score: float  # 0.0 - 1.0
    detail: str


def venv_python() -> Path | None:
    candidate = project_root() / ".venv" / "bin" / "python3"
    if candidate.exists():
        return candidate
    candidate = project_root() / ".venv" / "bin" / "python"
    if candidate.exists():
        return candidate
    return None


def venv_env() -> dict[str, str]:
    """Environment for subprocesses run with the .venv interpreter.

    Calling `.venv/bin/python` directly does not activate the venv: PATH stays
    untouched, so tools like ruff/pytest installed in `.venv/bin` are invisible
    to `shutil.which`. We replicate `source .venv/bin/activate` instead, so
    player scripts and pytest see the same environment they would in a shell.
    """
    env = os.environ.copy()
    py = venv_python()
    if py is not None:
        venv_bin = py.parent
        env["PATH"] = os.pathsep.join([str(venv_bin), env.get("PATH", "")])
        env["VIRTUAL_ENV"] = str(venv_bin.parent)
    return env


def run_mission_check(mission: Mission) -> CheckResult:
    if mission.type == "check_script":
        return _run_check_script(mission)
    if mission.type == "pytest":
        return _run_pytest(mission)
    return CheckResult(passed=False, score=0.0, detail=f"Unbekannter Mission-Typ: {mission.type}")


def _run_check_script(mission: Mission) -> CheckResult:
    import quest.checks as checks_mod

    if not mission.check_function:
        return CheckResult(False, 0.0, "Mission hat keine check_function definiert.")
    func = getattr(checks_mod, mission.check_function, None)
    if func is None:
        return CheckResult(False, 0.0, f"check_function '{mission.check_function}' nicht gefunden in quest/checks.py")
    try:
        result = func(Path(mission.dir))
    except Exception as exc:  # noqa: BLE001 - surface any student-triggered crash as a failed check
        return CheckResult(False, 0.0, f"Check-Funktion ist abgestuerzt: {exc!r}")
    return result


def _run_pytest(mission: Mission) -> CheckResult:
    py = venv_python()
    if py is None:
        return CheckResult(
            False,
            0.0,
            "Keine .venv gefunden. Lege zuerst eine virtuelle Umgebung im Projektroot an "
            "(siehe Campaign 0, Mission 'Isolation Protocol') und installiere pytest.",
        )

    mission_dir = Path(mission.dir)
    test_path = mission_dir / (mission.test_path or "tests")
    if not test_path.exists():
        return CheckResult(False, 0.0, f"Test-Pfad nicht gefunden: {test_path}")

    junit_path = mission_dir / ".quest_junit.xml"
    cmd = [str(py), "-m", "pytest", str(test_path), "-q", f"--junit-xml={junit_path}"]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(mission_dir),
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
            env=venv_env(),
        )
    except FileNotFoundError:
        return CheckResult(False, 0.0, "pytest ist in der .venv nicht installiert.")
    except subprocess.TimeoutExpired:
        return CheckResult(False, 0.0, "Tests haben das Zeitlimit (60s) ueberschritten.")

    if not junit_path.exists():
        detail = proc.stdout + "\n" + proc.stderr
        return CheckResult(False, 0.0, f"pytest konnte nicht ausgefuehrt werden:\n{detail.strip()[-2000:]}")

    try:
        root = ET.parse(junit_path).getroot()
        suite = root.find("testsuite") if root.tag != "testsuite" else root
        total = int(suite.get("tests", 0))
        failures = int(suite.get("failures", 0))
        errors = int(suite.get("errors", 0))
        skipped = int(suite.get("skipped", 0))
    finally:
        junit_path.unlink(missing_ok=True)

    if total == 0:
        return CheckResult(False, 0.0, "Keine Tests gefunden.")

    passed_count = total - failures - errors - skipped
    ratio = passed_count / total
    passed = failures == 0 and errors == 0 and passed_count > 0

    detail_lines = [f"{passed_count}/{total} Tests bestanden."]
    if proc.stdout.strip():
        detail_lines.append(proc.stdout.strip()[-3000:])
    return CheckResult(passed=passed, score=ratio, detail="\n".join(detail_lines))


def run_script(script_path: Path, args: list[str] | None = None, timeout: int = 15) -> subprocess.CompletedProcess:
    py = venv_python()
    interpreter = str(py) if py else "python3"
    return subprocess.run(
        [interpreter, str(script_path), *(args or [])],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        env=venv_env(),
    )


def read_json_if_exists(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
