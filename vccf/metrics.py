from math import log10, floor
import numpy as np
import pandas as pd
from logger import Logger
from column import Column


class Metrics:
    COUNT_BASE = np.array([
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
    ])

    DATETIME_BASE = np.array([
        Column.author_when,
        Column.committer_when,
    ])

    PERCENTAGE_BASE = np.array([
        Column.author_contributions_percent,
    ])

    def __init__(self, data):
        self.logger = Logger.create(name=__name__)
        self.data = data

    @classmethod
    def bin(cls, arr):
        return np.ceil(np.log1p(arr))

    @classmethod
    def round_sig(cls, x, sig=1):
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    @classmethod
    def flag(cls, a, **kwargs):
        """
        # col = np.asarray([np.unique(bin_metrics[:, i]) for i in np.arange(bin_metrics.shape[1])])
        # return np.apply_along_axis(self.flag, axis=1, arr=bin_metrics, col=col)
        :param a: 
        :param kwargs: 
        :return: 
        """
        l = [(kwargs['col'][i] == v).astype(int) for i, v in enumerate(a)]
        return [item for sublist in l for item in sublist]

    @classmethod
    def per_to_int(cls, a):
        return [round(p * 100) for p in a]

    @classmethod
    def dt_rank(cls, a):
        return pd.to_datetime(a).astype(int) // 10**16

    def create_count_base(self):
        metrics = self.data[:, self.COUNT_BASE]
        return np.apply_along_axis(self.bin, axis=1, arr=metrics.astype(float)).astype(int)

    def create_datetime_base(self):
        metrics = self.data[:, self.DATETIME_BASE]
        return np.apply_along_axis(self.dt_rank, axis=0, arr=metrics).astype(int)

    def create_percentage_base(self):
        metrics = self.data[:, self.PERCENTAGE_BASE]
        return np.apply_along_axis(self.per_to_int, axis=1, arr=metrics).astype(int)

    def create_vector(self):
        """
        Bind metrics from Git metadata
        @TODO
        Commit message - author names and email addresses
        :return:
        """
        return np.hstack((
            self.create_count_base(),
            self.create_datetime_base(),
            self.create_percentage_base(),
        ))


if __name__ == '__main__':
    pass
