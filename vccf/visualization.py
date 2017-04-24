from logger import Logger
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Visualization:
    def __init__(self):
        self.logger = Logger.create(name=__name__)

    @classmethod
    def plot_pr_curve(cls, x, y, title, filename):
        # Plot Precision-Recall curve
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
