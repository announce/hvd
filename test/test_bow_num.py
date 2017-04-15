import unittest
from vccf.bow_num import BowNum


class TestBowNum(unittest.TestCase):
    def test_bin_string(self):
        # Totally different as string but the same as bin
        x = BowNum.bin_str('1.01')
        y = BowNum.bin_str('0.99')
        self.assertEqual(x, y)

    def test_keep_str(self):
        x = BowNum.bin_str('foo 20.01 bar')
        self.assertRegexpMatches(x, 'foo [\d\.]+ bar')

    def test_bin_zero(self):
        x = BowNum.bin_num(0)
        y = BowNum.bin_num(0.0)
        self.assertEqual(x, 0)
        self.assertEqual(x, y)

    def test_bin_large_num(self):
        x = BowNum.bin_num(30000)
        self.assertEqual(x, 11)

    def test_bin_percentage(self):
        self.assertEqual(0, BowNum.bin_percentage(0))
        self.assertEqual(1, BowNum.bin_percentage(0.1))
        self.assertEqual(2, BowNum.bin_percentage(0.4))
        self.assertEqual(3, BowNum.bin_percentage(0.7))
        self.assertEqual(4, BowNum.bin_percentage(1))


if __name__ == "__main__":
    unittest.main()
