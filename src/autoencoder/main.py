"""
This files executes the actual training, optimization and testing the LSTM.
"""

from functools import partial
from .model_definition import build_vae
from utils import (load_data, split_data, tune_model, train_model,
    test_model, visualize_model)

def main():
    df = load_data("data/auto")
    data_train, data_test = split_data(df=df, test_ratio=0.8)

    model = tune_model(partial(build_vae, 100), *data_train)
    train_model(model, *data_train)
    test_model(model, *data_test)
    visualize_model(model)

if __name__ == "__main__":
    main()
