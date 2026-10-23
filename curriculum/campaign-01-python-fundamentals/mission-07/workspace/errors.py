"""Mission: Config Loader -- custom error type."""


class ConfigError(Exception):
    """Raised when a config file exists but cannot be parsed."""
