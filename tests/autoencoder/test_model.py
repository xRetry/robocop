import unittest
import numpy as np
from src.autoencoder.model_definition import build_vae

class TestModel(unittest.TestCase):
    # NOTE: Currently disabled
    # def test_build_model(self):
    #     model = build_model()
    #     model.fit(np.random.rand(1, 100), epochs=1, batch_size=1, verbose=0)
    pass

if __name__ == "__main__":
    unittest.main()
