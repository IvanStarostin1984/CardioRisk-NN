import time
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
import cross_validate  # noqa: E402


def test_cross_validation_runs_quickly():
    start = time.time()
    auc1 = cross_validate.cross_validate(folds=5, fast=True, seed=0)
    auc2 = cross_validate.cross_validate(folds=5, fast=True, seed=0)
    assert isinstance(auc1, float)
    assert abs(auc1 - auc2) < 0.05
    assert auc1 >= 0.85
    assert time.time() - start < 30
