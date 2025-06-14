from torch import nn


def build_mlp(input_dim: int) -> nn.Module:
    """Return a small two-layer MLP."""
    return nn.Sequential(
        nn.Linear(input_dim, 32),
        nn.ReLU(),
        nn.Linear(32, 16),
        nn.ReLU(),
        nn.Linear(16, 1),
    )
