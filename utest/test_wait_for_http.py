import json
from unittest.mock import MagicMock

import pytest

from Browser import Browser


def response_chunk(body_part: str, content_type: str = "text/plain", **extra):
    metadata = {
        "status": 200,
        "headers": json.dumps({"content-type": content_type}),
        "statusText": "OK",
        "url": "http://localhost/api",
        "ok": True,
        "request": {
            "headers": json.dumps({}),
            "method": "GET",
            "postData": None,
        },
        **extra,
    }
    return MagicMock(log="", json=json.dumps(metadata), bodyPart=body_part)


@pytest.fixture
def stub() -> MagicMock:
    return MagicMock()


@pytest.fixture
def browser(stub: MagicMock, stub_grpc_channel) -> Browser:
    browser = Browser()
    stub_grpc_channel(browser, stub)
    return browser


def test_json_body_is_parsed_even_without_json_content_type(browser, stub):
    stub.WaitForResponse.return_value = [response_chunk('{"greeting": "HELLO"}')]
    assert browser.wait_for_response()["body"] == {"greeting": "HELLO"}


def test_json_number_body_is_parsed_to_int(browser, stub):
    stub.WaitForResponse.return_value = [response_chunk("42")]
    assert browser.wait_for_response()["body"] == 42


def test_json_boolean_body_is_parsed_to_bool(browser, stub):
    stub.WaitForResponse.return_value = [response_chunk("true")]
    assert browser.wait_for_response()["body"] is True


def test_json_list_body_is_parsed_to_list(browser, stub):
    stub.WaitForResponse.return_value = [response_chunk("[1, 2]", "text/html")]
    assert browser.wait_for_response()["body"] == [1, 2]


def test_text_body_stays_string(browser, stub):
    stub.WaitForResponse.return_value = [response_chunk("HELLO", "text/html")]
    assert browser.wait_for_response()["body"] == "HELLO"


def test_body_chunks_are_joined_before_parsing(browser, stub):
    stub.WaitForResponse.return_value = [
        response_chunk('{"greeting": '),
        response_chunk('"HELLO"}'),
    ]
    assert browser.wait_for_response()["body"] == {"greeting": "HELLO"}


def test_empty_body_leaves_body_key_out(browser, stub):
    stub.WaitForResponse.return_value = [response_chunk("")]
    assert "body" not in browser.wait_for_response()


def test_unreadable_body_is_none(browser, stub):
    stub.WaitForResponse.return_value = [response_chunk("", body=None)]
    assert browser.wait_for_response()["body"] is None


def test_response_metadata_is_returned(browser, stub):
    stub.WaitForResponse.return_value = [response_chunk("HELLO")]
    response = browser.wait_for_response()
    assert response.status == 200
    assert response.statusText == "OK"
    assert response.url == "http://localhost/api"
    assert response.ok is True
    assert response.headers == {"content-type": "text/plain"}
    assert response.request.method == "GET"


def nested_request(post_data: str, content_type: str) -> dict:
    return {
        "headers": json.dumps({"content-type": content_type}),
        "method": "POST",
        "postData": post_data,
    }


def test_nested_post_data_is_parsed_with_json_content_type(browser, stub):
    request = nested_request('{"name": "George"}', "application/json")
    stub.WaitForResponse.return_value = [response_chunk("", request=request)]
    response = browser.wait_for_response()
    assert response.request.postData == {"name": "George"}
    assert response.request.headers == {"content-type": "application/json"}


def test_nested_post_data_stays_string_without_json_content_type(browser, stub):
    request = nested_request('{"name": "George"}', "text/plain")
    stub.WaitForResponse.return_value = [response_chunk("", request=request)]
    assert browser.wait_for_response().request.postData == '{"name": "George"}'
