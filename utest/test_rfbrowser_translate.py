from approvaltests import verify_all

from Browser.entry.translation import (
    MISSING_CHECKSUM,
    _get_heading,
    _table_doc_updated,
    DOC_CHANGED,
    NO_LIB_KEYWORD,
    MISSING_TRANSLATION,
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
