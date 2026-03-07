from unittest.mock import MagicMock

import pytest

from Browser.utils.data_types import Scope
from Browser.utils.settings_stack import SettingsStack


def _make_ctx(suite_ids=None, is_test_case_running=False, current_test_id=None):
    ctx = MagicMock()
    ctx.suite_ids = suite_ids if suite_ids is not None else {}
    ctx.is_test_case_running = is_test_case_running
    ctx.current_test_id = current_test_id
    return ctx


def test_init_stores_global_setting():
    stack = SettingsStack("initial", _make_ctx())
    assert stack.get() == "initial"


def test_init_without_setter():
    stack = SettingsStack(42, _make_ctx())
    assert stack.setter_function is None


def test_start_inherits_current_value():
    stack = SettingsStack("global", _make_ctx())
    stack.start("suite-1", Scope.Suite)
    assert stack.get() == "global"


def test_start_multiple_frames_last_wins():
    stack = SettingsStack("global", _make_ctx())
    stack.start("suite-1", Scope.Suite)
    stack.start("test-1", Scope.Test)
    assert stack.get() == "global"


def test_end_removes_frame_and_returns_to_parent():
    stack = SettingsStack("global", _make_ctx())
    stack.start("suite-1", Scope.Suite)
    stack.start("test-1", Scope.Test)
    stack.end("test-1")
    assert stack.get() == "global"


def test_end_calls_setter_when_value_changed():
    setter = MagicMock()
    stack = SettingsStack("global", _make_ctx(), setter_function=setter)
    stack.start("suite-1", Scope.Suite)
    stack._stack["suite-1"].setting = "suite-value"
    stack.start("test-1", Scope.Test)
    stack.end("test-1")
    setter.assert_called_once_with("suite-value")


def test_end_calls_setter_when_scope_type_changes_even_if_value_same():
    setter = MagicMock()
    stack = SettingsStack("global", _make_ctx(), setter_function=setter)
    stack.start("suite-1", Scope.Suite)
    stack.start("test-1", Scope.Test)
    stack.end("test-1")
    setter.assert_called_once_with("global")


def test_end_does_not_call_setter_when_no_setter_function():
    stack = SettingsStack("global", _make_ctx(), setter_function=None)
    stack.start("suite-1", Scope.Suite)
    stack._stack["suite-1"].setting = "suite-value"
    stack.start("test-1", Scope.Test)
    stack.end("test-1")  # no setter_function — should not raise


def test_end_unknown_id_is_noop():
    stack = SettingsStack("global", _make_ctx())
    stack.start("suite-1", Scope.Suite)
    stack.end("nonexistent")  # should not raise
    assert stack.get() == "global"


def test_set_global_overwrites_all_frames():
    ctx = _make_ctx(suite_ids={"s1": None})
    stack = SettingsStack("global", ctx)
    stack.start("s1", Scope.Suite)
    stack.start("t1", Scope.Test)
    stack.set("new-global", Scope.Global)
    assert stack.get() == "new-global"
    stack.end("t1")
    stack.end("s1")
    assert stack.get() == "new-global"


def test_set_global_calls_setter():
    setter = MagicMock()
    stack = SettingsStack("original", _make_ctx(), setter_function=setter)
    stack.set("changed", Scope.Global)
    setter.assert_called_once_with("changed")


def test_set_global_does_not_call_setter_when_unchanged():
    setter = MagicMock()
    stack = SettingsStack("same", _make_ctx(), setter_function=setter)
    stack.set("same", Scope.Global)
    setter.assert_not_called()


def test_set_falls_back_to_global_when_no_suite_ids():
    ctx = _make_ctx(suite_ids={})
    stack = SettingsStack("initial", ctx)
    stack.set("forced-global", Scope.Suite)  # should be treated as Global
    assert stack.get() == "forced-global"


def test_set_suite_inserts_suite_frame():
    ctx = _make_ctx(suite_ids={"s1": None})
    stack = SettingsStack("global", ctx)
    stack.start("s1", Scope.Suite)
    stack.set("suite-val", Scope.Suite)
    assert stack.get() == "suite-val"


def test_set_suite_pops_test_frame_first():
    ctx = _make_ctx(
        suite_ids={"s1": None}, is_test_case_running=True, current_test_id="t1"
    )
    stack = SettingsStack("global", ctx)
    stack.start("s1", Scope.Suite)
    stack.start("t1", Scope.Test)
    assert stack._last_setting.typ == Scope.Test
    stack.set("suite-val", Scope.Suite)
    assert stack._last_setting.typ == Scope.Suite
    assert stack.get() == "suite-val"


def test_set_none_scope_treated_as_suite():
    ctx = _make_ctx(suite_ids={"s1": None})
    stack = SettingsStack("global", ctx)
    stack.start("s1", Scope.Suite)
    stack.set("suite-via-none", scope=None)
    assert stack.get() == "suite-via-none"
    assert stack._last_setting.typ == Scope.Suite


def test_set_test_inserts_test_frame():
    ctx = _make_ctx(
        suite_ids={"s1": None}, is_test_case_running=True, current_test_id="t1"
    )
    stack = SettingsStack("global", ctx)
    stack.start("s1", Scope.Suite)
    stack.start("t1", Scope.Test)
    stack.set("test-val", Scope.Test)
    assert stack.get() == "test-val"
    assert stack._last_setting.typ == Scope.Test


def test_set_test_raises_when_not_in_test():
    ctx = _make_ctx(suite_ids={"s1": None}, is_test_case_running=False)
    stack = SettingsStack("global", ctx)
    stack.start("s1", Scope.Suite)
    with pytest.raises(ValueError):
        stack.set("test-val", Scope.Test)


def test_set_returns_original_value():
    ctx = _make_ctx(suite_ids={"s1": None})
    stack = SettingsStack("original", ctx)
    original = stack.set("new-value", Scope.Global)
    assert original == "original"


def test_get_returns_innermost_value():
    ctx = _make_ctx(
        suite_ids={"s1": None}, is_test_case_running=True, current_test_id="t1"
    )
    stack = SettingsStack("global", ctx)
    stack.start("s1", Scope.Suite)
    stack._stack["s1"].setting = "suite"
    stack.start("t1", Scope.Test)
    stack._stack["t1"].setting = "test"
    assert stack.get() == "test"
