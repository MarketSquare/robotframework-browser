from typing import Any

from robot.api import logger  # type: ignore
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS  # type: ignore

if not EXECUTION_CONTEXTS.current:
    setattr(logger, "info", lambda msg, html: print(f"INFO: {msg}"))
    setattr(logger, "debug", lambda msg, html: print(f"DEBUG: {msg}"))
    setattr(logger, "warn", lambda msg, html: print(f"WARN: {msg}"))


def info(msg: Any, html=False):
    logger.info(msg, html)


def debug(msg: Any, html=False):
    logger.debug(msg, html)


def warn(msg: Any, html=False):
    logger.warn(msg, html)
