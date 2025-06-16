"""Logistic regression baseline for CardioRisk-NN."""

from __future__ import annotations

import argparse
import sys
from typing import Tuple

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

from data_utils import load_data


def _load_scaled(seed: int) -> Tuple:
    """Return scaled train/test numpy arrays."""
    x_train, x_test, y_train, y_test = load_data(random_state=seed)
    scaler = StandardScaler().fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)
    return x_train, x_test, y_train.numpy(), y_test.numpy(), scaler


def train_model(seed: int, model_path: str | None = "baseline.pkl") -> float:
    """Train logistic regression and return ROC-AUC."""
    x_train, x_test, y_train, y_test, scaler = _load_scaled(seed)
    model = LogisticRegression(max_iter=1000)
    model.fit(x_train, y_train)
    if model_path:
        joblib.dump((scaler, model), model_path)
    preds = model.predict_proba(x_test)[:, 1]
    return float(roc_auc_score(y_test, preds))


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Train logistic regression")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model-path", default="baseline.pkl")
    parsed = parser.parse_args(args)
    auc = train_model(parsed.seed, parsed.model_path)
    print(f"ROC-AUC: {auc:.3f}")
    if auc < 0.84:
        sys.exit(1)


if __name__ == "__main__":
    main()
