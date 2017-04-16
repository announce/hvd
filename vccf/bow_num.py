import math
import re
from logger import Logger
from app_error import AppError


class BowNum:
    # https://docs.python.org/2/library/re.html#simulating-scanf
    INT_MATCHER = r'[-+]?\d+'
    FLOAT_MATCHER = r'[-+]?(\d+(\.\d*)?|\.\d+)'
    SCI_MATCHER = r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'

    def __init__(self):
        self.logger = Logger.create(name=__name__)
        self.numeric_matcher = self.FLOAT_MATCHER

    def bin_str(self, s):
        """
        :param str s:
        :rtype: str
        :return: Replace numeric part with classified bin
        """
        try:
            return re.sub(
                self.numeric_matcher,
                self.replacer,
                s)
        except Exception as inst:
            self.logger.warn('%s\t%s\t%s' % (type(inst), inst, s[:100]))
            return s

    def replacer(self, matched):
        m = matched.group()
        bin = self.bin_num(float(m))
        if bin == float('Inf'):
            self.logger.warn('Ignoring \'%s\' (mistakenly matched with scientific \'e\' notation)' % m)
            return m
        else:
            return str(int(bin))

    def bin_num(self, num):
        """
        For features with skewed distribution
        To ensure that similar values are still identified as being similar
        as "1.01" and "0.99" represent totally different strings
        We choose different bin sizes depending on the type of the feature.
        If the numerical values are rather evenly distributed, we apply a uniform grid,
        whereas for features with skewed distribution we a apply a logarithmic partitioning.
        Replace all numeric token N by log(N) in each patch
        :param float num:
        :rtype: float
        :return: Classified bin
        """
        try:
            x = math.log1p(math.fabs(num))
            return math.ceil(x)
        except Exception as inst:
            self.logger.warn('%s\t%s\t%f' % (type(inst), inst, num))
            return num

    def bin_percentage(self, p, divider=33.3):
        """
        :param float p: Percentage
        :param float divider:
        :rtype: float
        :return: Classify p into 3 bins as default
        """
        if p < 0.0 or 1.0 < p:
            raise AppError('Argument "p" is %f but it must be within 0.0 to 1.0' % p)
        c = min(100, max(1, divider))
        return int(math.ceil(float(p)/c*100))


if __name__ == '__main__':
    bn = BowNum()
    # print BowNum.bin_num(31000)
    # print BowNum.bin_str('1.01')
    # print BowNum.bin_str('0.99')
    # print BowNum.bin_percentage(2.01428936878e-06)
    # print BowNum.bin_percentage(0.001)
    print bn.bin_percentage(0)
    # print BowNum.bin_percentage(0.5)
    # print BowNum.bin_percentage(0.9)

