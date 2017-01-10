import unittest
import unittest.mock

import hpolib
import hpolib.config
import hpolib.util.data_manager

import numpy as np


class TestDataManager(unittest.TestCase):

    @unittest.mock.patch.object(hpolib.util.data_manager.MNISTData,
                                '_MNISTData__load_data')
    @unittest.mock.patch('os.path.join')
    @unittest.mock.patch('os.path.isdir')
    def test_loadMNIST(self, isdir_mock, join_mock, load_mock):
        # Set up mock effects
        load_mock.side_effect = [np.random.randn(60000, 28*28),
                                 np.random.randn(60000, 1),
                                 np.random.randn(10000, 28*28),
                                 np.random.randn(10000, 1)]
        join_mock.side_effect = ["tmp/MNIST"]
        isdir_mock.return_vaue = True

        # Load Data
        dm = hpolib.util.data_manager.MNISTData()
        X_train, y_train, X_val, y_val, X_test, y_test = dm.load()

        # Assert array shape
        self.assertEqual(X_train.shape[0], 50000)
        self.assertEqual(X_train.shape[1], 28*28)
        self.assertEqual(X_val.shape[0], 10000)
        self.assertEqual(X_val.shape[1], 28*28)
        self.assertEqual(X_test.shape[0], 10000)
        self.assertEqual(X_test.shape[1], 28*28)

        self.assertEqual(y_train.shape[0], 50000)
        self.assertEqual(y_train.shape[1], 1)
        self.assertEqual(y_val.shape[0], 10000)
        self.assertEqual(y_val.shape[1], 1)
        self.assertEqual(y_test.shape[0], 10000)
        self.assertEqual(y_test.shape[1], 1)

        # Assert mocks
        self.assertEqual(join_mock.call_args[0][0], hpolib._config.data_dir)
        self.assertEqual(join_mock.call_args[0][1], "MNIST")

    def test_load_openml(self):

        # Load Data
        dm = hpolib.util.data_manager.OpenMLData(openml_task_id=75191)
        X_train, y_train, X_val, y_val, X_test, y_test = dm.load()

        # Assert array shape
        n = 98528
        n_test = int(n * 0.33)
        n_train_valid = n - n_test

        n_train = int(n_train_valid * (1 - 0.33))
        n_valid = n_train_valid - n_train
        self.assertEqual(X_train.shape[0], n_train)
        self.assertEqual(X_train.shape[1], 100)
        self.assertEqual(X_val.shape[0], n_valid)
        self.assertEqual(X_val.shape[1], 100)
        self.assertEqual(X_test.shape[0], n_test)
        self.assertEqual(X_test.shape[1], 100)

        self.assertEqual(y_train.shape[0], n_train)
        self.assertEqual(y_val.shape[0], n_valid)
        self.assertEqual(y_test.shape[0], n_test)

