"""Train an MLP on the heart disease dataset."""

import argparse
import sys
from sklearn.metrics import roc_auc_score
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from data_utils import load_data
from model import build_mlp


def _load_split(seed: int):
    """Return standardised train/test tensors."""
    x_train, x_test, y_train, y_test = load_data(random_state=seed)
    mean = x_train.mean(0, keepdim=True)
    std = x_train.std(0, unbiased=False, keepdim=True)
    x_train = (x_train - mean) / (std + 1e-6)
    x_test = (x_test - mean) / (std + 1e-6)
    return x_train, x_test, y_train, y_test


def train_model(
    fast: bool,
    seed: int,
    model_path: str | None = "model.pt",
) -> float:
    """Train the MLP and return ROC-AUC."""
    torch.manual_seed(seed)
    x_train, x_test, y_train, y_test = _load_split(seed)
    model = build_mlp(x_train.shape[1])
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loader = DataLoader(
        TensorDataset(x_train, y_train.unsqueeze(1)),
        batch_size=64,
        shuffle=True,
    )
    epochs = 3 if fast else 200
    for _ in range(epochs):
        for features, target in loader:
            optimizer.zero_grad()
            out = model(features)
            loss = criterion(out, target)
            loss.backward()
            optimizer.step()

    if model_path:
        torch.save(model, model_path)

    model.eval()
    with torch.no_grad():
        preds = model(x_test).squeeze()
    return roc_auc_score(y_test.numpy(), preds.numpy())


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model-path", default="model.pt")
    parsed = parser.parse_args(args)
    auc = train_model(parsed.fast, parsed.seed, parsed.model_path)
    print(f"ROC-AUC: {auc:.3f}")
    if auc < 0.90:
        sys.exit(1)


if __name__ == "__main__":
    main()
