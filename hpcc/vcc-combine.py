import sys
import os
from datetime import datetime
from argparse import ArgumentParser
import numpy as np
import scipy as sp
import pandas as pd
from scipy import sparse
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from vccf.logger import Logger
from vccf.patch import Patch
from vccf.message import Message
from vccf.metrics import Metrics
from vccf.stop_words import StopWords
from vccf.column import Column
from vccf.data_loader import DataLoader
from vccf.option import Option, Mask
from vccf.visualization import Visualization


class VccCombine:
    def __init__(self, task_id, patch_mode, filename, opt_keys=None):
        started_at = datetime.now()
        self.task_id = task_id
        self.patch_mode = patch_mode
        self.filename = filename
        self.logger = Logger.create(name=__name__)
        self.opt_keys = () if opt_keys is None else opt_keys

    def execute(self):
        option = Option().select(self.opt_keys)
        self.logger.info('Option:\n%s' % option)
        self.logger.info('Started loading data \'%s\'' % self.filename)
        data = DataLoader.load(self.filename)
        self.logger.info('Data loaded #%d' % len(data))

        patch = Patch(data, mode=self.patch_mode).normalized()
        message = Message(data).normalized()
        candidates = [u' '.join([v, message[i]]) for i, v in enumerate(patch)]
        stop_words = StopWords(data).list()
        vectorizer = TfidfVectorizer(min_df=option['count_vectorizer']['min_df'],
                                     max_features=len(candidates)//2,
                                     stop_words=stop_words)
        X = vectorizer.fit_transform(candidates)
        # print vectorizer.get_feature_names()

        # Now X is sparse array looks like:
        # [[0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  ...,
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]]

        # X2 = X
        metrics = Metrics(data).create_vector()
        X2 = sparse.hstack((metrics, X))

        labels = data[:, Column.type]
        y = is_vcc = (labels == 'blamed_commit')

        # Split into training and test
        X_train, \
        X_test, \
        y_train, \
        y_test = train_test_split(X2,
                                  y,
                                  test_size=option['model_selection']['test_size'],
                                  random_state=option['model_selection']['random_state'])

        # Run classifier
        classifier = LinearSVC(C=option['svm']['c'],
                               class_weight=option['svm']['class_weight'],
                               loss=option['svm']['loss'])

        # accuracy
        y_score = classifier.fit(X_train, y_train).decision_function(X_test)
        accuracy = classifier.score(X_test, y_test)
        self.logger.info(accuracy)

        # Compute Precision-Recall and plot curve
        precision = dict()
        recall = dict()
        average_precision = dict()
        precision[0], recall[0], _ = precision_recall_curve(y_test, y_score)
        average_precision[0] = average_precision_score(y_test, y_score)

        Visualization.plot_pr_curve(
            x=recall[0],
            y=precision[0],
            title='%s %r: AUC=%.2f' % (
                self.__class__.__name__,
                data.shape,
                average_precision[0],
            ),
            filename=os.path.join('logs', 'figure_%d' % self.task_id)
        ) if option['visualization']['output'] else None
        self.logger.info(average_precision)
        return average_precision


if __name__ == '__main__':
    parser = ArgumentParser(description=u'History-based Vulnerability detector')
    parser.add_argument(
        '-i',
        '--task_id',
        type=int,
        default=0,
        help='Task ID',
    )
    parser.add_argument(
        '-m',
        '--patch_mode',
        type=Patch.Mode.from_string,
        default=Patch.Mode.RESERVED_WORD_ONLY,
        choices=list(Patch.Mode),
        help='Patch Mode',
    )
    parser.add_argument(
        '-f',
        '--filename',
        type=str,
        default='vcc_data_40x800.npz',
        help='Data filename',
    )
    parser.add_argument(
        '-o',
        '--options',
        type=int,
        nargs='*',
        default=[],
        choices=Mask.keys()
    )
    args = parser.parse_args()
    VccCombine(
        task_id=args.task_id,
        patch_mode=args.patch_mode,
        filename=args.filename,
        opt_keys=tuple(args.options)
    ).execute()
