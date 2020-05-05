from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y

import numpy as np

from core.utils import get_implied_probability, get_implied_probability_vec


class OddsClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.X, self.y = None, None
        self.X_prob = None

    def predict_proba(self, X):
        if X.ndim == 1:
            p = get_implied_probability_vec(X)
        elif X.ndim == 2:
            p1 = get_implied_probability_vec(X[:, 0])
            p2 = 1 - get_implied_probability_vec(X[:, 1])
            p = (p1 + p2) / 2
        return p

    def fit(self, X, y):
        self.X, self.y = X.copy(), y.copy()
        self.X_prob = self.predict_proba(X)
        self.y_hat = self.predict(X)

    def predict(self, X):
        p = self.predict_proba(X)
        y_hat = np.array(np.where(p > 0.5, 1, 0))
        return y_hat

