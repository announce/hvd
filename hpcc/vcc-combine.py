
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.cross_validation import train_test_split
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import label_binarize
from sklearn import cross_validation
from scipy import sparse
import numpy as np
import scipy as sp
from datetime import datetime
from vccf.logger import Logger
from vccf.patch_normalizer import PatchNormalizer
from vccf.metrics import Metrics
from vccf.column import Column
from vccf.data import Data

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


logger = Logger.create(name=__name__)
logger.info('Started loading data')
# data = Data.load('vcc_sample_40x800.npz')
# data = Data.load('vcc_data.npz')
data = Data.load('vcc_sample_all.npz')
logger.info('Data loaded #%d' % len(data))

patches = data[:, Column.patch]
labels = data[:, Column.type]

normalized_patches = PatchNormalizer().normalize_patches(patches)

# @TODO: stop_words=[]
vectorizer = CountVectorizer(min_df=2, stop_words=None)
X = vectorizer.fit_transform(normalized_patches)
# feature_names = vectorizer.get_feature_names()
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

y = is_vcc = (labels == 'blamed_commit')

# Split into training and test
X_train, X_test, y_train, y_test = train_test_split(X2, y, test_size=0.33, random_state=0)

# Run classifier
# weight = {0:.01, 1:1}
weight = {0: 1, 1: .01}
classifier = LinearSVC(C=1.0, class_weight=weight)
y_score = classifier.fit(X_train, y_train).decision_function(X_test)

# Compute Precision-Recall and plot curve
precision = dict()
recall = dict()
average_precision = dict()
precision[0], recall[0], _ = precision_recall_curve(y_test, y_score)
average_precision[0] = average_precision_score(y_test, y_score)

# Plot Precision-Recall curve
plt.clf()
plt.plot(recall[0], precision[0], label='Precision-Recall curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Precision-Recall example: AUC={0:0.2f}'.format(average_precision[0]))
plt.legend(loc="lower left")
plt.savefig("figure_%s" % datetime.now().strftime('%s'))

logger.info(average_precision)
