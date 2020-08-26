import json
from typing import Dict, List, Optional

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    ColorScheme,
    SupportedBrowsers,
    ViewportDimensions,
    locals_to_params,
    logger,
    timestr_to_millisecs,
)


class PlaywrightState(LibraryComponent):
    """Keywords to manage Playwright side Browsers, Contexts and Pages.
    """

    """ Helpers for Switch_ and Close_ keywords """

    def _correct_browser(self, browser: str):
        if browser == "ALL":
            raise ValueError
        if browser != "CURRENT":
            self.switch_browser(browser)

    def _correct_context(self, context: str):
        if context == "ALL":
            raise ValueError
        if context != "CURRENT":
            self.switch_context(context)

    @keyword(tags=["BrowserControl"])
    def open_browser(
        self,
        url: Optional[str] = None,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: bool = False,
    ):
        """Opens a new browser instance.

        Creates a new browser, context and page with specified settings.
            Only supports some of the settings Create _ Keywords do

        ``url`` <str> Navigates to URL if provided. Defaults to None.

        ``browser`` < ``firefox`` | ``chromium`` | ``webkit`` > Specifies which browser to use. The
        supported browsers are listed in the table below. The browser names
        are case-sensitive.
        |   = Value =     |        = Name(s) =                                   |
        | firefox         | [https://www.mozilla.org/en-US/firefox/new|Firefox]  |
        | chromium        | [https://www.chromium.org/Home|Chromium]             |
        | webkit          | [https://webkit.org/|webkit]                         |

        ``headless`` <bool> If set to False, a GUI is provided otherwise it is hidden. Defaults to False.
        """

        self.new_browser(browser, headless=headless)
        self.new_context()
        self.new_page(url)

    @keyword(tags=["BrowserControl"])
    def close_browser(self, browser: str = "CURRENT"):
        """Closes the current browser. Activated browser is set to first active browser.
        Closes all context and pages belonging to this browser.

        ``browser`` < ``CURRENT`` | ``ALL`` |str> If value is not ``CURRENT``
        it should be a string referencing the id of the browser to be closed.
        If ``ALL`` is provided `Close All Browsers` is executed.
        """
        with self.playwright.grpc_channel() as stub:
            if browser == "ALL":
                self.close_all_browsers()
                return
            if browser != "CURRENT":
                self.switch_browser(browser)

            response = stub.CloseBrowser(Request.Empty())
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def close_all_browsers(self):
        """Closes all open browsers, contexts and pages."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseAllBrowsers(Request().Empty())
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def close_context(self, context: str = "CURRENT", browser: str = "CURRENT"):
        """Closes a Context. Activated context is set to first active context.
        Closes pages belonging to this context.

        ``context`` < ``CURRENT`` | ``ALL`` |str> Close context with specified id. If ``ALL``
        is passed, all contexts of the specified browser are closed. Defaults to CURRENT.

        ``browser`` < ``CURRENT`` | ``ALL`` |str> Close context in specified browser. If value is not "CURRENT"
        it should be a string referencing the id of the browser where to close context.
        If ALL is passed, all contexts of the browser will be closed.
        """
        with self.playwright.grpc_channel() as stub:
            self._correct_browser(browser)
            if context == "ALL":
                return NotImplementedError()
            if context != "CURRENT":
                self.switch_context(context)

            response = stub.CloseContext(Request().Empty())
            logger.info(response.log)

    @keyword(tags=["BrowserControl"])
    def close_page(
        self, page: str = "CURRENT", context: str = "CURRENT", browser: str = "CURRENT"
    ):
        # Add to page if ALL is implemented: If ALL is passed, all pages of the context will be closed.
        """Closes the ``page`` in ``context`` in ``browser``. Defaults to current for all three.
        Activated page is set to first active page.

        ``page`` < ``CURRENT`` | ``ALL`` |str> Id of the page to close. If value is not "CURRENT"
        it should be a string referencing the id of the context where to close page.
        If ``ALL`` is passed, all pages of the given context are closed. Defaults to CURRENT.

        ``context`` < ``CURRENT`` | ``ALL`` |str> Id of the context that belongs to the page to be closed.
        If ``ALL`` is passed, the requested pages of all contexts are closed. Defaults to CURRENT.

        ``browser`` < ``CURRENT`` | ``ALL`` |str> Id of the browser that belongs to the page to be closed.
        If ``ALL`` is passed, the requested pages depending of the context of all browsers are closed.
        Defaults to CURRENT.
        """
        with self.playwright.grpc_channel() as stub:
            self._correct_browser(browser)
            self._correct_context(context)

            if page == "ALL":
                return NotImplementedError()
            if page != "CURRENT":
                self.switch_page(page)

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

        ``browser`` <chromium|firefox|webkit> Opens the specified browser. Defaults to chromium.

        ``headless`` <bool> Set to False if you want a GUI. Defaults to False.

        ``executablePath`` <str> Path to a browser executable to run instead of the bundled one.
        If executablePath is a relative path, then it is resolved relative to current working
        directory. Note that Playwright only works with the bundled Chromium, Firefox or
        WebKit, use at your own risk. Defaults to None.

        ``args`` <List<str>> Additional arguments to pass to the browser instance. The list of
        Chromium flags can be found [http://peter.sh/experiments/chromium-command-line-switches/ | here].
        Defaults to None.

        ``ignoreDefaultArgs`` <List<str>> If an array is given, then filters out the given default arguments.
        Defaults to None.

        ``proxy`` <Dict> Network proxy settings.
        - server <string> Proxy to be used for all requests. HTTP and SOCKS proxies are supported, for example ``http://myproxy.com:3128`` or ``socks5://myproxy.com:3128``. Short form ``myproxy.com:3128`` is considered an HTTP proxy.
        - bypass <string> Optional coma-separated domains to bypass proxy, for example ``".com, chromium.org, .domain.com"``.
        - username <string> Optional username to use if HTTP proxy requires authentication.
        - password <string> Optional password to use if HTTP proxy requires authentication.

        ``downloadsPath`` <str> If specified, accepted downloads are downloaded into this folder.
        Otherwise, temporary folder is created and is deleted when browser is closed.

        ``handleSIGINT`` <bool> Close the browser process on Ctrl-C. Defaults to True.

        ``handleSIGTERM`` <bool> Close the browser process on SIGTERM. Defaults to True.

        ``handleSIGHUP`` <bool> Close the browser process on SIGHUP. Defaults to True.

        ``timeout`` <int> Maximum time in milliseconds to wait for the browser instance to start.
        Defaults to 30000 (30 seconds). Pass 0 to disable timeout.

        ``env`` <Dict<str, str|int|bool>> Specify environment variables that will
        be visible to the browser. Defaults to None.

        ``devtools`` <bool> Chromium-only Whether to auto-open a Developer Tools panel for each tab.
        If this option is true, the headless option will be set false.

        ``slowMo`` <int> Slows down Playwright operations by the specified amount of milliseconds.
        Useful so that you can see what is going on. Defaults to no delay.
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
                Request().Browser(browser=browser.name, rawOptions=options)
            )
            logger.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def new_context(
        self,
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
        hideRfBrowser: bool = False,
    ):
        """Create a new BrowserContext with specified options.

        Returns a stable identifier for the created context
        that can be used in `Switch Context`.

        ``acceptDownloads`` <bool> Whether to automatically downloadall the attachments.
        Defaults to False where all the downloads are canceled.

        ``ignoreHTTPSErrors`` <bool> Whether to ignore HTTPS errors during navigation.
        Defaults to False.

        ``bypassCSP`` <bool> Toggles bypassing page's Content-Security-Policy. Defaults to False.

        ``viewport`` <dict> Sets a consistent viewport for each page.
        Defaults to an ``{'width': 1280, 'height': 720}`` viewport.
        Value of ``viewport`` can be a dict or a string
        representation of a dictionary.

        ``userAgent`` <str> Specific user agent to use in this context.

        ``deviceScaleFactor`` <float> Specify device scale factor
        (can be thought of as dpr). Defaults to 1.

        ``isMobile`` <bool> Whether the meta viewport tag is taken into account
        and touch events are enabled. Defaults to False. Not supported in Firefox.

        ``hasTouch`` <bool> Specifies if viewport supports touch events. Defaults to False.

        ``javaScriptEnabled`` <bool> Whether or not to enable JavaScript in the context.
        Defaults to True.

        ``timezoneId`` <str> Changes the timezone of the context.
        See [https://source.chromium.org/chromium/chromium/src/+/master:third_party/icu/source/data/misc/metaZones.txt | ICU’s metaZones.txt]
        for a list of supported timezone IDs.

        ``geolocation`` <dict> Sets the geolocation. No location is set be default.
        - ``latitude`` <number> Latitude between -90 and 90. **Required**
        - ``longitude`` <number> Longitude between -180 and 180. **Required**
        - ``accuracy`` Optional <number> Non-negative accuracy value. Defaults to 0.
        Example usage: ``{'latitude': 59.95, 'longitude': 30.31667}``

        ``locale`` <str> Specify user locale, for example ``en-GB``, ``de-DE``, etc.
        Locale will affect ``navigator.language`` value, ``Accept-Language`` request header value
        as well as number and date formatting rules.

        ``permissions`` <list<str>> A list of permissions to grant to all pages in this context.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsercontextgrantpermissionspermissions-options | grantPermissions]
        for more details.

        ``extraHTTPHeaders`` <dict[str, str]> A dictionary containing additional HTTP headers
        to be sent with every request. All header values must be strings.

        ``offline`` <bool> Whether to emulate network being offline. Defaults to False.

        ``httpCredentials`` <Dict<str, str>> Credentials for HTTP authentication.
        - example: ``{'username': 'admin', 'password': '123456'}``
        - ``username`` <str>
        - ``password`` <str>

        ``colorScheme`` <dark|light|no-preference> Emulates 'prefers-colors-scheme'
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
                Request().Context(rawOptions=options, hideRfBrowser=hideRfBrowser)
            )
            logger.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def new_page(self, url: Optional[str] = None):
        """Open a new Page. A Page is the Playwright equivalent to a tab.
            Returns a stable identifier for the created page.

            ``url`` <str> If specified it will open the new page to the specified URL.

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.NewPage(Request().Url(url=url))
            logger.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def switch_browser(self, id: str):
        """Switches the currently active Browser to another open Browser.
            Returns a stable identifier for the previous browser.

            ``id`` <str> Id of the browser to be changed to. Starting at 0. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchBrowser(Request().Index(index=id))
            logger.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def switch_context(self, id: str, browser: str = "CURRENT"):
        """ Switches the active BrowserContext to another open context.
        Returns a stable identifier for the previous context.

        ``id`` <str> Id of the context to be changed to. Randomly generated UUID. **Required**

        ``browser`` < ``CURRENT`` | ``ALL`` |str> Switch context in specified browser. If value is not "CURRENT"
        it should be an int referencing the id of the browser where to switch context.
        If ALL is passed, the contexts of the browser will be closed.
        """
        with self.playwright.grpc_channel() as stub:
            if browser == "ALL":
                raise NotImplementedError
            self._correct_browser(browser)
            response = stub.SwitchContext(Request().Index(index=id))
            logger.info(response.log)
            return response.body

    @keyword(tags=["BrowserControl"])
    def switch_page(self, id: str, context: str = "CURRENT", browser: str = "CURRENT"):
        """Switches the active browser page to another open page by ``id``.
        Returns a stable identifier for the previous page.
        Newly opened pages get appended to the end of the list.

        ``id`` < ``CURRENT`` | ``NEW `` | str> Id of the page to be changed to. Randomly generated UUID. **Required**

        ``context`` < ``CURRENT`` | ``ALL`` |str> Switch page in specified context. If value is not "CURRENT"
        it should be an int referencing the id of the context where to switch page.
        If ALL is passed, the pages of all contexts switch.

        ``browser`` < ``CURRENT`` | ``ALL`` |str> Switch page in specified browser. If value is not "CURRENT"
        it should be an int referencing the id of the browser where to switch page.
        If ALL is passed, the page of all browsers depending on the context switch.
        """
        with self.playwright.grpc_channel() as stub:
            if context == "ALL":
                raise NotImplementedError
            if browser == "ALL":
                raise NotImplementedError

            self._correct_browser(browser)
            self._correct_context(context)
            response = stub.SwitchPage(Request().Index(index=id))
            logger.info(response.log)
            return response.body
