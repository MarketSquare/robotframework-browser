from robot.api import logger  # type: ignore


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

    @property
    def playwright(self):
        return self.library.playwright
