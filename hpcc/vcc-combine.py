import os
import platform
from argparse import ArgumentParser
import numpy as np
import scipy as sp
import pandas as pd
from scipy import sparse
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from vccf.logger import Logger
from vccf.timer import Timer
from vccf.patch import Patch
from vccf.message import Message
from vccf.metrics import Metrics
from vccf.stop_words import StopWords
from vccf.column import Column
from vccf.effectiveness import Effectiveness
from vccf.contribution import Contribution
from vccf.data_set import DataSet
from vccf.option import Option, Mask
from vccf.classification import Classification
from vccf.evaluation import Evaluation
from vccf.visualization import Visualization


class VccCombine:
    def __init__(self, task_id, patch_mode, filename):
        self.timer = Timer().start()
        self.task_id = task_id
        self.patch_mode = patch_mode
        self.filename = filename
        self.logger = Logger.create(
            name=__name__,
            filename=os.path.join('logs', platform.node(), str(task_id), '%s.log' % os.path.basename(__file__)))
        self.data_set = DataSet()
        self.option = Option()
        self.evaluation = Evaluation()

    def set_opt(self, opt_keys):
        opt_keys = () if opt_keys is None else opt_keys
        self.option = self.option.select(opt_keys)
        return self

    def exit(self):
        self.logger.info('Exiting task %d at %s' % (
            self.task_id,
            self.timer.stop()
        ))
        return self

    def execute(self):
        self.logger.info('Started executing task_id %d at %s' % (self.task_id, self.timer))
        data = self.data_set.load(self.filename)
        self.evaluation.shape = data.shape

        patch_container = Patch(data, mode=self.patch_mode)
        patch = patch_container.normalized()
        message = Message(data).normalized()
        candidates = [u' '.join([v, message[i]]) for i, v in enumerate(patch)]
        stop_words = StopWords(data).list()

        vectorizer = TfidfVectorizer(min_df=self.option['count_vectorizer']['min_df'],
                                     max_features=len(candidates)//2,
                                     stop_words=stop_words)
        x1 = vectorizer.fit_transform(candidates)

        # Now x1 is sparse array storing like:
        # [[0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  ...,
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]
        #  [0 0 0 ..., 0 0 0]]

        mtr = Metrics(data)
        x2 = sparse.hstack((mtr.create_vector(), x1))
        labels = data[:, Column.type]
        y = is_vcc = (labels == 'blamed_commit')

        # Importance
        features = vectorizer.get_feature_names() + mtr.keys()
        iif = Effectiveness(
            task_id=self.task_id,
            option=self.option,
            labels=vectorizer.get_feature_names() + mtr.keys()
        ).train(x2, is_vcc).is_important_features()
        x3 = x2.tocsr()[:, iif]
        adopted_features = np.array(features)[iif]

        # Split into training and test
        test_size = self.option['model_selection']['test_size']
        x_train, \
        x_test, \
        y_train, \
        y_test = train_test_split(x3,
                                  y,
                                  test_size=self.option['model_selection']['test_size'],
                                  random_state=self.option['model_selection']['random_state'])

        # Train model
        classifier = Classification(self.option).train(x_train, y_train)

        # Save classifier model
        if self.option['save_model'] is True:
            self.data_set.save(os.path.join('logs', 'model_%d' % self.task_id), model=classifier)

        # Start evaluation
        y_score = classifier.decision_function(x_test)
        accuracy = classifier.score(x_test, y_test)

        contribution = Contribution(model=classifier,
                                    labels=adopted_features,
                                    patch_container=patch_container).explain()

        precision, recall, _ = metrics.precision_recall_curve(y_test, y_score)
        average_precision = metrics.average_precision_score(y_test, y_score)

        # Compute ROC and plot curve
        yi_test = y_test.astype(int)
        fpr, tpr, _ = metrics.roc_curve(yi_test, y_score, pos_label=1)
        roc_auc = metrics.auc(fpr, tpr)

        # Score F1
        yb_score = y_score.round().astype(bool)
        f1 = metrics.f1_score(y_test, yb_score)

        # Keep evaluation
        self.evaluation.store(size=self.evaluation.Size(1-test_size, test_size),
                              roc=self.evaluation.ROC(fpr, tpr, roc_auc),
                              pr=self.evaluation.PrecisionRecall(precision, recall, average_precision),
                              accuracy=accuracy,
                              f1=f1,
                              contribution=contribution)
        # Output report
        self.logger.info('(F1, accuracy, average_precision) = (%0.2f, %0.2f, %0.2f)' %
                         (f1,
                          accuracy,
                          average_precision,))
        report = metrics.classification_report(y_test, yb_score)
        [self.logger.info(line) for line in ['--'] + report.splitlines() + ['--']]

        if self.option['visualization']['output']:
            self.visualize()
        return self

    def visualize(self):
        # Title of figure
        title = '%r %r' % (
            self.patch_mode,
            self.evaluation.shape,
        )

        # Plot precision-recall curves
        Visualization.plot_pr_curve(
            pr=self.evaluation.pr,
            size=self.evaluation.size,
            title='PR %s' % title,
            filename=os.path.join('logs', platform.node(), str(self.task_id), 'pr')
        )

        # Plot ROC curves
        Visualization.plot_roc_curve(
            roc=self.evaluation.roc,
            size=self.evaluation.size,
            title='ROC %s' % title,
            filename=os.path.join('logs', platform.node(), str(self.task_id), 'roc')
        )

        # Plot contribution
        Visualization.plot_contribution(
            ctb=self.evaluation.contribution.pop(),
            title=title,
            filename=os.path.join('logs', platform.node(), str(self.task_id), 'ctb')
        )
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
        filename=args.filename
    ).set_opt(
        opt_keys=tuple(args.options)
    ).execute().exit()
