from sklearn.svm import SVC


class SVM:
    def __init__(self):
        self.svc = SVC(kernel='rbf')

    def fit(self, X, y):
        self.svc.fit(X, y)

    def predict(self, X):
        return self.svc.predict(X)
