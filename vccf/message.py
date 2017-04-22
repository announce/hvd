from logger import Logger
from column import Column


class Message:
    def __init__(self, data):
        """
        :param data
        """
        self.logger = Logger.create(name=__name__)
        self.data = data

    def normalized(self):
        """
        :rtype: unicode
        :return:
        """
        return u' '.join(self.data[:, Column.message])


if __name__ == '__main__':
    pass
