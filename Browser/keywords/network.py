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

import contextlib
import json
from datetime import timedelta
from typing import Any, Optional, Union

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import DotDict, keyword, logger
from ..utils.data_types import PageLoadStates, RegExp, RequestMethod


def _get_headers(body: str, headers: dict):
    try:
        json.loads(body)
        return {"Content-Type": "application/json", **headers}
    except json.decoder.JSONDecodeError:
        return headers


def _format_response(response: dict) -> dict:
    _jsonize_content(response, "body")
    if "request" in response:
        request = response["request"]
        _jsonize_content(request, "postData")
    logger.info(response)
    return response


def _jsonize_content(data, bodykey):
    headers = json.loads(data.get("headers", "{}"))
    data["headers"] = headers
    lower_headers = {k.lower(): v for k, v in headers.items()}
    if (
        "content-type" in lower_headers
        and "application/json" in lower_headers["content-type"]
        and bodykey in data
        and data[bodykey]
    ):
        with contextlib.suppress(json.decoder.JSONDecodeError, TypeError):
            data[bodykey] = json.loads(data[bodykey])


class Network(LibraryComponent):
    @keyword(tags=("HTTP",))
    def http(
        self,
        url: str,
        method: RequestMethod = RequestMethod.GET,
        body: Optional[str] = None,
        headers: Optional[dict] = None,
    ) -> Any:
        """Performs an HTTP request in the current browser context

        | =Arguments= | =Description= |
        | ``url`` | The request url, e.g. ``/api/foo``. |
        | ``method`` | The HTTP method for the request. Defaults to GET. |
        | ``body`` | The request body. GET requests cannot have a body. If the body can be parsed as JSON, the ``Content-Type`` header for the request will be automatically set to ``application/json``. Defaults to None. |
        | ``headers`` | A dictionary of additional request headers. Defaults to None. |

        The response is a Python dictionary with following attributes:
          - ``status`` <int> The status code of the response.
          - ``statusText`` <str> Status text corresponding to ``status``, e.g OK or INTERNAL SERVER ERROR. This may not be available for all browser.
          - ``body`` <dict> | <str> The response body. If the body can be parsed as a JSON object,
          it will be returned as Python dictionary, otherwise it is returned as a string.
          - ``headers`` <dict> A dictionary containing all response headers.
          - ``ok`` <bool> Whether the request was successful, i.e. the ``status`` is range 200-299.

        Here's an example of using Robot Framework dictionary variables and extended variable syntax to
        do assertions on the response object:

        | &{res}=             `HTTP`                       /api/endpoint
        | Should Be Equal     ${res.status}              200
        | Should Be Equal     ${res.body.some_field}     some value

        [https://forum.robotframework.org/t//4296|Comment >>]
        """
        if headers is None:
            headers = {}
        body = body if body else ""
        with self.playwright.grpc_channel() as stub:
            response = stub.HttpRequest(
                Request().HttpRequest(
                    url=url,
                    method=method.name if method else "GET",
                    body=body,
                    headers=json.dumps(_get_headers(body, headers)),
                )
            )
            logger.debug(response.log)
            response_dict = _format_response(json.loads(response.json))
            try:
                return DotDict(response_dict)
            except Exception:
                logger.debug(f"Returned response is of type {type(response_dict)}")
                return response_dict

    def _wait_for_http_request(self, matcher, timeout):
        with self.playwright.grpc_channel() as stub:
            response = stub.WaitForRequest(
                Request().HttpCapture(
                    urlOrPredicate=matcher,
                    timeout=self.get_timeout(timeout),
                )
            )
            logger.debug(response.log)
            # Add format response back here
            return response.body

    def _wait_for_http_response(self, matcher, timeout):
        body = ""
        with self.playwright.grpc_channel() as stub:
            for responce in stub.WaitForResponse(
                Request().HttpCapture(
                    urlOrPredicate=matcher,
                    timeout=self.get_timeout(timeout),
                )
            ):
                logger.info(responce.log)
                body = body + responce.bodyPart
            response_json = json.loads(responce.json)
            not_none = object()
            with contextlib.suppress(json.decoder.JSONDecodeError):
                body = json.loads(body)
            if response_json.get("body", not_none) is not None and body:
                response_json["body"] = body
            return _format_response(response_json)

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_request(
        self, matcher: Union[str, RegExp] = "", timeout: Optional[timedelta] = None
    ) -> Any:
        """Waits for request matching matcher to be made.

        | =Arguments= | =Description= |
        | ``matcher`` | Request URL matcher. Can be a string (Glob-Pattern), JavaScript RegExp (encapsulated in / with following flags) or JavaScript arrow-function that receives the [https://playwright.dev/docs/api/class-request|Request] object and returns a boolean. By default (with empty string) matches first available request. For additional information, see the Playwright [https://playwright.dev/docs/api/class-page#page-wait-for-request|waitForRequest] documentation. |
        | ``timeout`` | Timeout supports Robot Framework time format. Uses default timeout if not set. |

        See `Wait For Response` for more details.

        *CAUTION:* Before Browser library 17.0.0, the ``matcher`` argument was always either a regex or JS function.
        But the regex did not needed to be in slashes.
        The most simple way to migrate to the new syntax is to add slashes around the matcher.
        So ``/api/get/json`` becomes ``//api/get/json/``.

        [https://forum.robotframework.org/t//4348|Comment >>]
        """
        request = self._wait_for_http_request(matcher, timeout)
        try:
            return DotDict(request)
        except Exception:
            logger.debug(f"Returned request is of type {type(request)}")
            return request

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_response(
        self, matcher: Union[str, RegExp] = "", timeout: Optional[timedelta] = None
    ) -> Union[DotDict, Any]:
        """Waits for response matching matcher and returns the response as robot dict.

        The response, which is returned by this keyword, is a robot dictionary with following attributes:
          - ``status`` <int> The status code of the response.
          - ``statusText`` <str> Status text corresponding to ``status``, e.g OK or INTERNAL SERVER ERROR. This may not be available for all browser.
          - ``body`` <dict | str> The response body. If the body can be parsed as a JSON object,
          it will be returned as Python dictionary, otherwise it is returned as a string.
          - ``headers`` <dict> A dictionary containing all response headers.
          - ``ok`` <bool> Whether the request was successful, i.e. the ``status`` is range 200-299.
          - ``request`` <dict> containing ``method`` <str>, ``headers`` <dict> and ``postData`` <dict> | <str>
          - ``url`` <str> url of the request.

        | =Arguments= | =Description= |
        | ``matcher`` | Request URL matcher. Can be a string (Glob-Pattern), JavaScript RegExp (encapsulated in / with following flags) or JavaScript arrow-function that receives the Response object and returns a boolean. By default (with empty string) matches first available request. For additional information, see the Playwright [https://playwright.dev/docs/api/class-page#page-wait-for-response|page.waitForResponse] documentation. |
        | ``timeout`` | Timeout supports Robot Framework time format. Uses default timeout if not set. |

        *CAUTION:* Before Browser library 17.0.0, the ``matcher`` argument was always either a regex or JS function.
        But the regex did not needed to be in slashes.
        The most simple way to migrate to the new syntax is to add slashes around the matcher.
        So ``/api/get/json`` becomes ``//api/get/json/``.

        == Matcher Examples: ==

        === Glob-Pattern: ===

        Glob-Patterns are strings that can contain wildcards. The following wildcards are supported:

        Possible wildcards/patterns are:
        - ``*`` matches any number of characters, except ``/``
        - ``**`` matches any number of characters, including ``/``
        - ``?`` matches one character, except ``/``
        - ``[abc]`` matches one character in the brackets (in this example ``a``, ``b`` or ``c``)
        - ``[a-z]`` matches one character in the range (in this example ``a`` to ``z``)
        - ``{foo,bar,baz}`` matches one of the strings in the braces (in this example ``foo``, ``bar`` or ``baz``)

        Example:
        | `Wait For Response`    **/api/get/text    # matches any request with url ending with /api/get/text. example: https://browser.fi/api/get/text

        === RegExp: ===

        Regular Expressions are JavaScript regular expressions encapsulated in ``/`` with optional following flags:
        Be aware that backslashes need to be escaped in Robot Framework, e.g. ``\\\\w`` instead of ``\\w``.
        See [https://regex101.com|regex101] for more information on Regular Expressions.

        Example:
        | `Wait For Response`    /http://\\\\w+:\\\\d+/api/get/text/i    # matches any request with url ending with /api/get/text and containing http:// followed by any word and port. example: http://localhost:8080/api/get/text

        === JavaScript Arrow-Function: ===

        JavaScript Arrow-Functions are anonymous JavaScript functions that receive the
        [https://playwright.dev/docs/api/class-response|Response] object and return a boolean.

        Example:
        | `Wait For Response`    response => response.url() === 'http://localhost/api/post' && response.status() === 200    # matches any response with url http://localhost/api/post and status code 200

        == Robot Examples: ==

        Synchronous Example:
        | `Click`                \\#delayed_request    # Creates response which should be waited before next actions
        | `Wait For Response`    matcher=/http://\\\\w+:\\\\d+/api/get/text/i
        | `Click`                \\#save

        Asynchronous Example:
        | ${promise} =    `Promise To`    `Wait For Response`    timeout=60s
        | `Click`           \\#delayed_request    # Creates response which should be waited before pressing save.
        | `Click`           \\#next
        | `Wait For`        ${promise}            # Waits for the response
        | `Click`           \\#save

        JavaScript Function Example:
        | `Click`               \\#delayed_request    # Creates response which should be waited before pressing save.
        | `Wait For Response`   [https://playwright.dev/docs/api/class-response/|response] => response.url().endsWith('json') && response.request().method() === 'GET'

        [https://forum.robotframework.org/t//4349|Comment >>]
        """
        response = self._wait_for_http_response(matcher, timeout)
        try:
            return DotDict(response)
        except Exception:
            logger.debug(f"Returned response is of type {type(response)}")
            return response

    @keyword(tags=("Wait", "HTTP"))
    def wait_until_network_is_idle(self, timeout: Optional[timedelta] = None):
        """*DEPRECATED!!* Use `Wait For Load State` instead. rfbrowser transform --wait-until-network-is-idle path/to/test command automatically transforms keyword to new format.

        If you have:
        | `Wait Until Network Is Idle`    timeout=3s
        then change it to:
        | `Wait For Load State`    networkidle    timeout=3s

        Waits until there has been at least one instance of 500 ms of no network traffic on the page after loading.

        Doesn't wait for network traffic that wasn't initiated within 500ms of page load.

        | =Arguments= | =Description= |
        | ``timeout`` | Timeout supports Robot Framework time format. Uses browser timeout if not set. |

        Example:
        | `Go To`                         ${URL}
        | `Wait Until Network Is Idle`    timeout=3s

        [https://forum.robotframework.org/t//4350|Comment >>]
        """
        self.library.wait_for_load_state(PageLoadStates.networkidle, timeout)

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_navigation(
        self,
        url: Union[str, RegExp],
        timeout: Optional[timedelta] = None,
        wait_until: PageLoadStates = PageLoadStates.load,
    ):
        """Waits until page has navigated to given ``url``.


        | =Arguments= | =Description= |
        | ``url`` | Expected navigation target address either the exact match or a JavaScript-like regex wrapped in ``/`` symbols. |
        | ``timeout`` | Timeout supports Robot Framework time format. Uses default timeout if not set. |
        | ``wait_until`` | When to consider operation succeeded, defaults to load. Events can be either: ``domcontentloaded`` - consider operation to be finished when the DOMContentLoaded event is fired. ``load`` - consider operation to be finished when the load event is fired. ``networkidle`` - consider operation to be finished when there are no network connections for at least 500 ms. ``commit`` - consider operation to be finished when network response is received and the document started loading. |


        Keyword works only when page is loaded and does not work if URL fragment changes. Example if
        https://marketsquare.github.io/robotframework-browser/Browser.html changes to
        https://marketsquare.github.io/robotframework-browser/Browser.html#Wait%20For%20Navigation
        keyword will fail.

        Example:
        | `Go To`                  ${ROOT_URL}/redirector.html
        | `Wait for navigation`    ${ROOT_URL}/posted.html    wait_until=${wait_until}

        [https://forum.robotframework.org/t//4347|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.WaitForNavigation(
                Request().UrlOptions(
                    url=Request().Url(
                        url=url, defaultTimeout=int(self.get_timeout(timeout))
                    ),
                    waitUntil=wait_until.name,
                )
            )
            logger.debug(response.log)
