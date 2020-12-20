import pytest

from Browser.utils.deprecated import _method_to_keyword, _is_deprecated_attribute


class DummyClass:
    def keyword_with_args(self, arg1, arg2):
        pass

    def keyword_with(self, arg1, *args, **kwargs):
        pass


@pytest.fixture
def keyword():
    return DummyClass().keyword_with_args


def test_method_to_keyword():
    assert _method_to_keyword("bar") == "Bar"
    assert _method_to_keyword("BAR") == "Bar"
    assert _method_to_keyword("BaR_FoO") == "Bar Foo"


def test_is_deprecated_no_deprecate(keyword):
    assert _is_deprecated_attribute(keyword, False, (DummyClass(),), ()) is False


def test_is_deprecated_no_deprecate_usage(keyword):
    assert _is_deprecated_attribute(keyword, "arg2", (DummyClass(),), ()) is False
    assert _is_deprecated_attribute(keyword, "arg2", (DummyClass(), True), ()) is False


def test_test_is_deprecated_kwargs(keyword):
    assert (
        _is_deprecated_attribute(keyword, "kw_arg2", (DummyClass(),), ("kw_arg2",))
        is True
    )
    assert _is_deprecated_attribute(keyword, "kw_arg2", (DummyClass(),), ()) is False
    assert (
        _is_deprecated_attribute(keyword, "kw_arg2", (DummyClass(),), ("kw_arg1",))
        is False
    )


def test_test_is_deprecated_args(keyword):
    assert _is_deprecated_attribute(keyword, "arg1", (DummyClass(), True), ()) is True
    assert (
        _is_deprecated_attribute(keyword, "arg2", (DummyClass(), True, True), ())
        is True
    )
