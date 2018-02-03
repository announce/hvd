from datetime import datetime
import uuid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Visualization:
    def __init__(self):
        pass

    @classmethod
    def default_filename(cls):
        return 'figure_%s_%s' % datetime.now().strftime('%s'), uuid.uuid4().hex

    @classmethod
    def plot_pr_curve(cls, x, y, title='', filename=None):
        # Plot Precision-Recall curve
        filename = cls.default_filename() if filename is None else filename
        plt.clf()
        plt.figure()
        plt.plot(x, y, label='Precision-Recall curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title(title)
        plt.legend(loc="lower left")
        plt.savefig(filename)

    @classmethod
    def plot_roc_curve(cls, x, y, roc_auc, title='', filename=None):
        #  Receiver operating characteristic (ROC)
        filename = cls.default_filename() if filename is None else filename
        plt.figure()
        lw = 2
        plt.plot(x, y, color='darkorange',
                 lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
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
