import pytest

from Browser.utils import http_body
from Browser.utils.types import Secret


@pytest.mark.parametrize(
    ("value", "content", "content_type"),
    [
        ("hello", "hello", "text/plain; charset=utf-8"),
        ("", "", "text/plain; charset=utf-8"),
        (b"\x89\xff", b"\x89\xff", "application/octet-stream"),
        ({"a": [1, 2]}, '{"a":[1,2]}', "application/json"),
        (False, "false", "application/json"),
    ],
)
def test_made_up_body_gets_the_type_of_its_value(value, content, content_type):
    body = http_body.made_up(value)
    assert body.content == content
    assert body.content_type == content_type


def test_made_up_json_string_is_a_json_string():
    body = http_body.made_up(json_value='{"a": 1}')
    assert body.encoded == b'"{\\"a\\": 1}"'
    assert body.content_type == "application/json"


@pytest.mark.parametrize(
    ("name", "content_type"),
    [
        ("orders.json", "application/json"),
        ("page.html", "text/html; charset=utf-8"),
        ("payload.robotmock", "application/octet-stream"),
    ],
)
def test_made_up_file_gets_the_type_of_its_name(tmp_path, name, content_type):
    file = tmp_path / name
    file.write_bytes(b"\x00\xff")
    body = http_body.made_up(path=file)
    assert body.encoded == b"\x00\xff"
    assert body.content_type == content_type


def test_missing_file_fails(tmp_path):
    with pytest.raises(ValueError, match="is not a file"):
        http_body.made_up(path=tmp_path)


def test_no_made_up_body_is_empty_without_a_type():
    body = http_body.made_up()
    assert body.encoded == b""
    assert body.content_type is None


@pytest.mark.parametrize("value", ["<p>hi</p>", b"\x89\xff"])
def test_replacement_text_or_bytes_keeps_the_real_type(value):
    body = http_body.replacement(value)
    assert body is not None
    assert body.content == value
    assert body.content_type is None


def test_replacement_json_value_and_file_set_their_type(tmp_path):
    file = tmp_path / "orders.json"
    file.write_text("[]")
    assert http_body.replacement({"a": 1}).content_type == "application/json"
    assert http_body.replacement(json_value="x").content_type == "application/json"
    assert http_body.replacement(path=file).content_type == "application/json"


def test_no_replacement_keeps_the_real_body():
    assert http_body.replacement() is None


@pytest.mark.parametrize("rule", [http_body.made_up, http_body.replacement])
def test_more_than_one_body_fails(rule, tmp_path):
    with pytest.raises(
        ValueError, match=r"^Give at most one of body, json and path, got"
    ):
        rule("a", {"b": 1}, tmp_path)


def test_replacement_names_its_argument_in_the_json_error():
    with pytest.raises(ValueError, match=r"^request_body cannot be sent as JSON: "):
        http_body.replacement({"a": float("nan")}, name="request_body")


@pytest.mark.parametrize(
    ("value", "content_type"),
    [
        ('{"a": 1}', "application/json"),
        ("[1, 2]", "application/json"),
        ("hello", "text/plain; charset=utf-8"),
        (b"\x89\xff", None),
        ({"a": 1}, "application/json"),
    ],
)
def test_page_request_guesses_json_text_and_sends_bytes_without_a_type(
    value, content_type
):
    body = http_body.page_request(value)
    assert body is not None
    assert body.content_type == content_type


@pytest.mark.parametrize(
    ("value", "content", "content_type"),
    [
        ('{"a": 1}', '{"a": 1}', None),
        (b"\x00\xff", b"\x00\xff", None),
        (
            {"id": 9007199254740993, "x": 1.0},
            '{"id":9007199254740993,"x":1.0}',
            "application/json",
        ),
    ],
)
def test_api_request_leaves_text_and_bytes_to_playwright(value, content, content_type):
    body = http_body.api_request(value)
    assert body is not None
    assert body.content == content
    assert body.content_type == content_type


def test_api_request_json_error_says_what_to_give():
    with pytest.raises(ValueError, match="Give a string, bytes, or a dictionary"):
        http_body.api_request({"when": object()})


@pytest.mark.parametrize(
    "rule",
    [
        http_body.made_up,
        http_body.replacement,
        http_body.page_request,
        http_body.api_request,
    ],
)
def test_secret_and_bytearray_are_sent_as_their_value(rule):
    assert rule(Secret("token")).content == "token"
    assert rule(bytearray(b"\x89")).content == b"\x89"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), {1, 2}])
def test_value_that_json_cannot_hold_fails(value):
    with pytest.raises(ValueError, match=r"^json cannot be sent as JSON: "):
        http_body.made_up(json_value={"a": value})


@pytest.mark.parametrize(
    ("headers", "removed", "expected"),
    [
        ({}, (), {"Content-Type": "application/json"}),
        ({"X-A": "1"}, (), {"X-A": "1", "Content-Type": "application/json"}),
        ({"content-type": "text/csv"}, (), {"content-type": "text/csv"}),
        ({}, ("CONTENT-TYPE",), {}),
    ],
)
def test_content_type_in_headers_always_wins(headers, removed, expected):
    assert http_body.made_up({"a": 1}).headers(headers, removed) == expected


def test_body_without_a_type_leaves_headers_unchanged():
    assert http_body.replacement("x").headers({"X-A": "1"}) == {"X-A": "1"}
