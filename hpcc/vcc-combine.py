import sys
import os
from datetime import datetime
import numpy as np
import scipy as sp
from scipy import sparse
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from vccf.logger import Logger
from vccf.patch import Patch
from vccf.message import Message
from vccf.metrics import Metrics
from vccf.stop_words import StopWords
from vccf.column import Column
from vccf.data import Data
from vccf.visualization import Visualization


class VccCombine:
    def __init__(self, filename='vcc_data_40x800.npz'):
        self.filename = filename
        self.logger = Logger.create(name=__name__)

    def execute(self):
        self.logger.info('Started loading data \'%s\'' % self.filename)
        data = Data.load(self.filename)
        self.logger.info('Data loaded #%d' % len(data))

        patch = Patch(data).normalized()
        message = Message(data).normalized()
        candidates = [u' '.join([v, message[i]]) for i, v in enumerate(patch)]
        stop_words = StopWords(data).list()
        vectorizer = CountVectorizer(min_df=1, stop_words=stop_words)
        X = vectorizer.fit_transform(candidates)
        # feature_names = vectorizer.get_feature_names()
        # print feature_names

        # Now X is sparse array looks like:
        # [[0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  ...,
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]]

        metrics = Metrics(data).create_vector()
        X2 = sparse.hstack((metrics, X))

        labels = data[:, Column.cve]
        y = is_vcc = (labels != '')

        # Split into training and test
        X_train, X_test, y_train, y_test = train_test_split(X2, y, test_size=0.33, random_state=0)

        # Run classifier
        # classifier = LinearSVC(C=1.0, class_weight='balanced')
        weight = {0: .01, 1: .1}
        classifier = LinearSVC(C=1.0, class_weight=weight, loss='hinge')

        y_score = classifier.fit(X_train, y_train).decision_function(X_test)

        # Compute Precision-Recall and plot curve
        precision = dict()
        recall = dict()
        average_precision = dict()
        precision[0], recall[0], _ = precision_recall_curve(y_test, y_score)
        average_precision[0] = average_precision_score(y_test, y_score)
        Visualization.plot_pr_curve(
            x=recall[0],
            y=precision[0],
            title='%s %s: AUC=%.2f' % (
                self.__class__.__name__,
                os.path.basename(self.filename),
                average_precision[0],
            ),
            filename="figure_%s" % datetime.now().strftime('%s')
        )
        self.logger.info(average_precision)


if __name__ == '__main__':
    VccCombine(*sys.argv[1:]).execute()
