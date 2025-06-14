import time
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
import train  # noqa: E402
import calibrate  # noqa: E402


def test_calibration_runtime(tmp_path):
    start = time.time()
    model_path = tmp_path / "model.pt"
    plot_path = tmp_path / "cal.png"

    with pytest.raises(SystemExit):
        train.main(["--fast", "--seed", "0", "--model-path", str(model_path)])
    assert model_path.exists()

    calibrate.main(["--model-path", str(model_path), "--plot-path", str(plot_path)])
    assert plot_path.exists()
    assert time.time() - start < 10
