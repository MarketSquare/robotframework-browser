import json
from unittest.mock import MagicMock

import pytest

from Browser import Browser
from Browser.keywords.network import _readable

PNG_SIGNATURE = bytes.fromhex("89504e470d0a1a0a")


def request_metadata(
    post_data: str | None = None, content_type: str = "text/plain"
) -> dict:
    metadata = {
        "url": "http://localhost/api",
        "headers": json.dumps({"content-type": content_type}),
        "method": "POST" if post_data is not None else "GET",
        "postData": post_data,
        "allHeaders": {"content-type": content_type, "cookie": "session=1"},
        "headersArray": [{"name": "content-type", "value": content_type}],
        "resourceType": "fetch",
        "isNavigationRequest": False,
        "redirectedFrom": None,
        "redirectedTo": None,
        "frame": {"url": "http://localhost/", "name": ""},
        "hasPostData": post_data is not None,
    }
    return metadata


def message(json_text: str = "", body: bytes = b"", post_data: bytes = b""):
    return MagicMock(log="", json=json_text, bodyBytes=body, postDataBytes=post_data)


def response_messages(
    body: bytes | None,
    content_type: str = "text/plain",
    request: dict | None = None,
):
    request = request or request_metadata()
    metadata = {
        "status": 200,
        "headers": json.dumps({"content-type": content_type}),
        "statusText": "OK",
        "url": "http://localhost/api",
        "ok": True,
        "allHeaders": {"content-type": content_type, "set-cookie": "a=1"},
        "headersArray": [{"name": "set-cookie", "value": "a=1"}],
        "httpVersion": "HTTP/1.1",
        "serverAddr": {"ipAddress": "127.0.0.1", "port": 80},
        "securityDetails": None,
        "fromServiceWorker": False,
        "hasBody": body is not None,
        "request": request,
    }
    post_data = (request["postData"] or "").encode()
    return [message(json.dumps(metadata), body or b"", post_data)]


@pytest.fixture
def stub() -> MagicMock:
    return MagicMock()


@pytest.fixture
def browser(stub: MagicMock, stub_grpc_channel) -> Browser:
    browser = Browser()
    stub_grpc_channel(browser, stub)
    return browser


def body_of(browser: Browser, stub: MagicMock, raw: bytes, content_type="text/plain"):
    stub.WaitForResponse.return_value = response_messages(raw, content_type)
    return browser.wait_for_response()["body"]


def test_json_body_is_parsed_even_without_json_content_type(browser, stub):
    assert body_of(browser, stub, b'{"greeting": "HELLO"}') == {"greeting": "HELLO"}


def test_json_number_body_is_parsed_to_int(browser, stub):
    assert body_of(browser, stub, b"42") == 42


def test_json_boolean_body_is_parsed_to_bool(browser, stub):
    assert body_of(browser, stub, b"true") is True


def test_json_list_body_is_parsed_to_list(browser, stub):
    assert body_of(browser, stub, b"[1, 2]", "text/html") == [1, 2]


def test_text_body_stays_string(browser, stub):
    assert body_of(browser, stub, b"HELLO", "text/html") == "HELLO"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [(b"{}", {}), (b"[]", []), (b"0", 0), (b"false", False), (b"null", None)],
)
def test_falsy_json_body_is_kept(browser, stub, raw, expected):
    stub.WaitForResponse.return_value = response_messages(raw, "application/json")
    response = browser.wait_for_response()
    assert "body" in response
    assert response["body"] == expected


def test_empty_body_is_empty_string(browser, stub):
    assert body_of(browser, stub, b"") == ""


def test_json_string_body_is_decoded_only_once(browser, stub):
    raw = json.dumps('{"x": 1}').encode()
    assert body_of(browser, stub, raw, "application/json") == '{"x": 1}'


def test_nan_body_is_not_parsed_as_json(browser, stub):
    assert body_of(browser, stub, b"NaN") == "NaN"


def test_body_chunks_are_joined_before_parsing(browser, stub):
    first, *_ = response_messages(b'{"greeting": ')
    stub.WaitForResponse.return_value = [first, message(body=b'"HELLO"}')]
    assert browser.wait_for_response()["body"] == {"greeting": "HELLO"}


def test_unreadable_body_is_none_in_every_view(browser, stub):
    stub.WaitForResponse.return_value = response_messages(None)
    response = browser.wait_for_response()
    assert response["body"] is None
    assert response["bytes"] is None
    assert response["text"] is None
    assert response["json"] is None


def test_binary_body_keeps_its_bytes(browser, stub):
    stub.WaitForResponse.return_value = response_messages(PNG_SIGNATURE, "image/png")
    response = browser.wait_for_response()
    assert response["bytes"] == PNG_SIGNATURE
    assert response["text"] == PNG_SIGNATURE.decode("utf-8", errors="replace")
    assert response["json"] is None


def test_json_view_parses_regardless_of_content_type(browser, stub):
    stub.WaitForResponse.return_value = response_messages(b'{"a": 1}', "text/plain")
    assert browser.wait_for_response()["json"] == {"a": 1}


def test_json_view_is_none_where_body_falls_back_to_text(browser, stub):
    stub.WaitForResponse.return_value = response_messages(b"HELLO")
    response = browser.wait_for_response()
    assert response["text"] == "HELLO"
    assert response["json"] is None


def test_include_body_false_asks_node_to_exclude_the_body(browser, stub):
    stub.WaitForResponse.return_value = response_messages(None)
    browser.wait_for_response(include_body=False)
    assert stub.WaitForResponse.call_args.args[0].excludeBody is True


def test_response_metadata_is_returned(browser, stub):
    stub.WaitForResponse.return_value = response_messages(b"HELLO")
    response = browser.wait_for_response()
    assert response.status == 200
    assert response.statusText == "OK"
    assert response.url == "http://localhost/api"
    assert response.ok is True
    assert response.headers == {"content-type": "text/plain"}
    assert response.allHeaders["set-cookie"] == "a=1"
    assert response.httpVersion == "HTTP/1.1"
    assert response.serverAddr.port == 80
    assert response.request.method == "GET"
    assert response.request.url == "http://localhost/api"


def test_nested_post_data_is_parsed_with_json_content_type(browser, stub):
    request = request_metadata('{"name": "George"}', "application/json")
    stub.WaitForResponse.return_value = response_messages(b"", request=request)
    response = browser.wait_for_response()
    assert response.request.postData == {"name": "George"}
    assert response.request.headers == {"content-type": "application/json"}


def test_nested_post_data_stays_string_without_json_content_type(browser, stub):
    request = request_metadata('{"name": "George"}', "text/plain")
    stub.WaitForResponse.return_value = response_messages(b"", request=request)
    response = browser.wait_for_response()
    assert response.request.postData == '{"name": "George"}'
    assert response.request.postDataJSON == {"name": "George"}
    assert response.request.postDataBuffer == b'{"name": "George"}'


def test_nested_request_without_post_data_has_no_buffer(browser, stub):
    stub.WaitForResponse.return_value = response_messages(b"")
    request = browser.wait_for_response().request
    assert request.postDataBuffer is None
    assert request.postDataJSON is None


def captured_request(stub, post_data: str | None, content_type: str = "text/plain"):
    metadata = request_metadata(post_data, content_type)
    metadata["headers"] = json.loads(metadata["headers"])
    raw = post_data.encode() if post_data is not None else b""
    stub.WaitForRequest.return_value = [message(json.dumps(metadata), post_data=raw)]


def test_wait_for_request_returns_raw_post_data(browser, stub):
    captured_request(stub, '{"key": "value"}')
    request = browser.wait_for_request()
    assert request.postDataBuffer == b'{"key": "value"}'
    assert request.postDataJSON == {"key": "value"}


def test_wait_for_request_parses_form_post_data_like_playwright(browser, stub):
    captured_request(
        stub,
        "name=George&city=Helsinki&name=Ringo",
        "application/x-www-form-urlencoded",
    )
    assert browser.wait_for_request().postDataJSON == {
        "name": "Ringo",
        "city": "Helsinki",
    }


def test_wait_for_request_post_data_json_is_none_for_invalid_json(browser, stub):
    captured_request(stub, "not json")
    assert browser.wait_for_request().postDataJSON is None


def test_wait_for_request_keeps_legacy_keys(browser, stub):
    captured_request(stub, None)
    request = browser.wait_for_request()
    assert request.url == "http://localhost/api"
    assert request.method == "GET"
    assert request.headers == {"content-type": "text/plain"}
    assert request.postData is None
    assert request.postDataBuffer is None


def test_body_is_logged_as_formatted_json():
    assert _readable(b'{"a":1}') == '{\n  "a": 1\n}'


def test_body_is_logged_as_text_when_it_is_utf8():
    assert _readable("<p>Hyvä</p>".encode()) == "<p>Hyvä</p>"


def test_binary_body_is_logged_as_base64():
    assert _readable(PNG_SIGNATURE) == "8 bytes, base64: iVBORw0KGgo="
