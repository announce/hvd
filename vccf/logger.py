import sys
from logging import basicConfig, getLogger, Formatter, StreamHandler, DEBUG


class Logger:
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def __init__(self):
        pass


    @classmethod
    def create(cls, name, level=DEBUG, handler=None, fmt=FORMAT):
        basicConfig()
        # if handler is None:
        #     handler = StreamHandler(stream=sys.stdout)
        logger = getLogger(name)
        # handler.setLevel(level)
        logger.setLevel(level)
        # formatter = Formatter(fmt)
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        return logger


