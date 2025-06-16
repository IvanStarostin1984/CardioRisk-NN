import pandas as pd
from sklearn.model_selection import train_test_split
import torch


def load_data(test_size: float = 0.2, random_state: int = 42):
    """Load heart.csv and split into train/test sets."""
    df = pd.read_csv("data/heart.csv", na_values="?")
    df = df.fillna(df.mean(numeric_only=True))
    df = df.astype(float)
    df["target"] = (df["target"] > 0).astype(float)
    features = torch.tensor(
        df.drop(columns="target").values,
        dtype=torch.float32,
    )
    target = torch.tensor(df["target"].values, dtype=torch.float32)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )
    return x_train, x_test, y_train, y_test
