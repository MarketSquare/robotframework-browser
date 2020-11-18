# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from datetime import timedelta
from typing import Any, Dict, List, Optional

from robot.utils import get_link_path  # type: ignore

from ..assertion_engine import verify_assertion, with_assertion_polling
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    ColorScheme,
    GeoLocation,
    HttpCredentials,
    Proxy,
    SelectionType,
    SupportedBrowsers,
    ViewportDimensions,
    convert_typed_dict,
    find_by_id,
    keyword,
    locals_to_params,
    logger,
)
from ..utils.data_types import AssertionOperator


class PlaywrightState(LibraryComponent):
    """Keywords to manage Playwright side Browsers, Contexts and Pages."""

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

    @keyword(tags=("Setter", "BrowserControl"))
    def open_browser(
        self,
        url: Optional[str] = None,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: bool = False,
        pause_on_failure: bool = True,
    ):
        """Opens a new browser instance. Use this keyword for quick experiments or debugging sessions.
        Use `New Page` directly instead of `Open Browser` for production and automated execution.
        See `Browser, Context and Page` for more information about Browser and related concepts.

        Creates a new browser, context and page with specified settings.
            Only supports some of the settings Create _ Keywords do

        ``url`` Navigates to URL if provided. Defaults to None.

        ``browser`` Specifies which browser to use. The
        supported browsers are listed in the table below. The browser names
        are case-sensitive.
        |   = Value =     |        = Name(s) =                                   |
        | firefox         | [https://www.mozilla.org/en-US/firefox/new|Firefox]  |
        | chromium        | [https://www.chromium.org/Home|Chromium]             |
        | webkit          | [https://webkit.org/|webkit]                         |

        ``headless`` If set to False, a GUI is provided otherwise it is hidden. Defaults to False.

        ``pause_on_failure`` Stop execution when failure detected and leave browser open. Defaults to True.
        """
        logger.warn(
            "Open Browser is for quick experimentation and debugging only. Use New Page for production."
        )
        browser_id = self.new_browser(browser, headless=headless)
        self.new_context()
        self.new_page(url)
        if pause_on_failure:
            self.library._pause_on_failure.add(browser_id)

    @keyword(tags=("Setter", "BrowserControl"))
    def close_browser(self, browser: str = "CURRENT"):
        """Closes the current browser. Activated browser is set to first active browser.
        Closes all context and pages belonging to this browser.
        See `Browser, Context and Page` for more information about Browser and related concepts.

        ``browser`` < ``CURRENT`` | ``ALL`` | str > If value is not ``CURRENT``
        it should be a string referencing the id of the browser to be closed.
        If ``ALL`` is provided `Close All Browsers` is executed.
        """
        with self.playwright.grpc_channel() as stub:
            if browser == "ALL":
                response = stub.CloseAllBrowsers(Request().Empty())
                self.library._pause_on_failure.clear()
                logger.info(response.log)
                return
            if browser != "CURRENT":
                self.switch_browser(browser)

            response = stub.CloseBrowser(Request.Empty())
            closed_browser_id = response.body
            self.library._pause_on_failure.discard(closed_browser_id)
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def close_context(self, context: str = "CURRENT", browser: str = "CURRENT"):
        """Closes a Context. Activated context is set to first active context.
        Closes pages belonging to this context.
        See `Browser, Context and Page` for more information about Context and related concepts.

        ``context`` < ``CURRENT`` | ``ALL`` | str > Close context with specified id. If ``ALL``
        is passed, all contexts of the specified browser are closed. Defaults to CURRENT.

        ``browser`` < ``CURRENT`` | ``ALL`` | str > Close context in specified browser. If value is not "CURRENT"
        it should be a string referencing the id of the browser where to close context.
        """
        for browser_instance in self._get_browser_instances(browser):
            if browser_instance["id"] == "NO BROWSER OPEN":
                logger.info("No browsers open. can not closing context.")
                return
            self.switch_browser(browser_instance["id"])
            contexts = self._get_context(context, browser_instance["contexts"])
            self._close_context(contexts)

    def _close_context(self, contexts):
        with self.playwright.grpc_channel() as stub:
            for context in contexts:
                self.context_cache.remove(context["id"])
                self.switch_context(context["id"])
                response = stub.CloseContext(Request().Empty())
                logger.info(response.log)

    def _get_context(self, context, contexts):
        if context == "ALL":
            return contexts
        if context == "CURRENT":
            current_ctx = self.switch_context("CURRENT")
            try:
                return [find_by_id(current_ctx, contexts, log_error=False)]
            except StopIteration:
                logger.info("No open context found.")
                return []
        return [find_by_id(context, contexts)]

    def _get_browser_instances(self, browser):
        catalog = self.get_browser_catalog()
        if browser == "ALL":
            browser_ids = [browser_instance["id"] for browser_instance in catalog]
        elif browser == "CURRENT":
            browser_ids = [self.switch_browser("CURRENT")]
        else:
            browser_ids = [browser]
        return [find_by_id(browser_id, catalog) for browser_id in browser_ids]

    @keyword(tags=("Setter", "BrowserControl"))
    def close_page(
        self, page: str = "CURRENT", context: str = "CURRENT", browser: str = "CURRENT"
    ):
        """Closes the ``page`` in ``context`` in ``browser``. Defaults to current for all three.
        Activated page is set to first active page.
        See `Browser, Context and Page` for more information about Page and related concepts.

        ``page`` < ``CURRENT`` | ``ALL`` | str > Id of the page to close. If value is not "CURRENT"
        it should be a string referencing the id of the context where to close page.
        If ``ALL`` is passed, all pages of the given context are closed. Defaults to CURRENT.

        ``context`` < ``CURRENT`` | ``ALL`` | str > Id of the context that belongs to the page to be closed.
        If ``ALL`` is passed, the requested pages of all contexts are closed. Defaults to CURRENT.

        ``browser`` < ``CURRENT`` | ``ALL`` | str > Id of the browser that belongs to the page to be closed.
        If ``ALL`` is passed, the requested pages depending of the context of all browsers are closed.
        Defaults to CURRENT.
        """
        with self.playwright.grpc_channel() as stub:
            catalog = self.library.get_browser_catalog()

            if browser == "ALL":
                browser_ids = [b["id"] for b in catalog]
            elif browser == "CURRENT":
                current_browser = self.switch_browser("CURRENT")
                browser_ids = [current_browser]
                if current_browser == "NO BROWSER OPEN":
                    return
            else:
                browser_ids = [browser]

            browsers = [find_by_id(b_id, catalog) for b_id in browser_ids]

            for b in browsers:
                self.switch_browser(b["id"])
                contexts = b["contexts"]
                if context != "ALL":
                    if context == "CURRENT":
                        current_ctx = self.switch_context("CURRENT")
                        if current_ctx == "NO CONTEXT OPEN":
                            return
                        contexts = [find_by_id(current_ctx, contexts)]
                    else:
                        contexts = [find_by_id(context, contexts)]
                for c in contexts:

                    self.switch_context(c["id"])
                    if page == "ALL":
                        page_ids = [p["id"] for p in c["pages"]]
                    else:
                        page_ids = [page]

                    for p in page_ids:
                        if p == "NO PAGE OPEN":
                            return
                        if page != "CURRENT":
                            self.switch_page(p)
                        response = stub.ClosePage(Request().Empty())
                        logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def new_browser(
        self,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: bool = True,
        executablePath: Optional[str] = None,
        args: Optional[List[str]] = None,
        ignoreDefaultArgs: Optional[List[str]] = None,
        proxy: Optional[Proxy] = None,
        downloadsPath: Optional[str] = None,
        handleSIGINT: bool = True,
        handleSIGTERM: bool = True,
        handleSIGHUP: bool = True,
        timeout: timedelta = timedelta(seconds=30),
        env: Optional[Dict] = None,
        devtools: bool = False,
        slowMo: timedelta = timedelta(seconds=0),
    ) -> str:

        """Create a new playwright Browser with specified options.
        See `Browser, Context and Page` for more information about Browser and related concepts.

        Returns a stable identifier for the created browser.

        ``browser`` Opens the specified browser. Defaults to chromium.

        ``headless`` Set to False if you want a GUI. Defaults to False.

        ``executablePath`` Path to a browser executable to run instead of the bundled one.
        If executablePath is a relative path, then it is resolved relative to current working
        directory. Note that Playwright only works with the bundled Chromium, Firefox or
        WebKit, use at your own risk. Defaults to None.

        ``args`` Additional arguments to pass to the browser instance. The list of
        Chromium flags can be found [http://peter.sh/experiments/chromium-command-line-switches/ | here].
        Defaults to None.

        ``ignoreDefaultArgs`` If an array is given, then filters out the given default arguments.
        Defaults to None.

        ``proxy`` Network proxy settings.
        - server <string> Proxy to be used for all requests. HTTP and SOCKS proxies are supported, for example ``http://myproxy.com:3128`` or ``socks5://myproxy.com:3128``. Short form ``myproxy.com:3128`` is considered an HTTP proxy.
        - bypass <string> Optional coma-separated domains to bypass proxy, for example ``".com, chromium.org, .domain.com"``.
        - username <string> Optional username to use if HTTP proxy requires authentication.
        - password <string> Optional password to use if HTTP proxy requires authentication.

        ``downloadsPath`` If specified, accepted downloads are downloaded into this folder.
        Otherwise, temporary folder is created and is deleted when browser is closed.

        ``handleSIGINT`` Close the browser process on Ctrl-C. Defaults to True.

        ``handleSIGTERM`` Close the browser process on SIGTERM. Defaults to True.

        ``handleSIGHUP`` Close the browser process on SIGHUP. Defaults to True.

        ``timeout`` Maximum time in milliseconds to wait for the browser instance to start.
        Defaults to 30000 (30 seconds). Pass 0 to disable timeout.

        ``env`` <Dict<str, str|int|bool>> Specify environment variables that will
        be visible to the browser. Defaults to None.

        ``devtools`` Chromium-only Whether to auto-open a Developer Tools panel for each tab.
        If this option is true, the headless option will be set false.

        ``slowMo`` Slows down Playwright operations by the specified amount of milliseconds.
        Useful so that you can see what is going on. Defaults to no delay.
        """
        params = locals_to_params(locals())
        params = convert_typed_dict(self.new_context.__annotations__, params)
        if timeout:
            params["timeout"] = self.convert_timeout(timeout)
        params["slowMo"] = self.convert_timeout(slowMo)

        browser_path = self.library.external_browser_executable.get(browser)
        if browser_path:
            params["executablePath"] = browser_path

        options = json.dumps(params, default=str)
        logger.info(options)

        with self.playwright.grpc_channel() as stub:
            response = stub.NewBrowser(
                Request().Browser(browser=browser.name, rawOptions=options)
            )
            logger.info(response.log)
            return response.body

    @keyword(tags=("Setter", "BrowserControl"))
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
        geolocation: Optional[GeoLocation] = None,
        locale: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        extraHTTPHeaders: Optional[Dict[str, str]] = None,
        offline: bool = False,
        httpCredentials: Optional[HttpCredentials] = None,
        colorScheme: Optional[ColorScheme] = None,
        proxy: Optional[Proxy] = None,
        videosPath: Optional[str] = None,
        videoSize: Optional[ViewportDimensions] = None,
        defaultBrowserType: Optional[SupportedBrowsers] = None,
        hideRfBrowser: bool = False,
    ) -> str:
        """Create a new BrowserContext with specified options.
        See `Browser, Context and Page` for more information about BrowserContext.

        Returns a stable identifier for the created context
        that can be used in `Switch Context`.

        ``acceptDownloads`` Whether to automatically downloads all the attachments.
        Defaults to False where all the downloads are canceled.

        ``ignoreHTTPSErrors`` Whether to ignore HTTPS errors during navigation.
        Defaults to False.

        ``bypassCSP`` Toggles bypassing page's Content-Security-Policy. Defaults to False.

        ``viewport`` Sets a consistent viewport for each page.
        Defaults to an ``{'width': 1280, 'height': 720}`` viewport.
        Value of ``viewport`` can be a dict or a string
        representation of a dictionary.

        ``userAgent`` Specific user agent to use in this context.

        ``deviceScaleFactor`` Specify device scale factor
        (can be thought of as dpr). Defaults to 1.

        ``isMobile`` Whether the meta viewport tag is taken into account
        and touch events are enabled. Defaults to False. Not supported in Firefox.

        ``hasTouch`` Specifies if viewport supports touch events. Defaults to False.

        ``javaScriptEnabled`` Whether or not to enable JavaScript in the context.
        Defaults to True.

        ``timezoneId`` Changes the timezone of the context.
        See [https://source.chromium.org/chromium/chromium/src/+/master:third_party/icu/source/data/misc/metaZones.txt | ICU’s metaZones.txt]
        for a list of supported timezone IDs.

        ``geolocation`` Sets the geolocation. No location is set by default.
        - ``latitude`` <number> Latitude between -90 and 90.
        - ``longitude`` <number> Longitude between -180 and 180.
        - ``accuracy`` Optional <number> Non-negative accuracy value. Defaults to 0.
        Example usage: ``{'latitude': 59.95, 'longitude': 30.31667}``

        ``locale`` Specify user locale, for example ``en-GB``, ``de-DE``, etc.
        Locale will affect ``navigator.language`` value, ``Accept-Language`` request header value
        as well as number and date formatting rules.

        ``permissions`` A list of permissions to grant to all pages in this context.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsercontextgrantpermissionspermissions-options | grantPermissions]
        for more details.

        ``extraHTTPHeaders`` A dictionary containing additional HTTP headers
        to be sent with every request. All header values must be strings.

        ``offline`` Whether to emulate network being offline. Defaults to False.

        ``httpCredentials`` Credentials for HTTP authentication.
        - example: ``{'username': 'admin', 'password': '123456'}``
        - ``username``
        - ``password``

        ``colorScheme`` Emulates 'prefers-colors-scheme'
        media feature, supported values are 'light', 'dark', 'no-preference'.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#pageemulatemediaoptions|emulateMedia(options)]
        for more details. Defaults to ``light``.

        ``proxy`` Network proxy settings to use with this context.
        Note that browser needs to be launched with the global proxy for this option to work.
        If all contexts override the proxy, global proxy will be never used and can be any string

        ``videosPath`` Enables video recording for all pages to videosPath
        folder. If not specified, videos are not recorded.

        ``videoSize`` Specifies dimensions of the automatically recorded
        video. Can only be used if videosPath is set. If not specified the size will
        be equal to viewport. If viewport is not configured explicitly the video size
        defaults to 1280x720. Actual picture of the page will be scaled down if
        necessary to fit specified size.
        - Example {"width": 1280, "height": 720}

        ``defaultBrowserType`` If no browser is open and `New Context` opens a new browser
        with defaults, it now uses this setting.
        Very useful together with `Get Device` keyword:

        Example:
        | Test an iPhone
        |     ${device}=    `Get Device`    iPhone X
        |     `New Context`    &{device}        # unpacking here with &
        |     `New Page`    http://example.com

        A BrowserContext is the Playwright object that controls a single browser profile.
        Within a context caches and cookies are shared.
        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsernewcontextoptions|Playwright browser.newContext]
        for a list of supported options.

        If there's no open Browser this keyword will open one. Does not create pages.
        """
        params = locals_to_params(locals())
        params = convert_typed_dict(self.new_context.__annotations__, params)
        if not videosPath:
            params.pop("videoSize", None)
        options = json.dumps(params, default=str)
        logger.info(options)
        with self.playwright.grpc_channel() as stub:
            response = stub.NewContext(
                Request().Context(
                    rawOptions=options,
                    hideRfBrowser=hideRfBrowser,
                    defaultTimeout=int(self.timeout),
                )
            )
        logger.info(response.log)
        self.context_cache.add(response.body, self._get_video_size(params))
        return response.body

    def _get_video_size(self, params: dict) -> dict:
        if "videoSize" in params:
            return params["videoSize"]
        if "viewport" in params:
            return params["viewport"]
        return {"width": 1280, "height": 720}

    @keyword(tags=("Setter", "BrowserControl"))
    def new_page(self, url: Optional[str] = None) -> str:
        """Open a new Page. A Page is the Playwright equivalent to a tab.
        See `Browser, Context and Page` for more information about Page concept.
        Returns a stable identifier for the created page.

        When a `New Page` is called without an open browser, `New Browser`
        and `New Context` are executed with default values first.

        ``url`` If specified it will open the new page to the specified URL.

        """
        with self.playwright.grpc_channel() as stub:
            response = stub.NewPage(
                Request().Url(url=url, defaultTimeout=int(self.timeout))
            )
        logger.info(response.log)
        self._embed_video(json.loads(response.video))
        return response.body

    def _embed_video(self, video: dict):
        if not video.get("video_path"):
            logger.debug("Video is not enabled.")
            return
        relative_path = get_link_path(video.get("video_path"), self.outputdir)
        video_size = self.context_cache.get(video["contextUuid"])
        video_width = video_size["width"]
        video_height = video_size["height"]
        video_type = relative_path.split(".")[1]
        logger.info(
            '</td></tr><tr><td colspan="3">'
            f'<video width="{video_width}" height="{video_height}" controls>'
            f'<source src="{relative_path}" type="video/{video_type}"></video>',
            html=True,
        )

    @keyword(tags=("Getter", "BrowserControl"))
    @with_assertion_polling
    def get_browser_catalog(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Any = None,
    ) -> Dict:
        """Returns all browsers, open contexts in them and open pages in these contexts.
        See `Browser, Context and Page` for more information about these concepts.

        The data is parsed into a python list containing data representing the open Objects.

        On the root level the data contains a list of open browsers.

        Data can be manipulated also with ``assertion_operator`` for example to find
        a specific id based on index or page title with ``then`` operator.

        Return value can also be asserted against expected value.

        Sample:
        | [
        |   {
        |     "type": "chromium",
        |     "id": "browser=96207191-8147-44e7-b9ac-5e04f2709c1d",
        |     "contexts": [
        |       {
        |         "type": "context",
        |         "id": "context=525d8e5b-3c4e-4baa-bfd4-dfdbc6e86089",
        |         "activePage": "page=f90c97b8-eaaf-47f2-98b2-ccefd3450f12",
        |         "pages": [
        |           {
        |             "type": "page",
        |             "title": "Robocorp",
        |             "url": "https://robocorp.com/",
        |             "id": "page=7ac15782-22d2-48b4-8591-ff17663fa737",
        |             "timestamp": 1598607713.858
        |           },
        |           {
        |             "type": "page",
        |             "title": "Home - Reaktor",
        |             "url": "https://www.reaktor.com/",
        |             "id": "page=f90c97b8-eaaf-47f2-98b2-ccefd3450f12",
        |             "timestamp": 1598607714.702
        |           }
        |         ]
        |       }
        |     ],
        |     "activeContext": "context=525d8e5b-3c4e-4baa-bfd4-dfdbc6e86089",
        |     "activeBrowser": false
        |   },
        |   {
        |     "type": "firefox",
        |     "id": "browser=ad99abac-17a9-472b-ac7f-d6352630834e",
        |     "contexts": [
        |       {
        |         "type": "context",
        |         "id": "context=bc64f1ba-5e76-46dd-9735-4bd344afb9c0",
        |         "activePage": "page=8baf2991-5eaf-444d-a318-8045f914e96a",
        |         "pages": [
        |           {
        |             "type": "page",
        |             "title": "Software-Qualit\u00e4tssicherung und Softwaretest",
        |             "url": "https://www.imbus.de/",
        |             "id": "page=8baf2991-5eaf-444d-a318-8045f914e96a",
        |             "timestamp": 1598607716.828
        |           }
        |         ]
        |       }
        |     ],
        |     "activeContext": "context=bc64f1ba-5e76-46dd-9735-4bd344afb9c0",
        |     "activeBrowser": true
        |   }
        | ]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBrowserCatalog(Request().Empty())
            parsed = json.loads(response.json)
            logger.info(json.dumps(parsed))
            return verify_assertion(
                parsed, assertion_operator, assertion_expected, "Browser Catalog "
            )

    @keyword(tags=("Setter", "BrowserControl"))
    def switch_browser(self, id: str) -> str:
        """Switches the currently active Browser to another open Browser.
        Returns a stable identifier for the previous browser.
        See `Browser, Context and Page` for more information about Browser and related concepts.

        ``id`` Id of the browser to be changed to. Starting at 0.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchBrowser(Request().Index(index=id))
            logger.info(response.log)
            return response.body

    @keyword(tags=("Setter", "BrowserControl"))
    def switch_context(self, id: str, browser: str = "CURRENT") -> str:
        """Switches the active BrowserContext to another open context.
        Returns a stable identifier for the previous context.
        See `Browser, Context and Page` for more information about Context and related concepts.

        ``id`` Id of the context to be changed to. Randomly generated UUID.

        ``browser`` < ``CURRENT`` | str> Switch context in specified browser. If value is not "CURRENT"
        it should be an the id of the browser where to switch context.
        """
        with self.playwright.grpc_channel() as stub:
            self._correct_browser(browser)
            response = stub.SwitchContext(Request().Index(index=id))
            logger.info(response.log)
            return response.body

    @keyword(tags=("Setter", "BrowserControl"))
    def switch_page(
        self, id: str, context: str = "CURRENT", browser: str = "CURRENT"
    ) -> str:
        """Switches the active browser page to another open page by ``id`` or ``NEW``.
        Returns a stable identifier ``id`` for the previous page.
        See `Browser, Context and Page` for more information about Page and related concepts.

        ``id`` < ``CURRENT`` | ``NEW `` | str> Id of the page to be changed to or

        ``NEW`` for a page opened after the current page. This may timeout if no new pages
        exists before library timeout. See `Set Browser Timeout` for how to change the timeout.

        With ``CURRENT`` you can get the ``id`` of the "CURRENT" page


        ``context`` < ``CURRENT`` | str> Switch page in specified context. If value is not "CURRENT"
        it should be the id of the context where to switch page.

        ``browser`` < ``CURRENT`` | str> Switch page in specified browser. If value is not "CURRENT"
        it should be the id of the browser where to switch page.
        """
        with self.playwright.grpc_channel() as stub:
            if context.upper() == "ALL":
                raise NotImplementedError
            if browser.upper() == "ALL":
                raise NotImplementedError

            self._correct_browser(browser)
            self._correct_context(context)
            response = stub.SwitchPage(
                Request().IdWithTimeout(id=id, timeout=self.timeout)
            )
            logger.info(response.log)
            return response.body

    @keyword(tags=("Getter", "BrowserControl"))
    def get_browser_ids(self, browser: SelectionType = SelectionType.ALL) -> List:
        """Returns a list of ids from open browsers.
        See `Browser, Context and Page` for more information about Browser and related concepts.


        ``browser`` Defaults to ``ALL``
        - ``ALL`` Returns all ids as a list.
        - ``ACTIVE`` or ``CURRENT`` Returns the id of the currently active browser as list.

        The ACTIVE browser is a synonym for the CURRENT Browser.
        """
        if browser == SelectionType.ACTIVE:
            browser_item = self._get_active_browser_item(self.get_browser_catalog())
            if "id" in browser_item:
                return [browser_item["id"]]
        else:
            return [browser["id"] for browser in self.get_browser_catalog()]
        return []

    @keyword(tags=("Getter", "BrowserControl"))
    def get_context_ids(
        self,
        context: SelectionType = SelectionType.ALL,
        browser: SelectionType = SelectionType.ALL,
    ) -> List:
        """Returns a list of context ids based on the browser selection.
        See `Browser, Context and Page` for more information about Context and related concepts.


        ``context`` Defaults to ``ALL``
        - ``ALL`` Returns all context ids as a list.
        - ``ACTIVE`` Returns the id of the active context as a list.

        ``browser`` Defaults to ``ALL``
        - ``ALL`` context ids from all open browsers shall be fetched.
        - ``ACTIVE`` only context ids from the active browser shall be fetched.

        The ACTIVE context of the ACTIVE Browser is the ``Current`` Context.
        """
        if browser == SelectionType.ACTIVE:
            browser_item = self._get_active_browser_item(self.get_browser_catalog())
            if context == SelectionType.ACTIVE:
                if "activeContext" in browser_item:
                    return [browser_item["activeContext"]]
            else:
                if "contexts" in browser_item:
                    return [context["id"] for context in browser_item["contexts"]]
        else:
            if context == SelectionType.ACTIVE:
                context_ids = list()
                for browser_item in self.get_browser_catalog():
                    if "activeContext" in browser_item:
                        context_ids.append(browser_item["activeContext"])
                return context_ids
            else:
                context_ids = list()
                for browser_item in self.get_browser_catalog():
                    for context_item in browser_item["contexts"]:
                        context_ids.append(context_item["id"])
                return context_ids
        return []

    @keyword(tags=("Getter", "BrowserControl"))
    def get_page_ids(
        self,
        page: SelectionType = SelectionType.ALL,
        context: SelectionType = SelectionType.ALL,
        browser: SelectionType = SelectionType.ALL,
    ) -> List:
        """Returns a list of page ids based on the context and browser selection.
        See `Browser, Context and Page` for more information about Page and related concepts.


        ``page``
        - ``ALL`` Returns all page ids as a list.
        - ``ACTIVE`` Returns the id of the active page as a list.

        ``context``
        - ``ALL`` page ids from all contexts shall be fetched.
        - ``ACTIVE`` only page ids from the active context shall be fetched.

        ``browser``
        - ``ALL`` page ids from all open browsers shall be fetched.
        - ``ACTIVE`` only page ids from the active browser shall be fetched.

        The ACTIVE page of the ACTIVE context of the ACTIVE Browser is the ``Current`` Page.
        """
        if browser == SelectionType.ACTIVE:
            browser_item = self._get_active_browser_item(self.get_browser_catalog())
            if "contexts" in browser_item:
                if context == SelectionType.ACTIVE:
                    return self._get_page_ids_from_context_list(
                        page, self._get_active_context_item(browser_item)
                    )
                else:
                    return self._get_page_ids_from_context_list(
                        page, browser_item["contexts"]
                    )
        else:
            context_list = list()
            for browser_item in self.get_browser_catalog():
                if "contexts" in browser_item:
                    if context == SelectionType.ACTIVE:
                        context_list.extend(self._get_active_context_item(browser_item))
                    else:
                        context_list.extend(browser_item["contexts"])
            return self._get_page_ids_from_context_list(page, context_list)
        return []

    @staticmethod
    def _get_page_ids_from_context_list(
        page_selection_type: SelectionType, context_list
    ):
        page_ids = list()
        for context_item in context_list:
            if page_selection_type == SelectionType.ACTIVE:
                if "activePage" in context_item:
                    page_ids.append(context_item["activePage"])
            else:
                page_ids.extend([page["id"] for page in context_item["pages"]])
        return page_ids

    @staticmethod
    def _get_active_browser_item(browser_catalog):
        for browser in browser_catalog:
            if browser["activeBrowser"]:
                return browser
        return {}

    @staticmethod
    def _get_active_context_item(browser_item):
        for context in browser_item["contexts"]:
            if (
                "activeContext" in browser_item
                and browser_item["activeContext"] == context["id"]
            ):
                return [context]
        return []
