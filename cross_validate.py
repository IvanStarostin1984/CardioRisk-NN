"""K-fold validation helper for CardioRisk-NN."""

from __future__ import annotations

import argparse

import train


def cross_validate(folds: int = 5) -> float:
    """Return mean ROC-AUC over several random splits."""
    aucs = []
    for seed in range(folds):
        auc = train.train_model(True, seed=seed, model_path=None)
        aucs.append(auc)
    return float(sum(aucs) / len(aucs))


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run k-fold cross validation")
    parser.add_argument("--folds", type=int, default=5)
    parsed = parser.parse_args(args)
    mean_auc = cross_validate(parsed.folds)
    print(f"Mean ROC-AUC: {mean_auc:.3f}")


if __name__ == "__main__":
    main()
