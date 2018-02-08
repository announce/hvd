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
    import sys
    from datetime import date, datetime
    import json
    from vccf.column import Column

    def json_serial(obj):
        # https://stackoverflow.com/a/22238613/879951
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    ds = DataSet()
    ds.logger.disabled = True
    data = ds.load('vcc_data_40x800.npz')

    keys = Column.__members__.keys()
    labels = data[:, Column.type]
    values = data[(labels == 'blamed_commit')][0]

    print(json.dumps(
        dict(zip(keys, values)),
        default=json_serial,
    ))

