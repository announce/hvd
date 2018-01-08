import unittest
from vccf.bow_num import BowNum


class TestBowNum(unittest.TestCase):

    def setUp(self):
        self.bn = BowNum()

    def test_bin_string(self):
        # Totally different as string but the same as bin
        x = self.bn.bin_str('1.01')
        y = self.bn.bin_str('0.99')
        self.assertEqual(x, y)

    def test_keep_str(self):
        x = self.bn.bin_str('foo 20.01 bar')
        self.assertRegexpMatches(x, 'foo [\d\.]+ bar')

    def test_bin_zero(self):
        x = self.bn.bin_num(0)
        y = self.bn.bin_num(0.0)
        self.assertEqual(x, 0)
        self.assertEqual(x, y)

    def test_bin_large_num(self):
        x = self.bn.bin_num(30000)
        self.assertEqual(x, 11)

    def test_bin_percentage(self):
        self.assertEqual(0, self.bn.bin_percentage(0))
        self.assertEqual(1, self.bn.bin_percentage(0.1))
        self.assertEqual(2, self.bn.bin_percentage(0.4))
        self.assertEqual(3, self.bn.bin_percentage(0.7))
        self.assertEqual(4, self.bn.bin_percentage(1))


if __name__ == "__main__":
    unittest.main()
