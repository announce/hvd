import pprint

"""
Easier to represent option types as pure Python but not JSON or something else
"""
Default = {
    'count_vectorizer': {'min_df': 1},
    'model_selection': {
        'test_size': 0.33,
        # Better to be fixed to compare with other challenge
        'random_state': 28,
    },
    'svm': {
        'c': 1.0,
        'loss': 'squared_hinge',
        'class_weight': {
            0: 0.01,
            1: 1.0,
        }
    },
    'visualization': {'output': False}
}

Mask = {
    0: {},
    1: {'visualization': {'output': True}},
    2: {'count_vectorizer': {'min_df': 2}},
    3: {'svm': {'loss': 'hinge'}},
    4: {'svm': {'class_weight': None}},
    5: {'svm': {'class_weight': 'balanced'}},
}


class Option:
    def __init__(self, option=None):
        self.option = Default.copy() if option is None else option
        self.mask = Mask.copy()

    @classmethod
    def merge(cls, source, destination):
        # http://stackoverflow.com/a/20666342/879951
        for key, value in source.items():
            if getattr(value, 'items', None):
                node = destination.setdefault(key, {})
                cls.merge(value, node)
            else:
                destination[key] = value
        return destination

    def select(self, opt_keys=(), key_type=int):
        opt = self.option
        for i in opt_keys:
            opt = self.merge(self.mask.get(key_type(i), {}), opt)
        self.option = opt
        return self

    def __getitem__(self, index):
        return self.option[index]

    def __str__(self):
        return pprint.pformat(self.option)


if __name__ == '__main__':
    print(Option().select((1,)))
