import json
from pathlib import Path

from errors import ConfigError


def load_config(path: str, defaults: dict) -> dict:
    p = Path(path)
    if not p.exists():
        return dict(defaults)
    try:
        loaded = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid config at {path}: {exc}") from exc
    return {**defaults, **loaded}
