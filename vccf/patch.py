from unidiff.errors import UnidiffParseError
from logger import Logger
from app_error import AppError
from line_extractor import LineExtractor
from word_extractor import WordExtractor
from bow_num import BowNum
from column import Column


class Patch:
    WORD_ONLY = True

    def __init__(self, data):
        """
        :param data
        """
        self.logger = Logger.create(name=__name__)
        self.bow_num = BowNum()
        self.line_extractor = LineExtractor()
        self.word_extractor = WordExtractor()
        self.data = data

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

    def extract(self, lines):
        if self.WORD_ONLY:
            return u' '.join(
                [self.word_extractor.extract_words(l) for l in self.line_extractor.extract_lines(lines)]
            )
        else:
            return self.bow_num.bin_str(u' '.join(
                self.line_extractor.extract_lines(lines)
            ))


if __name__ == '__main__':
    pass
