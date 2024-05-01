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


def test_response_parsing_text():
    response = _format_response(
        {
            "headers": '{"Content-Type": "text/html; charset=UTF-8"}',
            "body": "{key:'value3'}",
        }
    )
    assert response["body"] == "{key:'value3'}"


def test_empty_response():
    response = _format_response(
        {"headers": '{"Content-Type": "application/json"}', "body": None}
    )
    assert response["body"] == None
