"""Train an MLP with Keras on the heart disease dataset."""

import argparse
import sys

import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_auc_score

from data_utils import load_data


def _load_split(seed: int):
    """Return standardised train/test arrays."""
    x_train, x_test, y_train, y_test = load_data(random_state=seed)
    x_train = x_train.numpy()
    x_test = x_test.numpy()
    y_train = y_train.numpy()
    y_test = y_test.numpy()
    mean = x_train.mean(axis=0, keepdims=True)
    std = x_train.std(axis=0, keepdims=True)
    x_train = (x_train - mean) / (std + 1e-6)
    x_test = (x_test - mean) / (std + 1e-6)
    return x_train, x_test, y_train, y_test


def _build_model(input_dim: int) -> tf.keras.Model:
    """Return a compiled Keras MLP."""
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(input_dim,)),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy")
    return model


def _fit_model(
    model: tf.keras.Model,
    x_train: np.ndarray,
    y_train: np.ndarray,
    fast: bool,
    patience: int,
) -> tf.keras.callbacks.History:
    """Train the model with early stopping and return history."""
    epochs = 12 if fast else 200
    cb = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=patience, restore_best_weights=True
    )
    return model.fit(
        x_train,
        y_train,
        epochs=epochs,
        batch_size=64,
        verbose=0,
        callbacks=[cb],
        validation_split=0.2,
    )


def train_model(
    fast: bool,
    seed: int,
    model_path: str | None = "model_tf.h5",
    patience: int = 5,
) -> tuple[float, int]:
    """Train the Keras MLP and return ROC-AUC and epochs used."""
    np.random.seed(seed)
    tf.random.set_seed(seed)
    x_train, x_test, y_train, y_test = _load_split(seed)
    model = _build_model(x_train.shape[1])
    history = _fit_model(model, x_train, y_train, fast, patience)
    if model_path:
        model.save(model_path)
    preds = model.predict(x_test, verbose=0).squeeze()
    auc = roc_auc_score(y_test, preds)
    return auc, len(history.history["loss"])


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model-path", default="model_tf.h5")
    parser.add_argument("--patience", type=int, default=5)
    parsed = parser.parse_args(args)
    auc, _ = train_model(
        parsed.fast, parsed.seed, parsed.model_path, patience=parsed.patience
    )
    print(f"ROC-AUC: {auc:.3f}")
    if auc < 0.90:
        sys.exit(1)


if __name__ == "__main__":
    main()
