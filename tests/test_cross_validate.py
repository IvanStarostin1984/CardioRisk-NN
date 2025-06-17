import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
import cross_validate  # noqa: E402


def test_cross_validation_runs_quickly():
    start = time.time()
    auc1 = cross_validate.cross_validate(folds=5, fast=True, seed=0)
    auc2 = cross_validate.cross_validate(folds=5, fast=True, seed=0)
    assert isinstance(auc1, float)
    assert abs(auc1 - auc2) < 0.05
    assert auc1 >= 0.85
    assert time.time() - start < 30


def _old_train_fold_torch(x_tr, y_tr, x_va, y_va, fast, seed):
    torch = cross_validate.train.torch
    torch.manual_seed(seed)
    mean = x_tr.mean(0, keepdim=True)
    std = x_tr.std(0, unbiased=False, keepdim=True)
    x_tr = (x_tr - mean) / (std + 1e-6)
    x_va = (x_va - mean) / (std + 1e-6)
    lr = 0.1 if fast else 0.001
    model, crit, opt = cross_validate.train._init_model(x_tr.shape[1], lr)
    tr_loader, val_loader = cross_validate.train._split_train_valid(
        x_tr,
        y_tr,
        seed,
    )
    va_loader = cross_validate.train._make_loader(
        x_va,
        y_va,
        shuffle=False,
    )
    epochs = 20 if fast else 200
    best, stale = 0.0, 0
    for _ in range(epochs):
        cross_validate.train._train_epoch(model, tr_loader, crit, opt)
        val_auc = cross_validate.train._calc_auc(model, val_loader)
        if val_auc > best:
            best, stale = val_auc, 0
        else:
            stale += 1
        if stale >= 5:
            break
    return float(cross_validate.train._calc_auc(model, va_loader))


def test_auc_not_lower_than_old_impl():
    x, y = cross_validate._load_dataset(seed=0)
    kf = cross_validate.KFold(n_splits=5, shuffle=True, random_state=0)
    tr, va = next(kf.split(x))
    auc_old = _old_train_fold_torch(x[tr], y[tr], x[va], y[va], True, 0)
    auc_new = cross_validate._train_fold_torch(
        x[tr],
        y[tr],
        x[va],
        y[va],
        True,
        0,
    )
    assert auc_new >= auc_old - 1e-4
