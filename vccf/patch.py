import uuid
from enum import Enum, unique
from unidiff.errors import UnidiffParseError
from logger import Logger
from app_error import AppError
from line_extractor import LineExtractor
from word_extractor import WordExtractor
from bow_num import BowNum
from column import Column


class Patch:
    UUID_ADDED, UUID_REMOVED, UUID_BOTH = [uuid.uuid4().hex for _ in range(3)]

    @unique
    class Mode(Enum):
        RESERVED_WORD_ONLY = 1
        LINE_TYPE_SENSITIVE = 2
        LINE_TYPE_INSENSITIVE = 3

    def __init__(self, data, mode):
        """
        :param data
        """
        self.logger = Logger.create(name=__name__)
        self.bow_num = BowNum()
        self.line_extractor = LineExtractor()
        self.word_extractor = WordExtractor()
        self.data = data
        self.mode = mode

    def normalized(self):
        """
        Make sure patches are encoded in unicode: unicode(patch, 'utf-8')
        :rtype: unicode
        :return:
        """
        patches = self.data[:, Column.patch]
        self.logger.info('Start extracting lines...')
        clean_patches = [u''] * len(patches)
        invalid_patches = []
        for index, patch in enumerate(patches):
            try:
                clean_patches[index] = self.extract(patch.splitlines())
            except UnidiffParseError as e:
                # @todo Recover 445 patches at total in vcc_data.npz
                invalid_patches.append((index, patch, e))

        if len(clean_patches) == len(invalid_patches):
            raise AppError('Failed to proceed all patches. Check diff format.')
        self.logger.info('Completed extracting lines including #%d invalid patches.' % len(invalid_patches))
        return clean_patches

    def sensitive(self, lines, suffix):
        return [
            self.word_extractor.suffix_words(self.bow_num.bin_str(l), suffix)
            for l in lines
        ]

    def extract(self, lines):
        if self.Mode.RESERVED_WORD_ONLY:
            return u' '.join(
                [self.word_extractor.extract_words(l) for l in self.line_extractor.extract_lines(lines)]
            )
        elif self.Mode.LINE_TYPE_INSENSITIVE:
            return self.bow_num.bin_str(u' '.join(
                self.line_extractor.extract_lines(lines)
            ))
        elif self.Mode.LINE_TYPE_SENSITIVE:
            b = self.sensitive(self.line_extractor.extract_lines(lines), self.UUID_BOTH)
            b.extend(self.sensitive(self.line_extractor.extract_added_lines(lines), self.UUID_ADDED))
            b.extend(self.sensitive(self.line_extractor.extract_removed_lines(lines), self.UUID_REMOVED))
            return b
        else:
            raise AppError("Choose mode from %r" % self.Mode.__name__)


if __name__ == '__main__':
    pass
