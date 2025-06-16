import time
from pathlib import Path

from cardiorisk import train_tf  # noqa: E402


def test_tf_training_stops_early():
    start = time.time()
    model_file = Path("model_tf.h5")
    if model_file.exists():
        model_file.unlink()
    auc, epochs = train_tf.train_model(
        False, seed=0, model_path="model_tf.h5", patience=1
    )
    assert epochs < 200
    assert time.time() - start < 20
    assert model_file.exists()
    model_file.unlink()
