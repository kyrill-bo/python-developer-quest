"""Minimal dark/terminal-style rendering helpers. ANSI only, no dependencies."""
from __future__ import annotations

import sys

_COLOR = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    if not _COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"


def bold(t: str) -> str:
    return _c("1", t)


def dim(t: str) -> str:
    return _c("2", t)


def green(t: str) -> str:
    return _c("32", t)


def red(t: str) -> str:
    return _c("31", t)


def yellow(t: str) -> str:
    return _c("33", t)


def cyan(t: str) -> str:
    return _c("36", t)


def magenta(t: str) -> str:
    return _c("35", t)


def header(title: str) -> str:
    bar = "=" * max(len(title) + 4, 40)
    return f"\n{bold(cyan(bar))}\n{bold(cyan('  ' + title))}\n{bold(cyan(bar))}\n"


def bar(current: int, total: int, width: int = 24) -> str:
    if total <= 0:
        filled = width
    else:
        filled = int(width * min(current, total) / total)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def status_icon(ok: bool) -> str:
    return green("[OK]") if ok else red("[FAIL]")


def lock_icon(unlocked: bool, done: bool) -> str:
    if done:
        return green("[x]")
    if unlocked:
        return yellow("[ ]")
    return dim("[locked]")
