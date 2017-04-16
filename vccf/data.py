import numpy as np


class Data:
    def __init__(self):
        pass

    @classmethod
    def load(cls, filename, key=None):
        npz = np.load(filename)
        key = npz.files[0] if key is None else key
        data = npz[key]
        npz.close()
        return data


if __name__ == '__main__':
    pass
