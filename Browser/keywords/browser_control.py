from typing import Optional, Union

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils.time_conversion import timestr_to_millisecs


class Control(LibraryComponent):
    """Keywords to do things on the current browser page and modify the page
    """

    @keyword
    def go_forward(self):
        """Navigates to the next page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoForward(Request.Empty())
            self.info(response.log)

    @keyword
    def go_back(self):
        """Navigates to the previous page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoBack(Request.Empty())
            self.info(response.log)

    @keyword
    def go_to(self, url: str):
        """Navigates to the given ``url``."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoTo(Request().Url(url=url))
            self.info(response.log)

    @keyword
    def take_page_screenshot(self, path: Optional[str] = None):
        """Takes screenshot of the current window and saves it to ``path``.

        The default path is the Robot Framework output directory.
        """
        if path is None:
            path = self.library.get_screenshot_path
        self.info(f"Taking screenshot into ${path}")
        with self.playwright.grpc_channel() as stub:
            response = stub.TakeScreenshot(Request().ScreenshotPath(path=path))
            self.info(
                f"Saved screenshot in <a href='file://{response.body}''>{response.body}</a>",
                html=True,
            )

    @keyword
    def set_timeout(self, timeout: str):
        """Sets the timeout used by most input and getter keywords.

        Technically this is the timeout of current playwright context.
        """
        parsed_timeout = timestr_to_millisecs(timeout)
        with self.playwright.grpc_channel() as stub:
            response = stub.SetTimeout(Request().Timeout(timeout=parsed_timeout))
            self.info(response.log)

    @keyword
    def add_style_tag(self, content: str):
        """Adds a <style type="text/css"> tag with the content.

        ``content``: Raw CSS content to be injected into frame.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.AddStyleTag(Request().StyleTag(content=content))
            self.info(response.log)

    @keyword
    def highlight_element(self, selector: str, duration: Union[str, int] = "5s"):
        """Adds a red highlight to elements matched by ``selector`` for ``duration``"""
        with self.playwright.grpc_channel() as stub:
            duration_ms = timestr_to_millisecs(duration)
            response = stub.HighlightElements(
                Request().ElementSelectorWithDuration(
                    selector=selector, duration=duration_ms
                )
            )
            self.info(response.log)

    @keyword
    def switch_active_page(self, index: int):
        """Switches the active browser page to another open page by ``index``.

            Newly opened pages get appended to the end of the list
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchActivePage(Request().Index(index=index))
            self.info(response.log)

    @keyword
    def auto_activate_pages(self):
        """Toggles automatically changing active page to latest opened page """
        with self.playwright.grpc_channel() as stub:
            response = stub.AutoActivatePages(Request().Empty())
            self.info(response.log)
