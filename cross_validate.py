"""K-fold validation helper for CardioRisk-NN."""

from __future__ import annotations

import argparse
from typing import Tuple

import torch
from sklearn.model_selection import KFold

import train
import train_tf
from data_utils import load_data as _load_tensors


def _load_dataset(seed: int) -> Tuple[torch.Tensor, torch.Tensor]:
    """Return the full dataset as tensors."""
    x_train, x_test, y_train, y_test = _load_tensors(random_state=seed)
    return torch.cat([x_train, x_test]), torch.cat([y_train, y_test])


def _train_fold_torch(
    x_tr: torch.Tensor,
    y_tr: torch.Tensor,
    x_va: torch.Tensor,
    y_va: torch.Tensor,
    fast: bool,
    seed: int,
) -> float:
    """Train one fold using PyTorch."""
    torch.manual_seed(seed)
    mean = x_tr.mean(0, keepdim=True)
    std = x_tr.std(0, unbiased=False, keepdim=True)
    x_tr = (x_tr - mean) / (std + 1e-6)
    x_va = (x_va - mean) / (std + 1e-6)
    lr = 0.1 if fast else 0.001
    model, crit, opt = train._init_model(x_tr.shape[1], lr)
    tr_loader, val_loader = train._split_train_valid(x_tr, y_tr, seed)
    va_loader = train._make_loader(x_va, y_va, shuffle=False)
    epochs = 20 if fast else 200
    best, stale = 0.0, 0
    for _ in range(epochs):
        train._train_epoch(model, tr_loader, crit, opt)
        val_auc = train._calc_auc(model, val_loader)
        if val_auc > best:
            best, stale = val_auc, 0
        else:
            stale += 1
        if stale >= 5:
            break
    return float(train._calc_auc(model, va_loader))


def _train_fold_tf(
    x_tr: torch.Tensor,
    y_tr: torch.Tensor,
    x_va: torch.Tensor,
    y_va: torch.Tensor,
    fast: bool,
    seed: int,
) -> float:
    """Train one fold using TensorFlow."""
    import numpy as np
    import tensorflow as tf
    from sklearn.metrics import roc_auc_score

    np.random.seed(seed)
    tf.random.set_seed(seed)
    x_tr = x_tr.numpy()
    y_tr = y_tr.numpy()
    x_va = x_va.numpy()
    y_va = y_va.numpy()
    mean = x_tr.mean(axis=0, keepdims=True)
    std = x_tr.std(axis=0, keepdims=True)
    x_tr = (x_tr - mean) / (std + 1e-6)
    x_va = (x_va - mean) / (std + 1e-6)
    model = train_tf._build_model(x_tr.shape[1])
    epochs = 12 if fast else 200
    cb = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=5, restore_best_weights=True
    )
    model.fit(
        x_tr,
        y_tr,
        epochs=epochs,
        batch_size=64,
        verbose=0,
        callbacks=[cb],
        validation_split=0.2,
    )
    preds = model.predict(x_va, verbose=0).squeeze()
    auc = roc_auc_score(y_va, preds)
    return float(auc)


def cross_validate(
    folds: int = 5,
    backend: str = "torch",
    fast: bool = True,
    seed: int = 0,
) -> float:
    """Return mean ROC-AUC over a KFold split."""
    x, y = _load_dataset(seed)
    kf = KFold(n_splits=folds, shuffle=True, random_state=seed)
    aucs: list[float] = []
    for i, (tr, va) in enumerate(kf.split(x)):
        if backend == "torch":
            auc = _train_fold_torch(x[tr], y[tr], x[va], y[va], fast, seed + i)
        elif backend == "tf":
            auc = _train_fold_tf(x[tr], y[tr], x[va], y[va], fast, seed + i)
        else:
            raise ValueError("backend must be 'torch' or 'tf'")
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--fast", dest="fast", action="store_true")
    group.add_argument("--no-fast", dest="fast", action="store_false")
    parser.set_defaults(fast=True)
    parser.add_argument("--seed", type=int, default=0)
    parsed = parser.parse_args(args)
    mean_auc = cross_validate(
        parsed.folds, backend=parsed.backend, fast=parsed.fast, seed=parsed.seed
    )
    print(f"Mean ROC-AUC: {mean_auc:.3f}")


if __name__ == "__main__":
    main()
