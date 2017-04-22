import numpy as np
from logger import Logger
from column import Column


class StopWords:
    PROHIBITED_COLUMNS = np.array([
        Column.author_email,
        Column.author_name,
        Column.committer_email,
        Column.committer_when,
    ])

    def __init__(self, data):
        """
        :param data
        """
        self.logger = Logger.create(name=__name__)
        self.data = data

    def list(self):
        """
        :rtype: numpy.flatiter
        :return:
        """
        return self.data[:, self.PROHIBITED_COLUMNS].flatten()


if __name__ == '__main__':
    pass
