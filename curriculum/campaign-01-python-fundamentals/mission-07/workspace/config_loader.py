"""Mission: Config Loader."""

from errors import ConfigError  # noqa: F401  (re-exported for callers)


def load_config(path: str, defaults: dict) -> dict:
    # TODO: load JSON from `path` if it exists and merge over `defaults`.
    # Missing file -> return a copy of defaults. Invalid JSON -> ConfigError.
    raise NotImplementedError
