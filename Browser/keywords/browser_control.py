import json
from enum import Enum, auto
from typing import Optional

from robot.api import logger  # type: ignore
from robot.utils.robottime import timestr_to_secs  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated.playwright_pb2 import Request


class SupportedBrowsers(Enum):
    chromium = auto()
    firefox = auto()
    webkit = (auto(),)


class Control:
    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def open_browser(
        self, url=None, browser=SupportedBrowsers.chromium, headless: bool = True
    ):
        """Opens a new browser instance.

        If ``url`` is provided, navigates there.

        The optional ``browser`` argument specifies which browser to use. The
        supported browsers are listed in the table below. The browser names
        are case-insensitive.
        |   = Browser =   |        = Name(s) =        |
        | Firefox         | firefox                   |
        | Chromium        | chromium                  |
        | WebKit          | webkit                    |

        """

        with self.playwright.grpc_channel() as stub:
            response = stub.OpenBrowser(
                Request().NewBrowser(
                    url=url or "", browser=browser.name, headless=headless
                )
            )
            logger.info(response.log)

    @keyword
    def close_browser(self):
        """Closes the current browser."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseBrowser(Request.Empty())
            logger.info(response.log)

    @keyword
    def go_forward(self):
        """Navigates to the next page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoForward(Request.Empty())
            logger.info(response.log)

    @keyword
    def go_back(self):
        """Navigates to the previous page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoBack(Request.Empty())
            logger.info(response.log)

    @keyword
    def go_to(self, url: str):
        """Navigates to the given ``url``."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoTo(Request().Url(url=url))
            logger.info(response.log)

    @keyword
    def take_page_screenshot(self, path: Optional[str] = None):
        """Takes screenshot of the current window and saves it to ``path``.

        The default path is the Robot Framework output directory.
        """
        if path is None:
            path = self.library.get_screenshot_path
        logger.info(f"Taking screenshot into ${path}")
        with self.playwright.grpc_channel() as stub:
            response = stub.TakeScreenshot(Request().ScreenshotPath(path=path))
            logger.info(
                f"Saved screenshot in <a href='file://{response.body}''>{response.body}</a>",
                html=True,
            )

    @keyword
    def set_timeout(self, timeout: str):
        """Sets the timeout used by most input and getter keywords.

        Technically this is the timeout of current playwright context.
        """
        parsed_timeout = float(timestr_to_secs(timeout)) * 1000
        with self.playwright.grpc_channel() as stub:
            response = stub.SetTimeout(Request().Timeout(timeout=parsed_timeout))
            logger.info(response.log)

    @keyword
    def add_style_tag(self, content: str):
        """Adds a <style type="text/css"> tag with the content.

        ``content``: Raw CSS content to be injected into frame.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.AddStyleTag(Request().StyleTag(content=content))
            logger.info(response.log)

    @keyword
    def highlight_element(self, selector: str, duration: Optional[str] = "5s"):
        """Adds a red highlight to elements matched by ``selector`` for ``duration``"""
        with self.playwright.grpc_channel() as stub:
            duration_ms: int = int(timestr_to_secs(duration) * 1000)
            response = stub.HighlightElements(
                Request().ElementSelectorWithDuration(
                    selector=selector, duration=duration_ms
                )
            )
            logger.info(response.log)

    @keyword
    def switch_active_page(self, index: int):
        """Switches the active browser page to another open page by ``index``.

            Newly opened pages get appended to the end of the list
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchActivePage(Request().Index(index=index))
            logger.info(response.log)

    @keyword
    def auto_activate_pages(self):
        """Toggles automatically changing active page to latest opened page """
        with self.playwright.grpc_channel() as stub:
            response = stub.AutoActivatePages(Request().Empty())
            logger.info(response.log)

    @keyword
    def new_browser(
        self,
        browser_type=SupportedBrowsers.chromium,
        **kwargs,
        # TODO: Remove commented code before merging
        # args: Optional[List[str]] = None,
        # headless: Optional[bool] = None,
        # devtools: Optional[bool] = None,
        # proxy: Optional[Dict] = None,
        # downloadsPath: Optional[str] = None,
        # slowMo: Optional[int] = None,
    ):
        with self.playwright.grpc_channel() as stub:
            options = json.dumps(kwargs)
            response = stub.NewBrowser(
                Request().NewBrowser(browser=browser_type.name, rawOptions=options)
            )
            logger.info(response.log)

    @keyword
    def new_context(
        self,
        **kwargs,
        # TODO: Remove commented code before merging
        # viewport: Optional[Dict[str, int]] = None,
        # bypassCSP: Optional[bool] = None,
        # userAgent: Optional[str] = None,
        # locale: Optional[str] = None,
        # timezoneId: Optional[str] = None,
        # geolocation: Optional[Dict] = None,
        # extraHTTPHeaders: Optional[Dict[str, str]] = None,
        # offline: Optional[bool] = None,
        # httpCredentials: Optional[Dict] = None,
        # isMobile: Optional[bool] = None,
        # hasTouch: Optional[bool] = None,
        # acceptDownloads: Optional[bool] = None,
    ):
        with self.playwright.grpc_channel() as stub:
            options = json.dumps(kwargs)
            logger.info(options)
            response = stub.NewContext(Request().NewContext(rawOptions=options))
            logger.info(response.log)

    @keyword
    def new_page(self, url: Optional[str] = None):
        with self.playwright.grpc_channel() as stub:
            response = stub.NewPage(Request().NewPage(url=url))
            logger.info(response.log)
