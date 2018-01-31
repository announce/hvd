from logging import getLogger, Formatter, StreamHandler, FileHandler,DEBUG
from os import path


class Logger:
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def __init__(self):
        pass

    @classmethod
    def create(cls, name, level=DEBUG, filename=None, fmt=FORMAT):
        formatter = Formatter(fmt)
        root_logger = getLogger(name)
        root_logger.setLevel(level)

        if filename is not None:
            file_handler = FileHandler(path.join('logs', '%s.log' % filename))
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        return root_logger
