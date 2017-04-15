#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from os import path
from unidiff import PatchSet


class LineExtractor:
    CPP_EXTENSIONS = ('.cc', '.cpp', '.cxx', '.C', '.c++', '.h', '.hh', '.hpp', '.hxx', '.h++')
    C_EXTENSIONS = ('.c', '.h')

    def __init__(self):
        pass

    @classmethod
    def extract_added_lines(cls, data):
        return cls.extract_lines(data, lambda line: line.is_added)

    @classmethod
    def extract_removed_lines(cls, data):
        return cls.extract_lines(data, lambda line: line.is_removed)

    @classmethod
    def extract_lines(cls, data, query=None, normalizer=None):
        query = cls.is_added_or_removed if query is None else query
        normalizer = cls.normalize if normalizer is None else normalizer
        patch = PatchSet(data)
        return (normalizer(line)
                for file in patch
                if cls.has_target_extension(file)
                for hunk in file
                if cls.is_target_hunk(hunk)
                for line in hunk
                if query(line))

    @classmethod
    def is_added_or_removed(cls, line):
        return line.is_added or line.is_removed

    @classmethod
    def normalize(cls, str):
        return re.sub(r'[ \t]+', ' ', str.value.strip())

    @classmethod
    def has_target_extension(cls, file):
        # Only need C/C++ file
        _, extension = path.splitext(file.path)
        return extension in (cls.CPP_EXTENSIONS + cls.C_EXTENSIONS)

    @classmethod
    def is_target_hunk(cls, _):
        return True

