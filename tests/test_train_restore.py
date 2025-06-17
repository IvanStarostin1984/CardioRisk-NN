import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import train  # noqa: E402


def _old_train_model(seed: int) -> float:
    torch = train.torch
    torch.manual_seed(seed)
    x_tr, x_te, y_tr, y_te = train._load_split(seed)
    lr = 0.1
    model, crit, opt = train._init_model(x_tr.shape[1], lr)
    tr_loader, val_loader = train._split_train_valid(x_tr, y_tr, seed)
    te_loader = train._make_loader(x_te, y_te, shuffle=False)
    best, stale = 0.0, 0
    for _ in range(20):
        train._train_epoch(model, tr_loader, crit, opt)
        val_auc = train._calc_auc(model, val_loader)
        if val_auc > best:
            best, stale = val_auc, 0
        else:
            stale += 1
        if stale >= 1:
            break
    return float(train._calc_auc(model, te_loader))


def test_train_restores_best_state():
    auc_old = _old_train_model(0)
    auc_new = train.train_model(True, seed=0, model_path=None, patience=1)
    assert auc_new >= auc_old - 1e-4
