import json
from Browser.keywords.network import _format_response


def test_response_parsing_lowercase():
    response = _format_response(
        {"headers": '{"content-type": "application/json"}', "body": '{"key":"value1"}'}
    )
    assert response["body"]["key"] == "value1"


def test_response_parsing_caps():
    response = _format_response(
        {"headers": '{"Content-Type": "application/json"}', "body": '{"key":"value2"}'}
    )
    assert response["body"]["key"] == "value2"
    assert response["headers"]["Content-Type"] == "application/json"


def test_response_parsing_text():
    response = _format_response(
        {
            "headers": '{"Content-Type": "text/html; charset=UTF-8"}',
            "body": "{key:'value3'}",
        }
    )
    assert response["body"] == "{key:'value3'}"
    assert response["headers"]["Content-Type"] == "text/html; charset=UTF-8"


def test_empty_response():
    response = _format_response(
        {"headers": '{"Content-Type": "application/json"}', "body": None}
    )
    assert response["body"] == None
    assert response["headers"]["Content-Type"] == "application/json"


def test_format_response_with_invalid_json_body():
    response = _format_response(
        {"headers": '{"content-type": "application/json"}', "body": "{invalid: json}"}
    )
    assert response["body"] == "{invalid: json}"
    assert response["headers"]["content-type"] == "application/json"


def test_format_response_with_no_body():
    response = _format_response({"headers": '{"content-type": "application/json"}'})
    assert "body" not in response
    assert response["headers"]["content-type"] == "application/json"


def test_format_response_with_no_headers():
    response = _format_response({"body": '{"key":"value1"}'})
    assert response["body"] == '{"key":"value1"}'
    assert response["headers"] == {}


def test_format_response_with_empty_response():
    response = _format_response({})
    assert "body" not in response
    assert response["headers"] == {}


def test_format_response_with_json_list_body():
    body_list = '[{"key":"value1"}, {"key":"value2"}]'
    response = _format_response(
        {"headers": '{"content-type": "application/json"}', "body": body_list}
    )
    assert isinstance(response["body"], list)
    assert response["body"][0]["key"] == "value1"
    assert response["body"][1]["key"] == "value2"
    assert response["headers"]["content-type"] == "application/json"

    response = _format_response(
        {
            "headers": '{"content-type": "application/json"}',
            "body": json.loads(body_list),
        }
    )
    assert isinstance(response["body"], list)
    assert response["body"][0]["key"] == "value1"
    assert response["body"][1]["key"] == "value2"
    assert response["headers"]["content-type"] == "application/json"


def testtest_format_response_with_json_int_body():
    body_int = 1
    response = _format_response(
        {"headers": '{"content-type": "application/json"}', "body": body_int}
    )
    assert response["body"] == 1
    assert response["headers"]["content-type"] == "application/json"


def testtest_format_response_with_json_byte_body():
    body_byte = b"byte"
    response = _format_response(
        {"headers": '{"content-type": "application/json"}', "body": body_byte}
    )
    assert response["body"] == b"byte"
    assert response["headers"]["content-type"] == "application/json"
