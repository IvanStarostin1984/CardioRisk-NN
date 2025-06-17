"""Evaluation helpers for CardioRisk-NN."""

import argparse
from pathlib import Path

import torch
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader, TensorDataset

from train import train_model, _load_split
from data_utils import load_data as _load_tensors


def evaluate(seed: int = 0) -> float:
    """Run a short training to compute ROC-AUC."""
    return train_model(fast=True, seed=seed, model_path=None)


def load_data(batch_size: int = 64) -> DataLoader:
    """Return full dataset loader via :func:`data_utils.load_data`."""
    x_train, x_test, y_train, y_test = _load_tensors()
    features = torch.cat([x_train, x_test])
    targets = torch.cat([y_train, y_test])
    dataset = TensorDataset(features, targets.unsqueeze(1))
    return DataLoader(dataset, batch_size=batch_size)


def evaluate_saved_model(model_path: Path, seed: int = 0) -> float:
    """Load a saved model and print ROC-AUC."""
    _, x_test, _, y_test = _load_split(seed)
    model = torch.load(model_path, map_location="cpu")
    model.eval()

    with torch.no_grad():
        preds = model(x_test).squeeze()

    auc = roc_auc_score(y_test.numpy(), preds.numpy())
    print(f"ROC-AUC: {auc:.3f}")
    return auc


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a saved model")
    parser.add_argument(
        "--model-path", default="model.pt", type=Path, help="Path to .pt file"
    )
    args = parser.parse_args()
    evaluate_saved_model(args.model_path)


if __name__ == "__main__":
    main()
