import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import cross_validate  # noqa: E402


def test_main_no_fast(monkeypatch):
    called = {}

    def fake_cv(folds, backend="torch", fast=True, seed=0):
        called["fast"] = fast
        called["folds"] = folds
        called["backend"] = backend
        called["seed"] = seed
        return 0.0

    monkeypatch.setattr(cross_validate, "cross_validate", fake_cv)
    cross_validate.main(
        ["--no-fast", "--backend", "tf", "--folds", "2", "--seed", "5"]
    )
    assert called["fast"] is False
    assert called["folds"] == 2
    assert called["backend"] == "tf"
    assert called["seed"] == 5
