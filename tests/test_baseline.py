import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import baseline  # noqa: E402


def test_baseline_auc(tmp_path):
    model_path = tmp_path / "baseline.pkl"
    auc = baseline.train_model(seed=0, model_path=str(model_path))
    assert auc >= 0.84
    assert model_path.exists()
