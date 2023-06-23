"""
This files contains convenience function for training, optimizing, testing and visualizing Tensorflow models.
"""

import os
from typing import Tuple, Callable, Optional
import numpy as np
import pandas as pd
from keras import Model, callbacks
import keras_tuner as kt
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def load_data(folder_path) -> pd.DataFrame:
    """Creates a dataframe from all files in the data/auto directory."""

    dfs = [
        pd.read_parquet(os.path.join(folder_path, file_name))
        for file_name 
        in os.listdir(folder_path)
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

def train_model(model: Model, features_train: np.ndarray, labels_train: Optional[np.ndarray]=None, num_epochs: int=100):
    """Trains the model given the training data."""

    if labels_train is None:
        model.fit(features_train, epochs=num_epochs, validation_split=0.2)
    else:
        model.fit(features_train, labels_train, epochs=num_epochs, validation_split=0.2)


def tune_model(fn_build: Callable[[kt.HyperParameters], Model], features_train: np.ndarray, labels_train: np.ndarray) -> Model:
    """Returns the best model (untrained) for the provided model builder function."""

    tuner = kt.BayesianOptimization(
        fn_build,
        max_trails=20,
    )
    if tuner.hypermodel is None: 
        raise RuntimeError("Tuner definition failed.")

    stop_early = callbacks.EarlyStopping(monitor='val_loss', patience=5)
    tuner.search(features_train, labels_train, epochs=50, validation_split=0.2, callbacks=[stop_early])

    best_hp = tuner.get_best_hyperparameters(num_trials=1)[0]

    best_model = tuner.hypermodel.build(best_hp)
    return best_model


def test_model(model: Model, features_test: np.ndarray, label_test: np.ndarray):
    """Evaluates the model on the test dataset."""

    preds = model.predict(features_test)
    
    # TODO: Implement
    pass

def visualize_model(encoder: Model, features: np.ndarray):
    """
    Uses t-SNE to visualize the trained VAE.

    Args:
        encoder (Model): The encoder of an VAE
        features (np.ndarray): Input (sensor) data
    """

    _, _, samples = encoder.predict(features)

    sne = TSNE(n_components=2, learning_rate="auto", init="random")
    x_embed = sne.fit_transform(samples)

    plt.figure(figsize=(600, 400))
    plt.plot(x_embed[0], x_embed[1])
    plt.show()

if __name__ == "__main__":
    pass
