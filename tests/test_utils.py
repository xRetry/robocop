import unittest
import pandas as pd
import numpy as np
from src.utils import split_data

class TestSplitData(unittest.TestCase):
    def test_positive_case(self):
        data = np.ones((10, 10))
        df = pd.DataFrame(data)
        train, test = split_data(df, 0.1)

        self.assertTrue(isinstance(train, np.ndarray))
        self.assertTrue(isinstance(test, np.ndarray))
        self.assertTupleEqual(train.shape, (9, 10))
        self.assertTupleEqual(test.shape, (1, 10))


if __name__ == "__main__":
    unittest.main()


