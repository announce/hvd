from sklearn.svm import LinearSVC, SVC
from sklearn.naive_bayes import MultinomialNB


class Classification:
    def __init__(self, option):
        self.option = option

    def train(self, x_train, y_train):
        # Run classifier
        # classifier = SVC(C=self.option['svm']['c'])
        classifier = LinearSVC(C=self.option['svm']['c'],
                               class_weight=self.option['svm']['class_weight'],
                               loss=self.option['svm']['loss'])
        # classifier = MultinomialNB()
        classifier.fit(x_train, y_train)
        # clf_pf.partial_fit(X, Y, np.unique(Y))
        # y_score = classifier.predict(x_test)
        # accuracy = classifier.score(x_train, y_train)

        return classifier


if __name__ == '__main__':
    pass
