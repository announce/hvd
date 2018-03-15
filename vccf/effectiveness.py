import os
import graphviz
from sklearn import tree
from vccf.logger import Logger


class Effectiveness:
    def __init__(self, task_id, option, labels):
        self.logger = Logger.create(name=__name__)
        self.option = option
        self.task_id = task_id
        self.labels = labels

    def train(self, x_train, y_train):
        self.logger.info('DecisionTree: %r' % (x_train.shape,))
        clf = tree.DecisionTreeClassifier(random_state=0, max_depth=x_train.shape[0])
        clf.fit(x_train, y_train)
        dot_data = tree.export_graphviz(clf,
                                        feature_names=self.labels,
                                        out_file=None,
                                        filled=True,
                                        special_characters=True)
        graph = graphviz.Source(dot_data)
        graph.render(os.path.join('logs', 'figure_%d_dt.gv' % self.task_id))
        return dot_data


if __name__ == '__main__':
    pass
