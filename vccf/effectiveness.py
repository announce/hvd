import os
import platform
import graphviz
import numpy as np
from sklearn import tree
from vccf.logger import Logger


class Effectiveness:
    IMPORTANCE = 0.4

    def __init__(self, task_id, option, labels):
        self.logger = Logger.create(name=__name__)
        self.option = option
        self.task_id = task_id
        self.labels = labels
        self.clf = None

    def train(self, x_train, y_train):
        self.logger.info('DecisionTree: %r' % (x_train.shape,))
        self.clf = clf = tree.DecisionTreeClassifier(
            random_state=0,
            max_depth=max(x_train.shape[0]//10, 1000)
        )
        clf.fit(x_train, y_train)
        dot_data = tree.export_graphviz(clf,
                                        feature_names=self.labels,
                                        out_file=None,
                                        filled=True,
                                        special_characters=True)
        graph = graphviz.Source(dot_data)
        graph.render(os.path.join('logs', platform.node(), str(self.task_id), 'dt.gv'))
        return self

    def is_important_features(self):
        # Gini importance
        fi = np.array(self.clf.feature_importances_)
        bl = np.where(fi > self.IMPORTANCE)
        self.logger.info('Important features: #%d' % np.count_nonzero(fi))
        return bl[0]


if __name__ == '__main__':
    pass
