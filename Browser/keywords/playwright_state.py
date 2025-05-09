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
import os
from contextlib import suppress
from copy import copy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional, Union
from uuid import uuid4

from assertionengine import AssertionOperator, verify_assertion
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS, BuiltIn
from robot.utils import get_link_path

from Browser.utils.data_types import BrowserInfo, TracingGroupMode
from Browser.utils.misc import get_download_id
from Browser.utils.robot_booleans import is_truthy

from ..assertion_engine import assertion_formatter_used, with_assertion_polling
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    ClientCertificate,
    ColorScheme,
    DownloadInfo,
    ForcedColors,
    GeoLocation,
    HttpCredentials,
    NewPageDetails,
    PageLoadStates,
    Permission,
    Proxy,
    RecordHar,
    RecordVideo,
    ReduceMotion,
    SelectionType,
    ServiceWorkersPermissions,
    SupportedBrowsers,
    ViewportDimensions,
    convert_typed_dict,
    find_by_id,
    keyword,
    locals_to_params,
    logger,
)
from ..utils.logger import LOGLEVEL


class PlaywrightState(LibraryComponent):
    """Keywords to manage Playwright side Browsers, Contexts and Pages."""

    # Helpers for Switch_ and Close_ keywords

    def _correct_browser(self, browser: Union[SelectionType, str]):
        if browser == SelectionType.ALL:
            raise ValueError
        if browser == SelectionType.CURRENT:
            return
        self.switch_browser(browser)

    def _correct_context(self, context: Union[SelectionType, str]):
        if context == SelectionType.ALL:
            raise ValueError
        if context == SelectionType.CURRENT:
            return
        self.switch_context(context)

    @keyword(tags=("Setter", "BrowserControl"))
    def open_browser(
        self,
        url: Optional[str] = None,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: bool = False,
        pause_on_failure: bool = True,
        bypassCSP=True,
    ):
        """Opens a new browser instance. Use this keyword for quick experiments or debugging sessions.

        Use `New Page` directly instead of `Open Browser` for production and automated execution.
        See `Browser, Context and Page` for more information about Browser and related concepts.

        Creates a new browser, context and page with specified settings.


        | =Argument=          | =Description= |
        | ``url``              | Navigates to URL if provided. Defaults to None. |
        | ``browser``          | Specifies which browser to use. The supported browsers are listed in the table below. |
        | ``headless``         | If set to False, a GUI is provided otherwise it is hidden. Defaults to False. |
        | ``pause_on_failure`` | Stop execution when failure detected and leave browser open. Defaults to True. |
        | ``bypassCSP``        | Defaults to bypassing CSP and enabling custom script attach to the page. |

        Browsers:

        |   = Value =     |        = Name(s) =                                   |
        | ``firefox``     | [https://www.mozilla.org/en-US/firefox/new|Firefox]  |
        | ``chromium``    | [https://www.chromium.org/Home|Chromium]             |
        | ``webkit``      | [https://webkit.org/|webkit]                         |

        [https://forum.robotframework.org/t//4310|Comment >>]
        """
        logger.warn(
            "Open Browser is for quick experimentation and debugging only. Use New Page for production."
        )
        browser_id = self.new_browser(browser, headless=headless)
        self.new_context(bypassCSP=bypassCSP)
        self.new_page(url)
        if pause_on_failure:
            self.library.pause_on_failure.add(browser_id)

    @keyword(tags=("Setter", "BrowserControl"))
    def close_browser(self, browser: Union[SelectionType, str] = SelectionType.CURRENT):
        """Closes the current browser.

        Active browser is set to the browser that was active before this one. Closes all context and pages belonging
        to this browser. See `Browser, Context and Page` for more information about Browser and
        related concepts.


        | =Argument=  | =Description= |
        | ``browser`` | Browser to close. ``CURRENT`` selects the active browser. ``ALL`` closes all browsers. When a browser id is provided, that browser is closed. |



        Example:
        | `Close Browser`    ALL        # Closes all browsers
        | `Close Browser`    CURRENT    # Close current browser
        | `Close Browser`               # Close current browser
        | `Close Browser`    ${id}      # Close browser matching id

        [https://forum.robotframework.org/t//4239|Comment >>]
        """
        browser = SelectionType.create(browser)
        with self.playwright.grpc_channel() as stub:
            if browser == SelectionType.ALL:
                response = stub.CloseAllBrowsers(Request().Empty())
                self.library.pause_on_failure.clear()
                logger.info(response.log)
                self.browser_arg_mapping.clear()
                return
            if browser != SelectionType.CURRENT:
                self.switch_browser(browser)

            response = stub.CloseBrowser(Request.Empty())
            closed_browser_id = response.body
            self.delete_browser_id_from_arg_mapping(closed_browser_id)
            self._update_tracing_contexts()
            self.library.pause_on_failure.discard(closed_browser_id)
            logger.info(response.log)

    def delete_browser_id_from_arg_mapping(self, closed_browser_id: str) -> None:
        for option_hash, browser_id in list(self.browser_arg_mapping.items()):
            if browser_id == closed_browser_id:
                del self.browser_arg_mapping[option_hash]

    @keyword(tags=("Setter", "BrowserControl"))
    def close_context(
        self,
        context: Union[SelectionType, str] = SelectionType.CURRENT,
        browser: Union[SelectionType, str] = SelectionType.CURRENT,
        *,
        save_trace: bool = True,
    ):
        """Closes a Context.

        Active context is set to the context that was active before this one. Closes pages belonging to this context.
        See `Browser, Context and Page` for more information about Context and related concepts.

        | =Argument=  | =Description= |
        | ``context`` | Context to close. ``CURRENT`` selects the active context. ``ALL`` closes all contexts. When a context id is provided, that context is closed. |
        | ``browser`` | Browser where to close context. ``CURRENT`` selects the active browser. ``ALL`` closes all browsers. When a browser id is provided, that browser is closed. |
        | ``save_trace`` | If set to ``False``, the trace of this context is not saved, even if it was enables by `New Context`. Defaults to ``True``. |

        Example:
        | `Close Context`                          #  Closes current context and current browser
        | `Close Context`    CURRENT    CURRENT    #  Closes current context and current browser
        | `Close Context`    ALL        CURRENT    #  Closes all context from current browser and current browser
        | `Close Context`    ALL        ALL        #  Closes all context from current browser and all browser

        [https://forum.robotframework.org/t//4240|Comment >>]
        """
        context = SelectionType.create(context)
        browser = SelectionType.create(browser)
        for browser_instance in self._get_browser_ids(browser):
            if browser_instance["id"] == "NO BROWSER OPEN":
                logger.info("No browsers open. can not closing context.")
                return
            active_browser = self._get_active_browser_item(
                self._get_browser_catalog(include_page_details=False)
            )
            if active_browser["id"] != browser_instance["id"]:
                self._switch_browser(browser_instance["id"], "TRACE")
            with suppress(Exception):
                contexts = self._get_context(context, browser_instance["contexts"])
                self._close_pw_context(contexts, save_trace)
        self._update_tracing_contexts()

    def _update_tracing_contexts(self):
        if self.library.tracing_contexts:
            all_context_ids = self.get_context_ids()
            self.library.tracing_contexts = [
                ctx_id
                for ctx_id in self.library.tracing_contexts
                if ctx_id in all_context_ids
            ]

    def _close_pw_context(self, contexts, save_trace=True):
        with self.playwright.grpc_channel() as stub:
            for context in contexts:
                self.context_cache.remove(context["id"])
                self.switch_context(context["id"])
                response = stub.CloseContext(Request().Bool(value=save_trace))
                logger.info(response.log)

    def _get_context(self, context, contexts):
        if context == SelectionType.ALL:
            return contexts
        if context == SelectionType.CURRENT:
            current_ctx = self.switch_context("CURRENT")
            try:
                return [find_by_id(current_ctx, contexts, log_error=False)]
            except StopIteration:
                logger.info("No open context found.")
                return []
        return [find_by_id(context, contexts, log_error=False)]

    def _get_browser_ids(self, browser) -> list:
        catalog = self._get_browser_catalog(include_page_details=False)
        if browser == SelectionType.ALL:
            browser_ids = [browser_instance["id"] for browser_instance in catalog]
        elif browser == SelectionType.CURRENT:
            current_browser = self.switch_browser("CURRENT")
            browser_ids = [current_browser]
            if current_browser == "NO BROWSER OPEN":
                browser_ids = []
        else:
            browser_ids = [browser]
        return [find_by_id(browser_id, catalog) for browser_id in browser_ids]

    def _get_context_id(
        self, context_selection: Union[str, SelectionType], contexts: list
    ) -> list:
        if context_selection == SelectionType.CURRENT:
            current_ctx = self.switch_context("CURRENT")
            if current_ctx == "NO CONTEXT OPEN":
                return []
            contexts = [find_by_id(current_ctx, contexts, log_error=False)]
        elif context_selection != SelectionType.ALL:
            contexts = [find_by_id(str(context_selection), contexts, log_error=False)]
        return contexts

    @keyword(tags=("Setter", "BrowserControl"))
    def close_page(
        self,
        page: Union[SelectionType, str] = SelectionType.CURRENT,
        context: Union[SelectionType, str] = SelectionType.CURRENT,
        browser: Union[SelectionType, str] = SelectionType.CURRENT,
        runBeforeUnload: bool = False,
    ):
        """Closes the ``page`` in ``context`` in ``browser``.

        Defaults to current for all three. Active page is set to the page that was active before this one.
        See `Browser, Context and Page` for more information about Page and related concepts.

        ``runBeforeUnload`` defines where to run the
        [https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event|before unload]
        page handlers. Defaults to false.


        | =Argument=  | =Description= |
        | ``page``    | Page to close. ``CURRENT`` selects the active page. ``ALL`` closes all pages. When a page id is provided, that page is closed. |
        | ``context`` | Context where to close page. ``CURRENT`` selects the active context. ``ALL`` closes all contexts. When a context id is provided, that context is closed. |
        | ``browser`` | Browser where to close page. ``CURRENT`` selects the active browser. ``ALL`` closes all browsers. When a browser id is provided, that browser is closed. |

        Returns a list of dictionaries containing id, errors and console messages from the page.

        Example
        | `Close Page`                                       # Closes current page, within the current context and browser
        | `Close Page`    CURRENT     CURRENT     CURRENT    # Closes current page, within the current context and browser
        | `Close Page`    ALL         ALL         ALL        # Closes all pages, within all contexts and browsers

        [https://forum.robotframework.org/t//4241|Comment >>]
        """
        page = SelectionType.create(page)
        context = SelectionType.create(context)
        browser = SelectionType.create(browser)
        result = []
        browser_ids = self._get_browser_ids(browser)
        with self.playwright.grpc_channel() as stub:
            for browser_id in browser_ids:
                self.switch_browser(browser_id["id"])
                contexts_ids = browser_id["contexts"]
                try:
                    contexts_ids = self._get_context_id(context, contexts_ids)
                except StopIteration:
                    continue
                for context_id in contexts_ids:
                    self.switch_context(context_id["id"])
                    if page == SelectionType.ALL:
                        pages_ids = [p["id"] for p in context_id["pages"]]
                    else:
                        pages_ids = [page]

                    for page_id in pages_ids:
                        if page_id == "NO PAGE OPEN":
                            return None
                        if page != SelectionType.CURRENT:
                            self.switch_page(page_id)
                        response = stub.ClosePage(
                            Request().ClosePage(runBeforeUnload=runBeforeUnload)
                        )
                        if response.log:
                            logger.info(response.log)
                        result.append(
                            {
                                "errors": json.loads(response.errors),
                                "console": json.loads(response.console),
                                "id": response.pageId,
                            }
                        )
        return result

    @keyword(tags=("Setter", "BrowserControl"))
    def set_default_run_before_unload(self, runBeforeUnload: bool) -> bool:
        """Set default runBeforeUnload value when `Close Page` is called indirectly.

        Close Page is called indirectly when
        [https://marketsquare.github.io/robotframework-browser/Browser.html#Automatic%20page%20and%20context%20closing|automatic page closing]
        is done. The default value is false and this keyword can be used to change value.
        Returns the old runBeforeUnload value.

        [https://forum.robotframework.org/t/6203|Comment >>]
        """
        old_value = self.library.auto_closing_default_run_before_unload
        self.library.auto_closing_default_run_before_unload = runBeforeUnload
        return old_value

    @keyword(tags=("Setter", "BrowserControl"))
    def connect_to_browser(
        self,
        wsEndpoint: str,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        use_cdp: bool = False,
        *,
        timeout: timedelta = timedelta(seconds=30),
    ):
        """Connect to a Playwright browser server via playwright websocket or Chrome DevTools Protocol.

        See `Launch Browser Server` for more information about how to launch a playwright browser server.

        See `Browser, Context and Page` for more information about Browser and related concepts.

        Returns a stable identifier for the connected browser.

        | =Argument=     | =Description= |
        | ``wsEndpoint`` | Address to connect to. Either ``ws://`` or ``http://`` if cdp is used. |
        | ``browser``    | Opens the specified browser. Defaults to ``chromium``. |
        | ``use_cdp``    | Connect to browser via Chrome DevTools Protocol. Defaults to False. Works only with Chromium based browsers. |
        | ``timeout``    | Maximum time in Robot Framework time format to wait for the connection to be established. Defaults to 30 seconds. Pass 0 to disable timeout. |

        To Connect to a Browser viw Chrome DevTools Protocol, the browser must be started with this protocol enabled.
        This typically done by starting a Chrome browser with the argument ``--remote-debugging-port=9222`` or similar.
        When the browser is running with activated CDP, it is possible to connect to it either with websockets (``ws://``)
        or via HTTP (``http://``). The HTTP connection can be used when ``use_cdp`` is set to True.
        A typical address for a CDP connection is ``http://127.0.0.1:9222``.

        [https://forum.robotframework.org/t//4242|Comment >>]
        """
        timeout_ms = int(self.convert_timeout(timeout))
        with self.playwright.grpc_channel() as stub:
            response = stub.ConnectToBrowser(
                Request().ConnectBrowser(
                    url=wsEndpoint,
                    browser=browser.name,
                    connectCDP=use_cdp,
                    timeout=timeout_ms,
                )
            )
            logger.info(response.log)
            return response.body

    @keyword(tags=("Setter", "BrowserControl"))
    def new_browser(
        self,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: bool = True,
        *,
        args: Optional[list[str]] = None,
        channel: Optional[str] = None,
        chromiumSandbox: bool = False,
        devtools: bool = False,
        downloadsPath: Optional[str] = None,
        env: Optional[dict] = None,
        executablePath: Optional[str] = None,
        firefoxUserPrefs: Optional[dict[str, Union[str, int, float, bool]]] = None,
        handleSIGHUP: bool = True,
        handleSIGINT: bool = True,
        handleSIGTERM: bool = True,
        ignoreDefaultArgs: Union[list[str], bool, None] = None,
        proxy: Optional[Proxy] = None,
        reuse_existing: bool = True,
        slowMo: timedelta = timedelta(seconds=0),
        timeout: timedelta = timedelta(seconds=30),
    ) -> str:
        """Create a new playwright Browser with specified options.

        See `Browser, Context and Page` for more information about Browser and related concepts.

        Returns a stable identifier for the created browser.

        | =Arguments= | =Description= |
        | ``browser`` | Opens the specified [#type-SupportedBrowsers|browser]. Defaults to chromium. |
        | ``headless`` | Set to False if you want a GUI. Defaults to True. |
        | ``args`` | Additional arguments to pass to the browser instance. The list of Chromium flags can be found [http://peter.sh/experiments/chromium-command-line-switches/|here]. Defaults to None. |
        | ``channel`` | Allows to operate against the stock Google Chrome and Microsoft Edge browsers. For more details see: [https://playwright.dev/docs/browsers#google-chrome--microsoft-edge|Playwright documentation]. |
        | ``chromiumSandbox`` | Enable Chromium sandboxing. Defaults to False. |
        | ``devtools`` | Chromium-only Whether to auto-open a Developer Tools panel for each tab. |
        | ``downloadsPath`` | If specified, accepted downloads are downloaded into this folder. Otherwise, temporary folder is created and is deleted when browser is closed. Regarding file deletion, see the docs of `Download` and `Promise To Wait For Download`. |
        | ``env`` | Specifies environment variables that will be visible to the browser. Dictionary keys are variable names, values are the content. Defaults to None. |
        | ``executablePath`` | Path to a browser executable to run instead of the bundled one. If executablePath is a relative path, then it is resolved relative to current working directory. Note that Playwright only works with the bundled Chromium, Firefox or WebKit, use at your own risk. Defaults to None. |
        | ``firefoxUserPrefs`` |Firefox user preferences. Learn more about the Firefox user preferences at [https://support.mozilla.org/en-US/kb/about-config-editor-firefox|about:config]. |
        | ``handleSIGHUP`` | Close the browser process on SIGHUP. Defaults to True. |
        | ``handleSIGINT`` | Close the browser process on Ctrl-C. Defaults to True. |
        | ``handleSIGTERM`` | Close the browser process on SIGTERM. Defaults to True. |
        | ``ignoreDefaultArgs`` | If True, Playwright does not pass its own configurations args and only uses the ones from args. If a list is given, then filters out the given default arguments. Dangerous option; use with care. Defaults to False. |
        | ``proxy`` | Network [#type-Proxy|Proxy] settings. Structure: ``{'server': <str>, 'bypass': <Optional[str]>, 'username': <Optional[str]>, 'password': <Optional[str]>}`` |
        | ``reuse_existing`` | If set to True, an existing browser instance, that matches the same arguments, will be reused. If no same configured Browser exist, a new one is started. Defaults to True. |
        | ``slowMo`` | Slows down Playwright operations by the specified amount of seconds or `timedelta`. Useful so that you can see what is going on. Defaults to no delay. |
        | ``timeout`` | Maximum time in Robot Framework time format to wait for the browser instance to start. Defaults to 30 seconds. Pass 0 to disable timeout. |


        [https://forum.robotframework.org/t//4306|Comment >>]
        """
        params = locals_to_params(locals())
        parameter_hash = self._get_parameter_hash(params)
        existing_browser_id = self._switch_to_existing_browser(
            reuse_existing, parameter_hash
        )
        if existing_browser_id:
            return existing_browser_id
        params = self._set_browser_options(params, browser, channel, slowMo, timeout)
        options = json.dumps(params, default=str)
        logger.info(options)

        with self.playwright.grpc_channel() as stub:
            response = stub.NewBrowser(
                Request().Browser(browser=browser.name, rawOptions=options)
            )
            logger.info(response.log)
            self.browser_arg_mapping[parameter_hash] = response.body
            return response.body

    @keyword(tags=("Setter", "BrowserControl"))
    def launch_browser_server(
        self,
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: bool = True,
        *,
        args: Optional[list[str]] = None,
        channel: Optional[str] = None,
        chromiumSandbox: bool = False,
        devtools: bool = False,
        downloadsPath: Optional[str] = None,
        env: Optional[dict] = None,
        executablePath: Optional[str] = None,
        firefoxUserPrefs: Optional[dict[str, Union[str, int, float, bool]]] = None,
        handleSIGHUP: bool = True,
        handleSIGINT: bool = True,
        handleSIGTERM: bool = True,
        ignoreDefaultArgs: Union[list[str], bool, None] = None,
        port: Optional[int] = None,
        proxy: Optional[Proxy] = None,
        reuse_existing: bool = True,
        slowMo: timedelta = timedelta(seconds=0),
        timeout: timedelta = timedelta(seconds=30),
        wsPath: Optional[str] = None,
    ) -> str:
        """Launches a new playwright Browser server with specified options.

        Returns a websocket endpoint (wsEndpoint) string that can be used to connect to the server.

        | =Arguments= | =Description= |
        | ``port`` | Port to use for the browser server. Defaults to 0, which results in a random free port being assigned. |
        | ``wsPath`` | If set, Playwright will listen on the given path in addition to the main port. For security, this defaults to an unguessable string. |

        Check `New Browser` for the other argument docs.

        The launched browser server can be used to connect to it with `Connect To Browser` keyword.
        This keyword can also be used from command line with ``rfbrowser launch-browser-server`` command.

        see [https://playwright.dev/docs/api/class-browserserver#browser-server|Playwright documentation] for more information.

        [https://forum.robotframework.org/t//4306|Comment >>]
        """
        params = locals_to_params(locals())
        params = self._set_browser_options(params, browser, channel, slowMo, timeout)
        options = json.dumps(params, default=str)
        logger.info(options)
        with self.playwright.grpc_channel() as stub:
            response = stub.LaunchBrowserServer(
                Request().Browser(browser=browser.name, rawOptions=options)
            )
            logger.info(response.log)
            return response.body

    @keyword(tags=("Setter", "BrowserControl"))
    def close_browser_server(self, wsEndpoint: str) -> None:
        """Close a playwright Browser Server identified by its websocket endpoint (wsEndpoint).

        The wsEndpoint string is returned by `Launch Browser Server` and is also used by `Connect To Browser`.

        | =Arguments=     | =Description= |
        | ``wsEndpoint`` | Address of the browser server. Example: ``ws://127.0.0.1:63784/ca69bf0e9471391e8183d9ac1e90e1ba``|
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseBrowserServer(Request().ConnectBrowser(url=wsEndpoint))
            logger.info(response.log)
            self._update_tracing_contexts()

    def _switch_to_existing_browser(
        self, reuse_existing: bool, parameter_hash: int
    ) -> Optional[str]:
        if not reuse_existing:
            return None
        existing_browser_id = self.browser_arg_mapping.get(parameter_hash)
        if existing_browser_id is None:
            return None
        try:
            self.switch_browser(existing_browser_id)
            logger.info(f"Reusing existing browser with id: {existing_browser_id}")
            return existing_browser_id
        except AssertionError:
            self.browser_arg_mapping.pop(parameter_hash, None)
            return None

    def _get_parameter_hash(self, params: dict[str, Any]) -> int:
        params.pop("reuse_existing", None)
        return hash(repr(params))

    @keyword(tags=("Setter", "BrowserControl"))
    def new_context(
        self,
        *,
        acceptDownloads: bool = True,
        baseURL: Optional[str] = None,
        bypassCSP: bool = False,
        clientCertificates: Optional[list[ClientCertificate]] = None,
        colorScheme: Optional[ColorScheme] = None,
        defaultBrowserType: Optional[SupportedBrowsers] = None,
        deviceScaleFactor: Optional[float] = None,
        extraHTTPHeaders: Optional[dict[str, str]] = None,
        forcedColors: ForcedColors = ForcedColors.none,
        geolocation: Optional[GeoLocation] = None,
        hasTouch: Optional[bool] = None,
        httpCredentials: Optional[HttpCredentials] = None,
        ignoreHTTPSErrors: bool = False,
        isMobile: Optional[bool] = None,
        javaScriptEnabled: bool = True,
        locale: Optional[str] = None,
        offline: bool = False,
        permissions: Optional[list[Permission]] = None,
        proxy: Optional[Proxy] = None,
        recordHar: Optional[RecordHar] = None,
        recordVideo: Optional[RecordVideo] = None,
        reducedMotion: ReduceMotion = ReduceMotion.no_preference,
        screen: Optional[dict[str, int]] = None,
        serviceWorkers: Optional[
            ServiceWorkersPermissions
        ] = ServiceWorkersPermissions.allow,
        storageState: Optional[str] = None,
        timezoneId: Optional[str] = None,
        tracing: Union[bool, Path, None] = None,
        userAgent: Optional[str] = None,
        viewport: Optional[ViewportDimensions] = ViewportDimensions(
            width=1280, height=720
        ),
    ) -> str:
        """Create a new BrowserContext with specified options.

        See `Browser, Context and Page` for more information about BrowserContext.

        Returns a stable identifier for the created context
        that can be used in `Switch Context`.


        | =Arguments=              | =Description= |
        | ``acceptDownloads``      | Whether to automatically download all the attachments. Defaults to True where all the downloads are accepted. |
        | ``baseURL``              | When using `Go To`, `Wait For Request`, `Wait For Response` or `Wait For Navigation` it takes the base URL in consideration by using the URL() constructor for building the corresponding URL. Unset by default. Examples: ``baseURL=http://localhost:3000`` and navigating to ``/bar.html`` results in ``http://localhost:3000/bar.html``. ``baseURL=http://localhost:3000/foo/`` and navigating to ``./bar.html`` results in ``http://localhost:3000/foo/bar.html``. ``baseURL=http://localhost:3000/foo`` (without trailing slash) and navigating to ``./bar.html`` results in ``http://localhost:3000/bar.html``. |
        | ``bypassCSP``            | Toggles bypassing page's Content-Security-Policy. Defaults to False. |
        | ``clientCertificates``   | Specifies a client certificate for mTLS authentication, for example ``clientCertificates=[{'origin': 'https://playwright.dev', 'pfxPath': 'certificate.p12', 'passphrase': 'password'}]``. *NOTE:* The origin needs to be exact whithout any path. |
        | ``colorScheme``          | Emulates `'prefers-colors-scheme'` media feature, supported values are `'light'`, `'dark'`, `'no-preference'`. |
        | ``defaultBrowserType``   | If no browser is open and `New Context` opens a new browser with defaults, it now uses this setting. Very useful together with `Get Device` keyword. |
        | ``deviceScaleFactor``    | Specify device scale factor (can be thought of as dpr). Defaults to ``1``. |
        | ``extraHTTPHeaders``     | A dictionary containing additional HTTP headers to be sent with every request. All header values must be strings. |
        | ``forcedColors``         | Emulates `forced-colors` media feature, supported values are `active` and `none`. |
        | ``geolocation``          | A dictionary containing ``latitude`` and ``longitude`` or ``accuracy`` to emulate. If ``latitude`` or ``longitude`` is not specified, the device geolocation won't be overriden. |
        | ``hasTouch``             | Specifies if viewport supports touch events. Defaults to False. |
        | ``httpCredentials``      | Credentials for [https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication|HTTP authentication]. |
        | ``ignoreHTTPSErrors``    | Whether to ignore HTTPS errors during navigation. Defaults to False. |
        | ``isMobile``             | Whether the meta viewport tag is taken into account and touch events are enabled. Defaults to False. |
        | ``javaScriptEnabled``    | Whether or not to enable JavaScript in the context. Defaults to True. |
        | ``locale``               | Specify user locale, for example ``en-GB``, ``de-DE``, etc. |
        | ``offline``              | Toggles browser's offline mode. Defaults to False. |
        | ``permissions``          | A list containing permissions to grant to all pages in this context. All permissions that are not listed here will be automatically denied. |
        | ``proxy``                | Network proxy settings to use with this context. Defaults to None. *NOTE:* For Chromium on Windows the browser needs to be launched with the global proxy for this option to work. If all contexts override the proxy, global proxy will be never used and can be any string, for example ``proxy={ server: 'http://per-context' }``. |
        | ``recordHar``            | Enables [http://www.softwareishard.com/blog/har-12-spec/|HAR] recording for all pages into to a file. Must be path to file, example ${OUTPUT_DIR}/har.file. If not specified, the HAR is not recorded. Make sure to await context to close for the to be saved. |
        | ``recordVideo``          | Enables video recording for all pages into a folder. If not specified videos are not recorded. Make sure to close context for videos to be saved. Video is not support in remote browsers. |
        | ``reduceMotion``         | Emulates `prefers-reduced-motion` media feature, supported values are `reduce`, `no-preference`. |
        | ``screen``               | Emulates consistent window screen size available inside web page via window.screen. Is only used when the viewport is set. Example {'width': 414, 'height': 896} |
        | ``serviceWorkers``       | Whether to allow sites to register Service workers. Defaults to 'allow'. |
        | ``storageState``         | Restores the storage stated created by the `Save Storage State` keyword. Must be full path to the file. |
        | ``timezoneId``           | Changes the timezone of the context. See [https://source.chromium.org/chromium/chromium/src/+/master:third_party/icu/source/data/misc/metaZones.txt|ICU`s metaZones.txt] for a list of supported timezone IDs. |
        | ``tracing``              | Boolean ``True`` (recommendation) or file path or directory where the [https://playwright.dev/docs/api/class-tracing/|tracing] file is saved. The string `{contextid}` will be replaces with the context id. Path to *.zip files can be absolute or relative to ${OUTPUT_DIR}. Path to folders can be absolute or relative to ${OUTPUT_DIR}/browser/traces. If boolean ``True`` or a directory is given, the trace file will automatically be named ``trace_{contextid}.tip``. Temporary trace files will be saved to ${OUTPUT_DIR}/Browser/traces/temp. Tracing is automatically closed when context is closed. Temporary trace files will be automatically deleted at start of each test execution. Trace file can be opened after the test execution by running command from shell: ``rfbrowser show-trace /path/to/trace.zip``. Tracing can also be enables by setting a Robot Framework variable or environment variable ``ROBOT_FRAMEWORK_BROWSER_TRACING`` to ``True``. |
        | ``userAgent``            | Specific user agent to use in this context. |
        | ``viewport``             | A dictionary containing ``width`` and ``height``. Emulates consistent viewport for each page. Defaults to 1280x720. null disables the default viewport. If ``width`` and ``height`` is  ``0``, the viewport will scale with the window. |


        Example:
        | Test an iPhone
        |     ${device}=    `Get Device`    iPhone X
        |     `New Context`    &{device}        # unpacking here with &
        |     `New Page`    http://example.com

        A BrowserContext is the Playwright object that controls a single browser profile.
        Within a context caches and cookies are shared. See
        [https://playwright.dev/docs/api/class-browser#browsernewcontextoptions|Playwright browser.newContext]
        for a list of supported options.

        If there's no open Browser this keyword will open one. Does not create pages.

        [https://forum.robotframework.org/t//4307|Comment >>]
        """
        params = locals_to_params(locals())
        if permissions:
            params["permissions"] = [
                (
                    permission.value
                    if not isinstance(permission, str)
                    else Permission[permission].value
                )
                for permission in permissions
            ]
        params["viewport"] = copy(viewport)
        trace_file = self._resolve_trace_file(tracing)
        params = self._set_context_options(params, httpCredentials, storageState)
        options = json.dumps(params, default=str)
        response = self._new_context(options, trace_file)
        context_options = self._mask_credentials(json.loads(response.contextOptions))
        logger.info(response.log)
        logger.info(context_options)
        if response.newBrowser:
            logger.info(
                "No browser was open. New browser was automatically opened "
                "when this context is created."
            )
        self.context_cache.add(response.id, self._get_video_size(params))
        return response.id

    @keyword()
    def new_persistent_context(
        self,
        userDataDir: str = "",  # TODO: change to PurePath
        browser: SupportedBrowsers = SupportedBrowsers.chromium,
        headless: bool = True,
        *,
        acceptDownloads: bool = True,
        args: Optional[list[str]] = None,
        baseURL: Optional[str] = None,
        bypassCSP: bool = False,
        channel: Optional[str] = None,
        chromiumSandbox: bool = False,
        colorScheme: Optional[ColorScheme] = None,
        defaultBrowserType: Optional[SupportedBrowsers] = None,
        deviceScaleFactor: Optional[float] = None,
        devtools: bool = False,
        downloadsPath: Optional[str] = None,
        env: Optional[dict] = None,
        executablePath: Optional[str] = None,
        extraHTTPHeaders: Optional[dict[str, str]] = None,
        forcedColors: ForcedColors = ForcedColors.none,
        geolocation: Optional[GeoLocation] = None,
        handleSIGHUP: bool = True,
        handleSIGINT: bool = True,
        handleSIGTERM: bool = True,
        hasTouch: Optional[bool] = None,
        httpCredentials: Optional[HttpCredentials] = None,
        ignoreDefaultArgs: Union[list[str], bool, None] = None,
        ignoreHTTPSErrors: bool = False,
        isMobile: Optional[bool] = None,
        javaScriptEnabled: bool = True,
        locale: Optional[str] = None,
        offline: bool = False,
        permissions: Optional[list[Permission]] = None,
        proxy: Optional[Proxy] = None,
        recordHar: Optional[RecordHar] = None,
        recordVideo: Optional[RecordVideo] = None,
        reducedMotion: ReduceMotion = ReduceMotion.no_preference,
        screen: Optional[dict[str, int]] = None,
        serviceWorkers: Optional[
            ServiceWorkersPermissions
        ] = ServiceWorkersPermissions.allow,
        slowMo: timedelta = timedelta(seconds=0),
        timeout: timedelta = timedelta(seconds=30),
        timezoneId: Optional[str] = None,
        tracing: Union[bool, Path, None] = None,
        url: Optional[str] = None,
        userAgent: Optional[str] = None,
        viewport: Optional[ViewportDimensions] = ViewportDimensions(
            width=1280, height=720
        ),
    ):
        """Open a new
        [https://playwright.dev/docs/api/class-browsertype#browser-type-launch-persistent-context | persistent context].

        `New Persistent Context` does basically executes `New Browser`, `New Context` and `New Page` in one step with setting a profile at the same time.

        This keyword returns a tuple of browser id, context id and page details. (New in Browser 15.0.0)

        | =Argument=               | =Description= |
        | ``userDataDir``          | Path to a User Data Directory, which stores browser session data like cookies and local storage. More details for Chromium and Firefox. Note that Chromium's user data directory is the parent directory of the "Profile Path" seen at chrome://version. Pass an empty string to use a temporary directory instead. |
        | ``browser``              | Browser type to use. Default is Chromium. |
        | ``headless``             | Whether to run browser in headless mode. Defaults to ``True``. |
        | other arguments          | Please see `New Browser`, `New Context` and `New Page` for more information about the other arguments. |

        If you want to use extensions you need to download the extension as a .zip, enable loading the extension, and load the extensions using chromium arguments like below. Extensions only work with chromium and with a headful browser.

        | ${launch_args}=  Set Variable  ["--disable-extensions-except=./ublock/uBlock0.chromium", "--load-extension=./ublock/uBlock0.chromium"]
        | ${browserId}  ${contextId}  ${pageDetails}=  `New Persistent Context`  browser=chromium  headless=False  url=https://robocon,io  args=${launch_args}

        Check `New Browser`, `New Context` and `New Page` for the specific argument docs.

        [https://forum.robotframework.org/t//4309|Comment >>]
        """
        params = locals_to_params(locals())
        if permissions:
            params["permissions"] = [
                (
                    permission.value
                    if not isinstance(permission, str)
                    else Permission[permission].value
                )
                for permission in permissions
            ]
        params["viewport"] = copy(viewport)
        trace_file = self._resolve_trace_file(tracing)
        params = self._set_browser_options(params, browser, channel, slowMo, timeout)
        params = self._set_context_options(params, httpCredentials, None)
        options = json.dumps(params, default=str)

        with self.playwright.grpc_channel() as stub:
            catalog = self._get_browser_catalog(include_page_details=False)
            previously_active_browser_id = None
            existing_browser_ids = []
            for browser_info in catalog:
                if browser_info["activeBrowser"]:
                    previously_active_browser_id = browser_info["id"]
                existing_browser_ids.append(browser_info["id"])
            response = stub.NewPersistentContext(
                Request().PersistentContext(
                    browser=browser.name,
                    rawOptions=options,
                    defaultTimeout=int(self.timeout),
                    traceFile=str(trace_file),
                )
            )
            self.add_context_and_keyword_call_stack_to_trace(
                trace_file=trace_file, ctx_id=response.id
            )
            context_options = self._mask_credentials(
                json.loads(response.contextOptions)
            )
            logger.info(response.log)
            logger.info(context_options)
            browser_id = response.browserId

            if url:
                try:
                    stub.GoTo(
                        Request().UrlOptions(
                            url=Request().Url(
                                url=url, defaultTimeout=int(self.get_timeout(timeout))
                            )
                        )
                    )
                except Exception as e:
                    if browser_id in existing_browser_ids:
                        self.close_context()
                        self.switch_browser(previously_active_browser_id)
                        logger.debug(
                            "Teardown: Closed new Context and switched back "
                            f"to previously active browser: {previously_active_browser_id}"
                        )
                    else:
                        self.close_browser()
                        logger.debug("Teardown: Closed new persistent context.")
                    raise e
            self.context_cache.add(response.id, self._get_video_size(params))
            video_path = self._embed_video(json.loads(response.video))
            return (
                browser_id,
                response.id,
                NewPageDetails(page_id=response.pageId, video_path=video_path),
            )

    def _resolve_trace_file(self, tracing: Union[bool, None, Path]) -> str:
        if isinstance(tracing, str):
            tracing = Path(tracing)
        tracing_by_var = (
            is_truthy(
                BuiltIn().get_variable_value("${ROBOT_FRAMEWORK_BROWSER_TRACING}", "")
            )
            if EXECUTION_CONTEXTS.current
            else False
        )
        tracing_by_env = is_truthy(os.getenv("ROBOT_FRAMEWORK_BROWSER_TRACING") or "")
        if not tracing and not tracing_by_var and not tracing_by_env:
            return ""
        if tracing is True or tracing_by_var or tracing_by_env:
            return str(
                self.traces_output
            )  # will be extended by '`trace_${context_id}.zip`' on js side.
        if isinstance(tracing, Path) and tracing.suffix == ".zip":
            return str(Path(self.outputdir, tracing).resolve())
        return str(Path(self.traces_output, str(tracing)).resolve())

    def _set_context_options(self, params, httpCredentials, storageState):
        params = convert_typed_dict(self.new_context.__annotations__, params)
        params = self._set_video_path(params)
        params = self._set_video_size_to_int(params)
        reduced_motion = str(params.get("reducedMotion"))
        reduced_motion = reduced_motion.replace("_", "-")
        params["reducedMotion"] = reduced_motion
        if storageState and not Path(storageState).is_file():
            raise ValueError(
                f"storageState argument value '{storageState}' is not file, but it should be."
            )
        if "httpCredentials" in params and params["httpCredentials"] is not None:
            secret = self.resolve_secret(httpCredentials, "httpCredentials")
            params["httpCredentials"] = secret
        masked_params = self._mask_credentials(params.copy())
        logger.info(json.dumps(masked_params, default=str, indent=2))
        return params

    def _set_browser_options(self, params, browser, channel, slowMo, timeout):
        params = convert_typed_dict(self.new_context.__annotations__, params)
        params["timeout"] = self.convert_timeout(timeout)
        params["slowMo"] = self.convert_timeout(slowMo)
        browser_path = self.library.external_browser_executable.get(browser)
        if browser_path:
            params["executablePath"] = browser_path
        if channel and browser != SupportedBrowsers.chromium:
            raise ValueError(
                f"Must use {SupportedBrowsers.chromium.name} browser with channel definition"
            )
        params["tracesDir"] = str(self.traces_temp / str(uuid4()))
        return params

    def _new_context(self, options: str, trace_file: Union[Path, str]):
        with self.playwright.grpc_channel() as stub:
            context = stub.NewContext(
                Request().Context(
                    rawOptions=options,
                    defaultTimeout=int(self.timeout),
                    traceFile=str(trace_file),
                )
            )
            self.add_context_and_keyword_call_stack_to_trace(
                trace_file=trace_file, ctx_id=context.id
            )
        return context

    def add_context_and_keyword_call_stack_to_trace(self, trace_file, ctx_id):
        if (
            not trace_file
            or self.library.tracing_group_mode == TracingGroupMode.Playwright
        ):
            return None
        self.library.tracing_contexts.append(ctx_id)
        if self.library.tracing_group_mode == TracingGroupMode.Browser:
            return self.open_trace_group(
                **(self.library.keyword_call_stack[-1]), context_id=ctx_id
            )
        for keyword_call in self.library.keyword_call_stack:
            self.open_trace_group(**keyword_call, context_id=ctx_id)
        return None

    def _mask_credentials(self, data: dict):
        if "httpCredentials" in data:
            data["httpCredentials"] = "XXX"
        return data

    def _set_video_path(self, params: dict) -> dict:
        record_video = params.get("recordVideo", {})
        video_path = record_video.get("dir")
        if not record_video:
            return params
        if video_path is None:
            vid_path = self.video_output
        elif Path(video_path).is_absolute():
            vid_path = params["recordVideo"]["dir"]
        else:
            vid_path = self.video_output / video_path
        params["recordVideo"]["dir"] = Path(vid_path).resolve().absolute()
        return params

    def _get_record_video_size(self, params) -> tuple[Optional[int], Optional[int]]:
        width = params.get("recordVideo", {}).get("size", {}).get("width")
        height = params.get("recordVideo", {}).get("size", {}).get("height")
        return int(width) if width else None, int(height) if height else None

    def _set_video_size_to_int(self, params: dict) -> dict:
        if "recordVideo" not in params:
            return params
        params["recordVideo"]["size"] = self._get_video_size(params)
        return params

    def _get_video_size(self, params: dict) -> dict:
        width, height = self._get_record_video_size(params)
        if width and height:
            return {"width": width, "height": height}
        if "viewport" in params:
            return params["viewport"]
        return {"width": 1280, "height": 720}

    @keyword(tags=("Setter", "BrowserControl"))
    def new_page(
        self,
        url: Optional[str] = None,
        wait_until: PageLoadStates = PageLoadStates.load,
    ) -> NewPageDetails:
        """Open a new Page.

        A Page is the Playwright equivalent to a tab. See `Browser, Context and Page`
        for more information about Page concept.

        | =Arguments=    | =Description= |
        | ``url``        | Optional URL to navigate the page to. The url should include protocol, e.g. `https://` |
        | ``wait_until`` | When to consider operation succeeded, defaults to load. Events can be either: ``domcontentloaded`` - consider operation to be finished when the DOMContentLoaded event is fired. ``load`` - consider operation to be finished when the load event is fired. ``networkidle`` - consider operation to be finished when there are no network connections for at least 500 ms. ``commit`` - consider operation to be finished when network response is received and the document started loading. |


        Returns `NewPageDetails` as dictionary for created page.
        `NewPageDetails` (dict) contains the keys ``page_id`` and ``video_path``. ``page_id`` is a stable identifier for
        the created page. ``video_path`` is path to the created video or empty if video is not
        created.

        When a `New Page` is called without an open browser, `New Browser`
        and `New Context` are executed with default values first.

        [https://forum.robotframework.org/t//4308|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.NewPage(
                # '' will be treated as falsy on .ts side.
                # TODO: Use optional url field instead once it stabilizes at upstream
                # https://stackoverflow.com/a/62566052
                Request().UrlOptions(
                    url=Request().Url(
                        url=(url or ""), defaultTimeout=int(self.timeout)
                    ),
                    waitUntil=wait_until.name,
                )
            )
        logger.info(response.log)
        if response.newBrowser:
            logger.info(
                "No browser and context was open. New browser and context was "
                "automatically opened when page is created."
            )
        if response.newContext and not response.newBrowser:
            logger.info(
                "No context was open. New context was automatically opened when "
                "this page is created."
            )
        video_path = self._embed_video(json.loads(response.video))
        return NewPageDetails(page_id=response.body, video_path=video_path)

    def _embed_video(self, video: dict) -> str:
        if not video.get("video_path"):
            logger.debug("Video is not enabled.")
            return ""
        video_path = video.get("video_path")
        relative_path = get_link_path(video_path, self.outputdir)
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
        return str(video_path)

    @keyword(tags=("Getter", "BrowserControl", "Assertion"))
    @with_assertion_polling
    @assertion_formatter_used
    def get_browser_catalog(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> list[BrowserInfo]:
        """Returns all browsers, open contexts in them and open pages in these contexts.

        See `Browser, Context and Page` for more information about these concepts.

        | =Arguments= | =Description= |
        | assertion_operator | Optional assertion operator. See `Assertions` for more information. |
        | assertion_expected | Optional expected value. See `Assertions` for more information. |
        | message            | Optional custom message to use on failure. See `Assertions` for more information. |

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

        [https://forum.robotframework.org/t//4259|Comment >>]
        """

        catalog = self._get_browser_catalog()
        logger.debug(json.dumps(catalog, indent=2))
        formatter = self.get_assertion_formatter("Get Browser Catalog")
        return verify_assertion(
            catalog,
            assertion_operator,
            assertion_expected,
            "Browser Catalog",
            message,
            formatter,
        )

    def _get_browser_catalog(self, include_page_details: bool = True) -> list:
        with self.playwright.grpc_channel() as stub:
            response = stub.GetBrowserCatalog(
                Request().Bool(value=include_page_details)
            )
            return json.loads(response.json)

    @keyword(tags=("Getter", "BrowserControl", "Assertion"))
    def get_console_log(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
        *,
        full: bool = False,
        last: Union[int, timedelta, None] = None,
    ) -> list[dict]:
        """Returns the console log of the active page.

        If assertions are used and fail, this keyword will fail immediately without retrying.

        | =Arguments= | =Description= |
        | assertion_operator | Optional assertion operator. See `Assertions` for more information. |
        | assertion_expected | Optional expected value. See `Assertions` for more information. |
        | message            | Optional custom message to use on failure. See `Assertions` for more information. |
        | full               | If true, returns the full console log. If false, returns only new entries that were added since last time. |
        | last               | If set, returns only the last n entries. Can be `int` for number of entries or `timedelta` for time period. |

        The returned data is a `list` of log messages.

        A log message is a `dict` with the following structure:
        | [{
        |   "type": str,
        |   "text": str,
        |   "location": {
        |     "url": str,
        |     "lineNumber": int,
        |     "columnNumber": int
        |   },
        |   "time": str
        | }]

        Example:
        | [{
        |   'type': 'log',
        |   'text': 'Stuff loaded...',
        |   'location': {
        |     'url': 'https://example.com/js/chunk-769742de.6a462276.js',
        |     'lineNumber': 60,
        |     'columnNumber': 63771
        |   },
        |   'time': '2023-02-05T17:42:52.064Z'
        | }]

        Keys:
        | =Key= | =Description= |
        | ``type`` | One of the following values: ``log``, ``debug``, ``info``, ``error``, ``warning``, ``dir``, ``dirxml``, ``table``, ``trace``, ``clear``, ``startGroup``, ``startGroupCollapsed``, ``endGroup``, ``assert``, ``profile``, ``profileEnd``, ``count``, ``timeEnd`` |
        | ``text`` | The text of the console message. |
        | ``location.url`` | The URL of the resource that generated this message. |
        | ``location.lineNumber`` | The line number in the resource that generated this message (0-based). |
        | ``location.columnNumber`` | The column number in the resource that generated this message (0-based). |
        | ``time`` | The timestamp of the log message as ISO 8601 string. |

        [https://forum.robotframework.org/t//5267|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetConsoleLog(Request().Bool(value=full))
            if response.log:
                logger.info(response.log)
            log_messages = json.loads(response.json)
            returned_messages = self._slice_messages(log_messages, last)
            return verify_assertion(
                returned_messages,
                assertion_operator,
                assertion_expected,
                "Console Log",
                message,
            )

    @keyword(tags=("Getter", "BrowserControl", "Assertion"))
    def get_page_errors(
        self,
        assertion_operator: Optional[AssertionOperator] = None,
        assertion_expected: Optional[Any] = None,
        message: Optional[str] = None,
        *,
        full: bool = False,
        last: Union[int, timedelta, None] = None,
    ) -> dict:
        """Returns the page errors of the active page.

        If assertions are used and fail, this keyword will fail immediately without retrying.

        | =Arguments= | =Description= |
        | assertion_operator | Optional assertion operator. See `Assertions` for more information. |
        | assertion_expected | Optional expected value. See `Assertions` for more information. |
        | message            | Optional custom message to use on failure. See `Assertions` for more information. |
        | full               | If true, returns the full console log. If false, returns only new entries that were added since last time. |
        | last               | If set, returns only the last n entries. Can be `int` for number of entries or `timedelta` for time period. |

        The returned data is a `list` of error messages.

        An error message is a `dict` with the following structure:
        | {
        |   "name": str,
        |   "message": str,
        |   "stack": str,
        |   "time": str
        | }

        Example:
        | [{
        |   'name': 'ReferenceError',
        |   'message': 'YT is not defined',
        |   'stack': 'ReferenceError: YT is not defined\\n    at HTMLIFrameElement.onload (https://example.com/:20:2245)',
        |   'time': '2023-02-05T20:08:48.912Z'
        | }]

        Keys:
        | =Key= | =Description= |
        | ``name`` | The name/type of the error. |
        | ``message`` | The human readable error message. |
        | ``stack`` | The stack trace of the error, if given. |
        | ``time`` | The timestamp of the error as ISO 8601 string. |

        [https://forum.robotframework.org/t//5268|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetErrorMessages(Request().Bool(value=full))
            if response.log:
                logger.info(response.log)
            errors = json.loads(response.json)
            returned_errors = self._slice_messages(errors, last)
            return verify_assertion(
                returned_errors,
                assertion_operator,
                assertion_expected,
                "Page Errors",
                message,
            )

    def _slice_messages(self, message, last):
        if isinstance(last, int):
            return message[-last:]
        if not isinstance(last, timedelta):
            return message
        returned_messages = []
        now = datetime.now(timezone.utc)
        for msg in reversed(message):
            if datetime.strptime(msg["time"], "%Y-%m-%dT%H:%M:%S.%f%z") < now - last:
                # Only from python 3.11 and later... datetime.fromisoformat(msg["time"]) < now - last:
                break
            returned_messages.append(msg)
        return returned_messages

    @keyword(tags=("Setter", "BrowserControl"))
    def switch_browser(self, id: str) -> str:  # noqa: A002
        """Switches the currently active Browser to another open Browser.

        Returns a stable identifier for the previous browser.
        See `Browser, Context and Page` for more information about Browser and related concepts.

        | =Arguments= | =Description= |
        | id          | The id of the browser to switch to. Example: ``browser=96207191-8147-44e7-b9ac-5e04f2709c1d``. A browser id is returned by `New Browser` when it is started or can be fetched from the browser catalog when returned by `Get Browser Catalog`. |

        [https://forum.robotframework.org/t//4334|Comment >>]
        """
        logger.info(f"Switching browser to {id}")
        return self._switch_browser(id)

    def _switch_browser(self, id: str, loglevel: LOGLEVEL = "INFO") -> str:  # noqa: A002
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchBrowser(Request().Index(index=id))
            logger.write(
                response.log,
                loglevel=loglevel,
            )
            return response.body

    @keyword(tags=("Setter", "BrowserControl"))
    def switch_context(
        self,
        id: str,  # noqa: A002
        browser: Union[SelectionType, str] = SelectionType.CURRENT,
    ) -> str:
        """Switches the active BrowserContext to another open context.

        Returns a stable identifier for the previous context.
        See `Browser, Context and Page` for more information about Context and related concepts.

        | =Arguments= | =Description= |
        | ``id``      | The id of the context to switch to. Example: ``context=525d8e5b-3c4e-4baa-bfd4-dfdbc6e86089``. A context id is returned by `New Context` when it is started or can be fetched from the browser catalog when returned by `Get Browser Catalog`. |
        | ``browser`` | The browser in which to search for that context. ``CURRENT`` for the currently active browser, ``ALL`` to search in all open browsers or the id of the browser where to switch context. |

        Example:
        | ${first_context} =     `New Context`
        | `New Page`             ${URL1}
        | ${second_context} =    `New Context`
        | `New Page`             ${URL2}
        | `Switch Context`       ${first_context}    # Switches back to first context and page.

        [https://forum.robotframework.org/t//4335|Comment >>]
        """
        logger.info(f"Switching context to {id} in {browser}")
        browser = SelectionType.create(browser)
        id = SelectionType.create(id)  # noqa: A001

        if isinstance(id, str):
            parent_browser_id = self._get_context_parent_id(id)
            if browser == SelectionType.ALL:
                self._correct_browser(parent_browser_id)
            else:
                if isinstance(browser, str) and browser != parent_browser_id:
                    raise ValueError(f"Context {id} is not in browser {browser}")
                self._correct_browser(browser)
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchContext(Request().Index(index=str(id)))
            logger.info(response.log)
            return response.body

    def _get_page_uid(self, id) -> str:  # noqa: A002
        if isinstance(id, dict):
            uid = id.get("page_id")
            if not uid:
                raise ValueError(
                    f"Invalid page id format: {id} . Expected format: {NewPageDetails.__annotations__}"
                )
        else:
            uid = SelectionType.create(id)
        if isinstance(uid, str) and not (
            uid.lower().startswith("page=") or uid.upper() == "NEW"
        ):
            raise ValueError(f"Malformed page `id`: {uid}")
        return uid

    @keyword(tags=("Setter", "BrowserControl"))
    def switch_page(
        self,
        id: Union[NewPageDetails, str],  # noqa: A002
        context: Union[SelectionType, str] = SelectionType.CURRENT,
        browser: Union[SelectionType, str] = SelectionType.CURRENT,
    ) -> str:
        """Switches the active browser page to another open page by ``id`` or ``NEW``.

        Returns a stable identifier ``id`` for the previous page.
        See `Browser, Context and Page` for more information about Page and related concepts.

        | =Arguments= | =Description= |
        | ``id``      | The id or alias of the page to switch to. Example: ``page=8baf2991-5eaf-444d-a318-8045f914e96a`` or ``NEW``. Can be a string or a dictionary returned by `New Page` Keyword. A page id can be fetched from the browser catalog when returned by `Get Browser Catalog`. ``NEW`` can be used to switch to a pop-up that just has been opened by the webpage, ``CURRENT`` can be used to switch to the active page of a different context or browser, identified by their id. |
        | ``context`` | The context in which to search for that page. ``CURRENT`` for the currently active context, ``ALL`` to search in all open contexts or the id of the context where to switch page. |
        | ``browser`` | The browser in which to search for that page. ``CURRENT`` for the currently active browser, ``ALL`` to search in all open browsers or the id of the browser where to switch page. |

        ``New`` may timeout if no new pages exists before library timeout.

        Example:
        | `Click`           button#pops_up    # Open new page
        | ${previous} =    `Switch Page`      NEW

        [https://forum.robotframework.org/t//4336|Comment >>]
        """
        logger.info(f"Switching to page {id},context {context}, browser {browser}")
        context = SelectionType.create(context)
        browser = SelectionType.create(browser)
        correct_context_selected = True
        correct_browser_selected = True
        uid = self._get_page_uid(id)

        if (
            not (isinstance(uid, str) and uid.upper() == "NEW")
            and uid != SelectionType.CURRENT
        ):
            parent_browser_id, parent_context_id = self._get_page_parent_ids(str(uid))
            if isinstance(browser, str) and browser != parent_browser_id:
                logger.error(
                    f"Page {uid} is not in browser {browser}. Switching to browser {parent_browser_id}"
                )
                correct_browser_selected = False
            if isinstance(context, str) and context != parent_context_id:
                logger.error(
                    f"Page {uid} is not in context {context}. Switching to context {parent_context_id}"
                )
                correct_context_selected = False
            if not correct_context_selected or not correct_browser_selected:
                raise ValueError(f"Page Switch to {uid} failed")

            if context == SelectionType.ALL:
                self.switch_context(parent_context_id, browser)
            elif context == SelectionType.CURRENT and browser == SelectionType.ALL:
                self.switch_browser(parent_browser_id)
            elif context == SelectionType.ALL and browser == SelectionType.ALL:
                self.switch_context(parent_context_id, parent_browser_id)
            elif isinstance(context, str):
                self.switch_context(context, browser)
            elif context == SelectionType.CURRENT and isinstance(browser, str):
                self.switch_browser(browser)

        logger.debug(f"Page:    {uid}")
        logger.debug(f"Context: {context}")
        logger.debug(f"Browser: {browser}")

        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchPage(
                Request().IdWithTimeout(id=str(uid), timeout=self.timeout)
            )
            logger.info(response.log)
            return response.body

    def _get_page_parent_ids(self, page_id: str) -> tuple[str, str]:
        browser_catalog = self._get_browser_catalog(include_page_details=False)
        for browser in browser_catalog:
            for context in browser["contexts"]:
                for page in context["pages"]:
                    if page["id"] == page_id:
                        return browser["id"], context["id"]
        raise ValueError(f"No page with requested id '{page_id}' found.")

    def _get_context_parent_id(self, context_id: str) -> str:
        browser_catalog = self._get_browser_catalog(include_page_details=False)
        for browser in browser_catalog:
            for context in browser["contexts"]:
                if context["id"] == context_id:
                    return browser["id"]
        raise ValueError(f"No context with requested id '{context_id}' found.")

    @keyword(tags=("Getter", "BrowserControl"))
    def get_browser_ids(self, browser: SelectionType = SelectionType.ALL) -> list[str]:
        """Returns a list of ids from open browsers.
        See `Browser, Context and Page` for more information about Browser and related concepts.


        ``browser`` Defaults to ``ALL``
        - ``ALL`` / ``ANY`` Returns all ids as a list.
        - ``ACTIVE`` / ``CURRENT`` Returns the id of the currently active browser as list.

        | =Arguments= | =Description= |
        | ``browser`` | The browser to get the ids from. ``ALL`` for all open browsers, ``ACTIVE`` for the currently active browser or the id of the browser to get the ids from. |

        The ACTIVE browser is a synonym for the CURRENT Browser.

        [https://forum.robotframework.org/t//4260|Comment >>]
        """
        if browser == SelectionType.CURRENT:
            browser_item = self._get_active_browser_item(
                self._get_browser_catalog(include_page_details=False)
            )
            if "id" in browser_item:
                return [browser_item["id"]]
        else:
            return [
                browser["id"]
                for browser in self._get_browser_catalog(include_page_details=False)
            ]
        return []

    @keyword(tags=("Getter", "BrowserControl"))
    def get_context_ids(
        self,
        context: SelectionType = SelectionType.ALL,
        browser: SelectionType = SelectionType.ALL,
    ) -> list:
        """Returns a list of context ids based on the browser selection.
        See `Browser, Context and Page` for more information about Context and related concepts.

        ``ALL`` and ``ANY`` are synonyms.
        ``ACTIVE`` and ``CURRENT`` are also synonyms.

        | =Arguments= | =Description= |
        | ``context`` | The context to get the ids from. ``ALL`` will return all ids from selected browser(s), ``ACTIVE`` for the one active context of each selected browser. |
        | ``browser`` | The browser to get the context ids from. ``ALL`` Context ids from all open browsers shall be fetched. ``ACTIVE`` Only context ids from the active browser shall be fetched. |

        The ACTIVE context of the ACTIVE Browser is the ``Current`` Context.

        [https://forum.robotframework.org/t//4264|Comment >>]
        """
        if browser == SelectionType.CURRENT:
            browser_item = self._get_active_browser_item(
                self._get_browser_catalog(include_page_details=False)
            )
            if context == SelectionType.CURRENT:
                if "activeContext" in browser_item:
                    return [browser_item["activeContext"]]
            elif "contexts" in browser_item:
                return [context["id"] for context in browser_item["contexts"]]
        elif context == SelectionType.CURRENT:
            context_ids = []
            for browser_item in self._get_browser_catalog(include_page_details=False):
                if "activeContext" in browser_item:
                    context_ids.append(browser_item["activeContext"])
            return context_ids
        else:
            context_ids = []
            for browser_item in self._get_browser_catalog(include_page_details=False):
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
    ) -> list:
        """Returns a list of page ids based on the context and browser selection.
        See `Browser, Context and Page` for more information about Page and related concepts.

        ``ALL`` and ``ANY`` are synonyms.
        ``ACTIVE`` and ``CURRENT`` are also synonyms.

        | =Arguments= | =Description= |
        | ``page``    | The page to get the ids from. ``ALL`` Returns all page ids as a list. ``ACTIVE`` Returns the id of the active page as a list. |
        | ``context`` | The context to get the page ids from. ``ALL`` Page ids from all contexts shall be fetched. ``ACTIVE`` Only page ids from the active context shall be fetched. |
        | ``browser`` | The browser to get the page ids from. ``ALL`` Page ids from all open browsers shall be fetched. ``ACTIVE`` Only page ids from the active browser shall be fetched. |


        Example:
        | Test Case
        |     `New Page`    http://www.imbus.de
        |     `New Page`    http://www.reaktor.com
        |     ${current_page}=   `Get Page IDs`    ACTIVE    ACTIVE    ACTIVE
        |     Log                Current page ID is: ${current_page}[0]
        |     ${all_pages}=      `Get Page IDs`    CURRENT   CURRENT   ALL
        |     Log Many           These are all Page IDs    @{all_pages}

        The ACTIVE page of the ACTIVE context of the ACTIVE Browser is the ``Current`` Page.

        [https://forum.robotframework.org/t//4274|Comment >>]
        """
        if browser == SelectionType.CURRENT:
            browser_item = self._get_active_browser_item(
                self._get_browser_catalog(include_page_details=False)
            )
            if "contexts" in browser_item:
                if context == SelectionType.CURRENT:
                    return self._get_page_ids_from_context_list(
                        page, self._get_active_context_item(browser_item)
                    )
                return self._get_page_ids_from_context_list(
                    page, browser_item["contexts"]
                )
        else:
            context_list = []
            for browser_item in self._get_browser_catalog(include_page_details=False):
                if "contexts" in browser_item:
                    if context == SelectionType.CURRENT:
                        context_list.extend(self._get_active_context_item(browser_item))
                    else:
                        context_list.extend(browser_item["contexts"])
            return self._get_page_ids_from_context_list(page, context_list)
        return []

    @staticmethod
    def _get_page_ids_from_context_list(
        page_selection_type: SelectionType, context_list
    ):
        page_ids = []
        for context_item in context_list:
            if page_selection_type == SelectionType.CURRENT:
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

    @keyword(tags=("Getter", "BrowserControl"))
    def save_storage_state(self) -> str:
        """Saves the current active context storage state to a file.

        Web apps use cookie-based or token-based authentication, where
        authenticated state is stored as
        [https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies|cookies]
        or in
        [https://developer.mozilla.org/en-US/docs/Web/API/Storage|local storage].
        Keyword retrieves the storage state from authenticated contexts and
        save it to disk. Then `New Context` can be created with prepopulated
        state.

        Please note state file may contains secrets and should not be shared
        with people outside of your organisation.

        The file is created in ${OUTPUTDIR}/browser/state folder and file(s)
        are automatically deleted when new test execution starts. File path
        is returned by the keyword.

        Example:
        | Test Case
        |     `New context`
        |     `New Page`    https://login.page.html
        |     #  Perform login
        |     `Fill Secret`    id=username    $username
        |     `Fill Secret`    id=password    $password
        |     `Click`    id=button
        |     `Get Text`    id=header    ==    Something
        |     #  Save storage to disk
        |     ${state_file} =    `Save Storage State`
        |     #  Create new context with saved state
        |     `New context`    storageState=${state_file}
        |     `New Page`    https://login.page.html
        |     #  Login is not needed because authentication is read from state file
        |     `Get Text`    id=header    ==    Something

        [https://forum.robotframework.org/t//4318|Comment >>]
        """
        file = str(self.state_file / f"{uuid4()!s}.json")
        self.state_file.mkdir(parents=True, exist_ok=True)
        log = self._save_storage_state(file)
        logger.info(log)
        return file

    def _save_storage_state(self, path: str) -> str:
        with self.playwright.grpc_channel() as stub:
            response = stub.SaveStorageState(Request().FilePath(path=path))
        return response.log

    def set_peer_id(self, new_id) -> str:
        """Sets the peer_id for the current GRPC connection to browser's backend.

        Useful for sharing the same browsers or even pages among multiple separate
        python processes. Meaningful usage requires the port of both Browser library
        instances to be configured the same.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SetPeerId(Request().Index(index=new_id))
            return response.body

    @keyword(tags=("Setter", "BrowserControl"))
    def cancel_download(self, download: Union[DownloadInfo, str]):
        """Cancels an active download.

        | =Arguments= | =Description= |
        | download    | A `DownloadInfo` object or id of the download to be canceled. |

        [https://forum.robotframework.org/t//6478|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.CancelDownload(
                Request().DownloadID(id=get_download_id(download))
            )
            logger.info(response.log)

    # Mute this from automatic group logging before this is exposed as keyword
    def open_trace_group(
        self,
        name: str,
        file: Union[Path, str, None] = None,
        line: int = 0,
        column: int = 0,
        context_id: str = "",
    ):
        """Opens the trace group in the trace viewer"""
        if not self.library.tracing_contexts:
            return
        with suppress(Exception), self.playwright.grpc_channel() as stub:
            stub.OpenTraceGroup(
                Request().TraceGroup(
                    name=name,
                    file=str(file or ""),
                    line=line,
                    column=column,
                    contextId=context_id,
                )
            )

    # Mute this from automatic group logging before this is exposed as keyword
    def close_trace_group(self):
        """Closes the trace group in the trace viewer"""
        if not self.library.tracing_contexts:
            return
        with suppress(Exception), self.playwright.grpc_channel() as stub:
            stub.CloseTraceGroup(Request().Empty())
