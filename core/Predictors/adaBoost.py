from sklearn.ensemble import AdaBoostClassifier

class AdaBoost:
    def __init__(self):
        self.adaBoost = AdaBoostClassifier(n_estimators=100)

    def fit(self, X, y):
        self.adaBoost.fit(X, y)

    def predict(self, X):
        return self.adaBoost.predict(X)