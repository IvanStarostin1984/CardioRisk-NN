"""Train an MLP on the heart disease dataset."""

import argparse
import sys
from sklearn.metrics import roc_auc_score
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, random_split

from data_utils import load_data
from model import build_mlp


def _load_split(seed: int):
    """Return standardised train/test tensors."""
    x_train, x_test, y_train, y_test = load_data(random_state=seed)
    mean = x_train.mean(0, keepdim=True)
    std = x_train.std(0, unbiased=False, keepdim=True)
    x_train = (x_train - mean) / (std + 1e-6)
    x_test = (x_test - mean) / (std + 1e-6)
    return x_train, x_test, y_train, y_test


def _train_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
):
    """Train one epoch."""
    model.train()
    for features, target in loader:
        optimizer.zero_grad()
        out = model(features)
        loss = criterion(out, target)
        loss.backward()
        optimizer.step()


def _init_model(n_features: int, lr: float = 0.001):
    """Return model, criterion and optimizer."""
    model = build_mlp(n_features)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    return model, criterion, optimizer


def _make_loader(
    x: torch.Tensor,
    y: torch.Tensor,
    shuffle: bool = True,
) -> DataLoader:
    """Return a DataLoader for the given tensors."""
    dataset = TensorDataset(x, y.unsqueeze(1))
    return DataLoader(dataset, batch_size=64, shuffle=shuffle)


def _split_train_valid(
    x_train: torch.Tensor, y_train: torch.Tensor, seed: int
) -> tuple[DataLoader, DataLoader]:
    """Return loaders for the train/validation split."""
    val_size = max(1, len(x_train) // 5)
    train_size = len(x_train) - val_size
    gen = torch.Generator().manual_seed(seed)

    dataset = TensorDataset(x_train, y_train.unsqueeze(1))
    train_ds, val_ds = random_split(
        dataset,
        [train_size, val_size],
        generator=gen,
    )

    return (
        DataLoader(train_ds, batch_size=64, shuffle=True),
        DataLoader(val_ds, batch_size=64, shuffle=False),
    )


def _calc_auc(model: nn.Module, loader: DataLoader) -> float:
    """Return ROC-AUC for the model on the loader."""
    model.eval()
    preds = []
    targets = []
    with torch.no_grad():
        for features, target in loader:
            preds.append(model(features).squeeze())
            targets.append(target.squeeze())
    preds = torch.cat(preds).numpy()
    targets = torch.cat(targets).numpy()
    return roc_auc_score(targets, preds)


def train_model(
    fast: bool,
    seed: int,
    model_path: str | None = "model.pt",
    patience: int = 5,
) -> float:
    """Train the MLP and return ROC-AUC."""
    torch.manual_seed(seed)
    x_train, x_test, y_train, y_test = _load_split(seed)
    lr = 0.1 if fast else 0.001
    model, criterion, optimizer = _init_model(x_train.shape[1], lr)
    train_loader, val_loader = _split_train_valid(x_train, y_train, seed)
    test_loader = _make_loader(x_test, y_test, shuffle=False)
    epochs = 20 if fast else 200
    best_auc = 0.0
    best_state: dict[str, torch.Tensor] | None = None
    stale = 0
    for epoch in range(epochs):
        _train_epoch(model, train_loader, criterion, optimizer)
        val_auc = _calc_auc(model, val_loader)
        if val_auc > best_auc:
            best_auc = val_auc
            stale = 0
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
        else:
            stale += 1
        if stale >= patience:
            print(f"Early stopping at epoch {epoch + 1}")
            break

    if best_state:
        model.load_state_dict(best_state)

    if model_path:
        torch.save(model, model_path)

    auc = _calc_auc(model, test_loader)
    return auc


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model-path", default="model.pt")
    parser.add_argument("--patience", type=int, default=5)
    parsed = parser.parse_args(args)
    auc = train_model(
        parsed.fast, parsed.seed, parsed.model_path, patience=parsed.patience
    )
    print(f"ROC-AUC: {auc:.3f}")
    if auc < 0.90:
        sys.exit(1)


if __name__ == "__main__":
    main()
