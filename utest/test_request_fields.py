from pathlib import Path

import pytest

from Browser.utils.data_types import FormFields, MultipartFields, QueryParams


def test_form_error_names_the_kind_of_value():
    with pytest.raises(ValueError, match="got a dictionary\\.$"):
        FormFields.from_dict({"q": {"a": 1}})


def test_form_values_become_text_with_booleans_like_javascript():
    fields = FormFields.from_dict({"q": "robot", "n": 2, "x": 1.5, "all": True})
    assert fields == {"q": "robot", "n": "2", "x": "1.5", "all": "true"}
    assert type(fields) is dict


@pytest.mark.parametrize("value", [{"a": 1}, [1], None, b"raw"])
def test_form_rejects_a_value_that_is_not_text_number_or_boolean(value):
    with pytest.raises(ValueError, match="'q' must be a string, a number or a boolean"):
        FormFields.from_dict({"q": value})


def test_form_fields_are_checked_again_without_change():
    fields = FormFields.from_dict({"all": False})
    assert FormFields.from_dict(fields) == fields


def test_query_params_keep_a_string_as_given():
    assert QueryParams.from_value("q=a%20b") == "q=a%20b"


def test_query_params_from_a_dictionary_are_form_fields():
    params = QueryParams.from_value({"page": 2})
    assert params == {"page": "2"}
    assert type(params) is dict


def test_query_params_reject_a_nested_value():
    with pytest.raises(ValueError, match="'q' must be"):
        QueryParams.from_value({"q": [1]})


def test_multipart_text_values_become_text():
    assert MultipartFields.from_dict({"n": 3, "flag": True, "s": "x"}) == {
        "n": "3",
        "flag": "true",
        "s": "x",
    }


def test_multipart_file_path_becomes_a_path():
    fields = MultipartFields.from_dict({"file": {"path": "a.png", "name": "b.png"}})
    assert fields["file"] == {"path": Path("a.png"), "name": "b.png"}


def test_multipart_file_buffer_text_is_encoded_as_utf8():
    fields = MultipartFields.from_dict({"file": {"name": "n.txt", "buffer": "€"}})
    assert fields["file"]["buffer"] == "€".encode()


def test_multipart_file_rejects_an_unknown_key():
    with pytest.raises(
        ValueError, match="unknown key 'mimetype'.*path, buffer, name and mimeType"
    ):
        MultipartFields.from_dict({"file": {"path": "a.png", "mimetype": "x"}})


@pytest.mark.parametrize(
    ("file", "message"),
    [
        ({"name": "x"}, "needs either 'path' or 'buffer', not neither"),
        ({"path": "a", "buffer": b"x", "name": "x"}, "not both"),
        ({"buffer": b"x"}, "with 'buffer' needs a 'name'"),
        ({"path": 1}, "'path' must be a path"),
        ({"buffer": 1, "name": "x"}, "'buffer' must be bytes or a string"),
        ({"path": "a", "name": 1}, "'name' must be a string"),
    ],
)
def test_multipart_file_rejects_an_invalid_file(file, message):
    with pytest.raises(ValueError, match=message):
        MultipartFields.from_dict({"file": file})


def test_multipart_rejects_a_list_value():
    with pytest.raises(
        ValueError, match="'file' must be a string, a number, a boolean or a file"
    ):
        MultipartFields.from_dict({"file": [1]})


def test_multipart_fields_are_checked_again_without_change():
    fields = MultipartFields.from_dict({"file": {"path": "a"}, "n": 1})
    assert MultipartFields.from_dict(fields) == fields


@pytest.mark.parametrize(
    ("convert", "message"),
    [
        (FormFields.from_dict, "FormFields must be a dictionary, got a string"),
        (
            MultipartFields.from_dict,
            "MultipartFields must be a dictionary, got a string",
        ),
        (
            QueryParams.from_value,
            "QueryParams must be a dictionary or a string, got a list",
        ),
    ],
)
def test_a_value_of_the_wrong_kind_fails(convert, message):
    with pytest.raises(ValueError, match=message):
        convert("q=1" if "QueryParams" not in message else [1])


def test_types_are_not_dictionaries_so_python_callers_get_no_builtin_conversion():
    assert not issubclass(FormFields, dict)
    assert not issubclass(MultipartFields, dict)
