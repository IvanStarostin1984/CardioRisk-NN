from cardiorisk import train  # noqa: E402
from cardiorisk import evaluate  # noqa: E402


def test_evaluate_saved_model(tmp_path):
    model_path = tmp_path / "model.pt"
    seed = 17
    train.train_model(
        True,
        seed=seed,
        model_path=str(model_path),
    )
    assert model_path.exists()

    auc = evaluate.evaluate_saved_model(model_path, seed=seed)
    assert auc >= 0.90
