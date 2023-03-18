"""
This files contains functions related to the Variational Autoencoder.
"""

import os
from typing import Tuple
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras import Model, layers

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
    
def build_model() -> Model:
    """Defines the architecture of the VAE and returns the compiled model."""

    # TODO: Implement
    return Model()

def train_model(model: Model, features_train: np.ndarray, labels_train: np.ndarray):
    """Trains the model given the training data."""

    # TODO: Implement
    pass

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

    model = build_model()
    train_model(model, *data_train)
    test_model(model, *data_test)
    visualize_model(model)


if __name__ == "__main__":
    main()
