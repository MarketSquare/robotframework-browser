import json
from enum import Enum
from typing import Dict, List, Optional, TypedDict

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..utils.meta_python import locals_to_params
from ..generated.playwright_pb2 import Request


class SupportedBrowsers(Enum):
    chromium = "chromium"
    firefox = "firefox"
    webkit = "webkit"


# Can't define with Enum class syntax because of the dash
ColorScheme = Enum("ColorScheme", ["dark", "light", "no-preference"])

ViewportDimensions = TypedDict("ViewportDimensions", {"width": int, "height": int})


class PlaywrightState(LibraryComponent):
    """Keywords to manage Playwright side Browsers, Contexts and Pages.
    """

    @keyword
    def open_browser(
        self,
        url=None,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: Optional[bool] = True,
    ):
        """Opens a new browser instance.

        Creates a new browser, context and page with specified settings.
            Only supports some of the settings Create _ Keywords do

        If ``url`` is provided, navigates there.

        The optional ``browser`` argument specifies which browser to use. The
        supported browsers are listed in the table below. The browser names
        are case-sensitive.
        |   = Value =     |        = Name(s) =                                   |
        | firefox         | [https://www.mozilla.org/en-US/firefox/new|Firefox]  |
        | chromium        | [https://www.chromium.org/Home|Chromium]             |
        | webkit          | [https://webkit.org/|webkit]                         |

        """

        self.create_browser(browser, headless=headless)
        self.create_context()
        self.create_page(url)

    @keyword
    def close_browser(self):
        """Closes the current browser. Activated browser is set to first active browser.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseBrowser(Request.Empty())
            self.info(response.log)

    @keyword
    def close_all_browsers(self):
        """Closes all open browsers."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseAllBrowsers(Request().Empty())
            self.info(response.log)

    @keyword
    def close_context(self):
        """Closes the current Context. Activated context is set to first active context."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseContext(Request().Empty())
            self.info(response.log)

    @keyword
    def close_page(self):
        """Closes the current Page. Activated page is set to first active page."""
        with self.playwright.grpc_channel() as stub:
            response = stub.ClosePage(Request().Empty())
            self.info(response.log)

    @keyword
    def create_browser(
        self,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        executablePath: Optional[str] = None,
        args: Optional[List[str]] = None,
        ignoreDefaultArgs: Optional[List[str]] = None,
        handleSIGINT: Optional[bool] = None,
        handleSIGTERM: Optional[bool] = None,
        handleSIGHUP: Optional[bool] = None,
        timeout: Optional[int] = None,
        env: Optional[Dict] = None,
        headless: Optional[bool] = None,
        devtools: Optional[bool] = None,
        proxy: Optional[Dict] = None,
        downloadsPath: Optional[str] = None,
        slowMo: Optional[int] = None,
    ):
        """Create a new playwright Browser with specified options.

        Returns a stable identifier for the created browser.

        A Browser is the Playwright object that controls a single Browser process.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsertypelaunchoptions |Playwright browserType.launch]
        for a full list of supported options.
        """
        params = locals_to_params(locals())
        options = json.dumps(params, default=str)
        self.info(options)

        with self.playwright.grpc_channel() as stub:

            response = stub.CreateBrowser(
                Request().Browser(browser=browser.value, rawOptions=options)
            )
            self.info(response.log)
            return response.body

    @keyword
    def create_context(
        self,
        hideRfBrowser=False,
        viewport: Optional[ViewportDimensions] = None,
        ignoreHTTPSErrors: Optional[bool] = None,
        javaScriptEnabled: Optional[bool] = None,
        bypassCSP: Optional[bool] = None,
        userAgent: Optional[str] = None,
        locale: Optional[str] = None,
        timezoneId: Optional[str] = None,
        geolocation: Optional[Dict] = None,
        permissions: Optional[List[str]] = None,
        extraHTTPHeaders: Optional[Dict[str, str]] = None,
        offline: Optional[bool] = None,
        httpCredentials: Optional[Dict] = None,
        deviceScaleFactor: Optional[int] = None,
        isMobile: Optional[bool] = None,
        hasTouch: Optional[bool] = None,
        colorScheme: Optional[ColorScheme] = None,
        acceptDownloads: Optional[bool] = None,
    ):
        """Create a new BrowserContext with specified options.

        Returns a stable identifier for the created context.

        Value of ``viewport`` should be an object or a string representation of an object like {'height': 720, 'width': 1280}

        A BrowserContext is the Playwright object that controls a single browser profile.
        Within a context caches and cookies are shared.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsernewcontextoptions|Playwright browser.newContext]
        for a list of supported options.
        If there's no open Browser will open one. Does not create pages.
        """
        params = locals_to_params(locals())
        options = json.dumps(params, default=str)
        self.info(options)
        with self.playwright.grpc_channel() as stub:
            response = stub.CreateContext(
                Request().Context(hideRfBrowser=hideRfBrowser, rawOptions=options)
            )
            self.info(response.log)
            return response.body

    @keyword
    def create_page(self, url: Optional[str] = None):
        """Open a new Page. A Page is the Playwright equivalent to a tab.

            Returns a stable identifier for the created page.
            If ``url`` parameter is specified will open the new page to the specified URL.

        """

        with self.playwright.grpc_channel() as stub:
            response = stub.CreatePage(Request().Url(url=url))
            self.info(response.log)
            return response.body

    @keyword
    def switch_page(self, index: int):
        """Switches the active browser page to another open page by ``index``.

            Returns a stable identifier for the previous page.

            Newly opened pages get appended to the end of the list
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchPage(Request().Index(index=index))
            self.info(response.log)
            return response.body

    @keyword
    def auto_activate_pages(self):
        """Toggles automatically changing active page to latest opened page."""
        with self.playwright.grpc_channel() as stub:
            response = stub.AutoActivatePages(Request().Empty())
            self.info(response.log)

    @keyword
    def switch_browser(self, index: int):
        """Switches the currently active Browser to another open Browser.

            Returns a stable identifier for the previous browser.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchBrowser(Request().Index(index=index))
            self.info(response.log)
            return response.body

    @keyword
    def switch_context(self, index: int):
        """ Switches the active BrowserContext to another open context.

            Returns a stable identifier for the previous context.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchContext(Request().Index(index=index))
            self.info(response.log)
            return response.body
