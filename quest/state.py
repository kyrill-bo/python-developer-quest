"""Persistence for player progress. Plain JSON files under state/.

Writes are atomic (write to temp file, then rename) so a crash mid-write
cannot corrupt state. Loading a corrupt/invalid file never crashes the CLI:
it backs the bad file up and starts a fresh PlayerState, explaining what
happened to the user.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from quest.model import AttemptRecord, PlayerState, utc_now_iso

STATE_DIR_NAME = "state"
PLAYER_FILE = "player.json"
HISTORY_FILE = "history.json"


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def state_dir() -> Path:
    d = project_root() / STATE_DIR_NAME
    d.mkdir(exist_ok=True)
    return d


def _atomic_write_json(path: Path, data) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


@dataclass
class LoadResult:
    player: PlayerState
    warning: str | None = None


def load_player() -> LoadResult:
    path = state_dir() / PLAYER_FILE
    if not path.exists():
        return LoadResult(player=PlayerState())
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise TypeError("player.json does not contain a JSON object")
        return LoadResult(player=PlayerState.from_dict(raw))
    except (json.JSONDecodeError, TypeError, OSError) as exc:
        backup = path.with_name(path.name + ".corrupt")
        try:
            path.replace(backup)
        except OSError:
            pass
        warning = (
            f"state/player.json war ungueltig ({exc}). "
            f"Datei wurde nach {backup.name} verschoben, neuer Spielstand wurde angelegt."
        )
        return LoadResult(player=PlayerState(), warning=warning)


def save_player(player: PlayerState) -> None:
    player.updated_at = utc_now_iso()
    _atomic_write_json(state_dir() / PLAYER_FILE, player.to_dict())


def load_history() -> list[AttemptRecord]:
    path = state_dir() / HISTORY_FILE
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return []
        return [AttemptRecord(**item) for item in raw]
    except (json.JSONDecodeError, TypeError, OSError):
        return []


def append_history(record: AttemptRecord) -> None:
    history = load_history()
    history.append(record)
    data = [vars(r) for r in history]
    _atomic_write_json(state_dir() / HISTORY_FILE, data)
