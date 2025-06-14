"""Train an MLP on the heart disease dataset."""

import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


def _load_split(seed: int):
    df = pd.read_csv("data/heart.csv").replace("?", np.nan).astype(float)
    df.fillna(df.mean(), inplace=True)
    y = (df.pop("target") > 0).astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        df, y, test_size=0.2, random_state=seed, stratify=y
    )
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    return x_train, x_test, y_train, y_test


def train_model(fast: bool, seed: int) -> float:
    x_train, x_test, y_train, y_test = _load_split(seed)
    epochs = 10 if fast else 200
    clf = MLPClassifier(
        hidden_layer_sizes=(32, 16),
        max_iter=epochs,
        random_state=seed,
    )
    clf.fit(x_train, y_train)
    proba = clf.predict_proba(x_test)[:, 1]
    return roc_auc_score(y_test, proba)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parsed = parser.parse_args(args)
    auc = train_model(parsed.fast, parsed.seed)
    print(f"ROC-AUC: {auc:.3f}")


if __name__ == "__main__":
    main()
