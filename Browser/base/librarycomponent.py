from robot.api import logger  # type: ignore


class LibraryComponent:
    def __init__(self, library):
        self.library = library

    def info(self, msg: str, html=False):
        logger.info(msg, html)

    def debug(self, msg: str, html=False):
        logger.debug(msg, html)
