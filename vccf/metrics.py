import numpy as np
import pandas as pd
from logger import Logger
from column import Column


class Metrics:
    COUNT_BASE = [
        Column.additions,
        Column.deletions,
        Column.past_changes,
        Column.past_different_authors,
        # Column.future_different_authors,
        Column.hunk_count,
        Column.forks_count,
        Column.watchers_count,
        Column.subscribers_count,
        Column.open_issues_count,
        Column.size,
        Column.distinct_authors_count,
        Column.commits_count,
    ]

    DATETIME_BASE = [
        Column.author_when,
        Column.committer_when,
    ]

    PERCENTAGE_BASE = [
        Column.author_contributions_percent,
    ]

    def __init__(self, data):
        self.logger = Logger.create(name=__name__)
        self.data = data

    @classmethod
    def bin(cls, arr):
        # return np.ceil(np.log1p(arr))
        d = (np.nanmax(arr) - np.nanmin(arr)) // 100
        return arr // abs(d)

    @classmethod
    def per_to_int(cls, a):
        return [round(p * 1000) for p in a]

    @classmethod
    def dt_approx(cls, a):
        return pd.to_datetime(a).astype(int) // 10**16

    def create_count_base(self):
        metrics = self.data[:, self.COUNT_BASE]
        return np.apply_along_axis(self.bin, axis=0, arr=metrics.astype(float))

    def create_datetime_base(self):
        metrics = self.data[:, self.DATETIME_BASE]
        return np.apply_along_axis(self.dt_approx, axis=0, arr=metrics)

    def create_percentage_base(self):
        metrics = self.data[:, self.PERCENTAGE_BASE]
        return np.apply_along_axis(self.per_to_int, axis=0, arr=metrics)

    def create_vector(self):
        """
        Bind metrics from Git metadata
        :return:
        """
        # print self.create_count_base()

        m1 = np.hstack((
            self.create_count_base(),
            self.create_datetime_base(),
            self.create_percentage_base(),
        ))
        return pd.DataFrame(m1).fillna(0).astype(int)


if __name__ == '__main__':
    pass
