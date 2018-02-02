import numpy as np


class Contribution:

    def __init__(self, model, labels, top_n=20):
        self.model = model
        self.labels = labels
        self.top_n = top_n
        self.weight = model.coef_.ravel()
        self.top_coefficients = None

    def explain(self):
        positive_coefficients = np.argsort(self.weight)[-self.top_n:]
        negative_coefficients = np.argsort(self.weight)[:self.top_n]
        self.top_coefficients = np.hstack([
            positive_coefficients,
            negative_coefficients,
        ])
        return self

    def range(self):
        return np.arange(2 * self.top_n)

    def height(self):
        return np.arange(1, 1 + 2 * self.top_n)

    def nominee_weights(self):
        w = self.weight[self.top_coefficients]
        return np.fabs(w)

    def nominee_names(self):
        return np.array(self.labels)[self.top_coefficients]


if __name__ == '__main__':
    pass
