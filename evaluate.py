"""Evaluation helpers for CardioRisk-NN."""

from train import train_model


def evaluate(seed: int = 0) -> float:
    """Run a short training to compute ROC-AUC."""
    return train_model(fast=True, seed=seed, model_path=None)


def main(args=None) -> None:
    auc = evaluate()
    print(f"ROC-AUC: {auc:.3f}")


import argparse
from pathlib import Path

import pandas as pd
import torch
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader, TensorDataset


def load_data(batch_size: int = 64) -> DataLoader:
    """Load the Cleveland heart dataset as a DataLoader."""
    df = pd.read_csv(Path("data") / "heart.csv")
    X = df.drop(columns=["target"]).to_numpy(dtype="float32")
    y = df["target"].to_numpy(dtype="float32")
    dataset = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    return DataLoader(dataset, batch_size=batch_size)


def evaluate_saved_model(model_path: Path) -> float:
    """Load a saved model and print ROC-AUC."""
    loader = load_data()
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a saved model")
    parser.add_argument(
        "--model-path", default="model.pt", type=Path, help="Path to .pt file"
    )
    args = parser.parse_args()
    evaluate_saved_model(args.model_path)


if __name__ == "__main__":
    main()
