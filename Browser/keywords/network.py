import json
from typing import Dict, Literal, Optional

from robotlibcore import keyword  # type: ignore

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
    @keyword(tags=["HTTP", "BrowserControl"])
    def http(
        self,
        url: str,
        method: RequestMethod = RequestMethod.GET,
        body: Optional[str] = None,
        headers: Optional[dict] = None,
    ):

        """Performs an HTTP request in the current browser context

        Accepts the following arguments:
          - ``url`` <string> The request url, e.g. ``/api/foo``.
          - ``method`` <string> The HTTP method for the request, one of GET, POST, PUT, PATCH, DELETE or HEAD.
          - ``body`` <string> The request body. GET requests cannot have a body. If the body can be parsed as JSON,
          the ``Content-Type`` header for the request will be automatically set to ``application/json``.
          - ``headers`` <dict> A dictionary of additional request headers.

        The response is a Python dictionary with following attributes:
          - ``status`` <int> The status code of the response.
          - ``statusText`` <string> Status text corresponding to ``status``, e.g OK or INTERNAL SERVER ERROR.
          - ``body`` <dict> | <string> The response body. If the body can be parsed as a JSON obejct,
          it will be returned as Python dictionary, otherwise it is returned as a string.
          - ``headers`` <dict> A dictionary containing all response headers.
          - ``ok`` <bool> Whether the request was successfull, i.e. the ``status`` is range 200-299.

        Here's an example of using Robot Framework dictionary variables and extended variable syntax to
        do assertions on the response object:

        | &{res}=  |  HTTP |  /api/endpoint |
        | Should Be Equal  |  ${res.status}  |  200  |
        | Should Be Equal  |  ${res.body.some_field}  |  some value  |

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
            return _format_response(json.loads(response.body))

    def _wait_for_http(self, method: Literal["Request", "Response"], matcher, timeout):
        with self.playwright.grpc_channel() as stub:
            function = getattr(stub, f"WaitFor{method}")
            response = function(
                Request().HttpCapture(
                    urlOrPredicate=matcher, timeout=timestr_to_millisecs(timeout),
                )
            )
            logger.debug(response.log)
            # Add format response back here
            return response.body

    @keyword(tags=["Wait", "HTTP"])
    def wait_for_request(self, matcher: str = "", timeout: str = ""):
        """ Waits for request matching matcher to be made.

        ``matcher``: Request URL string, JavaScript regex or JavaScript function to match request by.
        By default (with empty string) matches first available request.

        ``timeout``: (optional) uses default timout if not set.

        """
        return self._wait_for_http("Request", matcher, timeout)

    @keyword(tags=["Wait", "HTTP"])
    def wait_for_response(self, matcher: str = "", timeout: str = ""):
        """ Waits for response matching matcher and returns python dict with contents.

        ``matcher``: Request URL string, JavaScript regex or JavaScript function to match request by.
        By default (with empty string) matches first available request.

        ``timeout``: (optional) uses default timout if not set.

        """
        return self._wait_for_http("Response", matcher, timeout)
