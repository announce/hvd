import re
from unidiff import PatchSet


def extract_added_lines(str):
    return extract_lines(str, lambda line: line.is_added)


def extract_removed_lines(str):
    return extract_lines(str, lambda line: line.is_removed)


def extract_lines(str, query=(lambda line: line), normalizer=None):
    patches = PatchSet(str, encoding='utf-8')
    return [_normalize(line) if normalizer is None else normalizer(line)
            for files in patches for hunks in files for line in hunks
            if query(line)]


def _normalize(str):
    return re.sub(r'[ \t]+', ' ', str.value.strip())


if __name__ == '__main__':
    with open('4447bb33f09444920a8f1d89e1540137429351b6.diff', 'r') as diff:
        data = diff.readlines()
        print extract_added_lines(data)
        print extract_removed_lines(data)
