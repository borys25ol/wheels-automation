import logging
import os

import config


def create_logger(logger_name):
    """
    Initialize a logger.
    """
    config_name = os.getenv("CONFIG") or "dev"

    logger = logging.getLogger(logger_name)

    if not os.path.exists(config.LOGGER_PATH.parent):
        os.makedirs(config.LOGGER_PATH.parent, exist_ok=True)

    if config_name == "prod":
        logging.basicConfig(
            format=config.LOGGER_FORMAT, filename=config.LOGGER_PATH,
        )
    else:
        logging.basicConfig(format=config.LOGGER_FORMAT)

    logger.setLevel(level=logging.INFO)

    return logger
