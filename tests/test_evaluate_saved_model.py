import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import train  # noqa: E402
import evaluate  # noqa: E402


def test_evaluate_saved_model(tmp_path):
    model_path = tmp_path / "model.pt"
    seed = 17
    train.train_model(
        True,
        seed=seed,
        model_path=str(model_path),
    )
    assert model_path.exists()

    auc, f1 = evaluate.evaluate_saved_model(model_path, seed=seed)
    assert auc >= 0.90
    assert f1 >= 0.80
