"""Evaluation helpers for CardioRisk-NN."""

from pathlib import Path

import argparse
import pandas as pd
import torch
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader, TensorDataset

from train import train_model


def evaluate(seed: int = 0) -> float:
    """Run fast training with a fixed seed and return ROC-AUC."""
    return train_model(fast=True, seed=seed)


def _load_dataloader(batch_size: int = 64) -> DataLoader:
    """Return DataLoader for the heart dataset."""
    df = pd.read_csv(Path("data") / "heart.csv")
    X = df.drop(columns=["target"]).to_numpy(dtype="float32")
    y = df["target"].to_numpy(dtype="float32")
    dataset = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    return DataLoader(dataset, batch_size=batch_size)


def evaluate_saved(model_path: Path) -> float:
    """Evaluate a saved model file and print ROC-AUC."""
    loader = _load_dataloader()
    model = torch.load(model_path, map_location="cpu")
    model.eval()

    preds, labels = [], []
    with torch.no_grad():
        for features, target in loader:
            out = model(features).squeeze()
            preds.extend(out.tolist())
            labels.extend(target.tolist())

    auc = roc_auc_score(labels, preds)
    print(f"ROC-AUC: {auc:.3f}")
    return auc


def main(args=None) -> None:
    parser = argparse.ArgumentParser(description="Evaluate a saved model")
    parser.add_argument(
        "--model-path",
        type=Path,
        default="model.pt",
        help="Path to .pt file",
    )
    parsed = parser.parse_args(args)
    evaluate_saved(parsed.model_path)


if __name__ == "__main__":
    main()
