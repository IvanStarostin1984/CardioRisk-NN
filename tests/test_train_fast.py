import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import train  # noqa: E402


def test_fast_training_runs_under_20s():
    start = time.time()
    train.main(["--fast"])
    assert time.time() - start < 20
