import time

from cardiorisk import cross_validate  # noqa: E402


def test_cross_validation_runs_quickly():
    start = time.time()
    mean_auc = cross_validate.cross_validate(folds=5)
    assert mean_auc >= 0.85
    assert time.time() - start < 30
