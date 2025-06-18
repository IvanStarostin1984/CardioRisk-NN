import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
import cross_validate  # noqa: E402


def test_cross_validation_baseline_runs_quickly():
    start = time.time()
    auc1 = cross_validate.cross_validate(
        folds=3,
        backend="baseline",
        fast=True,
        seed=2,
    )
    auc2 = cross_validate.cross_validate(
        folds=3,
        backend="baseline",
        fast=True,
        seed=2,
    )
    assert isinstance(auc1, float)
    assert abs(auc1 - auc2) < 0.05
    assert auc1 >= 0.84
    assert time.time() - start < 20


def test_cli_patience_baseline(monkeypatch):
    called = {}

    def fake_cv(folds, backend="torch", fast=True, seed=0, patience=5):
        called["backend"] = backend
        called["patience"] = patience
        return 0.0

    monkeypatch.setattr(cross_validate, "cross_validate", fake_cv)
    cross_validate.main(["--backend", "baseline", "--patience", "6"])
    assert called["backend"] == "baseline"
    assert called["patience"] == 6
