from __future__ import annotations

from Browser.keywords.promises import Promises


class _Library:
    def get_keyword_arguments(self, kw: str) -> list:
        return ["name", ("file", "${SUITE_SOURCE}"), ("idle_timeout", None)]

    def get_keyword_types(self, kw: str) -> dict:
        return {}


def _promises() -> Promises:
    promises = Promises.__new__(Promises)
    promises.library = _Library()
    return promises


def test_non_string_positional_argument_is_passed_through():
    positional, named = _promises().resolve_arguments(
        "record_keyword", "Logged Only", None
    )
    assert positional == ("Logged Only", None)
    assert named == {}


def test_string_arguments_still_resolve_names():
    positional, named = _promises().resolve_arguments(
        "record_keyword", "K", "idle_timeout=1s"
    )
    assert positional == ("K",)
    assert named == {"idle_timeout": "1s"}
