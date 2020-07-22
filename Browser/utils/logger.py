from robot.api import logger  # type: ignore


def info(msg: str, html=False):
    logger.info(msg, html)


def debug(msg: str, html=False):
    logger.debug(msg, html)


def warn(msg: str, html=False):
    logger.warn(msg, html)
