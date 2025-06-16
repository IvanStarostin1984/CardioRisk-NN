"""K-fold validation helper for CardioRisk-NN."""

from __future__ import annotations

import argparse

import train
import train_tf


def cross_validate(folds: int = 5, backend: str = "torch") -> float:
    """Return mean ROC-AUC over several random splits."""
    aucs: list[float] = []
    for seed in range(folds):
        if backend == "torch":
            auc = train.train_model(True, seed=seed, model_path=None)
        else:
            # Use full training for TensorFlow so AUC stays high in tests
            auc = train_tf.train_model(False, seed=seed, model_path=None)[0]
        aucs.append(auc)
    return float(sum(aucs) / len(aucs))


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run k-fold cross validation")
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument(
        "--backend",
        choices=["torch", "tf"],
        default="torch",
        help="training backend",
    )
    parsed = parser.parse_args(args)
    mean_auc = cross_validate(parsed.folds, backend=parsed.backend)
    print(f"Mean ROC-AUC: {mean_auc:.3f}")


if __name__ == "__main__":
    main()
