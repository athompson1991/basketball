from sklearn.naive_bayes import GaussianNB

class NaiveBayes:
    def __init__(self):
        self.naiveBayes = GaussianNB()

    def fit(self, X, y):
        self.naiveBayes.fit(X, y)

    def predict(self, X):
        return self.naiveBayes.predict(X)