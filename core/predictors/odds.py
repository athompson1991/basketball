import warnings

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import accuracy_score
from sklearn.utils import resample
from sklearn.utils.multiclass import unique_labels

from core.utils import get_implied_probability_vec


class OddsClassifier(BaseEstimator, ClassifierMixin):

    def predict_proba(self, X):
        if isinstance(X, pd.DataFrame):
            X = np.array(X)
        if X.ndim == 1:
            p = get_implied_probability_vec(X)
        elif X.ndim == 2 and X.shape[1] == 1:
            p = get_implied_probability_vec(X.reshape(-1))
        elif X.ndim == 2 and X.shape[1] > 1:
            if X.shape[1] > 2:
                warnings.warn("More than 2 columns in data, first "
                              "two assumed to be money line odds")
            p1 = get_implied_probability_vec(X[:, 0])
            p2 = 1 - get_implied_probability_vec(X[:, 1])
            p = (p1 + p2) / 2
        return p

    def fit(self, X, y):
        if isinstance(X, pd.DataFrame):
            if X.ndim == 2 and X.shape[1] == 1:
                X = np.array(X).reshape(-1)
            else:
                X = np.array(X)
        if isinstance(y, pd.DataFrame):
            y = y.values.reshape(-1)
        self.X, self.y = X.copy(), y.copy()
        self.X_prob = self.predict_proba(X)
        self.y_hat = self.predict(X)
        self.classes_ = unique_labels(y)

    def predict(self, X):
        p = self.predict_proba(X)
        y_hat = np.array(np.where(p > 0.5, 1, 0))
        return y_hat

    def accuracy(self):
        return accuracy_score(self.y, self.predict(self.X))

    def bootstrap_accuracy(self, n_iterations=1000):
        n_iterations = 1000
        n_size = int(len(self.X) * 0.5)
        stats = list()
        if self.X.ndim > 1:
            values = np.append(self.X, self.y.reshape(-1, 1), 1)
        elif self.X.ndim == 1:
            values = np.column_stack((self.X, self.y))
        n_col = values.shape[1]
        for i in range(n_iterations):
            sample = resample(values, n_samples=n_size)
            predictions = self.predict(sample[:, :n_col-1])
            score = accuracy_score(sample[:, n_col-1], predictions)
            if i % 100 == 0:
                print(i)
                print(sample)
                print(predictions)
                print(score)
            stats.append(score)
        return stats
