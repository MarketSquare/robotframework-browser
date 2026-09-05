import hashlib

from approvaltests import verify_all

from Browser.entry.translation import (
    DOC_CHANGED,
    MISSING_CHECKSUM,
    MISSING_TRANSLATION,
    NO_LIB_KEYWORD,
    _get_heading,
    _table_doc_updated,
    _translation_entry,
)


def test_heading():
    verify_all("header", [*_get_heading(42), *_get_heading(6)])


def test_body_line():
    verify_all(
        "body",
        [
            _table_doc_updated("new_page", 42, MISSING_TRANSLATION),
            _table_doc_updated(
                "this_is_long_keyword_which_is_42_chars_len", 42, MISSING_TRANSLATION
            ),
            _table_doc_updated("close", 42, DOC_CHANGED),
            _table_doc_updated("new_page", 8, MISSING_TRANSLATION),
            _table_doc_updated("click", 8, NO_LIB_KEYWORD),
            _table_doc_updated("click", 8, DOC_CHANGED),
        ],
    )


def test_full_long_kw_table():
    lines = _get_heading(42)
    lines.append(_table_doc_updated("new_page", 42, MISSING_CHECKSUM))
    lines.append(
        _table_doc_updated(
            "this_is_long_keyword_which_is_42_chars_len", 42, MISSING_TRANSLATION
        )
    )
    lines.append(_table_doc_updated("close", 42, DOC_CHANGED))
    verify_all("all with long kw name", lines)


# Docstring as it reaches the entry builder on Python <= 3.12 and on >= 3.13.
# Python 3.13 strips the leading indentation at compile time, see issue #5219.
INDENTED_DOC = "First line.\n\n        Indented body line.\n    "
DEDENTED_DOC = "First line.\n\nIndented body line.\n"


def test_translation_entry_dedents_documentation():
    assert (
        _translation_entry("kw", INDENTED_DOC)["doc"]
        == "First line.\n\nIndented body line."
    )


def test_translation_entry_checksum_does_not_depend_on_python_version():
    indented = _translation_entry("kw", INDENTED_DOC)
    dedented = _translation_entry("kw", DEDENTED_DOC)
    assert indented["sha256"] == dedented["sha256"]
    assert indented["doc"] == dedented["doc"]


def test_translation_entry_handles_missing_documentation():
    assert _translation_entry("kw", None) == {
        "name": "kw",
        "doc": "",
        "sha256": hashlib.sha256(b"\xff\xfe").hexdigest(),
    }
