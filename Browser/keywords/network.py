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
import mimetypes
from collections.abc import Mapping
from datetime import timedelta
from enum import Enum
from pathlib import Path
from typing import Any, cast
from urllib.parse import parse_qsl

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    AbortErrorCode,
    CapturedRequest,
    CapturedResponse,
    ContextOrPage,
    FetchCache,
    FetchCredentials,
    FetchMode,
    FetchPriority,
    FetchRedirect,
    HttpResponse,
    JsonDotDict,
    MultipartFile,
    ReferrerPolicy,
    keyword,
    logger,
)
from ..utils.data_types import PageLoadStates, RegExp, RequestMethod


def _get_headers(body: str, headers: dict):
    if any(name.lower() == "content-type" for name in headers):
        return headers
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
        if message.log:
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
COOKIE_HEADER_KEYS = ("allHeaders", "headersArray")


def _post_data_text(request: dict, post_data: bytes) -> str | None:
    """The post data as Playwright's ``request.postData()`` returns it."""
    return (
        post_data.decode("utf-8", errors="replace") if request["hasPostData"] else None
    )


def _legacy_request_post_data(text: str | None) -> Any:
    if not text:
        return None
    try:
        return _strict_json_loads(text)
    except ValueError:
        return text


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


def _trace_enabled() -> bool:
    try:
        return BuiltIn().get_variable_value("${LOG LEVEL}") == "TRACE"
    except RobotNotRunningError:
        return False


def _trace_content(label: str, raw: bytes | None) -> None:
    if raw is not None and _trace_enabled():
        logger.trace(f"{label}:\n{_readable(raw)}")


def _debug_cookie_headers(label: str, data: dict) -> None:
    headers = {key: data[key] for key in COOKIE_HEADER_KEYS if data[key] is not None}
    if headers:
        logger.debug(f"{label} headers including cookies: {headers}")


def _log_request(request: dict) -> None:
    logger.info(_without(request, REQUEST_BODY_KEYS + COOKIE_HEADER_KEYS))
    _debug_cookie_headers("Request", request)
    _trace_content("Request post data", request["postDataBuffer"])


def _log_response(response: dict) -> None:
    metadata = _without(response, RESPONSE_BODY_KEYS + COOKIE_HEADER_KEYS)
    metadata["request"] = _without(
        response["request"], REQUEST_BODY_KEYS + COOKIE_HEADER_KEYS
    )
    logger.info(metadata)
    _debug_cookie_headers("Response", response)
    _debug_cookie_headers("Request", response["request"])
    _trace_content("Response body", response["bytes"])
    _trace_content("Request post data", response["request"]["postDataBuffer"])


METHODS_WITHOUT_BODY = ("GET", "HEAD")


def _form_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _set_given(request: Request.HttpRequest, **values: Any) -> None:
    for name, value in values.items():
        if value is not None:
            setattr(request, name, value.value if isinstance(value, Enum) else value)


def _multipart_field(name: str, value: Any) -> Request.MultipartField:
    if isinstance(value, Mapping):
        return _multipart_file(name, value)
    return Request.MultipartField(name=name, value=_form_value(value))


def _multipart_file(name: str, file: Mapping[str, Any]) -> Request.MultipartField:
    path, buffer = file.get("path"), file.get("buffer")
    if (path is None) == (buffer is None):
        raise ValueError(
            f"Multipart file {name!r} needs either 'path' or 'buffer', not {'both' if path else 'neither'}."
        )
    if path is not None:
        file_path = Path(path)
        if not file_path.is_file():
            raise FileNotFoundError(f"Multipart file {name!r}: no file at {file_path}.")
        return Request.MultipartField(
            name=name,
            path=str(file_path.resolve()),
            fileName=file.get("name") or file_path.name,
            mimeType=file.get("mimeType")
            or mimetypes.guess_type(file_path.name)[0]
            or "application/octet-stream",
        )
    if not file.get("name"):
        raise ValueError(f"Multipart file {name!r} with 'buffer' needs a 'name'.")
    content = cast(str | bytes, buffer)
    return Request.MultipartField(
        name=name,
        buffer=content.encode("utf-8") if isinstance(content, str) else bytes(content),
        fileName=file["name"],
        mimeType=file.get("mimeType") or "application/octet-stream",
    )


def _add_http_response_views(response: dict, body: bytes) -> None:
    text = body.decode("utf-8", errors="replace")
    response["body"] = text
    _jsonize_content(response, "body")
    response.update(bytes=body, text=text, json=_json_or_none(text))


class Network(LibraryComponent):
    @keyword(tags=("HTTP",))
    def http(
        self,
        url: str,
        method: RequestMethod = RequestMethod.GET,
        body: str | bytes | None = None,
        headers: dict | None = None,
        *,
        form: dict[str, str | int | float | bool] | None = None,
        multipart: dict[str, MultipartFile | str | int | float | bool] | None = None,
        credentials: FetchCredentials | None = None,
        redirect: FetchRedirect | None = None,
        mode: FetchMode | None = None,
        cache: FetchCache | None = None,
        referrer: str | None = None,
        referrerPolicy: ReferrerPolicy | None = None,
        integrity: str | None = None,
        keepalive: bool | None = None,
        priority: FetchPriority | None = None,
        timeout: timedelta | None = None,
    ) -> HttpResponse:
        """Sends an HTTP request with the browser's ``fetch`` from the active page.

        The request is a request of the page itself: a relative ``url`` is resolved against
        the URL of the page, the browser's CORS rules apply, the browser sends the cookies of
        the context by the ``credentials`` rule, and `Wait For Request` and
        `Wait For Response` see it. The browser does not let a page set some headers, such
        as ``Cookie``, ``Host`` or ``Origin``, and drops them without an error.

        The named-only arguments are the options of the browser's
        [https://developer.mozilla.org/en-US/docs/Web/API/RequestInit|fetch]. An argument
        that is not given keeps the browser's default.

        *Arguments:*
          - ``url``: The request URL, e.g. ``/api/foo``.
          - ``method``: The HTTP method. Defaults to ``GET``.
          - ``body``: The request body, as ``str`` or ``bytes``. ``GET`` and ``HEAD``
                cannot have a body: a ``str`` body is silently left out there, as it always
                was, and a ``bytes`` body fails. When a ``str`` body can be parsed as JSON,
                the ``Content-Type`` header is set to ``application/json``, unless
                ``headers`` already has a ``Content-Type``, in any case. Otherwise the
                browser sends a ``str`` body as ``text/plain;charset=UTF-8``, and ``bytes``
                without a ``Content-Type``.
          - ``headers``: A dictionary of request headers.
          - ``form``: A dictionary of form fields, sent URL-encoded as
                ``application/x-www-form-urlencoded``, the way the browser encodes a
                ``URLSearchParams`` body. Numbers and booleans are sent as text, a boolean
                as ``true`` or ``false``. Any other value is sent as its text, so a nested
                dictionary or list arrives as its Python representation.
          - ``multipart``: A dictionary of form fields sent as ``multipart/form-data``, the
                way the browser encodes a ``FormData`` body, in the order given. A value is
                a text field: a ``str``, a number or a boolean, sent like in ``form``. A file
                is a `MultipartFile` dictionary with either ``path`` or ``buffer``; its
                documentation says how to create one so that it is not sent as text. Do not
                set a ``Content-Type`` in ``headers``: the browser then leaves out the
                boundary of the parts, and the server cannot read the body. ``body``,
                ``form`` and ``multipart`` exclude each other, and ``form`` and
                ``multipart`` fail with ``GET`` and ``HEAD``.
          - ``credentials``: Whether cookies and HTTP authentication are sent, see
                `FetchCredentials`. The browser's default sends them only to the page's own
                origin.
          - ``redirect``: How a redirect is handled, see `FetchRedirect`.
          - ``mode``: Which cross-origin requests are allowed, see `FetchMode`.
          - ``cache``: How the browser's HTTP cache is used, see `FetchCache`.
          - ``referrer``: The URL sent as ``Referer``. It must be on the page's origin,
                otherwise the browser uses the page URL. ``about:client`` is the page URL,
                an empty string sends none.
          - ``referrerPolicy``: How much of the referrer is sent, see `ReferrerPolicy`.
          - ``integrity``: The expected hash of the response body as a
                [https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity|subresource integrity]
                value, e.g. ``sha256-...``. The keyword fails when the body does not match.
          - ``keepalive``: When ``True``, the request outlives the page, for example when it
                is closed. The body can be at most 64 KiB.
          - ``priority``: The priority relative to the page's other requests, see
                `FetchPriority`.
          - ``timeout``: How long to wait for the whole response, body included. Defaults to
                the library timeout; ``0`` waits without a limit.

        The keyword fails when ``fetch`` fails: on a network error, a request CORS blocks,
        ``redirect=error`` on a redirect or a wrong ``integrity``. A response with an error
        status, such as ``404``, does not fail it.

        Returns an `HttpResponse` with the status, the headers the page can read, the type
        of the response, the raw body as ``bytes`` and the views ``text`` and ``json``. The
        response is logged without its body, and the body at ``TRACE`` level.

        Assigned with ``&{response} =``, ``bytes`` holds base64 text. Assign with
        ``${response} =`` to get the raw ``bytes``.

        | ${response} =      `HTTP`    /api/endpoint
        | Should Be Equal    ${response.status}            ${200}
        | Should Be Equal    ${response.json.some_field}   some value
        |
        | &{fields} =        Create Dictionary    username=demo    password=mode
        | ${response} =      `HTTP`    /login    POST    form=${fields}
        |
        | &{file} =          Create Dictionary    path=${CURDIR}/avatar.png
        | &{fields} =        Create Dictionary    description=Profile picture    file=${file}
        | ${response} =      `HTTP`    /api/avatar    POST    multipart=${fields}    timeout=30s
        |
        | ${response} =      `HTTP`    /logo.png
        | Create Binary File    ${OUTPUT_DIR}/logo.png    ${response.bytes}

        [https://forum.robotframework.org/t//4296|Comment >>]
        """
        method_name = method.name if method else "GET"
        given = [
            name
            for name, value in (
                ("body", body),
                ("form", form),
                ("multipart", multipart),
            )
            if value
        ]
        if len(given) > 1:
            raise ValueError(
                f"Only one of body, form or multipart can be given, got {' and '.join(given)}."
            )
        if method_name in METHODS_WITHOUT_BODY:
            not_allowed = next(
                (
                    name
                    for name, value in (
                        ("bytes", isinstance(body, bytes) and body),
                        ("form", form),
                        ("multipart", multipart),
                    )
                    if value
                ),
                None,
            )
            if not_allowed:
                raise ValueError(
                    f"A {method_name} request cannot have a body, got {not_allowed}."
                )
        headers = headers or {}
        request = Request().HttpRequest(
            url=url,
            method=method_name,
            timeout=self.get_timeout(timeout),
            multipart=[
                _multipart_field(name, value)
                for name, value in (multipart or {}).items()
            ],
        )
        _set_given(
            request,
            credentials=credentials,
            redirect=redirect,
            mode=mode,
            cache=cache,
            referrer=referrer,
            referrerPolicy=referrerPolicy,
            integrity=integrity,
            keepalive=keepalive,
            priority=priority,
        )
        request.form.extend(
            Request.FormField(name=key, value=_form_value(value))
            for key, value in (form or {}).items()
        )
        if body and method_name not in METHODS_WITHOUT_BODY:
            if isinstance(body, bytes):
                request.bodyBytes = body
            else:
                request.body = body
                headers = _get_headers(body, headers)
        request.headers = json.dumps(headers)
        with self.playwright.grpc_channel() as stub:
            response, body_bytes, _ = _collect_stream(stub.HttpRequest(request))
        _add_http_response_views(response, body_bytes)
        logger.info(_without(response, RESPONSE_BODY_KEYS))
        _trace_content("Response body", response["bytes"])
        return cast(HttpResponse, JsonDotDict(response))

    def _wait_for_http_request(self, matcher, timeout, wait_for_all_fields) -> dict:
        with self.playwright.grpc_channel() as stub:
            messages = stub.WaitForRequest(
                Request().HttpCapture(
                    urlOrPredicate=matcher,
                    timeout=self.get_timeout(timeout),
                    waitForAllFields=wait_for_all_fields,
                )
            )
            request, _, post_data = _collect_stream(messages)
        request["postData"] = _legacy_request_post_data(
            _post_data_text(request, post_data)
        )
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
        request["postData"] = _post_data_text(request, post_data)
        _jsonize_content(request, "postData")
        _add_request_views(request, post_data)
        _log_response(response)
        return response

    @keyword(tags=("Wait", "HTTP"))
    def wait_for_request(
        self,
        matcher: str | RegExp = "",
        timeout: timedelta | None = None,
        *,
        wait_for_all_fields: bool = False,
    ) -> CapturedRequest:
        """Waits for a request matching ``matcher`` to be made and returns it as a `CapturedRequest`.

        By default only the request is awaited, not its response. The keyword returns as soon
        as the request is sent, so ``redirectedTo`` is always ``None`` here. See
        `Wait For Response` if the response is needed.

        The returned `CapturedRequest` mirrors Playwright's Request: the URL, method, headers
        (``allHeaders`` includes ``cookie``), the raw body as ``postDataBuffer``, the parsed
        body as ``postDataJSON``, the resource type and more. Its documentation lists every key
        and the parsing rules of the legacy ``postData`` key.

        The request is logged without its body. ``allHeaders`` and ``headersArray`` can
        contain cookies, so they are logged only at ``DEBUG`` level. The body is logged at
        ``TRACE`` level: as formatted JSON when it is JSON, as text when it is UTF-8,
        otherwise as base64.

        *Arguments:*
          - ``matcher``: Request URL matcher. Can be a string (Glob-Pattern), a
                JavaScript RegExp (enclosed in ``/`` with optional trailing flags) or a
                JavaScript arrow-function that receives the
                [https://playwright.dev/docs/api/class-request | Request] object and
                returns a boolean. By default (with an empty string) the first request
                is matched. The matcher syntax is the same as in `Wait For Response`,
                see its matcher examples. For additional information, see the Playwright
                [https://playwright.dev/docs/api/class-page#page-wait-for-request |
                waitForRequest] documentation.
          - ``timeout``: Timeout supports Robot Framework time format. Uses default
                timeout if not set.
          - ``wait_for_all_fields``: Some fields are known only later than the request itself:
                Chromium and WebKit report ``allHeaders`` and ``headersArray`` only when the
                response headers arrive. With the default ``False`` the keyword returns at once
                and those fields are ``None``. With ``True`` it also waits for them, within
                ``timeout``, and fails if they do not arrive in time or the browser cannot
                report them, for example because the page closed.

        Example:
        | ${promise} =    `Promise To`    `Wait For Request`    **/api/login    wait_for_all_fields=True
        | `Click`    id=login_button
        | ${request} =    `Wait For`    ${promise}
        | Should Contain    ${request.allHeaders}[cookie]    consent=

        See `Wait For Response` for more details about the matcher.

        [https://forum.robotframework.org/t//4348|Comment >>]
        """
        request = self._wait_for_http_request(matcher, timeout, wait_for_all_fields)
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

        The response is logged without its body. ``allHeaders`` and ``headersArray`` can
        contain cookies, so they are logged only at ``DEBUG`` level. The body is logged at
        ``TRACE`` level: as formatted JSON when it is JSON, as text when it is UTF-8,
        otherwise as base64.

        *Binary data:* ``bytes`` and ``request.postDataBuffer`` hold real ``bytes`` when read
        by key, as ``${response.bytes}`` or ``${response}[bytes]``. Everything that reads the
        dictionary through ``items()`` gets them as base64 text instead, so that the
        dictionary can be serialized with ``json.dumps``:
        - ``&{response} =`` assignment copies the outer dictionary through ``items()``, so
          after it ``bytes`` is base64 text, while ``request.postDataBuffer`` stays ``bytes``.
          Assign with ``${response} =`` to keep the real ``bytes`` everywhere.
        - ``FOR ... IN &{response}``, `Get Dictionary Items` and ``json.dumps`` return
          base64 text.
        - The variables view of the RobotCode debugger shows base64 text.

        *Arguments:*
          - ``matcher``: Response URL matcher. Can be a string (Glob-Pattern), a
                JavaScript RegExp (enclosed in ``/`` with optional trailing flags) or a
                JavaScript arrow-function that receives the Response object and returns
                a boolean. By default (with an empty string) the first response is
                matched. For additional information, see the Playwright
                [https://playwright.dev/docs/api/class-page#page-wait-for-response |
                page.waitForResponse] documentation.
          - ``timeout``: Timeout supports Robot Framework time format. Uses default
                timeout if not set. It covers both the wait for the response and reading
                its body and other fields; the keyword fails if they do not arrive in time.
          - ``include_body``: If ``False``, the response body is not read and not transferred,
                and ``body``, ``bytes``, ``text`` and ``json`` are ``None``. Use it when only the
                status or headers matter and the body is large or never ends.
                ``httpVersion``, ``serverAddr`` and ``securityDetails`` are then ``None`` too,
                because some browsers report them only after the whole body has arrived:
                ``httpVersion`` in Firefox and WebKit, the other two in WebKit.

        == Matcher Examples: ==

        === Glob-Pattern: ===

        Glob-Patterns are strings that can contain wildcards.
        Possible wildcards/patterns are:
        - ``*`` matches any number of characters, except ``/``
        - ``**`` matches any number of characters, including ``/``
        - ``{foo,bar,baz}`` matches one of the strings in the braces (in this example ``foo``, ``bar`` or ``baz``)

        ``?``, ``[`` and ``]`` match literally. To match exactly one character or a character
        class, use a RegExp (``/.../``, see below).

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

    @keyword(tags=("Route", "Setter"))
    def abort_requests(
        self,
        matcher: str,
        *,
        errorCode: AbortErrorCode = AbortErrorCode.failed,
        times: int | None = None,
        on: ContextOrPage = ContextOrPage.Context,
    ) -> str:
        """Adds a route rule that makes every request matching ``matcher`` fail.

        *Arguments:*
          - ``matcher``: Request URL matcher, a glob pattern or a JavaScript RegExp enclosed in
                ``/``, matched as in `Wait For Request`. An invalid RegExp fails.
          - ``errorCode``: The network error the request fails with, see `AbortErrorCode`.
          - ``times``: How many matching requests the rule aborts before it ends. ``None``
                (default) aborts every matching request until the rule is removed. Must be 1
                or more.
          - ``on``: Where the rule is added, see `ContextOrPage`. ``Context`` (default) for
                every page of the active context, also pages opened later, ``Page`` for the
                active page only: the rule stays on that page and does not follow
                `Switch Page`. Fails when no context or page is open.

        Returns the rule id, to give to `Remove Route Rule`.

        A rule ends when its context or page closes, when it is removed with
        `Remove Route Rule` or `Remove All Route Rules`, or when it has used up its ``times``.
        It does not end with the test or suite.

        A request that a service worker answers never reaches a route rule; open the context
        with ``serviceWorkers=block`` in `New Context` to route those requests too. Each
        aborted request is logged only in ``playwright-log.txt``.

        Example, an outage of two requests and then recovery:
        | `Abort Requests`    **/api/orders    times=2
        | `Click`    id=reload-orders    # request aborted
        | `Click`    id=reload-orders    # request aborted
        | `Click`    id=reload-orders    # reaches the server
        | `Get Text`    id=orders-status    ==    loaded

        See [https://robotframework-browser.org/docs/concepts/route-rules|route rules] for
        more.
        """
        if times is not None and times < 1:
            raise ValueError(f"times must be 1 or more, got {times}.")
        request = Request().RouteRule(
            url=matcher,
            times=times,
            abort=Request().RouteAbort(errorCode=errorCode.name),
        )
        with self.playwright.grpc_channel() as stub:
            if on == ContextOrPage.Page:
                response = stub.AddPageRoute(request)
            else:
                response = stub.AddContextRoute(request)
        logger.info(
            f"Added route rule {response.id}: abort {matcher} with {errorCode.name}, "
            f"times={times}, on={on.name}."
        )
        return response.id

    @keyword(tags=("Route", "Setter"))
    def remove_route_rule(self, rule_id: str):
        """Removes the route rule with ``rule_id``.

        *Arguments:*
          - ``rule_id``: The id that `Abort Requests` returned. The rule is found in any
                context, so a Page rule can be removed while another page is active.

        An unknown or already ended id, or no open context, is logged and the keyword passes.
        When the keyword returns, the rule affects no request: it waits for the rule's running
        handlers to finish.

        Example:
        | ${rule} =    `Abort Requests`    **/api/orders
        | `Click`    id=reload-orders    # request aborted
        | `Remove Route Rule`    ${rule}
        | `Click`    id=reload-orders    # reaches the server
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.RemoveRouteRule(Request().RouteRuleId(id=rule_id))
        logger.info(response.log)

    @keyword(tags=("Route", "Setter"))
    def remove_all_route_rules(self):
        """Removes the route rules of the active context and of every page in it.

        Only rules added by this library are removed, routes that a plugin or a JavaScript
        keyword added with ``page.route`` stay. Like `Remove Route Rule`, the keyword waits for
        running handlers to finish. It logs how many Context and Page rules it removed. With no
        rules, or no open context, it logs and passes, so it is safe in a teardown.

        Only the active context is covered. For several contexts, switch to each one:
        | FOR    ${context}    IN    @{contexts}
        |     `Switch Context`    ${context}
        |     `Remove All Route Rules`
        | END

        Example:
        | [Teardown]    `Remove All Route Rules`
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.RemoveAllRouteRules(Request().Empty())
        logger.info(response.log)
