import sys
from pathlib import Path

import torch

sys.path.append(str(Path(__file__).resolve().parents[1]))
import evaluate  # noqa: E402


def test_load_data_returns_loader():
    loader = evaluate.load_data(batch_size=8)
    features, target = next(iter(loader))
    assert isinstance(features, torch.Tensor)
    assert isinstance(target, torch.Tensor)
    assert features.shape[0] <= 8
    assert target.shape[1] == 1
