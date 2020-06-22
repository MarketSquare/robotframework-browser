from typing import Callable, ContextManager, List

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from Browser.generated.playwright_pb2_grpc import PlaywrightStub
from Browser.generated.playwright_pb2 import Empty
import Browser.generated.playwright_pb2 as playwright_pb2


class Control:
    def __init__(
        self,
        insecure_stub: Callable[[], ContextManager[PlaywrightStub]],
        supported_browsers: List[str],
    ):
        self._insecure_stub = insecure_stub
        self.supported_browsers = supported_browsers

    @keyword
    def open_browser(self, browser="Chrome", url=None):
        """Opens a new browser instance to the optional ``url``.
        The ``browser`` argument specifies which browser to use. The
        supported browsers are listed in the table below. The browser names
        are case-insensitive and some browsers have multiple supported names.
        |    = Browser =    |        = Name(s) =        |
        | Firefox           | firefox                   |
        | Google Chrome     | chrome                    |
        | WebKit            | webkit                    |

        """
        browser_ = browser.lower().strip()
        if browser_ not in self.supported_browsers:
            raise ValueError(
                f"{browser} is not supported, "
                f'it should be one of: {", ".join(self.supported_browsers)}'
            )
        with self._insecure_stub() as stub:
            response = stub.OpenBrowser(
                playwright_pb2.openBrowserRequest(url=url or "", browser=browser_)
            )
            logger.info(response.log)

    @keyword
    def close_browser(self):
        """Closes the current browser."""
        with self._insecure_stub() as stub:
            response = stub.CloseBrowser(Empty())
            logger.info(response.log)

    @keyword
    def go_to(self, url: str):
        """Navigates the current browser tab to the provided ``url``."""
        with self._insecure_stub() as stub:
            response = stub.GoTo(playwright_pb2.goToRequest(url=url))
            logger.info(response.log)

    @keyword
    def take_page_screenshot(self, path: str):
        with self._insecure_stub() as stub:
            response = stub.Screenshot(playwright_pb2.screenshotRequest(path=path))
            logger.info(response.log)
