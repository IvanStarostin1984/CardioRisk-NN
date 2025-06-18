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
    """Return the entire dataset as feature and target tensors."""
    x_tr, x_te, y_tr, y_te = _load_tensors(random_state=seed)
    x = torch.cat([x_tr, x_te])
    y = torch.cat([y_tr, y_te])
    return x, y


def _run_epochs(
    model: torch.nn.Module,
    crit: torch.nn.Module,
    opt: torch.optim.Optimizer,
    tr_loader: torch.utils.data.DataLoader,
    val_loader: torch.utils.data.DataLoader,
    epochs: int,
) -> dict[str, torch.Tensor] | None:
    """Return best state dict from early stopped training."""
    best_state, best, stale = None, 0.0, 0
    for _ in range(epochs):
        train._train_epoch(model, tr_loader, crit, opt)
        val_auc = train._calc_auc(model, val_loader)
        if val_auc > best:
            best, stale = val_auc, 0
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            stale += 1
        if stale >= 5:
            break
    return best_state


def _prep_fold(
    x_tr: torch.Tensor,
    y_tr: torch.Tensor,
    x_va: torch.Tensor,
    y_va: torch.Tensor,
    fast: bool,
    seed: int,
) -> tuple[
    torch.nn.Module,
    torch.nn.Module,
    torch.optim.Optimizer,
    torch.utils.data.DataLoader,
    torch.utils.data.DataLoader,
    torch.utils.data.DataLoader,
]:
    """Return model and loaders for one fold."""
    mean = x_tr.mean(0, keepdim=True)
    std = x_tr.std(0, unbiased=False, keepdim=True)
    x_tr = (x_tr - mean) / (std + 1e-6)
    x_va = (x_va - mean) / (std + 1e-6)
    lr = 0.1 if fast else 0.001
    model, crit, opt = train._init_model(x_tr.shape[1], lr)
    tr_loader, val_loader = train._split_train_valid(x_tr, y_tr, seed)
    va_loader = train._make_loader(x_va, y_va, shuffle=False)
    return model, crit, opt, tr_loader, val_loader, va_loader


def _train_fold_torch(
    x_tr: torch.Tensor,
    y_tr: torch.Tensor,
    x_va: torch.Tensor,
    y_va: torch.Tensor,
    fast: bool,
    seed: int,
) -> float:
    """Return ROC-AUC for one fold using the PyTorch trainer."""
    torch.manual_seed(seed)
    model, crit, opt, tr_loader, val_loader, va_loader = _prep_fold(
        x_tr, y_tr, x_va, y_va, fast, seed
    )
    epochs = 20 if fast else 200
    best_state = _run_epochs(model, crit, opt, tr_loader, val_loader, epochs)
    if best_state:
        model.load_state_dict(best_state)
    return float(train._calc_auc(model, va_loader))


def _setup_tf(seed: int):
    """Return tensorflow module with seeds set."""
    import numpy as np
    import tensorflow as tf

    np.random.seed(seed)
    tf.random.set_seed(seed)
    tf.keras.backend.clear_session()
    tf.keras.utils.set_random_seed(seed)
    return tf


def _prep_tf_data(
    x_tr: torch.Tensor,
    y_tr: torch.Tensor,
    x_va: torch.Tensor,
    y_va: torch.Tensor,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Convert tensors to normalised numpy arrays."""
    x_tr, x_va = x_tr.numpy(), x_va.numpy()
    y_tr, y_va = y_tr.numpy(), y_va.numpy()
    mean = x_tr.mean(axis=0, keepdims=True)
    std = x_tr.std(axis=0, keepdims=True)
    x_tr = (x_tr - mean) / (std + 1e-6)
    x_va = (x_va - mean) / (std + 1e-6)
    return x_tr, y_tr, x_va, y_va


def _fit_tf_model(
    model: "tf.keras.Model", x_tr: np.ndarray, y_tr: np.ndarray, fast: bool
) -> None:
    """Train Keras model with early stopping."""
    import tensorflow as tf

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


def _train_fold_tf(
    x_tr: torch.Tensor,
    y_tr: torch.Tensor,
    x_va: torch.Tensor,
    y_va: torch.Tensor,
    fast: bool,
    seed: int,
) -> float:
    """Return ROC-AUC for one fold using the TensorFlow trainer."""
    from sklearn.metrics import roc_auc_score

    tf = _setup_tf(seed)
    x_tr, y_tr, x_va, y_va = _prep_tf_data(x_tr, y_tr, x_va, y_va)
    model = train_tf._build_model(x_tr.shape[1])
    _fit_tf_model(model, x_tr, y_tr, fast)
    preds = model.predict(x_va, verbose=0).squeeze()
    auc = roc_auc_score(y_va, preds)
    return float(auc)


def _train_fold_baseline(
    x_tr: torch.Tensor,
    y_tr: torch.Tensor,
    x_va: torch.Tensor,
    y_va: torch.Tensor,
    fast: bool,
    seed: int,
) -> float:
    """Return ROC-AUC for one fold using logistic regression."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.preprocessing import StandardScaler

    x_tr = x_tr.numpy()
    y_tr = y_tr.numpy()
    x_va = x_va.numpy()
    y_va = y_va.numpy()
    scaler = StandardScaler().fit(x_tr)
    x_tr = scaler.transform(x_tr)
    x_va = scaler.transform(x_va)
    model = LogisticRegression(max_iter=1000)
    model.fit(x_tr, y_tr)
    preds = model.predict_proba(x_va)[:, 1]
    auc = roc_auc_score(y_va, preds)
    return float(auc)


def cross_validate(
    folds: int = 5,
    backend: str = "torch",
    fast: bool = True,
    seed: int = 0,
) -> float:
    """Return mean ROC-AUC over a KFold split."""

    def _run_fold(i: int, tr, va) -> float:
        if backend == "torch":
            return _train_fold_torch(x[tr], y[tr], x[va], y[va], fast, seed + i)
        if backend == "tf":
            return _train_fold_tf(x[tr], y[tr], x[va], y[va], fast, seed + i)
        if backend == "baseline":
            return _train_fold_baseline(x[tr], y[tr], x[va], y[va], fast, seed + i)
        raise ValueError("backend must be 'torch', 'tf' or 'baseline'")

    x, y = _load_dataset(seed)
    kf = KFold(n_splits=folds, shuffle=True, random_state=seed)
    aucs = [_run_fold(i, tr, va) for i, (tr, va) in enumerate(kf.split(x))]
    return float(sum(aucs) / len(aucs))


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run k-fold cross validation")
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument(
        "--backend",
        choices=["torch", "tf", "baseline"],
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
        parsed.folds,
        backend=parsed.backend,
        fast=parsed.fast,
        seed=parsed.seed,
    )
    print(f"Mean ROC-AUC: {mean_auc:.3f}")


if __name__ == "__main__":
    main()
