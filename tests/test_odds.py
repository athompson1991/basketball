from numpy.testing import assert_array_almost_equal, assert_array_equal

from core.predictors.odds import OddsClassifier
import numpy as np


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
        self.X_1p = np.array(
            [0.33333333, 0.68152866, 0.75, 0.90909091, 0.38461538])
        self.X_2p = np.array(
            [0.32291667, 0.66345937, 0.74679487, 0.89002933, 0.36774629])

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
        assert_array_almost_equal(y_hat, np.array([0, 1, 1, 1, 0]))

    def test_predict_2d(self):
        y_hat = self.classifier.predict(self.X_2d)
        assert_array_equal(y_hat, np.array([0, 1, 1, 1, 0]))

    def test_predict_proba_1d(self):
        p_hat = self.classifier.predict_proba(self.X_1d)
        assert_array_almost_equal(p_hat, self.X_1p)

    def test_predict_proba_1d(self):
        p_hat = self.classifier.predict_proba(self.X_2d)
        assert_array_almost_equal(p_hat, self.X_2p)
