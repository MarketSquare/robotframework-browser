import json
from enum import Enum
from typing import Dict, List, Optional, TypedDict

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..utils.meta_python import locals_to_params
from ..utils.time_conversion import timestr_to_millisecs
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

    @keyword(tags=["BrowserControl"])
    def open_browser(
        self,
        url=None,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: bool = True,
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

        self.new_browser(browser, headless=headless)
        self.new_context()
        self.new_page(url)

    @keyword(tags=["BrowserControl"])
    def close_browser(self):
        """Closes the current browser. Activated browser is set to first active browser.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseBrowser(Request.Empty())
            self.info(response.log)

    @keyword(tags=["BrowserControl"])
    def close_all_browsers(self):
        """Closes all open browsers."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseAllBrowsers(Request().Empty())
            self.info(response.log)

    @keyword(tags=["BrowserControl"])
    def close_context(self):
        """Closes the current Context. Activated context is set to first active context."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseContext(Request().Empty())
            self.info(response.log)

    @keyword(tags=["BrowserControl"])
    def close_page(self):
        """Closes the current Page. Activated page is set to first active page."""
        with self.playwright.grpc_channel() as stub:
            response = stub.ClosePage(Request().Empty())
            self.info(response.log)

    @keyword(tags=["BrowserControl"])
    def new_browser(
        self,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: bool = True,
        executablePath: Optional[str] = None,
        args: Optional[List[str]] = None,
        ignoreDefaultArgs: Optional[List[str]] = None,
        proxy: Optional[Dict] = None,
        downloadsPath: Optional[str] = None,
        handleSIGINT: bool = True,
        handleSIGTERM: bool = True,
        handleSIGHUP: bool = True,
        timeout: str = "30 seconds",
        env: Optional[Dict] = None,
        devtools: bool = False,
        slowMo: str = "0 seconds",
    ):
        """Create a new playwright Browser with specified options.

        Returns a stable identifier for the created browser.

        A Browser is the Playwright object that controls a single Browser process.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsertypelaunchoptions |Playwright browserType.launch]
        for a full list of supported options.
        """
        params = locals_to_params(locals())
        if timeout:
            params["timeout"] = timestr_to_millisecs(timeout)
        if slowMo:
            params["slowMo"] = timestr_to_millisecs(slowMo)
        options = json.dumps(params, default=str)
        self.info(options)

        with self.playwright.grpc_channel() as stub:

            response = stub.NewBrowser(
                Request().Browser(browser=browser.value, rawOptions=options)
            )
            self.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def new_context(
        self,
        hideRfBrowser: bool = False,
        acceptDownloads: bool = False,
        ignoreHTTPSErrors: bool = False,
        bypassCSP: bool = False,
        viewport: Optional[ViewportDimensions] = None,
        userAgent: Optional[str] = None,
        deviceScaleFactor: float = 1.0,
        isMobile: bool = False,
        hasTouch: bool = False,
        javaScriptEnabled: bool = True,
        timezoneId: Optional[str] = None,
        geolocation: Optional[Dict] = None,
        locale: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        extraHTTPHeaders: Optional[Dict[str, str]] = None,
        offline: bool = False,
        httpCredentials: Optional[Dict] = None,
        colorScheme: Optional[ColorScheme] = None,
    ):
        """Create a new BrowserContext with specified options.

        Returns a stable identifier for the created context.

        Value of ``viewport`` should be an object or a string
        representation of an object like {'height': 720, 'width': 1280}

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
            response = stub.NewContext(
                Request().Context(hideRfBrowser=hideRfBrowser, rawOptions=options)
            )
            self.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def new_page(self, url: Optional[str] = None):
        """Open a new Page. A Page is the Playwright equivalent to a tab.

            Returns a stable identifier for the created page.
            If ``url`` parameter is specified will open the new page to the specified URL.

        """

        with self.playwright.grpc_channel() as stub:
            response = stub.NewPage(Request().Url(url=url))
            self.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def switch_page(self, index: int):
        """Switches the active browser page to another open page by ``index``.

            Returns a stable identifier for the previous page.

            Newly opened pages get appended to the end of the list
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchPage(Request().Index(index=index))
            self.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def auto_activate_pages(self):
        """Toggles automatically changing active page to latest opened page."""
        with self.playwright.grpc_channel() as stub:
            response = stub.AutoActivatePages(Request().Empty())
            self.info(response.log)

    @keyword(tags=["BrowserControl"])
    def switch_browser(self, index: int):
        """Switches the currently active Browser to another open Browser.

            Returns a stable identifier for the previous browser.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchBrowser(Request().Index(index=index))
            self.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def switch_context(self, index: int):
        """ Switches the active BrowserContext to another open context.

            Returns a stable identifier for the previous context.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchContext(Request().Index(index=index))
            self.info(response.log)
            return response.body
