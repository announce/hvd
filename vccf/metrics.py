import numpy as np
import pandas
from logger import Logger
from column import Column


class Metrics:

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
        # @TODO Column.author_contributions_percent,
        # Corrupt data (all 0): Column.files_changed
        # Bind metrics from Git metadata
        target_metrics = map(lambda n: n-1, [
            Column.additions,
            Column.deletions,
            Column.past_different_authors,
            Column.future_different_authors,
            Column.hunk_count,
        ])
        metrics_data = np.array([row[target_metrics] for row in self.data])
        bin_metrics = self.bin(metrics_data.astype(float)).astype(int)
        # print bin_metrics
        # [[2 5 3 4 3]
        #  [5 4 2 3 3]
        #  [2 1 3 3 1]
        #  ...,
        #  [1 2 1 3 1]
        #  [4 4 0 6 3]
        #  [4 3 4 4 3]]
        col = np.asarray([np.unique(bin_metrics[:, i]) for i in np.arange(bin_metrics.shape[1])])
        return np.apply_along_axis(self.flag, axis=1, arr=bin_metrics, col=col)
        # return bin_metrics


if __name__ == '__main__':
    pass
