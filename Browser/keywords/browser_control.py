from pathlib import Path

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
        """Navigates to the given ``url``.

        ``url`` <str> URL to be navigated to. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GoTo(Request().Url(url=url))
            logger.info(response.log)

    def _get_screenshot_path(self, filename: str) -> Path:
        directory = self.library.outputdir
        # Filename didn't contain {index}
        if "{index}" not in filename:
            return Path(directory) / filename
        index = 0
        while True:
            logger.info(index)
            index += 1
            indexed = Path(filename.replace("{index}", str(index)))
            logger.debug(indexed)
            path = Path(directory) / indexed
            # Unique path was found
            if not path.with_suffix(".png").is_file():
                return path

    @keyword
    def take_screenshot(self, filename: str = "", selector: str = ""):
        """Takes a screenshot of the current window and saves it to ``path``. Saves it as a png.

        ``filename`` <str> Filename into which to save. The file will be saved into the robot framework output directory by default.
        String ``{index}`` in path will be replaced with a rolling number. Use this to not override filenames.

        ``selector`` <str> Take a screenshot of the element matched by selector.
        If not provided take a screenshot of current viewport.
        """
        string_path_no_extension = str(self._get_screenshot_path(filename))
        logger.debug(f"Taking screenshot into ${filename}")
        with self.playwright.grpc_channel() as stub:
            response = stub.TakeScreenshot(
                Request().ScreenshotOptions(
                    path=string_path_no_extension, selector=selector
                )
            )
            logger.info(
                f"Saved screenshot in <a href='file://{response.body}''>{response.body}</a>",
                html=True,
            )
            return response.body

    @keyword(tags=["BrowserControl"])
    def set_browser_timeout(self, timeout: str) -> str:
        """Sets the timeout used by most input and getter keywords.

        ``timeout`` <str> Timeout of it is for current playwright context. **Required**

        Returns the previous value of the timeout.
        """
        parsed_timeout = timestr_to_millisecs(timeout)
        old_timeout = self.timeout
        self.timeout = timeout
        with self.playwright.grpc_channel() as stub:
            response = stub.SetTimeout(Request().Timeout(timeout=parsed_timeout))
            logger.info(response.log)
        return old_timeout

    @keyword(tags=["BrowserControl"])
    def set_retry_assertions_until(self, timeout: str) -> str:
        """Sets the timeout used in retrying assertions when they fail.

        ``timeout`` <str>

        Returns the previous value of the retry_assertions_until.
        """
        old_retry_assertions_until = self.retry_assertions_until
        self.retry_assertions_until = timeout
        return old_retry_assertions_until

    @keyword(tags=["PageContent"])
    def add_style_tag(self, content: str):
        """Adds a <style type="text/css"> tag with the content.

        ``content`` <str> Raw CSS content to be injected into frame. **Required**
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
        the page with `New Context` before opening the page itself.

        ``width`` <int> Sets the width size. **Required**

        ``height`` <int> Sets the heigth size. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SetViewportSize(
                Request().Viewport(height=height, width=width)
            )
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def set_offline(self, offline: bool = True):
        """ Toggles current Context's offline emulation.

        ``offline`` <bool> Toggles the offline mode. Set to False to switch back
        to online mode. Defaults to True.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SetOffline(Request().Bool(value=offline))
            logger.info(response.log)
