import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from evaluate import evaluate  # noqa: E402


def test_roc_auc():
    auc = evaluate(seed=0)
    assert auc >= 0.85
