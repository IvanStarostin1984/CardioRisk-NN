import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import train  # noqa: E402
import evaluate  # noqa: E402


def test_imports():
    assert hasattr(train, "main")
    assert hasattr(evaluate, "main")
