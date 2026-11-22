import json
from datetime import timedelta
from typing import get_type_hints
from unittest.mock import MagicMock

import pytest
from robot.running.arguments.typeinfo import TypeInfo

from Browser import Browser
from Browser.keywords.network import Network


def response_messages(body: bytes = b"", **metadata) -> list[MagicMock]:
    meta = {
        "status": 200,
        "statusText": "OK",
        "ok": True,
        "url": "http://localhost/api",
        "headers": {"set-cookie": "session=1"},
        "headersArray": [{"name": "Set-Cookie", "value": "session=1"}],
        **metadata,
    }
    return [MagicMock(log="", json=json.dumps(meta), bodyBytes=body, postDataBytes=b"")]


@pytest.fixture
def stub() -> MagicMock:
    stub = MagicMock()
    stub.SendApiRequest.return_value = response_messages()
    return stub


@pytest.fixture
def browser(stub: MagicMock, stub_grpc_channel) -> Browser:
    browser = Browser()
    stub_grpc_channel(browser, stub)
    return browser


def sent(browser: Browser, stub: MagicMock, url="/api", **arguments):
    browser.send_api_request(url, **arguments)
    return stub.SendApiRequest.call_args.args[0]


def convert_like_robot(argument: str, value):
    hint = get_type_hints(Network.send_api_request)[argument]
    return TypeInfo.from_type_hint(hint).convert(
        value, custom_converters=Browser.ROBOT_LIBRARY_CONVERTERS
    )


def test_only_url_method_and_timeout_are_sent_by_default(browser, stub):
    request = sent(browser, stub)
    assert request.url == "/api"
    assert request.method == "GET"
    assert request.timeout == 10000
    for option in (
        "headers",
        "encodedParams",
        "dataText",
        "dataBytes",
        "dataJson",
        "failOnStatusCode",
        "maxRedirects",
        "maxRetries",
        "ignoreHTTPSErrors",
    ):
        assert not request.HasField(option), option
    assert not request.HasField("params")
    assert not request.HasField("form")
    assert not request.HasField("multipart")


def test_timeout_is_sent_in_milliseconds(browser, stub):
    assert sent(browser, stub, timeout=timedelta(seconds=2)).timeout == 2000


def test_headers_are_sent_as_json(browser, stub):
    request = sent(browser, stub, headers={"X-Robot": "Beep"})
    assert json.loads(request.headers) == {"X-Robot": "Beep"}


def test_dictionary_params_are_sent_as_fields_with_text_values(browser, stub):
    request = sent(browser, stub, params={"q": "robot", "page": 2, "all": True})
    assert request.HasField("params")
    assert [(field.name, field.value) for field in request.params.fields] == [
        ("q", "robot"),
        ("page", "2"),
        ("all", "true"),
    ]
    assert not request.HasField("encodedParams")


def test_string_params_are_sent_as_encoded_params(browser, stub):
    request = sent(browser, stub, params="q=a%20b")
    assert request.encodedParams == "q=a%20b"
    assert not request.HasField("params")


@pytest.mark.parametrize(
    ("data", "field", "value"),
    [
        ("hello", "dataText", "hello"),
        ("", "dataText", ""),
        (b"\x00\xff", "dataBytes", b"\x00\xff"),
        ({"name": "robot"}, "dataJson", '{"name":"robot"}'),
        ([1, 2], "dataJson", "[1,2]"),
        (
            {"id": 9007199254740993, "x": 1.0},
            "dataJson",
            '{"id":9007199254740993,"x":1.0}',
        ),
        (5, "dataJson", "5"),
        (False, "dataJson", "false"),
    ],
)
def test_data_is_sent_by_its_type(browser, stub, data, field, value):
    request = sent(browser, stub, data=data)
    assert getattr(request, field) == value
    others = {"dataText", "dataBytes", "dataJson"} - {field}
    assert not any(request.HasField(other) for other in others)


def test_form_values_are_sent_as_text(browser, stub):
    request = sent(browser, stub, form={"q": "robot", "n": 1, "all": False})
    assert [(field.name, field.value) for field in request.form.fields] == [
        ("q", "robot"),
        ("n", "1"),
        ("all", "false"),
    ]


def test_multipart_file_from_path_is_resolved_in_python(browser, stub, tmp_path):
    file = tmp_path / "notes.txt"
    file.write_text("hello")
    request = sent(browser, stub, multipart={"text": "a", "file": {"path": file}})
    assert request.multipart.fields[0].value == "a"
    assert request.multipart.fields[1].path == str(file.resolve())
    assert request.multipart.fields[1].fileName == "notes.txt"
    assert request.multipart.fields[1].mimeType == "text/plain"


@pytest.mark.parametrize("option", ["params", "form", "multipart"])
def test_an_empty_dictionary_is_sent_as_given(browser, stub, option):
    request = sent(browser, stub, **{option: {}})
    assert request.HasField(option)
    assert not getattr(request, option).fields


@pytest.mark.parametrize(
    ("option", "value"),
    [
        ("failOnStatusCode", True),
        ("maxRedirects", 0),
        ("maxRetries", 3),
        ("ignoreHTTPSErrors", True),
    ],
)
def test_given_options_are_sent(browser, stub, option, value):
    request = sent(browser, stub, **{option: value})
    assert request.HasField(option)
    assert getattr(request, option) == value


def test_response_has_metadata_and_body_views(browser, stub):
    stub.SendApiRequest.return_value = response_messages(b'{"name": "robot"}')
    response = browser.send_api_request("/api")
    assert response["status"] == 200
    assert response["headers"]["set-cookie"] == "session=1"
    assert response["headersArray"] == [{"name": "Set-Cookie", "value": "session=1"}]
    assert response["bytes"] == b'{"name": "robot"}'
    assert response["text"] == '{"name": "robot"}'
    assert response.json.name == "robot"
    assert "body" not in response


def test_response_body_that_is_not_json_has_no_json_view(browser, stub):
    stub.SendApiRequest.return_value = response_messages(b"\x89PNG")
    response = browser.send_api_request("/api")
    assert response["bytes"] == b"\x89PNG"
    assert response["text"] == "�PNG"
    assert response["json"] is None


def test_response_is_logged_without_headers_and_body(browser, stub, monkeypatch):
    info, debug = MagicMock(), MagicMock()
    monkeypatch.setattr("Browser.keywords.network.logger.info", info)
    monkeypatch.setattr("Browser.keywords.network.logger.debug", debug)
    stub.SendApiRequest.return_value = response_messages(b"secret body")
    browser.send_api_request("/api")
    logged = info.call_args.args[0]
    assert set(logged) == {"status", "statusText", "ok", "url"}
    assert "session=1" in debug.call_args.args[0]


def test_robot_rejects_a_nested_params_value():
    with pytest.raises(ValueError, match="'q' must be"):
        convert_like_robot("params", {"q": {"a": 1}})


def test_robot_keeps_dictionary_looking_data_as_text():
    assert convert_like_robot("data", '{"name": "robot"}') == '{"name": "robot"}'


def test_robot_keeps_a_dictionary_as_data():
    assert convert_like_robot("data", {"name": "robot"}) == {"name": "robot"}


def test_robot_keeps_string_params_as_text():
    assert convert_like_robot("params", "q=1&n=2") == "q=1&n=2"


@pytest.mark.parametrize("value", [5, 2.5, True])
def test_robot_keeps_a_number_or_boolean_as_data(value):
    converted = convert_like_robot("data", value)
    assert converted == value
    assert type(converted) is type(value)


@pytest.mark.parametrize(
    ("option", "value", "message"),
    [
        ("params", {"q": [1]}, "'q' must be"),
        ("form", {"q": {"a": 1}}, "'q' must be"),
        ("multipart", {"f": {"path": "a", "mimetype": "x"}}, "unknown key"),
        ("form", "{'q': 1}", "FormFields must be a dictionary"),
        ("multipart", "{'q': 1}", "MultipartFields must be a dictionary"),
    ],
)
def test_python_caller_gets_the_same_checks(browser, stub, option, value, message):
    with pytest.raises(ValueError, match=message):
        browser.send_api_request("/api", **{option: value})
    stub.SendApiRequest.assert_not_called()


@pytest.mark.parametrize(
    ("data", "message"),
    [
        ({"v": float("nan")}, "data cannot be sent as JSON: Out of range float values"),
        ({"b": b"x"}, "data cannot be sent as JSON: Object of type bytes"),
    ],
)
def test_data_that_is_not_json_fails_with_a_clear_message(browser, stub, data, message):
    with pytest.raises(ValueError, match=message):
        browser.send_api_request("/api", data=data)
    stub.SendApiRequest.assert_not_called()


def test_header_values_are_sent_as_text(browser, stub):
    request = sent(browser, stub, headers={"X-Count": 5, "X-On": True, "X-Ratio": 1.0})
    assert json.loads(request.headers) == {
        "X-Count": "5",
        "X-On": "true",
        "X-Ratio": "1",
    }


def test_a_header_value_that_is_not_text_number_or_boolean_fails(browser, stub):
    with pytest.raises(
        ValueError,
        match="Header 'X-List' must be a string, a number or a boolean, got a list",
    ):
        browser.send_api_request("/api", headers={"X-List": [1]})


def test_robot_accepts_another_mapping_as_form():
    from robot.utils import NormalizedDict

    assert convert_like_robot("form", NormalizedDict({"q": 1})) == {"q": "1"}


def test_robot_converts_the_string_none_to_no_params():
    assert convert_like_robot("params", "None") is None
