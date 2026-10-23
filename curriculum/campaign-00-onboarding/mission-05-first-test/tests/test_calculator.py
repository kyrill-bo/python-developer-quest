import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workspace"))

from calculator import add


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_with_negative():
    assert add(-1, -1) == -2


def test_add_with_zero():
    assert add(0, 5) == 5
