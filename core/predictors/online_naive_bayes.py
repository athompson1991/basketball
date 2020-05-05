import numpy as np


class OnlineNaiveBayes:

    def __init__(self, use_laplace_smoothing=True):
        self.laplace_smoothing = use_laplace_smoothing
        self.data_num = 0
        self.countNum = {}
        self.countFeature = {}
        self.prob_y = {}
        self.prob_X = []
        self.K = 0
        self.add_on_numer = 0
        self.add_on_denom = 0

    def fit(self, X, y):
        """
        Trains the model using given data set.
        Parameters: X is a n-by-d matrix
                    y is an n-dimensional array
        """
        n, d = np.shape(X)
        self.data_num += n

        # Update K
        new_labels = 0
        for i in range(n):
            if y[i] not in self.countNum:
                new_labels += 1
        self.K += new_labels

        # Update the number of instances for each label
        for i in range(n):
            label = y[i]
            if label not in self.countNum:
                self.countNum[label] = 0
            self.countNum[label] += 1

        # Update the probability of each label
        for i in self.countNum.keys():
            self.prob_y[i] = self.countNum[i] / self.data_num

        # Prepare to re-smoothing the P(X_i | y)
        for i in range(len(self.prob_X)):
            for key in self.prob_X[i].keys():
                self.prob_X[i][key] = self.prob_X[i][key] * (self.countFeature[key] + self.add_on_denom)

        # Update the number of features for each label
        for i in range(n):
            label = y[i]
            if label not in self.countFeature:
                self.countFeature[label] = 0
            for j in range(d):
                self.countFeature[label] += X[i, j]

        # Check if using the Laplace-smoothing
        if self.laplace_smoothing:
            self.add_on_numer = 1
            self.add_on_denom = self.K

        # Update the conditional probability of X_i given a label
        for i in range(d):
            if i == len(self.prob_X):
                self.prob_X.append({})
            for j in range(n):
                label = y[j]
                if label not in self.prob_X[i]:
                    self.prob_X[i][label] = self.add_on_numer
                self.prob_X[i][label] += X[j, i]
        for i in range(d):
            for label in self.prob_X[i].keys():
                self.prob_X[i][label] = self.prob_X[i][label] / (self.countFeature[label] + self.add_on_denom)

    def predict(self, X):
        """
        Used the classifier to predict values for each instance in X
        Parameters: X is a n-by-d matrix
        Returns: an n-dimensional array of the prediction results
        """
        n, d = np.shape(X)
        pred = np.zeros(n)
        for i in range(n):
            prob_Y = np.zeros(self.K)
            instance = X[i]

            # Get the sum of features in the instance
            sum_features = 0
            for index in range(d):
                sum_features += instance[index]

            # Get log-based values
            for j in range(self.K):
                prob_Y[j] = np.log(self.prob_y[j])
                for sum in range(1, np.int(sum_features)):
                    prob_Y[j] += np.log(sum)
                for index in range(d):
                    prob_Y[j] -= np.log(np.math.factorial(instance[index]))
                for index in range(d):
                    prob_Y[j] += instance[index] * np.log(self.prob_X[index][j])

            # Find the y value with the highest probability
            max_val = -float('inf')
            max_index = -1
            for j in range(self.K):
                if prob_Y[j] > max_val:
                    max_val = prob_Y[j]
                    max_index = j
            pred[i] = max_index

        return pred

    def predictProbs(self, X):
        """
        Used the model to predict a vector of class probabilities for each instance in X
        Parameters: X is a n-by-d matrix
        Returns: an n-by-K array of the probabilities of each predicted class
        """
        n, d = np.shape(X)
        pred = np.zeros((n, self.K))

        for i in range(n):
            prob_Y = np.zeros(self.K)
            instance = X[i]

            # Get the sum of features in the instance
            sum_features = 0
            for index in range(d):
                sum_features += instance[index]

            for j in range(self.K):
                prob_Y[j] = np.log(self.prob_y[j])
                for sum in range(1, np.int(sum_features)):
                    prob_Y[j] += np.log(sum)
                for index in range(d):
                    prob_Y[j] -= np.log(np.math.factorial(instance[index]))
                for index in range(d):
                    prob_Y[j] += instance[index] * np.log(self.prob_X[index][j])

            # Find and store the max log-based probability
            max_Prob = np.amax(prob_Y)
            # Transmit into actual probability distribution
            sum_exp = 0
            for j in range(self.K):
                sum_exp += np.exp(prob_Y[j] - max_Prob)
            for j in range(self.K):
                prob_Y[j] = np.exp(prob_Y[j] - max_Prob) / sum_exp
            pred[i] = prob_Y
        return pred