import time
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
import train_tf  # noqa: E402


def test_fast_training_tf_runs_under_20s():
    start = time.time()
    model_file = Path("model_tf.h5")
    if model_file.exists():
        model_file.unlink()
    with pytest.raises(SystemExit) as exc:
        train_tf.main(["--fast", "--seed", "0"])
    assert exc.value.code == 1
    assert time.time() - start < 20
    assert model_file.exists()
    model_file.unlink()
