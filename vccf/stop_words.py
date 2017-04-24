import numpy as np
from logger import Logger
from column import Column


class StopWords:
    SENSITIVE_COLUMNS = [
        Column.author_email,
        Column.author_name,
        Column.committer_email,
        Column.committer_name,
    ]

    def __init__(self, data):
        """
        :param data
        """
        self.logger = Logger.create(name=__name__)
        self.data = data

    def list(self):
        """
        :rtype: list[str]
        :return:
        """
        sensitive_data = self.data[:, self.SENSITIVE_COLUMNS]
        return np.unique(sensitive_data.flatten()).tolist()


if __name__ == '__main__':
    pass
