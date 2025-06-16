import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import cross_validate  # noqa: E402


def test_cross_validation_runs_quickly():
    start = time.time()
    mean_auc = cross_validate.cross_validate(folds=5)
    assert mean_auc >= 0.85
    assert time.time() - start < 30
