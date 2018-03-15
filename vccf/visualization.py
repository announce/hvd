from datetime import datetime
import uuid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Visualization:
    """
    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot
    """
    def __init__(self):
        pass

    @classmethod
    def default_filename(cls):
        return 'figure_%s_%s' % datetime.now().strftime('%s'), uuid.uuid4().hex

    @classmethod
    def plot_pr_curve(cls, pr, size, title, filename):
        # Plot Precision-Recall curve
        plt.clf()
        plt.figure()
        for i, (x, y, area) in enumerate(pr):
            s = size[i]
            plt.plot(x, y, label='Precision-recall %r (area={%0.2f})' % ((s.train, s.test), area))
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title(title)
        plt.legend()
        plt.savefig(filename)

    @classmethod
    def plot_roc_curve(cls, roc, size, title, filename):
        #  Receiver operating characteristic (ROC)
        plt.figure()
        for i, (x, y, area) in enumerate(roc):
            s = size[i]
            plt.plot(x, y, label='ROC curve %r (area = %0.2f)' % ((s.train, s.test), area))
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(title)
        plt.legend(loc="lower right")
        plt.savefig(filename)

    @classmethod
    def plot_contribution(cls, ctb, title='', filename=None):
        """
        :param ctb:
        :param title:
        :param filename:
        :type ctb: Contribution
        :return:
        """
        plt.figure(figsize=(8, 12))
        plt.grid(color='#cccccc', linestyle='-')
        colors = ['red' if c < 0 else 'blue' for c in ctb.weight[ctb.top_coefficients]]
        plt.barh(ctb.range(), ctb.nominee_weights(), color=colors, alpha=.6)
        plt.yticks(ctb.range(), ctb.nominee_names())
        plt.title(title)
        plt.tight_layout()
        plt.savefig(filename)


if __name__ == '__main__':
    pass
