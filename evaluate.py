"""Evaluation helpers for CardioRisk-NN."""

from train import train_model


def evaluate(seed: int = 0) -> float:
    """Run a short training to compute ROC-AUC."""
    return train_model(fast=True, seed=seed, model_path=None)


def main(args=None) -> None:
    auc = evaluate()
    print(f"ROC-AUC: {auc:.3f}")


if __name__ == "__main__":
    main()
