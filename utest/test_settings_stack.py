from unittest.mock import Mock

import pytest

from Browser.utils import SettingsStack, Scope


def test_scope_test():
    ctx = Mock()
    stack = SettingsStack("", ctx)
    assert stack.get() == ""

    stack.set("foobar", Scope.Test)
    assert stack.get() == "foobar"
    assert stack.get() == "foobar"


def test_scope_global():
    ctx = Mock()
    stack = SettingsStack("", ctx)
    assert stack.set("kala", Scope.Global) == ""
    assert stack.get() == "kala"


def test_scope_suite():
    ctx = Mock()
    stack = SettingsStack("", ctx)
    assert stack.set("kala", Scope.Global) == ""
    assert stack.set("tidii", Scope.Suite) == "kala"
    assert stack.set("foobar", Scope.Test) == "tidii"
    assert stack.get() == "foobar"


def test_scope_suite_oder():
    ctx = Mock()
    stack = SettingsStack("", ctx)
    assert stack.set("kala", Scope.Global) == ""
    assert stack.set("foobar", Scope.Test) == "kala"

    with pytest.raises(IndexError):
        stack.set("tidii", Scope.Suite)


def test_start():
    ctx = Mock()
    stack = SettingsStack("", ctx)
    stack.set("tidii", Scope.Suite)
    stack.start("id1", Scope.Suite)
    assert stack.get() == "tidii"
    stack.end("id1")
    assert stack.get() == "tidii"
