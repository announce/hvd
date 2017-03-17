#!/usr/bin/env python
# -*- coding: utf-8 -*-
# diff_extractor
import re
from unidiff import PatchSet


def extract_added_lines(data):
    return extract_lines(data, lambda line: line.is_added)


def extract_removed_lines(data):
    return extract_lines(data, lambda line: line.is_removed)


def extract_lines(data, query=None, normalizer=None):
    query = is_added_or_removed if query is None else query
    normalizer = _normalize if normalizer is None else normalizer
    patches = PatchSet(data)
    return (normalizer(line)
            for files in patches for hunks in files for line in hunks
            if query(line))


def is_added_or_removed(line):
    return line.is_added or line.is_removed


def _normalize(str):
    return re.sub(r'[ \t]+', ' ', str.value.strip())


if __name__ == '__main__':
    with open('sample.diff', 'r') as diff:
        diff_data = diff.readlines()
        print extract_added_lines(diff_data)
        print extract_removed_lines(diff_data)
