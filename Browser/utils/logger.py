from typing import Any

from robot.api import logger  # type: ignore


def info(msg: Any, html=False):
    logger.info(msg, html)


def debug(msg: Any, html=False):
    logger.debug(msg, html)


def warn(msg: Any, html=False):
    logger.warn(msg, html)


def error(msg: Any, html=False):
    logger.error(msg, html)
