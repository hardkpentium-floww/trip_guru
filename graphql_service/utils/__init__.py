import logging


def get_logger(file_path: str):
    return logging.getLogger(file_path)
