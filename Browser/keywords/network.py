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

import base64
import contextlib
import json
from datetime import timedelta
from typing import Any, cast
from urllib.parse import parse_qsl

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    CapturedRequest,
    CapturedResponse,
    DotDict,
    JsonDotDict,
    keyword,
    logger,
)
from ..utils.data_types import PageLoadStates, RegExp, RequestMethod


def _get_headers(body: str, headers: dict):
    try:
        json.loads(body)
        return {"Content-Type": "application/json", **headers}
    except json.decoder.JSONDecodeError:
        return headers


def _reject_constant(constant: str):
    raise ValueError(f"{constant} is not valid JSON")


def _strict_json_loads(text: str) -> Any:
    return json.loads(text, parse_constant=_reject_constant)


def _json_or_none(text: str) -> Any:
    try:
        return _strict_json_loads(text)
    except ValueError:
        return None


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
        with contextlib.suppress(ValueError, TypeError):
            data[bodykey] = _strict_json_loads(data[bodykey])


def _collect_stream(messages) -> tuple[dict, bytes, bytes]:
    metadata: dict | None = None
    body = bytearray()
    post_data = bytearray()
    for message in messages:
        logger.info(message.log)
        if metadata is None and message.json:
            metadata = json.loads(message.json)
        body += message.bodyBytes
        post_data += message.postDataBytes
    if metadata is None:
        raise ValueError("No data received from the Playwright wrapper.")
    return metadata, bytes(body), bytes(post_data)


def _post_data_json(post_data: bytes | None, headers: dict) -> Any:
    if not post_data:
        return None
    text = post_data.decode("utf-8", errors="replace")
    if "application/x-www-form-urlencoded" in headers.get("content-type", ""):
        return dict(parse_qsl(text, keep_blank_values=True))
    return _json_or_none(text)


RESPONSE_BODY_KEYS = ("body", "bytes", "text", "json")
REQUEST_BODY_KEYS = ("postData", "postDataBuffer", "postDataJSON")


def _add_request_views(request: dict, post_data: bytes) -> None:
    buffer = post_data if request.pop("hasPostData") else None
    request["postDataBuffer"] = buffer
    request["postDataJSON"] = _post_data_json(buffer, request["headers"])


def _add_response_views(response: dict, body: bytes) -> None:
    if not response.pop("hasBody"):
        response.update(dict.fromkeys(RESPONSE_BODY_KEYS))
        return
    text = body.decode("utf-8", errors="replace")
    try:
        legacy_body = _strict_json_loads(text)
        parsed = legacy_body
    except ValueError:
        legacy_body = text
        parsed = None
    response.update(body=legacy_body, bytes=body, text=text, json=parsed)


def _without(data: dict, keys: tuple[str, ...]) -> dict:
    return {key: value for key, value in data.items() if key not in keys}


def _readable(raw: bytes) -> str:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return f"{len(raw)} bytes, base64: {base64.b64encode(raw).decode('ascii')}"
    try:
        return json.dumps(_strict_json_loads(text), indent=2, ensure_ascii=False)
    except ValueError:
        return text


def _log_request(request: dict) -> None:
    logger.info(_without(request, REQUEST_BODY_KEYS))
    if request["postDataBuffer"] is not None:
        logger.trace(f"Request post data:\n{_readable(request['postDataBuffer'])}")


def _log_response(response: dict) -> None:
    metadata = _without(response, RESPONSE_BODY_KEYS)
    metadata["request"] = _without(response["request"], REQUEST_BODY_KEYS)
    logger.info(metadata)
    if response["bytes"] is not None:
        logger.trace(f"Response body:\n{_readable(response['bytes'])}")
    if response["request"]["postDataBuffer"] is not None:
        logger.trace(
            f"Request post data:\n{_readable(response['request']['postDataBuffer'])}"
        )


class Network(LibraryComponent):
    @keyword(tags=("HTTP",))
    def http(
        self,
        url: str,
        method: RequestMethod = RequestMethod.GET,
        body: str | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Performs an HTTP request in the current browser context

        The request is sent with the browser's ``fetch`` from the currently active page,
        so a relative ``url`` is resolved against the URL of that page.

        *Arguments:*
          - ``url``: The request url, e.g. ``/api/foo``.
          - ``method``: The HTTP method for the request. Defaults to GET.
          - ``body``: The request body. It is ignored for GET requests, because GET
                requests cannot have a body. If the body can be parsed as JSON, the
                ``Content-Type`` header for the request is automatically set to
                ``application/json``, unless ``headers`` already contains that header.
                Defaults to None.
          - ``headers``: A dictionary of additional request headers. Defaults to None.

        The response is a Robot Framework dictionary with the following attributes:
          - ``status`` <int> The status code of the response.
          - ``statusText`` <str> Status text corresponding to ``status``, e.g. OK or INTERNAL SERVER ERROR. This may not be available for all browsers.
          - ``body`` <dict> | <str> The response body. If the body can be parsed as a JSON object,
          it will be returned as Python dictionary, otherwise it is returned as a string.
          - ``headers`` <dict> A dictionary containing all response headers.
          - ``ok`` <bool> Whether the request was successful, i.e. the ``status`` is in the range 200-299.
          - ``url`` <str> The final URL of the response, after possible redirects.
          - ``redirected`` <bool> Whether the response is the result of a redirect.
          - ``type`` <str> The type of the response, e.g. ``basic`` or ``cors``.

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

    def _wait_for_http_request(self, matcher, timeout) -> dict:
        with self.playwright.grpc_channel() as stub:
            messages = stub.WaitForRequest(
                Request().HttpCapture(
                    urlOrPredicate=matcher,
                    timeout=self.get_timeout(timeout),
                )
            )
            request, _, post_data = _collect_stream(messages)
        _add_request_views(request, post_data)
        _log_request(request)
        return request

    def _wait_for_http_response(self, matcher, timeout, include_body) -> dict:
        with self.playwright.grpc_channel() as stub:
            messages = stub.WaitForResponse(
                Request().HttpCapture(
                    urlOrPredicate=matcher,
                    timeout=self.get_timeout(timeout),
                    excludeBody=not include_body,
                )
            )
            response, body, post_data = _collect_stream(messages)
        response["headers"] = json.loads(response["headers"])
        _add_response_views(response, body)
        request = response["request"]
        _jsonize_content(request, "postData")
        _add_request_views(request, post_data)
        _log_response(response)
        return response

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_request(
        self, matcher: str | RegExp = "", timeout: timedelta | None = None
    ) -> CapturedRequest:
        """Waits for a request matching ``matcher`` to be made and returns it as a `CapturedRequest`.

        Only the request is awaited, not its response. The keyword returns as soon as the
        request is sent, so ``redirectedTo`` is always ``None`` here. See `Wait For Response` if
        the response is needed.

        The returned `CapturedRequest` mirrors Playwright's Request: the URL, method, headers
        (``allHeaders`` includes ``cookie``), the raw body as ``postDataBuffer``, the parsed
        body as ``postDataJSON``, the resource type and more. Its documentation lists every key
        and the parsing rules of the legacy ``postData`` key.

        The request is logged without its body. The body is logged at ``TRACE`` level: as
        formatted JSON when it is JSON, as text when it is UTF-8, otherwise as base64.

        *Arguments:*
          - ``matcher``: Request URL matcher. Can be a string (Glob-Pattern), a
                JavaScript RegExp (enclosed in ``/`` with optional trailing flags) or a
                JavaScript arrow-function that receives the
                [https://playwright.dev/docs/api/class-request | Request] object and
                returns a boolean. By default (with an empty string) the first request
                is matched. For additional information, see the Playwright
                [https://playwright.dev/docs/api/class-page#page-wait-for-request |
                waitForRequest] documentation.
          - ``timeout``: Timeout supports Robot Framework time format. Uses default
                timeout if not set.

        See `Wait For Response` for more details about the matcher.

        [https://forum.robotframework.org/t//4348|Comment >>]
        """
        request = self._wait_for_http_request(matcher, timeout)
        return cast(CapturedRequest, JsonDotDict(request))

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_response(
        self,
        matcher: str | RegExp = "",
        timeout: timedelta | None = None,
        *,
        include_body: bool = True,
    ) -> CapturedResponse:
        """Waits for a response matching ``matcher`` and returns it as a `CapturedResponse`.

        The keyword waits until the response headers are received and then reads the response body.

        The returned `CapturedResponse` mirrors Playwright's Response: the status, headers
        (``allHeaders`` includes ``set-cookie``), the body as ``bytes``, ``text`` and ``json``,
        the HTTP version, server address, TLS details and the `CapturedRequest` it answers.
        Its documentation lists every key and the parsing rules of the legacy ``body`` key.

        The response is logged without its body. The body is logged at ``TRACE`` level: as
        formatted JSON when it is JSON, as text when it is UTF-8, otherwise as base64.

        *Arguments:*
          - ``matcher``: Response URL matcher. Can be a string (Glob-Pattern), a
                JavaScript RegExp (enclosed in ``/`` with optional trailing flags) or a
                JavaScript arrow-function that receives the Response object and returns
                a boolean. By default (with an empty string) the first response is
                matched. For additional information, see the Playwright
                [https://playwright.dev/docs/api/class-page#page-wait-for-response |
                page.waitForResponse] documentation.
          - ``timeout``: Timeout supports Robot Framework time format. Uses default
                timeout if not set.
          - ``include_body``: If ``False``, the response body is not read and not transferred,
                and ``body``, ``bytes``, ``text`` and ``json`` are ``None``. Use it when only the
                status or headers matter and the body is large.

        == Matcher Examples: ==

        === Glob-Pattern: ===

        Glob-Patterns are strings that can contain wildcards.
        Possible wildcards/patterns are:
        - ``*`` matches any number of characters, except ``/``
        - ``**`` matches any number of characters, including ``/``
        - ``?`` matches one character, except ``/``
        - ``[abc]`` matches one character in the brackets (in this example ``a``, ``b`` or ``c``)
        - ``[a-z]`` matches one character in the range (in this example ``a`` to ``z``)
        - ``{foo,bar,baz}`` matches one of the strings in the braces (in this example ``foo``, ``bar`` or ``baz``)

        Example:
        | `Wait For Response`    **/api/get/text    # matches any response with url ending with /api/get/text. example: https://browser.fi/api/get/text

        === RegExp: ===

        Regular Expressions are JavaScript regular expressions enclosed in ``/`` with optional trailing flags.
        Be aware that backslashes need to be escaped in Robot Framework, e.g. ``\\\\w`` instead of ``\\w``.
        See [https://regex101.com|regex101] for more information on Regular Expressions.

        Example:
        | `Wait For Response`    /http://\\\\w+:\\\\d+/api/get/text/i    # matches any response with url ending with /api/get/text and containing http:// followed by any word and port. example: http://localhost:8080/api/get/text

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

        Asserting the JSON body, a cookie and saving a binary body:
        | ${promise} =       `Promise To`    `Wait For Response`    matcher=**/api/login
        | `Click`            id=login-button
        | ${response} =      `Wait For`      ${promise}
        | Should Be Equal    ${response.json.user}    demo
        | Should Contain     ${response.allHeaders}[set-cookie]    sessionid=
        |
        | ${logo} =          `Promise To`    `Wait For Response`    matcher=**/logo.png
        | `Go To`            ${URL}
        | ${response} =      `Wait For`      ${logo}
        | Create Binary File    ${OUTPUT_DIR}/logo.png    ${response.bytes}

        Waiting only for the status of a large download:
        | ${response} =      `Wait For Response`    **/export.zip    include_body=False
        | Should Be Equal As Integers    ${response.status}    200

        [https://forum.robotframework.org/t//4349|Comment >>]
        """
        response = self._wait_for_http_response(matcher, timeout, include_body)
        response["request"] = JsonDotDict(response["request"])
        return cast(CapturedResponse, JsonDotDict(response))

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_navigation(
        self,
        url: str | RegExp,
        timeout: timedelta | None = None,
        wait_until: PageLoadStates = PageLoadStates.load,
    ):
        """Waits until the page has navigated to the given ``url``.

        *Arguments:*
          - ``url``: Expected navigation target address, either a Glob-Pattern (a plain
                string without wildcards matches exactly) or a JavaScript-like regex
                wrapped in ``/`` symbols.
          - ``timeout``: Timeout supports Robot Framework time format. Uses default
                timeout if not set.
          - ``wait_until``: When to consider the operation succeeded, defaults to load.
                Events can be either: ``domcontentloaded`` - consider operation to be
                finished when the DOMContentLoaded event is fired. ``load`` - consider
                operation to be finished when the load event is fired. ``networkidle`` -
                consider operation to be finished when there are no network connections
                for at least 500 ms. ``commit`` - consider operation to be finished when
                network response is received and the document started loading.


        The keyword works only when the page is loaded and it does not work if only the URL fragment changes. Example: if
        https://marketsquare.github.io/robotframework-browser/Browser.html changes to
        https://marketsquare.github.io/robotframework-browser/Browser.html#Wait%20For%20Navigation
        the keyword will fail.

        Example:
        | `Go To`                  ${ROOT_URL}/redirector.html
        | `Wait for navigation`    ${ROOT_URL}/posted.html    wait_until=${wait_until}

        If the wait times out, the page's load report is logged: whether its
        navigation committed, how far the document got and which requests
        were still open.

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
