__version__ = "0.1.0"
import grpc  # type: ignore

from robot.api import logger  # type: ignore

import Playwright.generated.playwright_pb2 as playwright_pb2
import Playwright.generated.playwright_pb2_grpc as playwright_pb2_grpc

_SUPPORTED_BROWSERS = ["chrome", "firefox", "webkit"]


class Playwright:
    """Playwright library is a web testing library for Robot Framework.

    This documents explains how to use keywords provided by the Playwright
    library. For information about installation, support, and more, please
    visit the
    [https://github.com/MarketSquare/robotframework-playwright|project pages].
    For more information about Robot Framework, see http://robotframework.org.

    Playwright library uses
    [https://github.com/microsoft/playwright|Playwright Node module]
    to automate [https://www.chromium.org/Home|Chromium],
    [https://www.mozilla.org/en-US/firefox/new/|Firefox]
    and [https://webkit.org/|WebKit] with a single library.

    == Table of contents ==

    %TOC%

    = Locating elements =

    All keywords in Playwright library that need to interact with an element
    on a web page take an argument typically named ``locator`` that specifies
    how to find the element.

    == Locator syntax ==

    Playwright library supports same locator strategies as the underlying
    Playwright None module: xpath, css and text. The strategy can either be
    explicitly specified with a prefix or the strategy can be implicit.

    === Implicit locator strategy ===

    The default locator strategy is `css`. If locator does not contain
    one of the know locator strategies, `css`, `xpath` or `text` it is
    assumed to contain css locator. Also `locators` starting with `//` or
    `(//` are considered as xpath locators.

    Examples:

    | `Click` | span > button | # Use css locator strategy the element.   |
    | `Click` | //span/button | # Use xpath locator strategy the element. |

    === Explicit locator strategy ===

    The explicit locator strategy is specified with a prefix using syntax
    ``strategy:value``. Spaces around the separator are ignored, so
    ``css:foo``, ``css: foo`` and ``css : foo`` are all equivalent.

    Locator strategies that are supported by default are listed in the table
    below.

    | = Strategy = |    = Match based on =   |         = Example =            |
    | css          | CSS selector.           | ``css:div#example``            |
    | xpath        | XPath expression.       | ``xpath://div[@id="example"]`` |
    | text         | Playwright text engine. | ``text:Login``                 |
    """

    @staticmethod
    def open_browser(browser="Chrome", url=None):
        if url is None:
            url = "about:blank"
        browser_ = browser.lower().strip()
        if browser_ not in _SUPPORTED_BROWSERS:
            raise ValueError(
                f"{browser} is not supported, "
                f'it should be one of: {", ".join(_SUPPORTED_BROWSERS)}'
            )
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = playwright_pb2_grpc.PlaywrightStub(channel)
            response = stub.OpenBrowser(
                playwright_pb2.openBrowserRequest(url=url, browser=browser_)
            )
            logger.info(response.log)

    @staticmethod
    def close_browser():
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = playwright_pb2_grpc.PlaywrightStub(channel)
            response = stub.CloseBrowser(playwright_pb2.Empty())
            logger.info(response.log)
