
import re
from logger import Logger
# from app_error import AppError


class WordExtractor:
    TOKEN_PATTERN = r'(?u)\b\w\w+\b'

    def __init__(self):
        self.logger = Logger.create(name=__name__)
        self.keywords = self.create_keywords()

    @classmethod
    def create_keywords(cls):
        # http://en.cppreference.com/w/cpp/keyword
        with open('cpp_keywords.txt') as f:
            cpp_keywords = f.readlines()
        return [w.strip() for w in cpp_keywords]

    def extract_words(self, line):
        text_list = re.findall(self.TOKEN_PATTERN, line)
        return u' '.join([text.lower() for text in text_list if text in self.keywords])

    def suffix_words(self, line, suffix):
        text_list = re.findall(self.TOKEN_PATTERN, line)
        return u' '.join(["%s_%s" % (text, suffix) for text in text_list])


if __name__ == '__main__':
    we = WordExtractor()
    ww = we.extract_words(['foo', 'bar', 'int function() { return aaa }', '', 'vvv'])
    print(ww)
    # pass
