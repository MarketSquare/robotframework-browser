from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.time_conversion import timestr_to_millisecs


class Control(LibraryComponent):
    """Keywords to do things on the current browser page and modify the page
    """

    @keyword(tags=["BrowserControl"])
    def go_forward(self):
        """Navigates to the next page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoForward(Request.Empty())
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def go_back(self):
        """Navigates to the previous page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoBack(Request.Empty())
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def go_to(self, url: str):
        """Navigates to the given ``url``."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoTo(Request().Url(url=url))
            logger.info(response.log)

    @keyword
    def take_page_screenshot(self, path: str = ""):
        """Takes screenshot of the current window and saves it to ``path``.

        The default path is the Robot Framework output directory.
        """
        if not path:
            path = self.library.get_screenshot_path
        logger.info(f"Taking screenshot into ${path}")
        with self.playwright.grpc_channel() as stub:
            response = stub.TakeScreenshot(Request().ScreenshotPath(path=path))
            logger.info(
                f"Saved screenshot in <a href='file://{response.body}''>{response.body}</a>",
                html=True,
            )

    @keyword(tags=["BrowserControl"])
    def set_timeout(self, timeout: str):
        """Sets the timeout used by most input and getter keywords.

        Timeout of is for current playwright context.
        """
        parsed_timeout = timestr_to_millisecs(timeout)
        with self.playwright.grpc_channel() as stub:
            response = stub.SetTimeout(Request().Timeout(timeout=parsed_timeout))
            logger.info(response.log)

    @keyword(tags=["PageContent"])
    def add_style_tag(self, content: str):
        """Adds a <style type="text/css"> tag with the content.

        ``content``: Raw CSS content to be injected into frame.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.AddStyleTag(Request().StyleTag(content=content))
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def set_viewport_size(self, width: int, height: int):
        """Sets current Pages viewport size to specified dimensions.

        In the case of multiple pages in a single browser,
        each page can have its own viewport size. However,
        `New Context` allows to set viewport size (and more) for all
        later opened pages in the context at once.

        `Set Viewport Size` will resize the page.
        A lot of websites don't expect phones to change size,
        so you should set the viewport size before navigating to
        the page with `New Context` before opening the page itself."""
        with self.playwright.grpc_channel() as stub:
            response = stub.SetViewportSize(
                Request().Viewport(height=height, width=width)
            )
            logger.info(response.log)
