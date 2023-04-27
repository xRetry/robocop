"""
This file containes the model definition of the LSTM.
"""

from tensorflow import keras
from keras import Model 
from keras.layers import Dense, Input, LSTM
import keras_tuner as kt

def build_lstm(hp: kt.HyperParameters) -> Model:
    """Defines the architecture of the LSTM and returns the compiled model."""

    dim_input = 100 # TODO: Change to match actual input dim
    dim_output = 3
    num_lstm: int = hp.Int("lstm amount", min_value=1, max_value=20)
    size_lstm: int = hp.Int("lstm size", min_value=10, max_value=1000)
    num_dense: int = hp.Int("dense amount", min_value=1, max_value=20)
    size_dense: int = hp.Int("dense size", min_value=10, max_value=1000)
    lr: float = hp.Float("learning rate", min_value=1e-6, max_value=1e-2, sampling="log")

    input = x = Input(shape=dim_input)
    for _ in range(num_lstm):
        x = LSTM(size_lstm)(x)
    for _ in range(num_dense):
        x = Dense(size_dense, activation="relu")(x)
    output = Dense(dim_output, activation="sigmoid")(x)

    lstm = Model(input, output, name="lstm")
    lstm.compile(optimizer=keras.optimizers.Adam(learning_rate=lr))
    return lstm


