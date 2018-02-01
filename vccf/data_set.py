import numpy as np


class DataSet:
    def __init__(self):
        pass

    @classmethod
    def load(cls, filename, key=None):
        npz = np.load(filename, encoding='bytes')
        key = npz.files[0] if key is None else key
        data = npz[key]
        npz.close()
        return data

    @classmethod
    def save(cls, filename, *args, **kwargs):
        return np.savez(filename, *args, **kwargs)


if __name__ == '__main__':
    pass
