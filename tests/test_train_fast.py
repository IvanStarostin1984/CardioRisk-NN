import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import train  # noqa: E402


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
