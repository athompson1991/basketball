from nose.tools import assert_true, assert_equal
from numpy.testing import assert_array_almost_equal, assert_array_equal
from core.predictors.odds import OddsClassifier
import numpy as np
import pandas as pd


class TestOddsClassifier:
    def setup(self):
        self.classifier = OddsClassifier()
        self.X_1d = np.array([200, -214, -300, -1000, 160])
        self.X_2d = np.array([
            [200, -220],
            [-214, 182],
            [-300, 290],
            [-1000, 675],
            [160, -185]
        ])
        self.y = np.array([0, 0, 0, 1, 1])
        p1 = [0.33333333, 0.68152866, 0.75, 0.90909091, 0.38461538]
        p2 = [0.32291667, 0.66345937, 0.74679487, 0.89002933, 0.36774629]
        self.X_1p = np.array(p1)
        self.X_2p = np.array(p2)

    def test_fit_1d(self):
        self.classifier.fit(self.X_1d, self.y)
        assert_array_equal(self.classifier.X, self.X_1d)
        assert_array_equal(self.classifier.y, self.y)
        assert_array_almost_equal(self.classifier.X_prob, self.X_1p, decimal=4)

    def test_fit_2d(self):
        self.classifier.fit(self.X_2d, self.y)
        assert_array_equal(self.classifier.X, self.X_2d)
        assert_array_equal(self.classifier.y, self.y)
        assert_array_almost_equal(self.classifier.X_prob, self.X_2p, decimal=4)

    def test_predict_1d(self):
        y_hat = self.classifier.predict(self.X_1d)
        assert_array_equal(y_hat, np.array([0, 1, 1, 1, 0]))

    def test_predict_2d(self):
        y_hat = self.classifier.predict(self.X_2d)
        assert_array_equal(y_hat, np.array([0, 1, 1, 1, 0]))

    def test_predict_proba_1d(self):
        p_hat = self.classifier.predict_proba(self.X_1d)
        assert_array_almost_equal(p_hat, self.X_1p)

    def test_predict_proba_1d(self):
        p_hat = self.classifier.predict_proba(self.X_2d)
        assert_array_almost_equal(p_hat, self.X_2p)

    def test_accuracy(self):
        self.classifier.fit(self.X_1d, self.y)
        accuracy = self.classifier.accuracy()
        assert_equal(accuracy, 2/5)

    def test_bootstrap_accuracy(self):
        self.classifier.fit(self.X_2d, self.y)
        acc = self.classifier.bootstrap_accuracy()
        self.classifier.fit(self.X_1d, self.y)
        acc = self.classifier.bootstrap_accuracy()


    def test_pandas(self):
        df = pd.DataFrame(self.X_2d)
        assert_array_almost_equal(self.classifier.predict_proba(df), self.X_2p)
        self.classifier.fit(df, self.y)
        assert_true(isinstance(self.classifier.X, np.ndarray))
        assert_true(isinstance(self.classifier.y, np.ndarray))

        df = pd.DataFrame(self.X_1d)
        assert_array_almost_equal(self.classifier.predict_proba(df), self.X_1p)
        self.classifier.fit(df, self.y)
        assert_array_equal(self.classifier.X, self.X_1d)
        assert_true(isinstance(self.classifier.X, np.ndarray))
        assert_true(isinstance(self.classifier.y, np.ndarray))

        y = pd.DataFrame(self.y)
        self.classifier.fit(df, y)
        assert_array_equal(self.classifier.y, self.y)
        assert_true(isinstance(self.classifier.y, np.ndarray))