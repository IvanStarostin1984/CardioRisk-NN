import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
import cross_validate  # noqa: E402


def test_cross_validation_tf_runs_quickly():
    start = time.time()
    auc1 = cross_validate.cross_validate(
        folds=3,
        backend="tf",
        fast=True,
        seed=1,
    )
    auc2 = cross_validate.cross_validate(
        folds=3,
        backend="tf",
        fast=True,
        seed=1,
    )
    assert isinstance(auc1, float)
    assert abs(auc1 - auc2) < 0.05
    assert auc1 >= 0.80
    assert time.time() - start < 40


def test_cli_patience_tf(monkeypatch):
    called = {}

    def fake_cv(folds, backend="torch", fast=True, seed=0, patience=5):
        called["patience"] = patience
        called["backend"] = backend
        return 0.0

    monkeypatch.setattr(cross_validate, "cross_validate", fake_cv)
    cross_validate.main(["--backend", "tf", "--patience", "4"])
    assert called["backend"] == "tf"
    assert called["patience"] == 4
