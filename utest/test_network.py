from pathlib import Path

import pytest

from Browser.keywords.network import (
    Network,
    _add_http_response_views,
    _get_headers,
)
from Browser.keywords.network import _multipart_field as _proto_multipart_field
from Browser.utils.data_types import MultipartFields
from utest.robot_conversion import convert_like_robot as _convert


def convert_like_robot(argument: str, value):
    return _convert(Network.http, argument, value)


def _multipart_field(name: str, value):
    checked = MultipartFields.from_dict({name: value})
    return _proto_multipart_field(name, checked[name])


def http_response(headers: str, body: bytes) -> dict:
    response = {"headers": headers}
    _add_http_response_views(response, body)
    return response


def test_legacy_body_is_parsed_with_lowercase_json_content_type():
    response = http_response(
        '{"content-type": "application/json"}', b'{"key":"value1"}'
    )
    assert response["body"]["key"] == "value1"


def test_legacy_body_is_parsed_with_capitalized_json_content_type():
    response = http_response(
        '{"Content-Type": "application/json"}', b'{"key":"value2"}'
    )
    assert response["body"]["key"] == "value2"
    assert response["headers"]["Content-Type"] == "application/json"


def test_legacy_body_stays_text_without_json_content_type():
    response = http_response('{"content-type": "text/plain"}', b'{"key":"value3"}')
    assert response["body"] == '{"key":"value3"}'
    assert response["json"] == {"key": "value3"}


def test_legacy_body_stays_text_when_json_is_invalid():
    response = http_response('{"content-type": "application/json"}', b"{invalid: json}")
    assert response["body"] == "{invalid: json}"
    assert response["json"] is None


def test_legacy_body_is_text_without_headers():
    response = http_response("{}", b'{"key":"value1"}')
    assert response["body"] == '{"key":"value1"}'
    assert response["headers"] == {}


def test_empty_body_gives_empty_views():
    response = http_response('{"content-type": "application/json"}', b"")
    assert response["body"] == ""
    assert response["bytes"] == b""
    assert response["text"] == ""
    assert response["json"] is None


def test_legacy_body_parses_json_list():
    response = http_response(
        '{"content-type": "application/json"}', b'[{"key":"value1"}, {"key":"value2"}]'
    )
    assert response["body"] == [{"key": "value1"}, {"key": "value2"}]


def test_nan_body_stays_text_and_is_not_json():
    response = http_response('{"content-type": "application/json"}', b"NaN")
    assert response["body"] == "NaN"
    assert response["json"] is None


def test_binary_body_is_kept_raw_and_text_uses_replacement_characters():
    raw = bytes.fromhex("89504e470d0a1a0a")
    response = http_response('{"content-type": "image/png"}', raw)
    assert response["bytes"] == raw
    assert response["text"] == raw.decode("utf-8", "replace")


def test_multipart_value_is_sent_as_text():
    field = _multipart_field("count", 3)
    assert (field.name, field.value) == ("count", "3")


def test_multipart_bool_is_sent_like_javascript():
    assert _multipart_field("flag", True).value == "true"


def test_multipart_file_from_path_takes_name_and_type_from_the_file(tmp_path):
    path = tmp_path / "avatar.png"
    path.write_bytes(b"png")
    field = _multipart_field("file", {"path": str(path)})
    assert field.path == str(path.resolve())
    assert field.fileName == "avatar.png"
    assert field.mimeType == "image/png"


def test_multipart_file_from_path_keeps_given_name_and_type(tmp_path):
    path = tmp_path / "data.bin"
    path.write_bytes(b"x")
    field = _multipart_field(
        "file", {"path": str(path), "name": "report.csv", "mimeType": "text/csv"}
    )
    assert (field.fileName, field.mimeType) == ("report.csv", "text/csv")


def test_multipart_file_from_buffer_encodes_text_as_utf8():
    field = _multipart_field("file", {"name": "notes.txt", "buffer": "häkä"})
    assert field.buffer == "häkä".encode()
    assert field.mimeType == "application/octet-stream"


def test_multipart_file_needs_path_or_buffer():
    with pytest.raises(
        ValueError, match="needs either 'path' or 'buffer', not neither"
    ):
        _multipart_field("file", {"name": "x.txt"})


def test_multipart_file_cannot_have_both_path_and_buffer(tmp_path):
    with pytest.raises(ValueError, match="not both"):
        _multipart_field("file", {"path": str(tmp_path), "buffer": b"x", "name": "x"})


def test_multipart_file_from_buffer_needs_a_name():
    with pytest.raises(ValueError, match="with 'buffer' needs a 'name'"):
        _multipart_field("file", {"buffer": b"x"})


def test_multipart_file_from_missing_path_fails(tmp_path):
    with pytest.raises(FileNotFoundError, match="no file at"):
        _multipart_field("file", {"path": str(tmp_path / "missing.png")})


def test_robot_converts_a_multipart_file_dictionary_with_path_to_path():
    converted = convert_like_robot("multipart", {"file": {"path": "avatar.png"}})
    assert converted["file"] == {"path": Path("avatar.png")}


def test_robot_encodes_a_text_buffer_of_a_multipart_file_as_utf8():
    converted = convert_like_robot(
        "multipart", {"file": {"name": "notes.txt", "buffer": "häkä €"}}
    )
    assert converted["file"]["buffer"] == "häkä €".encode()


def test_robot_keeps_a_multipart_text_that_looks_like_a_dictionary_as_text():
    converted = convert_like_robot("multipart", {"note": "{'path': 'a.png'}"})
    assert converted["note"] == "{'path': 'a.png'}"


def test_robot_rejects_a_multipart_file_with_an_unknown_key():
    with pytest.raises(ValueError, match="unknown key 'mimetype'"):
        convert_like_robot(
            "multipart", {"file": {"path": "a.png", "mimetype": "image/png"}}
        )


def test_robot_rejects_a_string_as_multipart():
    with pytest.raises(ValueError, match="cannot be converted to MultipartFields"):
        convert_like_robot("multipart", "{'file': {'path': 'a.png'}}")


def test_robot_rejects_a_nested_form_value():
    with pytest.raises(ValueError, match="'q' must be a string, a number or a boolean"):
        convert_like_robot("form", {"q": {"a": 1}})


def test_multipart_file_from_path_object(tmp_path):
    path = tmp_path / "avatar.png"
    path.write_bytes(b"png")
    field = _multipart_field("file", {"path": path})
    assert (field.path, field.fileName) == (str(path.resolve()), "avatar.png")


def test_json_content_type_is_added_for_a_json_body():
    assert _get_headers('{"a": 1}', {}) == {"Content-Type": "application/json"}


def test_own_content_type_in_any_case_is_kept_for_a_json_body():
    headers = {"content-type": "text/plain"}
    assert _get_headers('{"a": 1}', headers) == headers
