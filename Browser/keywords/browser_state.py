import json
from enum import Enum, auto
from typing import Optional

from robot.api import logger  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..generated.playwright_pb2 import Request


class SupportedBrowsers(Enum):
    chromium = auto()
    firefox = auto()
    webkit = auto()


class State:
    """Keywords to manage Playwright side Browsers, Contexts and Pages.
    """

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
    def new_browser(
        self, browser_type=SupportedBrowsers.chromium, **kwargs,
    ):
        with self.playwright.grpc_channel() as stub:
            options = json.dumps(kwargs)
            response = stub.NewBrowser(
                Request().NewBrowser(browser=browser_type.name, rawOptions=options)
            )
            logger.info(response.log)

    @keyword
    def new_context(
        self, **kwargs,
    ):
        with self.playwright.grpc_channel() as stub:
            options = json.dumps(kwargs)
            logger.info(options)
            response = stub.NewContext(Request().NewContext(rawOptions=options))
            logger.info(response.log)

    @keyword
    def new_page(self, url: Optional[str] = None):
        with self.playwright.grpc_channel() as stub:
            response = stub.NewPage(Request().Url(url=url))
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
    def switch_browser(self, index: int):
        raise NotImplementedError("Functionality not implemented yet")

    @keyword
    def switch_context(self, index: int):
        raise NotImplementedError("Functionality not implemented yet")
