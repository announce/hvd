import numpy as np
from vccf.logger import Logger


class DataSet:
    def __init__(self):
        self.logger = Logger.create(name=__name__)

    def load(self, filename, key=None):
        self.logger.info('Started loading data \'%s\'' % filename)
        with np.load(filename, encoding='bytes') as npz:
            key = npz.files[0] if key is None else key
            data = npz[key]
        self.logger.info('Data loaded #%d' % len(data))
        return data

    def save(self, filename, *args, **kwargs):
        self.logger.info('saving')
        return np.savez(filename, *args, **kwargs)


if __name__ == '__main__':
    pass
