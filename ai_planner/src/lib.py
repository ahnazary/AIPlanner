import logging

from config import LOG_LEVEL


def custom_logger():
    """
    Function that creates a logger
    The logger emits logs with a level of 20 (INFO) by default
    The log level can be changed by changing the value of the
    LOG_LEVEL variable in the config.py file
    """
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)

    return logger
