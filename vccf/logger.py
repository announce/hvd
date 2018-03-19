from logging import getLogger, Formatter, StreamHandler, FileHandler,DEBUG
import os


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
            Logger.ensure_directory_exists(path=filename)
            file_handler = FileHandler(filename)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        return root_logger

    @classmethod
    def ensure_directory_exists(cls, path):
        dirs = os.path.dirname(path)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
