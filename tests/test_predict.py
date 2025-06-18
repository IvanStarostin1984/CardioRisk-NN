import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
import train  # noqa: E402
import predict  # noqa: E402


def test_predict_creates_csv(tmp_path):
    model_path = tmp_path / "model.pt"
    out_csv = tmp_path / "preds.csv"
    train.train_model(True, seed=0, model_path=str(model_path))
    predict.predict_saved_model(model_path, out_csv, seed=0)
    assert out_csv.exists()
    df = pd.read_csv(out_csv)
    assert df.shape == (303, 1)

    args = [
        "--model-path",
        str(model_path),
        "--output",
        str(out_csv),
        "--seed",
        "0",
    ]
    predict.main(args)
    assert out_csv.exists()
