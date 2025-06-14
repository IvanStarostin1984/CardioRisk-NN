import time
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
import train  # noqa: E402


def test_fast_training_runs_under_20s():
    start = time.time()
    with pytest.raises(SystemExit) as exc:
        train.main(["--fast", "--seed", "0"])
    assert exc.value.code == 1
    assert time.time() - start < 20
