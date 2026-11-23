"""The network keywords take bodies, headers and matchers by the same rules."""

from typing import get_type_hints

import pytest
from robot.api.types import Secret
from robot.running.arguments.typeinfo import TypeInfo

from Browser import Browser
from Browser.keywords.network import Network
from Browser.keywords.playwright_state import PlaywrightState
from Browser.utils.data_types import RegExp


def convert(keyword, argument: str, value):
    hint = get_type_hints(keyword)[argument]
    return TypeInfo.from_type_hint(hint).convert(
        value, custom_converters=Browser.ROBOT_LIBRARY_CONVERTERS
    )


BODIES = [
    pytest.param(Network.http, "body", id="HTTP body"),
    pytest.param(Network.send_api_request, "data", id="Send API Request data"),
    pytest.param(Network.mock_responses, "body", id="Mock Responses body"),
    pytest.param(Network.modify_responses, "body", id="Modify Responses body"),
    pytest.param(Network.modify_responses, "request_body", id="Modify request_body"),
]

HEADERS = [
    pytest.param(Network.http, "headers", id="HTTP headers"),
    pytest.param(Network.send_api_request, "headers", id="Send API Request headers"),
    pytest.param(Network.mock_responses, "headers", id="Mock Responses headers"),
    pytest.param(PlaywrightState.new_context, "extraHTTPHeaders", id="New Context"),
    pytest.param(
        PlaywrightState.new_persistent_context,
        "extraHTTPHeaders",
        id="New Persistent Context",
    ),
]

HEADER_CHANGES = [
    pytest.param(Network.modify_responses, "headers", id="Modify Responses headers"),
    pytest.param(
        Network.modify_responses, "request_headers", id="Modify request_headers"
    ),
]


@pytest.mark.parametrize(("keyword", "argument"), BODIES)
@pytest.mark.parametrize("value", [{"a": 1}, [1, 2]], ids=["dictionary", "list"])
def test_dictionary_and_list_bodies_reach_the_keyword_as_json_values(
    keyword, argument, value
):
    assert convert(keyword, argument, value) == value


@pytest.mark.parametrize(("keyword", "argument"), BODIES)
def test_text_body_stays_text(keyword, argument):
    converted = convert(keyword, argument, "plain text")
    assert converted == "plain text"
    assert type(converted) is str


@pytest.mark.parametrize(("keyword", "argument"), BODIES)
def test_bytes_and_bytearray_bodies_are_kept_as_binary(keyword, argument):
    converted = convert(keyword, argument, b"\x89\xff")
    assert converted == b"\x89\xff"
    assert type(converted) is bytes
    assert convert(keyword, argument, bytearray(b"\x89\xff")) == bytearray(b"\x89\xff")


@pytest.mark.parametrize(("keyword", "argument"), BODIES)
def test_secret_body_stays_secret(keyword, argument):
    secret = Secret("token")
    assert convert(keyword, argument, secret) is secret


@pytest.mark.parametrize(("keyword", "argument"), HEADERS + HEADER_CHANGES)
def test_header_numbers_and_booleans_are_sent_as_javascript_text(keyword, argument):
    assert convert(keyword, argument, {"N": 5, "F": 1.5, "B": True}) == {
        "N": "5",
        "F": "1.5",
        "B": "true",
    }


@pytest.mark.parametrize(("keyword", "argument"), HEADERS + HEADER_CHANGES)
def test_secret_header_value_stays_secret(keyword, argument):
    secret = Secret("token")
    assert (
        convert(keyword, argument, {"Authorization": secret})["Authorization"] is secret
    )


@pytest.mark.parametrize(("keyword", "argument"), HEADERS + HEADER_CHANGES)
def test_nested_header_value_names_the_header(keyword, argument):
    with pytest.raises(ValueError, match="Header 'X-Data' must be .*got a dictionary"):
        convert(keyword, argument, {"X-Data": {"a": 1}})


@pytest.mark.parametrize(("keyword", "argument"), HEADERS)
def test_none_header_value_fails_where_headers_are_not_changes(keyword, argument):
    with pytest.raises(ValueError, match="Header 'X-Gone' must be .*got None"):
        convert(keyword, argument, {"X-Gone": None})


@pytest.mark.parametrize(("keyword", "argument"), HEADER_CHANGES)
def test_none_header_value_is_kept_as_a_removal(keyword, argument):
    assert convert(keyword, argument, {"X-Gone": None, "X-Empty": ""}) == {
        "X-Gone": None,
        "X-Empty": "",
    }


def test_regexp_from_string_accepts_a_javascript_regexp():
    assert RegExp.from_string("/api\\/items/i") == "/api\\/items/i"


def test_regexp_from_string_rejects_a_glob():
    with pytest.raises(ValueError, match="Invalid JavaScript RegExp string"):
        RegExp.from_string("**/api/items")


@pytest.mark.parametrize(("keyword", "argument"), HEADERS + HEADER_CHANGES)
def test_headers_written_as_text_are_a_dictionary(keyword, argument):
    assert convert(keyword, argument, '{"X-Tenant": "a"}') == {"X-Tenant": "a"}
