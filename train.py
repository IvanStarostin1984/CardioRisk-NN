"""Train an MLP on the heart disease dataset."""

import argparse
import sys

import torch
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader, TensorDataset

from data_utils import load_data
from model import build_mlp


def parse_args() -> argparse.Namespace:
    """CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--fast", action="store_true")
    return parser.parse_args()


def train(
    model: torch.nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
) -> None:
    """Run one training epoch."""
    model.train()
    for xb, yb in loader:
        optimizer.zero_grad()
        out = model(xb).squeeze()
        loss = F.binary_cross_entropy_with_logits(out, yb)
        loss.backward()
        optimizer.step()


def main() -> None:
    args = parse_args()
    epochs = 10 if args.fast else args.epochs

    x_train, x_test, y_train, y_test = load_data()
    train_ds = TensorDataset(x_train, y_train)
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)

    model = build_mlp(x_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    for _ in range(epochs):
        train(model, train_loader, optimizer)

    model.eval()
    with torch.no_grad():
        logits = model(x_test).squeeze()
        probs = torch.sigmoid(logits).numpy()
        auc = roc_auc_score(y_test.numpy(), probs)

    print(f"Test ROC-AUC: {auc:.3f}")
    if auc < 0.90:
        sys.exit(1)
    torch.save(model.state_dict(), "model.pt")

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
