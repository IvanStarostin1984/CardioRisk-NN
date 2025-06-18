"""Generate predictions from a saved model."""

import argparse
from pathlib import Path

import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset

from train import _load_split


def predict_saved_model(
    model_path: Path,
    output_path: Path,
    seed: int = 0,
) -> None:
    """Save model probabilities for the full dataset to ``output_path``."""
    x_train, x_test, _, _ = _load_split(seed)
    features = torch.cat([x_train, x_test])
    dataset = TensorDataset(features)
    loader = DataLoader(dataset, batch_size=64, shuffle=False)
    model = torch.load(model_path, map_location="cpu")
    model.eval()

    preds = []
    with torch.no_grad():
        for (batch,) in loader:
            logits = model(batch).squeeze()
            preds.append(torch.sigmoid(logits))

    df = pd.DataFrame({"prediction": torch.cat(preds).numpy()})
    df.to_csv(output_path, index=False)
    print(f"Saved predictions to {output_path}")


def main(args=None) -> None:
    parser = argparse.ArgumentParser(description="Generate CSV predictions")
    parser.add_argument("--model-path", default="model.pt", type=Path)
    parser.add_argument("--output", default="predictions.csv", type=Path)
    parser.add_argument("--seed", type=int, default=0)
    parsed = parser.parse_args(args)
    predict_saved_model(parsed.model_path, parsed.output, seed=parsed.seed)


if __name__ == "__main__":
    main()
