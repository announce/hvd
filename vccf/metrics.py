import numpy as np
import pandas as pd
from logger import Logger
from column import Column


class Metrics:
    COUNT_BASE = {
        'additions': Column.additions,
        'deletions': Column.deletions,
        'past_changes': Column.past_changes,
        'past_different_authors': Column.past_different_authors,
        # 'future_different_authors': Column.future_different_authors,
        'hunk_count': Column.hunk_count,
        'forks_count': Column.forks_count,
        'watchers_count': Column.watchers_count,
        'subscribers_count': Column.subscribers_count,
        'open_issues_count': Column.open_issues_count,
        'size': Column.size,
        'distinct_authors_count': Column.distinct_authors_count,
        'commits_count': Column.commits_count,
    }

    DATETIME_BASE = {
        'author_when': Column.author_when,
        'committer_when': Column.committer_when,
    }

    PERCENTAGE_BASE = {
        'author_contributions_percent': Column.author_contributions_percent,
    }

    def __init__(self, data):
        self.logger = Logger.create(name=__name__)
        self.data = data

    @classmethod
    def bin(cls, arr):
        # return np.ceil(np.log1p(arr))
        d = (np.nanmax(arr) - np.nanmin(arr)) // 4
        return arr // abs(d)

    @classmethod
    def per_to_int(cls, a):
        return [round(p * 100) for p in a]

    @classmethod
    def dt_approx(cls, a):
        return pd.to_datetime(a).astype(int) // 10**16

    def create_count_base(self):
        metrics = self.data[:, self.COUNT_BASE.values()]
        return np.apply_along_axis(self.bin, axis=0, arr=metrics.astype(float))

    def create_datetime_base(self):
        metrics = self.data[:, self.DATETIME_BASE.values()]
        return np.apply_along_axis(self.dt_approx, axis=0, arr=metrics)

    def create_percentage_base(self):
        metrics = self.data[:, self.PERCENTAGE_BASE.values()]
        return metrics

    def create_vector(self):
        m1 = np.hstack((
            self.create_count_base(),
            self.create_datetime_base(),
            self.create_percentage_base(),
        ))
        return pd.DataFrame(m1).fillna(0).astype(float)

    @classmethod
    def bind_col(cls, col, features):
        df = pd.DataFrame(features.transpose()).fillna(0).astype(float)

        bound = {
            '__%s__' % c[0]: f for c, f in zip(col.items(), df.as_matrix())
        }
        print(zip(col.items(), df))
        print(zip(col, df))
        return bound

    def create_dict(self):
        return {
            self.bind_col(self.COUNT_BASE, self.create_count_base()).items() +
            self.bind_col(self.DATETIME_BASE, self.create_datetime_base()).items() +
            self.bind_col(self.PERCENTAGE_BASE, self.create_percentage_base()).items()
        }

if __name__ == '__main__':
    pass
