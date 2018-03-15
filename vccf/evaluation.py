import collections
from vccf.logger import Logger


class Evaluation:
    """
    Model evaluation: quantifying the quality of predictions
    """
    def __init__(self):
        self.Size = Evaluation.size()
        self.ROC = Evaluation.roc()
        self.PrecisionRecall = Evaluation.pr()
        self.logger = Logger.create(name=__name__)
        self.shape = None
        self.size = []
        self.roc = []
        self.accuracy = []
        self.pr = []
        self.f1 = []
        self.contribution = []

    def store(self, size, roc, accuracy, pr, f1, contribution):
        self.size.append(size)
        self.roc.append(roc)
        self.accuracy.append(accuracy)
        self.pr.append(pr)
        self.f1.append(f1)
        self.contribution.append(contribution)
        return self

    @classmethod
    def size(cls):
        return collections.namedtuple('Size', ['train', 'test'])

    @classmethod
    def roc(cls):
        return collections.namedtuple('ROC', ['fpr', 'tpr', 'area'])

    @classmethod
    def pr(cls):
        return collections.namedtuple('PrecisionRecall', ['precision', 'recall', 'area'])


if __name__ == '__main__':
    print(Evaluation())
