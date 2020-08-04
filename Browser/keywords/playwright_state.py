import json
from typing import Dict, List, Optional

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.data_types import ColorScheme, SupportedBrowsers, ViewportDimensions
from ..utils.meta_python import locals_to_params
from ..utils.time_conversion import timestr_to_millisecs


class PlaywrightState(LibraryComponent):
    """Keywords to manage Playwright side Browsers, Contexts and Pages.
    """

    @keyword(tags=["BrowserControl"])
    def open_browser(
        self,
        url: Optional[str] = None,
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
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def close_all_browsers(self):
        """Closes all open browsers."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseAllBrowsers(Request().Empty())
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def close_context(self):
        """Closes the current Context. Activated context is set to first active context."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseContext(Request().Empty())
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def close_page(self):
        """Closes the current Page. Activated page is set to first active page."""
        with self.playwright.grpc_channel() as stub:
            response = stub.ClosePage(Request().Empty())
            logger.info(response.log)

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
        logger.info(options)

        with self.playwright.grpc_channel() as stub:

            response = stub.NewBrowser(
                Request().Browser(browser=browser.value, rawOptions=options)
            )
            logger.info(response.log)
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

        Returns a stable identifier for the created context
        that can be used in `Switch Context`.

        ``acceptDownloads`` <bool> Whether to automatically downloadall the attachments.
        Defaults to false where all the downloads are canceled.

        ``ignoreHTTPSErrors`` <bool> Whether to ignore HTTPS errors during navigation.
        Defaults to false.

        ``bypassCSP`` <bool> Toggles bypassing page's Content-Security-Policy.

        ``viewport`` <dict> Sets a consistent viewport for each page.
        Defaults to an ``{'width': 1280, 'height': 720}`` viewport.
        Value of ``viewport`` can be a dict or a string
        representation of a dictionary.

        ``userAgent`` <str> Specific user agent to use in this context.

        ``deviceScaleFactor`` <float> Specify device scale factor
        (can be thought of as dpr). Defaults to 1.

        ``isMobile`` <bool> Whether the meta viewport tag is taken into account
        and touch events are enabled. Defaults to false. Not supported in Firefox.

        ``hasTouch`` <bool> Specifies if viewport supports touch events. Defaults to false.

        ``javaScriptEnabled`` <bool> Whether or not to enable JavaScript in the context.
        Defaults to true.

        ``timezoneId`` <str> Changes the timezone of the context.
        See [https://source.chromium.org/chromium/chromium/deps/icu.git/+/faee8bc70570192d82d2978a71e2a615788597d1:source/data/misc/metaZones.txt?originalUrl=https:%2F%2Fcs.chromium.org%2F|ICU’s metaZones.txt]
        for a list of supported timezone IDs.

        ``geolocation`` <dict> ``{'latitude': 59.95, 'longitude': 30.31667}``
        - ``latitude`` <number> Latitude between -90 and 90. *required*
        - ``longitude`` <number> Longitude between -180 and 180. *required*
        - ``accuracy`` Optional <number> Non-negative accuracy value. Defaults to 0.

        ``locale`` <str> Specify user locale, for example ``en-GB``, ``de-DE``, etc.
        Locale will affect ``navigator.language`` value, ``Accept-Language`` request header value
        as well as number and date formatting rules.

        ``permissions`` <list[str]> A list of permissions to grant to all pages in this context.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsercontextgrantpermissionspermissions-options|grantPermissions] for more details.

        ``extraHTTPHeaders`` <dict[str, str]> A dictionary containing additional HTTP headers
        to be sent with every request. All header values must be strings.

        ``offline`` <bool> Whether to emulate network being offline. Defaults to ``False``.

        ``httpCredentials`` <Object> Credentials for HTTP authentication.
        - example: ``{'username': 'admin', 'password': '123456'}``
        - ``username`` <str>
        - ``password`` <str>

        ``colorScheme`` <"dark"|"light"|"no-preference"> Emulates 'prefers-colors-scheme'
        media feature, supported values are 'light', 'dark', 'no-preference'.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#pageemulatemediaoptions|emulateMedia(options)]
        for more details. Defaults to ``light``.

        A BrowserContext is the Playwright object that controls a single browser profile.
        Within a context caches and cookies are shared.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsernewcontextoptions|Playwright browser.newContext]
        for a list of supported options.

        If there's no open Browser will open one. Does not create pages.
        """
        params = locals_to_params(locals())
        options = json.dumps(params, default=str)
        logger.info(options)
        with self.playwright.grpc_channel() as stub:
            response = stub.NewContext(
                Request().Context(hideRfBrowser=hideRfBrowser, rawOptions=options)
            )
            logger.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def new_page(self, url: Optional[str] = None):
        """Open a new Page. A Page is the Playwright equivalent to a tab.

            Returns a stable identifier for the created page.
            If ``url`` parameter is specified will open the new page to the specified URL.

        """

        with self.playwright.grpc_channel() as stub:
            response = stub.NewPage(Request().Url(url=url))
            logger.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def switch_page(self, index: int):
        """Switches the active browser page to another open page by ``index``.

            Returns a stable identifier for the previous page.

            Newly opened pages get appended to the end of the list
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchPage(Request().Index(index=index))
            logger.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl", "EventHandler"])
    def auto_activate_pages(self):
        """Toggles automatically changing active page to latest opened page."""
        with self.playwright.grpc_channel() as stub:
            response = stub.AutoActivatePages(Request().Empty())
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def switch_browser(self, index: int):
        """Switches the currently active Browser to another open Browser.

            Returns a stable identifier for the previous browser.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchBrowser(Request().Index(index=index))
            logger.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def switch_context(self, index: int):
        """ Switches the active BrowserContext to another open context.

            Returns a stable identifier for the previous context.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchContext(Request().Index(index=index))
            logger.info(response.log)
            return response.body
