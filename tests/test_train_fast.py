import time
from pathlib import Path

from cardiorisk import train  # noqa: E402


def test_fast_training_runs_under_20s(capsys):
    start = time.time()
    model_file = Path("model.pt")
    if model_file.exists():
        model_file.unlink()

    train.train_model(True, seed=0, model_path="model.pt")

    out = capsys.readouterr().out
    assert "Early stopping" in out
    assert time.time() - start < 20
    assert model_file.exists()
    model_file.unlink()
