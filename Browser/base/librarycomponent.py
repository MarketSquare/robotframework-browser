from robot.api import logger  # type: ignore
from typing import Any

TRUE_STRINGS = {"TRUE", "YES", "ON", "1", "CHECKED"}
FALSE_STRINGS = {"FALSE", "NO", "OFF", "0", "UNCHECKED", "NONE", ""}


class LibraryComponent:
    def __init__(self, library):
        """Base class exposing attributes from the common context.

        :param library: The library itself as a context object.
        :type library: Browser.Browser
        """
        self.library = library

    def info(self, msg: str, html=False):
        logger.info(msg, html)

    def debug(self, msg: str, html=False):
        logger.debug(msg, html)

    def is_truthy(self, item: Any) -> bool:
        if isinstance(item, str):
            return item.upper() not in FALSE_STRINGS
        return bool(item)

    def is_falsy(self, item: Any) -> bool:
        return not self.is_truthy(item)

    @property
    def playwright(self):
        return self.library.playwright
