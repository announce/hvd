from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Visualization:
    def __init__(self):
        pass

    @classmethod
    def default_filename(cls):
        return 'figure_%s' % datetime.now().strftime('%s')

    @classmethod
    def plot_pr_curve(cls, x, y, title='', filename=None):
        # Plot Precision-Recall curve
        filename = cls.default_filename() if filename is None else filename
        plt.clf()
        plt.plot(x, y, label='Precision-Recall curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title(title)
        plt.legend(loc="lower left")
        plt.savefig(filename)


if __name__ == '__main__':
    pass
