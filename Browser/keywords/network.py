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
from os import PathLike
from pathlib import Path
from typing import Any, cast
from urllib.parse import parse_qsl

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    AbortErrorCode,
    APIResponse,
    CapturedRequest,
    CapturedResponse,
    ContextOrPage,
    FetchCache,
    FetchCredentials,
    FetchMode,
    FetchPriority,
    FetchRedirect,
    FormFields,
    HttpHeaderChanges,
    HttpHeaders,
    HttpResponse,
    JsonDotDict,
    JsonSerializable,
    MultipartFields,
    MultipartFile,
    QueryParams,
    ReferrerPolicy,
    keyword,
    logger,
)
from ..utils.data_types import (
    PageLoadStates,
    RegExp,
    RequestMethod,
)
from ..utils.types import Secret

HTTP_STATUS_CODES = range(100, 600)


def _check_times(times: int | None):
    if times is not None and times < 1:
        raise ValueError(f"times must be 1 or more, got {times}.")


def _reveal(value: Any) -> Any:
    return value.value if isinstance(value, Secret) else value


def _has_content_type(headers: dict[str, str]) -> bool:
    return any(name.lower() == "content-type" for name in headers)


def _check_status(status: int):
    if status not in HTTP_STATUS_CODES:
        raise ValueError(f"status must be from 100 to 599, got {status}.")


def _join_with_and(names: list[str]) -> str:
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def _check_at_most_one(**given: Any):
    given_names = [name for name, value in given.items() if value is not None]
    if len(given_names) > 1:
        raise ValueError(
            f"Give at most one of {_join_with_and(list(given))}, "
            f"got {_join_with_and(given_names)}."
        )


def _revealed_headers(headers: Mapping[str, Any] | None) -> dict[str, str]:
    return {name: _reveal(value) for name, value in (headers or {}).items()}


def _checked_headers(headers: Any) -> dict[str, str]:
    return _revealed_headers(
        None if headers is None else HttpHeaders.from_dict(headers)
    )


def _checked_header_changes(changes: Any) -> tuple[dict[str, str], list[str]]:
    checked = {} if changes is None else HttpHeaderChanges.from_dict(changes)
    removed = [name for name, value in checked.items() if value is None]
    kept = {name: value for name, value in checked.items() if value is not None}
    return _revealed_headers(kept), removed


def _plain_body(body: Any) -> Any:
    body = _reveal(body)
    return bytes(body) if isinstance(body, bytearray) else body


def _is_json_body(body: Any) -> bool:
    return body is not None and not isinstance(body, str | bytes)


def _with_content_type(headers: dict[str, str], content_type: str) -> dict[str, str]:
    return (
        headers
        if _has_content_type(headers)
        else {**headers, "Content-Type": content_type}
    )


def _change_log(changes: list[str]) -> str:
    return ", ".join(changes) if changes else "unchanged"


def _header_names(headers: Mapping[str, Any]) -> str:
    return f"[{', '.join(headers)}]"


def _request_changes(
    url: str | Secret | None,
    method: RequestMethod | None,
    headers: Mapping[str, Any],
    body: Any,
) -> list[str]:
    changes = []
    if url is not None:
        changes.append(f"url={'<secret>' if isinstance(url, Secret) else url}")
    if method is not None:
        changes.append(f"method={method.name}")
    if headers:
        changes.append(f"headers={_header_names(headers)}")
    if body is not None:
        changes.append("body")
    return changes


def _response_changes(
    status: int | None, payloads: dict[str, Any], headers: Mapping[str, Any]
) -> list[str]:
    changes = [] if status is None else [f"status={status}"]
    changes.extend(name for name, value in payloads.items() if value is not None)
    if headers:
        changes.append(f"headers={_header_names(headers)}")
    return changes


def _json_text(value: Any, name: str, hint: str = "") -> str:
    try:
        return json.dumps(value, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} cannot be sent as JSON: {error}.{hint}") from error


def _request_body(body: Any, headers: dict[str, str]) -> tuple[bytes, dict[str, str]]:
    if isinstance(body, bytes):
        return body, headers
    if isinstance(body, str):
        return body.encode("utf-8"), headers
    text = _json_text(body, "request_body")
    return text.encode("utf-8"), _with_content_type(headers, "application/json")


def _payload_with_content_type(
    body: Any,
    json_value: Any,
    path: PathLike | None,
    headers: dict[str, str],
) -> tuple[bytes, dict[str, str], str]:
    payload, content_type, payload_kind = _mock_payload(body, json_value, path)
    if content_type:
        headers = _with_content_type(headers, content_type)
    return payload, headers, payload_kind


def _modified_payload(
    body: Any,
    json_value: Any,
    path: PathLike | None,
    json_patch: dict[str, Any] | None,
    headers: dict[str, str],
) -> tuple[bytes | None, str | None, dict[str, str]]:
    if json_patch is not None:
        return None, _json_text(json_patch, "json_patch"), headers
    if body is None and json_value is None and path is None:
        return None, None, headers
    payload, headers, _ = _payload_with_content_type(body, json_value, path, headers)
    return payload, None, headers


def _mock_payload(
    body: Any, json_value: Any, path: PathLike | None
) -> tuple[bytes, str | None, str]:
    _check_at_most_one(body=body, json=json_value, path=path)
    if path is not None:
        file = Path(path)
        if not file.is_file():
            raise ValueError(f"path {file} is not a file.")
        content_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
        if content_type.startswith("text/"):
            content_type = f"{content_type}; charset=utf-8"
        return file.read_bytes(), content_type, f"file {file}"
    if json_value is not None:
        return (
            _json_text(json_value, "json").encode("utf-8"),
            "application/json",
            "json body",
        )
    if isinstance(body, bytes):
        return body, "application/octet-stream", "binary body"
    if isinstance(body, str):
        return body.encode("utf-8"), "text/plain; charset=utf-8", "text body"
    if body is not None:
        return _json_text(body, "body").encode("utf-8"), "application/json", "json body"
    return b"", None, "no body"


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


def _set_given(
    request: Request.HttpRequest | Request.ApiRequest, **values: Any
) -> None:
    for name, value in values.items():
        if value is not None:
            setattr(request, name, value.value if isinstance(value, Enum) else value)


def _multipart_field(name: str, value: str | MultipartFile) -> Request.MultipartField:
    if isinstance(value, str):
        return Request.MultipartField(name=name, value=value)
    if "path" in value:
        file_path = value["path"]
        if not file_path.is_file():
            raise FileNotFoundError(f"Multipart file {name!r}: no file at {file_path}.")
        return Request.MultipartField(
            name=name,
            path=str(file_path.resolve()),
            fileName=value.get("name") or file_path.name,
            mimeType=value.get("mimeType")
            or mimetypes.guess_type(file_path.name)[0]
            or "application/octet-stream",
        )
    return Request.MultipartField(
        name=name,
        buffer=value["buffer"],
        fileName=value["name"],
        mimeType=value.get("mimeType") or "application/octet-stream",
    )


def _multipart_fields(
    multipart: Mapping[str, str | MultipartFile],
) -> list[Request.MultipartField]:
    return [_multipart_field(name, value) for name, value in multipart.items()]


def _form_fields(fields: Mapping[str, str]) -> list[Request.FormField]:
    return [Request.FormField(name=name, value=value) for name, value in fields.items()]


def _checked_form(form: Any) -> dict[str, str] | None:
    return None if form is None else FormFields.from_dict(form)


def _checked_multipart(multipart: Any) -> dict[str, str | MultipartFile] | None:
    return None if multipart is None else MultipartFields.from_dict(multipart)


def _set_api_data(request: Request.ApiRequest, data: Any) -> None:
    data = _plain_body(data)
    if data is None:
        return
    if isinstance(data, str):
        request.dataText = data
    elif isinstance(data, bytes):
        request.dataBytes = data
    else:
        request.dataJson = _json_text(
            data,
            "data",
            " Give a string, bytes, or a dictionary, a list, a number or a boolean that "
            "holds only such values and None.",
        )


def _set_api_params(
    request: Request.ApiRequest, params: Mapping[str, str] | str
) -> None:
    if isinstance(params, str):
        request.encodedParams = params
    else:
        request.params.SetInParent()
        request.params.fields.extend(_form_fields(params))


def _set_fields(
    request: Request.ApiRequest | Request.HttpRequest,
    form: Mapping[str, str] | None,
    multipart: Mapping[str, str | MultipartFile] | None,
) -> None:
    if form is not None:
        request.form.SetInParent()
        request.form.fields.extend(_form_fields(form))
    if multipart is not None:
        request.multipart.SetInParent()
        request.multipart.fields.extend(_multipart_fields(multipart))


def _add_body_views(response: dict, body: bytes) -> str:
    text = body.decode("utf-8", errors="replace")
    response.update(bytes=body, text=text, json=_json_or_none(text))
    return text


API_RESPONSE_HEADER_KEYS = ("headers", "headersArray")


def _add_http_response_views(response: dict, body: bytes) -> None:
    views: dict = {}
    response["body"] = _add_body_views(views, body)
    _jsonize_content(response, "body")
    response.update(views)


class Network(LibraryComponent):
    @keyword(tags=("Setter", "HTTP"))
    def http(
        self,
        url: str,
        method: RequestMethod = RequestMethod.GET,
        body: JsonSerializable | bytes | Secret | None = None,
        # Not "| None": in a union RF drops the converter's error and reports only
        # "cannot be converted to HttpHeaders or None". A None default passes None anyway.
        headers: HttpHeaders = None,  # type: ignore[assignment]
        *,
        form: FormFields = None,  # type: ignore[assignment]
        multipart: MultipartFields = None,  # type: ignore[assignment]
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

        Use `Send API Request` instead for a request outside the page, which shares the
        cookies of the context but not the page's rules, such as CORS.

        The named-only arguments are the options of the browser's
        [https://developer.mozilla.org/en-US/docs/Web/API/RequestInit|fetch]. An argument
        that is not given keeps the browser's default.

        *Arguments:*
          - ``url``: The request URL, e.g. ``/api/foo``.
          - ``method``: The HTTP method. Defaults to ``GET``.
          - ``body``: The request body: text, a Robot Framework ``Secret``, ``bytes``, or a
                dictionary, a list, a number or a boolean, which is sent as JSON (see
                `JsonSerializable`) with the ``Content-Type`` ``application/json``. When a
                text body can be parsed as JSON, the ``Content-Type`` is also set to
                ``application/json``. Otherwise the browser sends text as
                ``text/plain;charset=UTF-8``, and ``bytes`` without a ``Content-Type``. A
                ``Content-Type`` in ``headers``, in any case, always wins.
          - ``headers``: `HttpHeaders` (a dictionary) of the request.
          - ``form``: `FormFields` (a dictionary), sent URL-encoded as
                ``application/x-www-form-urlencoded``, the way the browser encodes a
                ``URLSearchParams`` body.
          - ``multipart``: `MultipartFields` (a dictionary of text fields and files), sent as
                ``multipart/form-data`` the way the browser encodes a ``FormData`` body, in
                the order given. Do not set a ``Content-Type`` in ``headers``: the browser then leaves out the
                boundary of the parts, and the server cannot read the body.

        Give at most one of ``body``, ``form`` and ``multipart``. An empty ``form`` or
        ``multipart`` dictionary is given too: it sends an empty URL-encoded body or a
        multipart body without parts, as the browser does. ``GET`` and ``HEAD`` requests are
        sent without a body: a text, JSON, ``form`` or ``multipart`` body is left out, and a
        ``bytes`` body fails, so that binary data is not dropped unnoticed.
                For now the ``body`` and the files given as ``buffer`` can be at most 4 MiB
                together; a file given as ``path`` does not count.
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
        | VAR    &{fields} =    username=demo    password=mode
        | ${response} =      `HTTP`    /login    POST    form=${fields}
        |
        | VAR    &{file} =    path=${CURDIR}/avatar.png
        | VAR    &{fields} =    description=Profile picture    file=${file}
        | ${response} =      `HTTP`    /api/avatar    POST    multipart=${fields}    timeout=30s
        |
        | ${response} =      `HTTP`    /logo.png
        | Create Binary File    ${OUTPUT_DIR}/logo.png    ${response.bytes}

        [https://forum.robotframework.org/t//4296|Comment >>]
        """
        method_name = method.name if method else "GET"
        body = _plain_body(body)
        checked_form = _checked_form(form)
        checked_multipart = _checked_multipart(multipart)
        _check_at_most_one(body=body, form=checked_form, multipart=checked_multipart)
        sent_headers = _checked_headers(headers)
        if method_name in METHODS_WITHOUT_BODY:
            if isinstance(body, bytes):
                raise ValueError(
                    f"A {method_name} request is sent without a body, but bytes cannot be "
                    "left out silently. Give no body, or use another method, such as POST."
                )
            body = checked_form = checked_multipart = None
        request = Request().HttpRequest(
            url=url,
            method=method_name,
            timeout=self.get_timeout(timeout),
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
        _set_fields(request, checked_form, checked_multipart)
        if isinstance(body, bytes):
            request.bodyBytes = body
        elif isinstance(body, str):
            request.body = body
            sent_headers = _get_headers(body, sent_headers)
        elif body is not None:
            request.body = _json_text(body, "body")
            sent_headers = _with_content_type(sent_headers, "application/json")
        request.headers = json.dumps(sent_headers)
        with self.playwright.grpc_channel() as stub:
            response, body_bytes, _ = _collect_stream(stub.HttpRequest(request))
        _add_http_response_views(response, body_bytes)
        logger.info(_without(response, RESPONSE_BODY_KEYS))
        _trace_content("Response body", response["bytes"])
        return cast(HttpResponse, JsonDotDict(response))

    @keyword(name="Send API Request", tags=("Setter", "HTTP"))
    def send_api_request(
        self,
        url: str,
        method: RequestMethod = RequestMethod.GET,
        *,
        # Not "| None": in a union RF drops the converter's error and reports only
        # "cannot be converted to HttpHeaders or None". A None default passes None anyway.
        headers: HttpHeaders = None,  # type: ignore[assignment]
        params: QueryParams = None,  # type: ignore[assignment]
        data: JsonSerializable | bytes | Secret | None = None,
        form: FormFields = None,  # type: ignore[assignment]
        multipart: MultipartFields = None,  # type: ignore[assignment]
        timeout: timedelta | None = None,
        failOnStatusCode: bool | None = None,
        maxRedirects: int | None = None,
        maxRetries: int | None = None,
        ignoreHTTPSErrors: bool | None = None,
    ) -> APIResponse:
        """Sends an HTTP request through the active context, outside any page.

        The keyword is Playwright's
        [https://playwright.dev/docs/api/class-apirequestcontext#api-request-context-fetch|APIRequestContext.fetch]
        of the active context. The request is an API request, not page traffic:

        - It uses the cookies of the context. A cookie that a page received is sent, and a
          cookie that the response sets is there for the pages of the context too.
        - It uses the context's ``baseURL``, ``extraHTTPHeaders``, ``httpCredentials``,
          ``proxy``, ``userAgent``, ``ignoreHTTPSErrors`` and ``clientCertificates`` from
          `New Context`, as they are when the request is sent.
        - It needs an open context but no page, and fails when no context is open.
        - The browser's rules for a page do not apply: there is no CORS, and headers that a
          page cannot set, such as ``Origin`` or ``Cookie``, are sent as given.
        - Route rules, such as those of `Abort Requests`, and `Wait For Request` and
          `Wait For Response` do not see it.

        Use `HTTP` instead for a request that the page itself sends, with the page's rules.

        The named-only arguments are the options of Playwright's ``fetch``, with Playwright's
        names. An argument that is not given keeps Playwright's default.

        *Arguments:*
          - ``url``: The request URL. A relative URL is resolved against the context's
                ``baseURL`` and fails without one.
          - ``method``: The HTTP method. Defaults to ``GET``.
          - ``headers``: `HttpHeaders` (a dictionary) of the request. They override the
                context's ``extraHTTPHeaders`` with the same name.
          - ``params``: `QueryParams` (a dictionary or a string) added to the query of the
                ``url``. Characters such as ``&`` in a string keep their meaning in a query,
                see `QueryParams`. The string ``None`` adds no parameters.
          - ``data``: The request body, see `JsonSerializable`. Leave it out to send no body;
                the string ``None`` is sent as the text ``None``. A Robot Framework ``Secret`` is
                sent as its text.
                - A dictionary, a list, a number or a boolean is sent as JSON, exactly as
                  Python writes it, so large integers arrive unchanged. The ``Content-Type``
                  is ``application/json`` unless ``headers`` has one. A value that JSON
                  cannot hold, such as ``NaN``, a date or ``bytes`` inside a dictionary,
                  fails before the request is sent.
                - ``bytes`` are sent as given, as ``application/octet-stream`` unless
                  ``headers`` has a ``Content-Type``.
                - A string is sent as given, but the ``Content-Type`` in ``headers``
                  decides how. Without one, it is ``application/octet-stream``, also when
                  the string is JSON. With ``application/json``, parameters such as
                  ``charset`` aside, a string that is valid JSON is sent as given, and any
                  other string is encoded as a JSON string, so ``hello`` is sent as
                  ``"hello"``. Any other ``Content-Type``, also a JSON type such as
                  ``application/problem+json``, sends the string as given.
                - To send JSON written in the test data, give a dictionary, e.g.
                  ``data=${{ {"name": "robot"} }}``, or set the ``Content-Type`` in
                  ``headers``.
          - ``form``: `FormFields` (a dictionary), sent URL-encoded as
                ``application/x-www-form-urlencoded``.
          - ``multipart``: `MultipartFields` (a dictionary of text fields and files), sent as
                ``multipart/form-data``, in the order given. ``data``, ``form`` and
                ``multipart`` exclude each other, also when ``form`` or ``multipart`` is an
                empty dictionary.
                For now the ``data`` and the files given as ``buffer`` can be at most 4 MiB
                together; a file given as ``path`` does not count.
          - ``timeout``: How long to wait for the whole response, body included. Defaults to
                the library timeout; ``0`` waits without a limit.
          - ``failOnStatusCode``: When ``True``, the keyword fails on a status that is not
                2xx or 3xx. By default a response with an error status, such as ``404``, does
                not fail it.
          - ``maxRedirects``: How many redirects are followed. Playwright's default is 20,
                and it fails when there are more. ``0`` follows none and returns the redirect
                response.
          - ``maxRetries``: How often the request is retried when the connection is reset
                (``ECONNRESET``). Any other error fails at once, and an error status is never
                retried. Playwright's default is ``0``, no retry.
          - ``ignoreHTTPSErrors``: When ``True``, errors of the server's HTTPS certificate are
                ignored. They are also ignored when the context was opened with
                ``ignoreHTTPSErrors=True``; ``False`` cannot turn that off.

        The keyword fails on a network error, a timeout, too many redirects and, with
        ``failOnStatusCode``, an error status.

        Returns an `APIResponse` with the status, all headers, ``set-cookie`` included, the
        raw body as ``bytes`` and the views ``text`` and ``json``. The response is logged
        without its headers and body, the headers at ``DEBUG`` level, as they can contain
        cookies, and the body at ``TRACE`` level.

        Assigned with ``&{response} =``, ``bytes`` holds base64 text. Assign with
        ``${response} =`` to get the raw ``bytes``.

        | `New Context`    baseURL=https://example.com
        | `New Page`    /login
        | # ... log in on the page ...
        | VAR    &{user} =    name=robot
        | ${response} =    `Send API Request`    /api/users    POST    data=${user}    failOnStatusCode=True
        | Should Be Equal    ${response.status}    ${201}
        | Should Be Equal    ${response.json.name}    robot
        |
        | VAR    &{params} =    q=robot    page=${2}
        | ${response} =    `Send API Request`    /api/search    params=${params}
        |
        | VAR    &{file} =    path=${CURDIR}/avatar.png
        | VAR    &{fields} =    description=Profile picture    file=${file}
        | ${response} =    `Send API Request`    /api/avatar    POST    multipart=${fields}
        """
        checked_form = _checked_form(form)
        checked_multipart = _checked_multipart(multipart)
        _check_at_most_one(data=data, form=checked_form, multipart=checked_multipart)
        request = Request().ApiRequest(
            url=url,
            method=method.name if method else "GET",
            timeout=self.get_timeout(timeout),
        )
        _set_fields(request, checked_form, checked_multipart)
        if headers is not None:
            request.headers = json.dumps(_checked_headers(headers))
        checked_params = (
            None if params is None else QueryParams.from_value(cast(Any, params))
        )
        if checked_params is not None:
            _set_api_params(request, checked_params)
        _set_api_data(request, data)
        _set_given(
            request,
            failOnStatusCode=failOnStatusCode,
            maxRedirects=maxRedirects,
            maxRetries=maxRetries,
            ignoreHTTPSErrors=ignoreHTTPSErrors,
        )
        with self.playwright.grpc_channel() as stub:
            response, body, _ = _collect_stream(stub.SendApiRequest(request))
        _add_body_views(response, body)
        logger.info(_without(response, API_RESPONSE_HEADER_KEYS + RESPONSE_BODY_KEYS))
        logger.debug(f"Response headers: {response['headersArray']}")
        _trace_content("Response body", body)
        return cast(APIResponse, JsonDotDict(response))

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
                see its matcher examples. An invalid RegExp fails at once. For additional
                information, see the Playwright
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
                matched. An invalid RegExp fails at once. For additional information, see
                the Playwright
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
        Any matcher that starts with ``/`` and ends with ``/``, or with ``/`` and only the flag
        letters ``gimsuy``, is read as a RegExp. So a relative glob such as ``/api/users/`` or
        ``/api/items/my`` is a RegExp, ``api/users`` and ``api/items`` with the flags ``my``.
        Write it as ``**/api/users/`` to match it as a glob.
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
                wrapped in ``/`` symbols, as in `Wait For Response`. An invalid RegExp fails
                at once.
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

    @keyword(tags=("Route", "Setter", "HTTP"))
    def abort_requests(
        self,
        matcher: str | RegExp,
        *,
        errorCode: AbortErrorCode = AbortErrorCode.failed,
        times: int | None = None,
        on: ContextOrPage = ContextOrPage.Context,
    ) -> str:
        """Adds a route rule that makes every request matching ``matcher`` fail.

        *Arguments:*
          - ``matcher``: Request URL matcher: a glob pattern, a JavaScript RegExp enclosed in
                ``/``, or a JavaScript arrow function that receives the request
                [https://developer.mozilla.org/en-US/docs/Web/API/URL|URL] and returns a
                boolean, such as ``url => url.searchParams.get('id') === '7'``. Globs and
                RegExps match as in `Wait For Response`, see its matcher examples; unlike
                there, the function gets the URL, not the request. An invalid RegExp fails.
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
        aborted request is logged only in ``playwright-log.txt``. When several rules match a
        request, the newest one wins, and a Page rule wins over a Context rule.

        Example, an outage of two requests and then recovery:
        | `Abort Requests`    **/api/orders    times=2
        | `Click`    id=reload-orders    # request aborted
        | `Click`    id=reload-orders    # request aborted
        | `Click`    id=reload-orders    # reaches the server
        | `Get Text`    id=orders-status    ==    loaded

        See [https://robotframework-browser.org/docs/concepts/route-rules|route rules] for
        more.
        """
        _check_times(times)
        request = Request().RouteRule(
            url=matcher,
            times=times,
            abort=Request().RouteAbort(errorCode=errorCode.name),
        )
        rule_id = self._add_route_rule(request, on)
        logger.info(
            f"Added route rule {rule_id}: abort {matcher} with {errorCode.name}, "
            f"times={times}, on={on.name}."
        )
        return rule_id

    @keyword(tags=("Route", "Setter", "HTTP"))
    def mock_responses(
        self,
        matcher: str | RegExp,
        *,
        status: int = 200,
        body: JsonSerializable | bytes | Secret | None = None,
        # Not "| None": in a union RF drops the converter's error and reports only
        # "cannot be converted to JsonSerializable or None". A None default passes None.
        json: JsonSerializable = None,  # type: ignore[assignment]
        path: PathLike | None = None,
        headers: HttpHeaders = None,  # type: ignore[assignment]
        times: int | None = None,
        on: ContextOrPage = ContextOrPage.Context,
    ) -> str:
        """Adds a route rule that answers every request matching ``matcher`` with a mock response.

        The request never reaches the server.

        *Arguments:*
          - ``matcher``: Request URL matcher: a glob pattern, a JavaScript RegExp enclosed in
                ``/``, or a JavaScript arrow function that receives the request
                [https://developer.mozilla.org/en-US/docs/Web/API/URL|URL] and returns a
                boolean, such as ``url => url.searchParams.get('id') === '7'``. Globs and
                RegExps match as in `Wait For Response`, see its matcher examples; unlike
                there, the function gets the URL, not the request. An invalid RegExp fails.
          - ``status``: The response status, from 100 to 599. There is no reason phrase
                argument: the browser shows the standard phrase, or ``Unknown`` for a code
                such as 299.
          - ``body``: The response body as text or a Robot Framework ``Secret``, sent as
                UTF-8, or as bytes, sent unchanged. A dictionary, a list, a number or a
                boolean is sent as JSON, as with ``json``. ``body=`` is an empty body. To
                answer with a captured body, give its bytes, for example
                ``body=${response.bytes}`` from `Wait For Response`.
          - ``json``: A `JsonSerializable` value, such as a dictionary, list or number, sent
                as compact JSON. A string is sent as a JSON string, so JSON text goes in
                ``body`` with a Content-Type header. ``None`` means not given: for a JSON
                ``null`` body use ``body=null`` with a Content-Type header.
          - ``path``: A file whose bytes are the body; binary files work. A relative path
                resolves against the working directory.
          - ``headers``: `HttpHeaders` (a dictionary), all headers of the mock response.
          - ``times``: How many matching requests the rule answers before it ends. ``None``
                (default) answers every matching request until the rule is removed. Must be 1
                or more.
          - ``on``: Where the rule is added, see `ContextOrPage`. ``Context`` (default) for
                every page of the active context, also pages opened later, ``Page`` for the
                active page only: the rule stays on that page and does not follow
                `Switch Page`. Fails when no context or page is open.

        Give at most one of ``body``, ``json`` and ``path``; none is an empty body, for example
        with ``status=204``. Unless ``headers`` has a Content-Type, which always wins, the
        Content-Type is ``text/plain; charset=utf-8`` for a text ``body``,
        ``application/octet-stream`` for a bytes ``body``, ``application/json`` for
        ``json``, guessed from the file extension for ``path`` (``application/octet-stream``
        if unknown, and with ``charset=utf-8`` for a ``text/`` type, so give a file in another
        encoding its Content-Type in ``headers``), and none without a payload, which WebKit reports as
        ``application/octet-stream``.

        Returns the rule id, to give to `Remove Route Rule`.

        A rule ends when its context or page closes, when it is removed with
        `Remove Route Rule` or `Remove All Route Rules`, or when it has used up its ``times``.
        It does not end with the test or suite.

        A request that a service worker answers never reaches a route rule; open the context
        with ``serviceWorkers=block`` in `New Context` to route those requests too. Each
        answered request is logged only in ``playwright-log.txt``. When several rules match a
        request, the newest one wins, and a Page rule wins over a Context rule.

        The keyword never logs the body or header values, but a string value still shows in
        the keyword's arguments in the Robot Framework log; give a token as ``Secret`` to keep
        it out. With ``enable_playwright_debug`` in the library import, the values are visible
        as plain text in the Playwright debug log.

        A cross-origin mock response needs no CORS headers. If it sets its own
        ``Access-Control-Allow-Origin``, the browser checks it, so ``*`` together with
        credentials fails.

        Example, mock the orders and then fail the next request once:
        | `Mock Responses`    **/api/orders    json=${orders}
        | `Mock Responses`    **/api/orders    status=500    times=1
        | `Click`    id=reload-orders    # gets 500
        | `Click`    id=reload-orders    # gets ${orders}

        See [https://robotframework-browser.org/docs/concepts/route-rules|route rules] for
        more.
        """
        _check_times(times)
        _check_status(status)
        payload, response_headers, payload_kind = _payload_with_content_type(
            _plain_body(body), json, path, _checked_headers(headers)
        )
        request = Request().RouteRule(
            url=matcher,
            times=times,
            fulfill=Request().RouteFulfill(
                status=status, headers=response_headers, body=payload
            ),
        )
        rule_id = self._add_route_rule(request, on)
        logger.info(
            f"Added route rule {rule_id}: mock {matcher} with status {status} and "
            f"{payload_kind}, times={times}, on={on.name}."
        )
        return rule_id

    @keyword(tags=("Route", "Setter", "HTTP"))
    def modify_responses(
        self,
        matcher: str | RegExp,
        *,
        status: int | None = None,
        body: JsonSerializable | bytes | Secret | None = None,
        # Not "| None": in a union RF drops the converter's error and reports only
        # "cannot be converted to HttpHeaderChanges or None". A None default passes None.
        json: JsonSerializable = None,  # type: ignore[assignment]
        path: PathLike | None = None,
        json_patch: dict[str, Any] | None = None,
        headers: HttpHeaderChanges = None,  # type: ignore[assignment]
        request_url: str | Secret | None = None,
        request_method: RequestMethod | None = None,
        request_headers: HttpHeaderChanges = None,  # type: ignore[assignment]
        request_body: JsonSerializable | bytes | Secret | None = None,
        times: int | None = None,
        on: ContextOrPage = ContextOrPage.Context,
    ) -> str:
        """Adds a route rule that sends every request matching ``matcher`` to the server and changes the real response.

        The request reaches the server, and only the parts given here change, in the request
        on its way out and in the response on its way back. Every change is ``None`` by
        default, which keeps the real value; give at least one.

        *Arguments:*
          - ``matcher``: Request URL matcher: a glob pattern, a JavaScript RegExp enclosed in
                ``/``, or a JavaScript arrow function that receives the request
                [https://developer.mozilla.org/en-US/docs/Web/API/URL|URL] and returns a
                boolean, such as ``url => url.searchParams.get('id') === '7'``. Globs and
                RegExps match as in `Wait For Response`, see its matcher examples; unlike
                there, the function gets the URL, not the request. An invalid RegExp fails.
          - ``status``: The response status, from 100 to 599.
          - ``body``: Replaces the real body with text, a Robot Framework ``Secret``, bytes or
                a JSON value, as in `Mock Responses`.
          - ``json``: Replaces the real body with a JSON-encoded value, as in `Mock Responses`.
          - ``path``: Replaces the real body with the bytes of a file, as in `Mock Responses`.
          - ``json_patch``: Changes fields of the real JSON body, as an
                [https://www.rfc-editor.org/rfc/rfc7386|RFC 7386 JSON Merge Patch]: dictionaries
                merge, ``None`` deletes a key and a list replaces the whole list. Like ``json``,
                it fails for ``NaN``, ``Infinity`` and values JSON cannot hold.
          - ``headers``: `HttpHeaderChanges` (a dictionary) merged onto the real response
                headers: a value replaces the real header, ``None`` removes it.
          - ``request_url``: Sends the request to this URL instead, absolute or relative to the
                original one. The page keeps its original URL.
          - ``request_method``: Sends the request with this method.
          - ``request_headers``: `HttpHeaderChanges` (a dictionary) merged onto the real
                request headers, the same way as ``headers``.
          - ``request_body``: Sends this text or Robot Framework ``Secret`` as UTF-8, these
                bytes unchanged, or a dictionary, a list, a number or a boolean as JSON with the
                ``Content-Type`` ``application/json``, as the request body. A captured request body is
                ``${request.postDataBuffer}`` from `Wait For Request`.
          - ``times``: How many matching requests the rule changes before it ends. ``None``
                (default) changes every matching request until the rule is removed.
          - ``on``: Where the rule is added, see `ContextOrPage`.

        Give at most one of ``body``, ``json``, ``path`` and ``json_patch``. In ``headers`` and
        ``request_headers`` a given value wins, an empty string sends the header empty and
        ``None`` removes it.

        When the real request fails, the page request fails too. The real request gets the
        browser timeout that is in effect when the rule is added.

        Returns the rule id, to give to `Remove Route Rule`. Like the rules of
        `Abort Requests`, a rule ends with its context or page, when removed or when its
        ``times`` is used up. Header names are logged, never values or bodies; give tokens as
        ``Secret`` to keep them out of the keyword's arguments in the log.

        Example, an order in an edge-case state, fetched with a token:
        | VAR    ${token: Secret} =    %{API_TOKEN}
        | VAR    &{auth} =    Authorization=${token}
        | VAR    &{patch} =    state=cancelled    note=${None}
        | `Modify Responses`    **/api/orders/1    json_patch=${patch}    request_headers=${auth}

        See [https://robotframework-browser.org/docs/concepts/route-rules#modify-responses|route rules]
        for redirects, cookies on a changed URL, failures and more examples.
        """
        _check_times(times)
        response_headers, removed_headers = _checked_header_changes(headers)
        sent_headers, removed_request_headers = _checked_header_changes(request_headers)
        payloads = {"body": body, "json": json, "path": path, "json_patch": json_patch}
        _check_at_most_one(**payloads)
        request_changes = _request_changes(
            request_url,
            request_method,
            {**sent_headers, **dict.fromkeys(removed_request_headers)},
            request_body,
        )
        response_changes = _response_changes(
            status, payloads, {**response_headers, **dict.fromkeys(removed_headers)}
        )
        if not request_changes and not response_changes:
            raise ValueError("Modify Responses needs at least one change.")
        if status is not None:
            _check_status(status)
        replaced_body, json_patch_text, response_headers = _modified_payload(
            _plain_body(body), json, path, json_patch, response_headers
        )
        post_data = None
        request_body = _plain_body(request_body)
        if request_body is not None:
            post_data, sent_headers = _request_body(request_body, sent_headers)
        modify = Request().RouteModify(
            url=_reveal(request_url),
            method=request_method.name if request_method else None,
            postData=post_data,
            timeout=int(self.get_timeout(None)),
            status=status,
            requestHeaders=sent_headers,
            headers=response_headers,
            body=replaced_body,
            jsonPatch=json_patch_text,
            removedRequestHeaders=removed_request_headers,
            removedHeaders=removed_headers,
        )
        rule_id = self._add_route_rule(
            Request().RouteRule(url=matcher, times=times, modify=modify), on
        )
        logger.info(
            f"Added route rule {rule_id}: modify {matcher}, "
            f"request: {_change_log(request_changes)}; "
            f"response: {_change_log(response_changes)}, times={times}, on={on.name}."
        )
        return rule_id

    def _add_route_rule(self, request: Request.RouteRule, on: ContextOrPage) -> str:
        with self.playwright.grpc_channel() as stub:
            if on == ContextOrPage.Page:
                return stub.AddPageRoute(request).id
            return stub.AddContextRoute(request).id

    @keyword(tags=("Route", "Setter", "HTTP"))
    def remove_route_rule(self, rule_id: str):
        """Removes the route rule with ``rule_id``.

        *Arguments:*
          - ``rule_id``: The id that `Abort Requests`, `Mock Responses` or `Modify Responses`
                returned. The rule is found in any context, so a Page rule can be removed while
                another page is active.

        It logs how many times the rule ran. An unknown or already ended id, or no open context,
        is logged and the keyword passes. When the keyword returns, the rule affects no request:
        it waits for the rule's running handlers to finish.

        Example:
        | ${rule} =    `Abort Requests`    **/api/orders
        | `Click`    id=reload-orders    # request aborted
        | `Remove Route Rule`    ${rule}
        | `Click`    id=reload-orders    # reaches the server
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.RemoveRouteRule(Request().RouteRuleId(id=rule_id))
        logger.info(response.log)

    @keyword(tags=("Route", "Setter", "HTTP"))
    def remove_all_route_rules(self):
        """Removes the route rules of the active context and of every page in it.

        Only rules added by this library are removed, routes that a plugin or a JavaScript
        keyword added with ``page.route`` stay. Like `Remove Route Rule`, the keyword waits for
        running handlers to finish. It logs how many Context and Page rules it removed, and how
        many times each rule ran. With no rules, or no open context, it logs and passes, so it is
        safe in a teardown.

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
