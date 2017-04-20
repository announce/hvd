import numpy as np
from logger import Logger
from column import Column


class Metrics:
    COUNT_BASE = [
        Column.additions,
        Column.deletions,
        Column.past_different_authors,
        # Column.future_different_authors,
        Column.hunk_count,
    ]

    def __init__(self, data):
        self.logger = Logger.create(name=__name__)
        self.data = data

    @classmethod
    def bin(cls, arr):
        return np.ceil(np.log1p(arr))

    @classmethod
    def flag(cls, a, **kwargs):
        l = [(kwargs['col'][i] == v).astype(int) for i, v in enumerate(a)]
        return [item for sublist in l for item in sublist]

    def create_vector(self):
        """
        Bind metrics from Git metadata
        @TODO
        Column.author_contributions_percent
        Number of commits
        Number of unique contributors
        Commit message - author names and email addresses
        Star count
        Fork count
        :return:
        """

        count_base = self.data[:, map(lambda n: n-1, self.COUNT_BASE)]
        bin_metrics = self.bin(count_base.astype(float)).astype(int)

        # sparse.hstack

        # print bin_metrics
        # [[2 5 3 4 3]
        #  [5 4 2 3 3]
        #  [2 1 3 3 1]
        #  ...,
        #  [1 2 1 3 1]
        #  [4 4 0 6 3]
        #  [4 3 4 4 3]]
        # col = np.asarray([np.unique(bin_metrics[:, i]) for i in np.arange(bin_metrics.shape[1])])
        # return np.apply_along_axis(self.flag, axis=1, arr=bin_metrics, col=col)
        # return bin_metrics
        return metrics_data.astype(float)


if __name__ == '__main__':
    pass
