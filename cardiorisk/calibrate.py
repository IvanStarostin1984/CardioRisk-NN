"""Calibration helper for CardioRisk-NN."""

import argparse
from pathlib import Path

import torch
from sklearn.calibration import CalibrationDisplay
from sklearn.metrics import brier_score_loss
import matplotlib.pyplot as plt

from .evaluate import load_data


def _save_reliability_plot(
    labels: list[float], probs: list[float], plot_path: Path
) -> None:
    """Save calibration curve."""
    disp = CalibrationDisplay.from_predictions(labels, probs, n_bins=10)
    disp.ax_.set_title("Reliability curve")
    disp.figure_.tight_layout()
    disp.figure_.savefig(plot_path)
    plt.close(disp.figure_)


def calibrate_model(model_path: Path, plot_path: Path) -> float:
    """Compute Brier score and save reliability plot."""
    loader = load_data()
    model = torch.load(model_path, map_location="cpu")
    model.eval()

    probs, labels = [], []
    with torch.no_grad():
        for features, target in loader:
            logits = model(features).squeeze()
            prob = torch.sigmoid(logits)
            probs.extend(prob.tolist())
            labels.extend(target.tolist())

    brier = brier_score_loss(labels, probs)
    _save_reliability_plot(labels, probs, plot_path)
    print(f"Brier score: {brier:.3f}")
    return brier


def main(args=None) -> None:
    parser = argparse.ArgumentParser(description="Model calibration metrics")
    parser.add_argument("--model-path", default="model.pt", type=Path)
    parser.add_argument("--plot-path", default="calibration.png", type=Path)
    parsed = parser.parse_args(args)
    calibrate_model(parsed.model_path, parsed.plot_path)


if __name__ == "__main__":
    main()
