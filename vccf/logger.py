import sys
from logging import basicConfig, getLogger, Formatter, StreamHandler, DEBUG


class Logger:
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def __init__(self):
        pass

    @classmethod
    def create(cls, name, level=DEBUG, filename=None, fmt=FORMAT):
        basicConfig(filename=filename,
                    format=fmt)
        logger = getLogger(name)
        logger.setLevel(level)
        return logger
