from enum import Enum, auto
import json
from typing import Optional

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger


class RequestMethod(Enum):
    HEAD = auto()
    GET = auto()
    POST = auto()
    PUT = auto()
    PATCH = auto()
    DELETE = auto()


class Evaluation(LibraryComponent):
    @keyword(tags=["HTTP", "BrowserControl"])
    def http(
        self,
        url,
        method: RequestMethod = RequestMethod.GET,
        body: Optional[str] = None,
        headers: dict = {},
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
        body = body if body else ""
        with self.playwright.grpc_channel() as stub:
            response = stub.HttpRequest(
                Request().HttpRequest(
                    url=url,
                    method=method.name if method else "GET",
                    body=body,
                    headers=json.dumps(self._get_headers(body, headers)),
                )
            )
            logger.debug(response.log)
            return self._format_response(json.loads(response.body))

    def _get_headers(self, body, headers):
        try:
            json.loads(body)
            return {"Content-Type": "application/json", **headers}
        except json.decoder.JSONDecodeError:
            return headers

    def _format_response(self, response):
        headers = json.loads(response["headers"])
        response["headers"] = headers
        if "content-type" in headers and "application/json" in headers["content-type"]:
            try:
                response["body"] = json.loads(response["body"])
            except json.decoder.JSONDecodeError:
                pass
        logger.info(response)
        return response
