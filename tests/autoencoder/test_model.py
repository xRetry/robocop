import unittest
import numpy as np
import keras
import keras_tuner as kt
from src.autoencoder.model_definition import build_vae
from src.utils import train_model

class TestModel(unittest.TestCase):
    def test_build_model(self):
        vae = build_vae(100, kt.HyperParameters())
        vae.fit(np.random.rand(1, 100), epochs=1, batch_size=1, verbose=0)

    def test_vae(self):
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train = x_train.reshape((-1, 28*28)).astype("float32") / 255
        x_test = x_test.reshape((-1, 28*28)).astype("float32") / 255

        vae = build_vae(x_train.shape[1], kt.HyperParameters())
        train_model(vae, x_train, num_epochs=2)

if __name__ == "__main__":
    unittest.main()
