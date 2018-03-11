import numpy as np
from vccf.logger import Logger


class DataSet:
    def __init__(self):
        self.logger = Logger.create(name=__name__)

    def load(self, filename, key=None):
        self.logger.info('Started loading data \'%s\'' % filename)
        with np.load(filename, encoding='bytes') as npz:
            key = npz.files[0] if key is None else npz.files[key]
            data = npz[key]
        self.logger.info('Data loaded #%d' % len(data))
        return data

    def save(self, filename, *args, **kwargs):
        self.logger.info('Saving %s' % filename)
        return np.savez(filename, *args, **kwargs)


if __name__ == '__main__':
    # Print blamed_commit (VCC-only)
    import sys, os
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
    data = ds.load('vcc_data.npz')
    r_id = np.unique(data[:, Column.repository_id])
    r_name = np.unique(data[:, Column.name])
    print(json.dumps(
        dict(zip(r_id, r_name)),
        default=json_serial,
    ))

    # cache_file = os.path.join('var', 'vcc_only.npz')
    #
    # if os.access(cache_file, os.R_OK):
    #     vcc = ds.load(cache_file)
    # else:
    #     data = ds.load('vcc_data.npz')
    #     labels = data[:, Column.type]
    #     vcc = data[(labels == 'blamed_commit')]
    #     ds.save(cache_file, vcc)
    #
    # # Print blamed_commit (VCC-only)
    # vp = vcc[:, Column.patch].tolist()
    # vp.sort(key=len)
    # index = vp.index(vp[2])
    #
    # keys = Column.__members__.keys()
    # # values = vcc[index]
    #
    # print(json.dumps(
    #     dict(zip(keys, values)),
    #     default=json_serial,
    # ))
