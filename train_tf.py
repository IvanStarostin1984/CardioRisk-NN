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


def train_model(
    fast: bool,
    seed: int,
    model_path: str | None = "model_tf.h5",
) -> float:
    """Train the Keras MLP and return ROC-AUC."""
    np.random.seed(seed)
    tf.random.set_seed(seed)
    x_train, x_test, y_train, y_test = _load_split(seed)
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(x_train.shape[1],)),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy")
    epochs = 3 if fast else 200
    model.fit(x_train, y_train, epochs=epochs, batch_size=64, verbose=0)
    if model_path:
        model.save(model_path)
    preds = model.predict(x_test, verbose=0).squeeze()
    return roc_auc_score(y_test, preds)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model-path", default="model_tf.h5")
    parsed = parser.parse_args(args)
    auc = train_model(parsed.fast, parsed.seed, parsed.model_path)
    print(f"ROC-AUC: {auc:.3f}")
    if auc < 0.90:
        sys.exit(1)


if __name__ == "__main__":
    main()
