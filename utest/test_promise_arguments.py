from __future__ import annotations

from datetime import timedelta

import pytest

from Browser.keywords.promises import Promises


class _Library:
    def get_keyword_arguments(self, kw: str) -> list:
        return ["name", ("file", "${SUITE_SOURCE}"), ("idle_timeout", None)]

    def get_keyword_types(self, kw: str) -> dict:
        return {"name": str, "file": str | None, "idle_timeout": timedelta | None}


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


def test_non_string_positional_argument_is_converted():
    positional, _ = _promises().resolve_arguments("record_keyword", "K", None, 2)
    assert positional == ("K", None, timedelta(seconds=2))


def test_string_arguments_still_resolve_names():
    positional, named = _promises().resolve_arguments(
        "record_keyword", "K", "idle_timeout=1s"
    )
    assert positional == ("K",)
    assert named == {"idle_timeout": timedelta(seconds=1)}


def test_non_string_positional_after_named_fails():
    with pytest.raises(ValueError, match="follows named arguments"):
        _promises().resolve_arguments("record_keyword", "file=x.resource", None)
