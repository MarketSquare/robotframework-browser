from unittest.mock import patch

import pytest
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

from Browser.browser import Browser


class MyLib(Browser):
    """A user library built by subclassing Browser, imported under its own name."""


@pytest.fixture
def browser():
    return Browser()


def _imported(mapping):
    return patch.object(BuiltIn, "get_library_instance", return_value=mapping)


def test_own_name_is_recognised(browser: Browser):
    with _imported({"Browser": browser}):
        assert browser._is_own_keyword("Browser") is True


def test_alias_is_recognised(browser: Browser):
    with _imported({"PW": browser}):
        assert browser._is_own_keyword("PW") is True


def test_name_not_imported_is_not_own(browser: Browser):
    with _imported({"PW": browser}):
        assert browser._is_own_keyword("Browser") is False


def test_another_library_is_not_own(browser: Browser):
    with _imported({"Browser": browser, "Collections": object()}):
        assert browser._is_own_keyword("Collections") is False


def test_subclass_recognises_its_own_name(browser: Browser):
    my_lib = MyLib()
    with _imported({"Browser": browser, "MyLib": my_lib}):
        assert my_lib._is_own_keyword("MyLib") is True


def test_instances_do_not_claim_each_others_keywords(browser: Browser):
    """Both instances are registered as listeners and both see every keyword."""
    my_lib = MyLib()
    imported = {"Browser": browser, "MyLib": my_lib}
    with _imported(imported):
        assert browser._is_own_keyword("MyLib") is False
        assert my_lib._is_own_keyword("Browser") is False


def test_lookup_is_cached(browser: Browser):
    with _imported({"Browser": browser}) as get_instance:
        assert browser._is_own_keyword("Browser") is True
        assert browser._is_own_keyword("Browser") is True
    assert get_instance.call_count == 1


def test_negative_lookup_is_cached(browser: Browser):
    with _imported({"Browser": browser}) as get_instance:
        assert browser._is_own_keyword("Collections") is False
        assert browser._is_own_keyword("Collections") is False
    assert get_instance.call_count == 1


def test_cache_is_cleared_between_suites(browser: Browser):
    with _imported({"PW": browser}):
        assert browser._is_own_keyword("PW") is True
    browser._own_libname_cache.clear()
    with _imported({"PW": object()}):
        assert browser._is_own_keyword("PW") is False


def test_outside_a_robot_run_nothing_is_own(browser: Browser):
    with patch.object(
        BuiltIn, "get_library_instance", side_effect=RobotNotRunningError
    ):
        assert browser._is_own_keyword("Browser") is False
    assert browser._own_libname_cache == {}


def _run_listener_hooks(library, imported, libname, kwname="Fill Secret"):
    """Drive the two listener hooks and report what they decided to do."""
    attrs = {
        "args": [],
        "source": None,
        "lineno": 1,
        "type": "KEYWORD",
        "status": "PASS",
        "libname": libname,
        "kwname": kwname,
    }
    shown: list = []
    logging_calls: list = []
    with (
        patch.object(BuiltIn, "get_library_instance", return_value=imported),
        patch.object(
            Browser, "_show_keyword_call", lambda self, a: shown.append(a["libname"])
        ),
        patch.object(Browser, "_set_logging", lambda self, s: logging_calls.append(s)),
    ):
        library._start_keyword(kwname, attrs)
        library._end_keyword(kwname, attrs)
    return shown, logging_calls


def test_listener_hooks_act_on_the_plain_import():
    browser = Browser(show_keyword_call_banner=True)
    shown, logging_calls = _run_listener_hooks(browser, {"Browser": browser}, "Browser")
    assert shown == ["Browser"]
    assert logging_calls == [False, True]


def test_listener_hooks_act_on_an_aliased_import():
    browser = Browser(show_keyword_call_banner=True)
    shown, logging_calls = _run_listener_hooks(browser, {"PW": browser}, "PW")
    assert shown == ["PW"]
    assert logging_calls == [False, True]


def test_listener_hooks_act_on_a_subclassed_import(browser: Browser):
    my_lib = MyLib(show_keyword_call_banner=True)
    shown, logging_calls = _run_listener_hooks(
        my_lib, {"Browser": browser, "MyLib": my_lib}, "MyLib"
    )
    assert shown == ["MyLib"]
    assert logging_calls == [False, True]


def test_listener_hooks_ignore_another_librarys_keyword():
    browser = Browser(show_keyword_call_banner=True)
    shown, logging_calls = _run_listener_hooks(
        browser, {"Browser": browser, "Collections": object()}, "Collections"
    )
    assert shown == []
    assert logging_calls == []
