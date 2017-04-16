from unidiff.errors import UnidiffParseError
from logger import Logger
from app_error import AppError
from line_extractor import LineExtractor
from bow_num import BowNum


class PatchNormalizer:
    def __init__(self):
        self.logger = Logger.create(name=__name__)
        self.bow_num = BowNum()
        self.line_extractor = LineExtractor()

    def normalize_patches(self, patches):
        """
        :param unicode patches: unicode(patch, 'utf-8')
        :rtype: unicode
        :return:
        """
        self.logger.info('Start extracting lines...')
        clean_patches = [u''] * len(patches)
        invalid_patches = []
        for index, patch in enumerate(patches):
            try:
                clean_patches[index] = self.bow_num.bin_str(u' '.join(
                    self.line_extractor.extract_lines(patch.splitlines())
                ))
            except UnidiffParseError as e:
                # @todo Recover 445 patches at total in vcc_data.npz
                invalid_patches.append((index, patch, e))

        if len(clean_patches) == len(invalid_patches):
            raise AppError('Failed to proceed all patches. Check diff format.')
        self.logger.info('Completed extracting lines including #%d invalid patches.' % len(invalid_patches))
        return clean_patches


if __name__ == '__main__':
    pass
