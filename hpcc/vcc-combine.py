import os
from argparse import ArgumentParser
import numpy as np
import scipy as sp
import pandas as pd
from scipy import sparse
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC, SVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from vccf.logger import Logger
from vccf.timer import Timer
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
        self.timer = Timer().start()
        self.task_id = task_id
        self.patch_mode = patch_mode
        self.filename = filename
        self.logger = Logger.create(name=__name__, filename=task_id)
        self.opt_keys = () if opt_keys is None else opt_keys

    def exit(self):
        self.logger.info('Exiting task %d at %s' % (
            self.task_id,
            self.timer.stop()
        ))
        return self

    def execute(self):
        self.logger.info('Started executing task_id %d at %s' % (self.task_id, self.timer))
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
        x1 = vectorizer.fit_transform(candidates)
        # print vectorizer.get_feature_names()

        # Now x1 is sparse array looks like:
        # [[0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  ...,
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]]

        # x2 = x1
        m = Metrics(data).create_vector()
        x2 = sparse.hstack((m, x1))
        labels = data[:, Column.type]
        y = is_vcc = (labels == 'blamed_commit')

        # Split into training and test
        x_train, \
        x_test, \
        y_train, \
        y_test = train_test_split(x2,
                                  y,
                                  test_size=option['model_selection']['test_size'],
                                  random_state=option['model_selection']['random_state'])

        # Run classifier
        classifier = SVC(C=option['svm']['c'],
                         class_weight=option['svm']['class_weight'])
        # classifier = LinearSVC(C=option['svm']['c'],
        #                        class_weight=option['svm']['class_weight'],
        #                        loss=option['svm']['loss'])

        # accuracy
        y_score = classifier.fit(x_train, y_train).decision_function(x_test)
        accuracy = classifier.score(x_test, y_test)
        self.logger.info('Accuracy %r' % accuracy)
        self.logger.debug('y_score[1:10] %r', y_score[1:10])

        # Compute Precision-Recall and plot curve
        precision = dict()
        recall = dict()
        average_precision = dict()
        precision[0], recall[0], _ = metrics.precision_recall_curve(y_test, y_score)
        average_precision[0] = metrics.average_precision_score(y_test, y_score)
        self.logger.info('Average precision %r' % average_precision)

        Visualization.plot_pr_curve(
            x=recall[0],
            y=precision[0],
            title='%r %r: AUC=%f' % (
                self.patch_mode,
                data.shape,
                average_precision[0],
            ),
            filename=os.path.join('logs', 'figure_%d_pr' % self.task_id)
        ) if option['visualization']['output'] else None

        # Compute ROC and plot curve
        yi_test = y_test.astype(int)
        fpr, tpr, _ = metrics.roc_curve(yi_test, y_score, pos_label=1)
        roc_auc = metrics.auc(fpr, tpr)

        Visualization.plot_roc_curve(
            x=fpr,
            y=tpr,
            roc_auc=roc_auc,
            title='%r %r: area=%f' % (
                self.patch_mode,
                data.shape,
                roc_auc,
            ),
            filename=os.path.join('logs', 'figure_%d_roc' % self.task_id)
        ) if option['visualization']['output'] else None

        yb_score = y_score.round().astype(bool)
        f1 = metrics.f1_score(y_test, yb_score)
        report = metrics.classification_report(y_test, yb_score)
        self.logger.info('F1 score %r' % f1)

        # Output report in multiline
        [self.logger.info(line) for line in ['--'] + report.splitlines() + ['--']]

        return self


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
    ).execute().exit()
