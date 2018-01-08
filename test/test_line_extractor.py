from os import path
import unittest
from vccf.line_extractor import LineExtractor


class TestLineExtractor(unittest.TestCase):
    @classmethod
    def sample_diff(cls):
        with open(path.join(path.dirname(__file__), 'sample.diff'), 'r') as f:
            return f.readlines()

    def test_extract_added_lines(self):
        expected = 'static inline void __ip6_dst_store(struct sock *sk, struct dst_entry *dst,'
        added_lines = LineExtractor.extract_added_lines(self.sample_diff())
        self.assertTrue(expected in added_lines)

    def test_extract_removed_lines(self):
        expected = 'static inline void ip6_dst_store(struct sock *sk, struct dst_entry *dst,'
        removed_lines = LineExtractor.extract_removed_lines(self.sample_diff())
        self.assertTrue(expected in removed_lines)

if __name__ == "__main__":
    unittest.main()
