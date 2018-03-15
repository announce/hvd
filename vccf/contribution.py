import numpy as np


class Contribution:

    def __init__(self, model, labels, patch_container, top_n=20):
        self.model = model
        self.labels = labels
        self.top_n = top_n
        self.weight = model.coef_.ravel()
        self.patch_container = patch_container
        self.top_coefficients = None

    def explain(self):
        # TODO: check out of bounds error
        positive_coefficients = np.argsort(self.weight)[-self.top_n:]
        negative_coefficients = np.argsort(self.weight)[:self.top_n]
        self.top_coefficients = np.hstack([
            positive_coefficients,
            negative_coefficients,
        ])
        return self

    def range(self):
        return np.arange(2 * self.top_n)

    # def height(self):
    #     return np.arange(1, 1 + 2 * self.top_n)

    def nominee_weights(self):
        w = self.weight[self.top_coefficients]
        return np.fabs(w)

    def nominee_names(self):
        nominees = np.array(self.labels)[self.top_coefficients]
        humanized_labels = [
            self.humanize(l) for l in nominees
        ] if self.patch_container.mode is self.patch_container.Mode.LINE_TYPE_SENSITIVE else nominees
        return humanized_labels

    def humanize(self, label):
        return label.replace(
            self.patch_container.UUID_ADDED,
            'ADDED',
        ).replace(
            self.patch_container.UUID_REMOVED,
            'REMOVED',
        ).replace(
            self.patch_container.UUID_MIXED,
            'MIXED',
        )


if __name__ == '__main__':
    pass
