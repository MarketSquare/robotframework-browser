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
from typing import Any, Dict, Optional

from typing_extensions import Literal

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger
from ..utils.data_types import PageLoadStates, RequestMethod


def _get_headers(body: str, headers: Dict):
    try:
        json.loads(body)
        return {"Content-Type": "application/json", **headers}
    except json.decoder.JSONDecodeError:
        return headers


def _format_response(response: Dict):
    _jsonize_content(response, "body")
    if "request" in response:
        request = response["request"]
        _jsonize_content(request, "postData")
    logger.info(response)
    return response


def _jsonize_content(data, bodykey):
    headers = json.loads(data["headers"])
    data["headers"] = headers
    lower_headers = dict((k.lower(), v) for k, v in headers.items())
    if (
        "content-type" in lower_headers
        and "application/json" in lower_headers["content-type"]
    ):
        try:
            data[bodykey] = json.loads(data[bodykey])
        except json.decoder.JSONDecodeError:
            pass


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
          - ``statusText`` <str> Status text corresponding to ``status``, e.g OK or INTERNAL SERVER ERROR.
          - ``body`` <dict> | <str> The response body. If the body can be parsed as a JSON obejct,
          it will be returned as Python dictionary, otherwise it is returned as a string.
          - ``headers`` <dict> A dictionary containing all response headers.
          - ``ok`` <bool> Whether the request was successfull, i.e. the ``status`` is range 200-299.

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
            return _format_response(json.loads(response.json))

    def _wait_for_http(self, method: Literal["Request", "Response"], matcher, timeout):
        with self.playwright.grpc_channel() as stub:
            function = getattr(stub, f"WaitFor{method}")
            response = function(
                Request().HttpCapture(
                    urlOrPredicate=matcher,
                    timeout=self.get_timeout(timeout),
                )
            )
            logger.debug(response.log)
            # Add format response back here
            return (
                response.body
                if method == "Request"
                else _format_response(json.loads(response.json))
            )

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_request(
        self, matcher: str = "", timeout: Optional[timedelta] = None
    ) -> Any:
        """Waits for request matching matcher to be made.


        | =Arguments= | =Description= |
        | ``matcher`` | Request URL string, JavaScript regex or JavaScript function to match request by. By default (with empty string) matches first available request. For additional information, see the Playwright [https://playwright.dev/docs/api/class-page/#page-wait-for-request|waitForRequest documentation]. |
        | ``timeout`` | Timeout supports Robot Framework time format. Uses default timeout if not set. |


        Example:
        | `Click`               \\#delayed_request
        | `Wait For Request`    timeout=1s

        Async Example:
        | ${promise} =    `Promise To`         `Wait For Request`    matcher=\\\\/\\\\/local\\\\w+\\\\:\\\\d+\\\\/api    timeout=3s
        | `Click`         \\#delayed_request
        | `Wait For`      ${promise}

        JavaScript Function Example:
        | `Click`               \\#delayed_request    # Creates response which should be waited before pressing save.
        | `Wait For Request`    [https://playwright.dev/docs/api/class-request|request] => request.url().endsWith('api/get/json') && request.method() === 'GET'

        [https://forum.robotframework.org/t//4348|Comment >>]
        """
        return self._wait_for_http("Request", matcher, timeout)

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_response(
        self, matcher: str = "", timeout: Optional[timedelta] = None
    ) -> Any:
        """Waits for response matching matcher and returns python dict with contents.


        | =Arguments= | =Description= |
        | ``matcher`` | Request URL string, JavaScript regex or JavaScript function to match request by. By default (with empty string) matches first available request. For additional information, see the Playwright [https://playwright.dev/docs/api/class-page/#page-wait-for-response|waitForResponse documentation]. |
        | ``timeout`` | Timeout supports Robot Framework time format. Uses default timeout if not set. |

        The response is a Python dictionary with following attributes:
          - ``status`` <int> The status code of the response.
          - ``statusText`` <str> Status text corresponding to ``status``, e.g OK or INTERNAL SERVER ERROR.
          - ``body`` <dict | str> The response body. If the body can be parsed as a JSON obejct,
          it will be returned as Python dictionary, otherwise it is returned as a string.
          - ``headers`` <dict> A dictionary containing all response headers.
          - ``ok`` <bool> Whether the request was successfull, i.e. the ``status`` is range 200-299.
          - ``request`` <dict> containing ``method`` <str>, ``headers`` <dict> and ``postData`` <dict> | <str>
          - ``url`` <str> url of the request.

        Synchronous Example:
        | `Click`                \\#delayed_request    # Creates response which should be waited before next actions
        | `Wait For Response`    matcher=\\\\/\\\\/local\\\\w+\\\\:\\\\d+\\\\/api
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
        return self._wait_for_http("Response", matcher, timeout)

    @keyword(tags=("Wait", "HTTP"))
    def wait_until_network_is_idle(self, timeout: Optional[timedelta] = None):
        """Waits until there has been at least one instance of 500 ms of no network traffic on the page after loading.

        Doesn't wait for network traffic that wasn't initiated within 500ms of page load.

        | =Arguments= | =Description= |
        | ``timeout`` | Timeout supports Robot Framework time format. Uses browser timeout if not set. |

        Example:
        | `Go To`                         ${URL}
        | `Wait Until Network Is Idle`    timeout=3s

        [https://forum.robotframework.org/t//4350|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.WaitUntilNetworkIsIdle(
                Request().Timeout(timeout=self.get_timeout(timeout))
            )
            logger.debug(response.log)

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_navigation(
        self,
        url: str,
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
