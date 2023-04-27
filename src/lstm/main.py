"""
This files executes the actual training, opmization and testing the LSTM.
"""

from .model_definition import build_lstm
from utils import (load_data, split_data, tune_model, 
    train_model, test_model)

def main():
    df = load_data("data/lstm")
    data_train, data_test = split_data(df=df, test_ratio=0.8)

    model = tune_model(build_lstm, *data_train)
    train_model(model, *data_train)
    test_model(model, *data_test)

if __name__ == "__main__":
    main()
