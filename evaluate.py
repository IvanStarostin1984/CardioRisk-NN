"""Evaluation helpers for CardioRisk-NN."""

from train import train_model


def evaluate(seed: int = 0) -> float:
    return train_model(fast=True, seed=seed)


def main(args=None):
    auc = evaluate()
    print(f"ROC-AUC: {auc:.3f}")


if __name__ == "__main__":
    main()
