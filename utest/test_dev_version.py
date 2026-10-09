import pytest
from invoke import Exit

from tasks import _next_version


def test_lowest_open_milestone_wins():
    assert _next_version(["v20.5.0", "v20.4.0", "v21.0.0"], "20.3.0") == "20.4.0"


def test_milestone_without_the_v_prefix():
    assert _next_version(["20.4.0"], "20.3.0") == "20.4.0"


def test_titles_that_are_not_versions_are_ignored():
    titles = ["Backlog", "v20.4.0", "Nice to have someday"]
    assert _next_version(titles, "20.3.0") == "20.4.0"


def test_no_open_milestone_falls_back_to_the_next_patch():
    assert _next_version([], "20.3.0") == "20.3.1"
    assert _next_version(["Backlog"], "20.3.9") == "20.3.10"


def test_fallback_ignores_a_suffix_on_the_released_version():
    assert _next_version([], "20.3.0.dev20260809101500") == "20.3.1"


def test_unreadable_released_version_is_an_error():
    with pytest.raises(Exit):
        _next_version([], "not a version")
