from typing import Optional

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated import playwright_pb2


class Control:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def open_browser(self, url=None, browser="Chrome"):
        """Opens a new browser instance.
        The optional ``url`` argument specifies what to open.
        The optional ``browser`` argument specifies which browser to use. The
        supported browsers are listed in the table below. The browser names
        are case-insensitive and some browsers have multiple supported names.
        |    = Browser =    |        = Name(s) =        |
        | Firefox           | firefox                   |
        | Google Chrome     | chrome                    |
        | WebKit            | webkit                    |

        """
        browser_ = browser.lower().strip()
        if browser_ not in self.library.SUPPORTED_BROWSERS:
            raise ValueError(
                f"{browser} is not supported, "
                f'it should be one of: {", ".join(self.library.SUPPORTED_BROWSERS)}'
            )
        with self.playwright.grpc_channel() as stub:
            response = stub.OpenBrowser(
                playwright_pb2.openBrowserRequest(url=url or "", browser=browser_)
            )
            logger.info(response.log)

    @keyword
    def close_browser(self):
        """Closes the current browser."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseBrowser(playwright_pb2.Empty())
            logger.info(response.log)

    @keyword
    def go_to(self, url: str):
        """Navigates the current browser tab to the provided ``url``."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoTo(playwright_pb2.goToRequest(url=url))
            logger.info(response.log)

    @keyword
    def take_page_screenshot(self, path: Optional[str] = None):
        """ Take screenshot of current browser state and saves it to path.
            By default saves to robot output dir.
        """
        if path is None:
            path = self.library.get_screenshot_path
        logger.info(f"Taking screenshot into ${path}")
        with self.playwright.grpc_channel() as stub:
            response = stub.Screenshot(playwright_pb2.screenshotRequest(path=path))
            logger.info(response.log)
