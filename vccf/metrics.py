import numpy as np
from logger import Logger
from column import Column


class Metrics:

    def __init__(self, data):
        self.logger = Logger.create(name=__name__)
        self.data = data

    def vectroize(self):
        # Now X is sparse array looks like:
        # [[0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  ...,
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]]

        # Bind metrics from Git metadata
        target_metrics = map(lambda n: n-1, [
            Column.additions,
            Column.deletions,
            Column.past_different_authors,
            Column.future_different_authors,
            Column.hunk_count,
            Column.files_changed,
        ])

        # @TODO Column.author_contributions_percent,
        metrics_data = np.array([row[target_metrics] for row in self.data])
        # Now combined X2 looks like
        # [[3L 66L 7L ..., 0L 0L 0L]
        #  [54L 23L 6L ..., 0L 0L 0L]
        #  [3L 1L 12L ..., 0L 0L 0L]
        #  ...,
        #  [1L 2L 1L ..., 0L 0L 0L]
        #  [46L 21L 0L ..., 0L 0L 0L]
        #  [32L 12L 42L ..., 0L 0L 0L]]
        return metrics_data


if __name__ == '__main__':
    pass
