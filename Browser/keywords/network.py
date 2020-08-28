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
from typing import Dict, Optional

from robotlibcore import keyword  # type: ignore
from typing_extensions import Literal

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.data_types import RequestMethod
from ..utils.time_conversion import timestr_to_millisecs


def _get_headers(body: str, headers: Dict):
    try:
        json.loads(body)
        return {"Content-Type": "application/json", **headers}
    except json.decoder.JSONDecodeError:
        return headers


def _format_response(response: Dict):
    headers = json.loads(response["headers"])
    response["headers"] = headers
    if "content-type" in headers and "application/json" in headers["content-type"]:
        try:
            response["body"] = json.loads(response["body"])
        except json.decoder.JSONDecodeError:
            pass
    logger.info(response)
    return response


class Network(LibraryComponent):
    @keyword(tags=["HTTP"])
    def http(
        self,
        url: str,
        method: RequestMethod = RequestMethod.GET,
        body: Optional[str] = None,
        headers: Optional[dict] = None,
    ):

        """Performs an HTTP request in the current browser context

        Accepts the following arguments:
          - ``url`` <str> The request url, e.g. ``/api/foo``.
          - ``method`` < ``GET`` | ``POST`` | ``PUT`` | ``PATCH`` | ``DELETE`` | ``HEAD`` > The HTTP method for the request. Defaults to GET.
          - ``body`` <str> The request body. GET requests cannot have a body. If the body can be parsed as JSON,
          the ``Content-Type`` header for the request will be automatically set to ``application/json``.
          Defaults to None.
          - ``headers`` <dict> A dictionary of additional request headers. Defaults to None.

        The response is a Python dictionary with following attributes:
          - ``status`` <int> The status code of the response.
          - ``statusText`` <str> Status text corresponding to ``status``, e.g OK or INTERNAL SERVER ERROR.
          - ``body`` <dict> | <str> The response body. If the body can be parsed as a JSON obejct,
          it will be returned as Python dictionary, otherwise it is returned as a string.
          - ``headers`` <dict> A dictionary containing all response headers.
          - ``ok`` <bool> Whether the request was successfull, i.e. the ``status`` is range 200-299.

        Here's an example of using Robot Framework dictionary variables and extended variable syntax to
        do assertions on the response object:

        | &{res}=             HTTP                       /api/endpoint
        | Should Be Equal     ${res.status}              200
        | Should Be Equal     ${res.body.some_field}     some value

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
            if not timeout:
                timeout = self.library.playwright.timeout
            function = getattr(stub, f"WaitFor{method}")
            response = function(
                Request().HttpCapture(
                    urlOrPredicate=matcher, timeout=timestr_to_millisecs(timeout),
                )
            )
            logger.debug(response.log)
            # Add format response back here
            return response.body if method == "Request" else response.json

    @keyword(tags=["Wait", "HTTP"])
    def wait_for_request(self, matcher: str = "", timeout: str = ""):
        """Waits for request matching matcher to be made.

        ``matcher`` <str> Request URL string, JavaScript regex or JavaScript function to match request by.
        By default (with empty string) matches first available request.

        ``timeout`` <str> Timeout in milliseconds. Uses default timeout of 10 seconds if not set.

        """
        return self._wait_for_http("Request", matcher, timeout)

    @keyword(tags=["Wait", "HTTP"])
    def wait_for_response(self, matcher: str = "", timeout: str = ""):
        """Waits for response matching matcher and returns python dict with contents.

        ``matcher`` <str> Request URL string, JavaScript regex or JavaScript function to match request by.
        By default (with empty string) matches first available request.

        ``timeout`` <str> Timeout in milliseconds. Uses default timeout of 10 seconds if not set.

        """
        return self._wait_for_http("Response", matcher, timeout)

    @keyword(tags=["Wait", "HTTP"])
    def wait_until_network_is_idle(self, timeout: str = ""):
        """Waits until there has been at least one instance of 500 ms of no network traffic on the page after loading.

        Doesn't wait for network traffic that wasn't initiated within 500ms of page load.

        ``timeout`` <str> Timeout in milliseconds. Uses default timeout of 10 seconds if not set.

        """
        with self.playwright.grpc_channel() as stub:
            if not timeout:
                timeout = self.library.playwright.timeout
            response = stub.WaitUntilNetworkIsIdle(
                Request().Timeout(timeout=timestr_to_millisecs(timeout))
            )
            logger.debug(response.log)
