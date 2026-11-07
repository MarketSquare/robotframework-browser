from unittest.mock import MagicMock

import pytest

from Browser.utils.data_types import Scope
from Browser.utils.settings_stack import scope_owner


def _make_ctx(suite_ids=None, is_test_case_running=False, current_test_id=None):
    ctx = MagicMock()
    ctx.suite_ids = suite_ids if suite_ids is not None else {}
    ctx.is_test_case_running = is_test_case_running
    ctx.current_test_id = current_test_id
    return ctx


def test_test_scope_belongs_to_the_running_test():
    ctx = _make_ctx({"s1": None}, is_test_case_running=True, current_test_id="s1-t1")
    assert scope_owner(Scope.Test, ctx) == "s1-t1"


def test_test_scope_outside_a_test_fails():
    ctx = _make_ctx({"s1": None}, is_test_case_running=False)
    with pytest.raises(ValueError, match="can not be set on suite level"):
        scope_owner(Scope.Test, ctx)


def test_suite_scope_belongs_to_the_innermost_suite_even_inside_a_test():
    ctx = _make_ctx(
        {"s1": None, "s1-s2": None}, is_test_case_running=True, current_test_id="t"
    )
    assert scope_owner(Scope.Suite, ctx) == "s1-s2"


def test_global_scope_has_no_owner():
    ctx = _make_ctx({"s1": None}, is_test_case_running=True, current_test_id="t")
    assert scope_owner(Scope.Global, ctx) is None


@pytest.mark.parametrize("scope", [Scope.Global, Scope.Suite, Scope.Test])
def test_every_scope_is_global_without_a_running_suite(scope):
    assert scope_owner(scope, _make_ctx()) is None
