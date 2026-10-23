import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from config_loader import load_config
from errors import ConfigError


def test_missing_file_returns_defaults(tmp_path):
    missing = tmp_path / "does_not_exist.json"
    defaults = {"debug": False, "max_connections": 10}
    result = load_config(str(missing), defaults)
    assert result == defaults
    assert result is not defaults  # must be a copy


def test_valid_file_overrides_defaults(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"max_connections": 50}', encoding="utf-8")
    defaults = {"debug": False, "max_connections": 10}
    result = load_config(str(config_file), defaults)
    assert result == {"debug": False, "max_connections": 50}


def test_invalid_json_raises_config_error(tmp_path):
    config_file = tmp_path / "broken.json"
    config_file.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(str(config_file), {"debug": False})


def test_defaults_not_mutated(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"a": 1}', encoding="utf-8")
    defaults = {"a": 0, "b": 2}
    load_config(str(config_file), defaults)
    assert defaults == {"a": 0, "b": 2}
