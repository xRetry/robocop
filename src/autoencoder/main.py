"""
This files contains functions related to the Variational Autoencoder.
"""

import os
from typing import Tuple, Callable
import numpy as np
import pandas as pd
from keras import Model, callbacks
from .model_definition import build_model
import keras_tuner as kt

def load_data() -> pd.DataFrame:
    """Creates a dataframe from all files in the data/static directory."""

    data_path = "../../data/static"
    dfs = [
        pd.read_parquet(os.path.join(data_path, file_name))
        for file_name 
        in os.listdir(data_path)
    ]

    return pd.concat(dfs)

def split_data(df: pd.DataFrame, test_ratio: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Splits the input dataframe into training and test data based on the provided ratio.

    Args:
        df (pd.DataFrame): The Pandas dataframe to be split
        test_ratio (float): The proportion of samples in the test split (between 0 and 1)

    Returns:
        Tuple[np.ndarray, np.ndarray]: The np.ndarrays contain the 2-dimensional train and test data
    """

    df_test = df.sample(frac=test_ratio)
    df_train = df.drop(df_test.index)
    return df_train.values, df_test.values

def train_model(model: Model, features_train: np.ndarray, labels_train: np.ndarray, num_epochs: int):
    """Trains the model given the training data."""

    model.fit(features_train, labels_train, epochs=num_epochs, validation_split=0.2)
    pass

def tune_model(fn_build: Callable[[kt.HyperParameters], Model], features_train: np.ndarray, labels_train: np.ndarray) -> Model:
    """Returns the best model (untrained) for the provided model builder function."""

    tuner = kt.BayesianOptimization(
        fn_build,
        max_trails=20,
    )

    stop_early = callbacks.EarlyStopping(monitor='val_loss', patience=5)
    tuner.search(features_train, labels_train, epochs=50, validation_split=0.2, callbacks=[stop_early])

    best_hp = tuner.get_best_hyperparameters(num_trials=1)[0]

    best_model = tuner.hypermodel.build(best_hp)
    return best_model


def test_model(model: Model, features_test: np.ndarray, label_test: np.ndarray):
    """Evaluates the model on the test dataset."""

    # TODO: Implement
    pass

def visualize_model(model: Model):
    """Uses t-SNE to visualize the trained VAE."""

    # TODO: Implement
    pass

def main():
    df = load_data()
    data_train, data_test = split_data(df=df, test_ratio=0.8)

    model = tune_model(build_model, *data_train)
    train_model(model, *data_train)
    test_model(model, *data_test)
    visualize_model(model)


if __name__ == "__main__":
    main()
