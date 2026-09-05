import inspect
import sys
from collections import defaultdict
from datetime import timedelta
from pathlib import Path

import pytest
from assertionengine import AssertionOperator

from Browser import Browser, KeyboardModifier, MouseButton
from Browser.entry.translation import get_library_translation

SPY_PLUGIN = str(Path(__file__).parent / "KeywordArgumentSpy.py")


@pytest.fixture
def browser(tmpdir):
    Browser._output_dir = tmpdir
    return Browser()


@pytest.fixture
def spy(tmpdir):
    Browser._output_dir = tmpdir
    return Browser(plugins=SPY_PLUGIN)


def last_call(spy):
    return spy.spy_calls[-1]


def test_invalid_enum_value_raises_robot_frameworks_own_error(browser):
    with pytest.raises(
        ValueError, match="cannot be converted to MouseButton"
    ) as exc_info:
        browser.click("//button", "nope")
    assert str(exc_info.value) == (
        "Argument 'button' got value 'nope' that cannot be converted to MouseButton: "
        "MouseButton does not have member 'nope'. Available: 'left', 'middle' and 'right'"
    )


def test_enum_reaches_the_keyword_body_converted(spy):
    spy.spy_enum("middle")
    assert last_call(spy) == ("spy_enum", (MouseButton.middle,), {})


def test_enum_converts_when_passed_by_name(spy):
    spy.spy_enum(button="right")
    assert last_call(spy) == ("spy_enum", (MouseButton.right,), {})


def test_none_reaches_the_body_as_none_on_a_bare_str_hint(spy):
    spy.spy_text(None)
    assert last_call(spy) == ("spy_text", (None,), {})


def test_none_reaches_the_body_on_an_enum_parameter(spy):
    spy.spy_enum(None)
    assert last_call(spy) == ("spy_enum", (None,), {})


def test_the_string_none_is_still_converted_by_its_hint(spy):
    spy.spy_text("None")
    assert last_call(spy) == ("spy_text", ("None",), {})


def test_var_positional_arguments_convert_per_element(spy):
    spy.spy_modifiers("//button", "left", "Alt", "Shift")
    assert last_call(spy) == (
        "spy_modifiers",
        ("//button", MouseButton.left, KeyboardModifier.Alt, KeyboardModifier.Shift),
        {"delay": None},
    )


def test_var_positional_converts_between_a_defaulted_positional_and_a_keyword_only(spy):
    spy.spy_modifiers("//button", "middle", "Alt", delay="1.5s")
    assert last_call(spy) == (
        "spy_modifiers",
        ("//button", MouseButton.middle, KeyboardModifier.Alt),
        {"delay": timedelta(seconds=1.5)},
    )


def test_var_positional_converts_without_a_defaulted_positional_or_keyword_only(spy):
    spy.spy_paths("//input", "a.txt", "b.txt", "c.txt")
    assert last_call(spy) == (
        "spy_paths",
        ("//input", Path("a.txt"), Path("b.txt"), Path("c.txt")),
        {},
    )


def test_var_positional_converts_when_it_is_the_first_parameter(browser):
    with pytest.raises(
        ValueError, match="cannot be converted to Permission"
    ) as exc_info:
        browser.grant_permissions("nope")
    assert str(exc_info.value).startswith(
        "Argument 'permissions' got value 'nope' that cannot be converted to Permission:"
    )


def test_var_positional_converts_on_the_real_click_with_options(browser):
    with pytest.raises(
        ValueError, match="cannot be converted to KeyboardModifier"
    ) as exc_info:
        browser.click_with_options("//button", "left", "nope")
    assert str(exc_info.value).startswith(
        "Argument 'modifiers' got value 'nope' that cannot be converted to "
        "KeyboardModifier: KeyboardModifier does not have member 'nope'."
    )


def test_none_inside_var_positional_stays_none(spy):
    spy.spy_modifiers("//button", "left", "Alt", None)
    assert last_call(spy) == (
        "spy_modifiers",
        ("//button", MouseButton.left, KeyboardModifier.Alt, None),
        {"delay": None},
    )


def test_var_keyword_arguments_convert_per_element(spy):
    spy.spy_counts(clicks="2", taps="3")
    assert last_call(spy) == ("spy_counts", (), {"clicks": 2, "taps": 3})


def test_none_inside_var_keyword_stays_none(spy):
    spy.spy_counts(clicks="2", taps=None)
    assert last_call(spy) == ("spy_counts", (), {"clicks": 2, "taps": None})


def test_keyword_with_a_renamed_robot_name_converts(spy):
    spy.spy_renamed("middle")
    assert last_call(spy) == ("spy_renamed", (MouseButton.middle,), {})


def test_a_renamed_keyword_is_wrapped_once_not_once_per_alias(spy):
    assert spy.attributes["spy_renamed"].__wrapped__ is spy.keywords["Spy Renamed"]
    assert spy.attributes["spy_renamed"] is spy.attributes["Spy Renamed"]


def test_every_keyword_is_wrapped_once_not_once_per_alias(browser):
    distinct_entries = {id(entry) for entry in browser.attributes.values()}
    assert len(browser.attributes) > len(browser.keywords), "no aliases to test against"
    assert len(distinct_entries) == len(browser.keywords)
    assert any(
        getattr(browser.attributes[name], "__wrapped__", None) is keyword
        for name, keyword in browser.keywords.items()
    )


def test_a_type_declared_on_the_keyword_decorator_converts(spy):
    # get_keyword_types is the source of truth, so `@keyword(types=...)` works for free.
    spy.spy_declared_type("middle")
    assert last_call(spy) == ("spy_declared_type", (MouseButton.middle,), {})


def test_keywords_without_convertible_parameters_are_left_unwrapped(spy):
    assert spy.attributes["spy_untyped"] is spy.keywords["spy_untyped"]


def test_jsextension_keywords_are_callable_and_unwrapped(tmpdir):
    Browser._output_dir = tmpdir
    extension = Path(__file__).parent / "custom_locator_handler.js"
    library = Browser(jsextension=str(extension))
    # jsextension keywords are generated without type annotations, so there is nothing to
    # convert against and they must pass through untouched.
    assert library.get_keyword_types("customLocatorHandler") == {}
    assert (
        library.attributes["customLocatorHandler"]
        is library.keywords["customLocatorHandler"]
    )


def test_a_wrong_number_of_arguments_raises_pythons_own_message(browser):
    with pytest.raises(TypeError) as exc_info:
        browser.click()
    assert "click() missing 1 required positional argument: 'selector'" in str(
        exc_info.value
    )


def test_the_robot_framework_path_does_not_convert(spy):
    spy.run_keyword("spy_enum", ["middle"])
    assert last_call(spy) == ("spy_enum", ("middle",), {})


def test_the_keyword_table_holds_unwrapped_methods(browser):
    assert not hasattr(browser.keywords["click"], "__wrapped__")
    assert browser.attributes["click"].__wrapped__ is browser.keywords["click"]
    for name, keyword in browser.keywords.items():
        entry = browser.attributes[name]
        assert entry is keyword or entry.__wrapped__ is keyword


def test_signature_and_converter_are_resolved_at_wrap_time_not_per_call(
    spy, monkeypatch
):
    def explode(*args, **kwargs):
        raise AssertionError("resolved per call instead of once at wrap time")

    monkeypatch.setattr(inspect, "signature", explode)
    monkeypatch.setattr(
        "Browser.utils.data_types.RobotTypeConverter.converter_for", explode
    )
    spy.spy_enum("middle")
    assert last_call(spy) == ("spy_enum", (MouseButton.middle,), {})


def test_wrapping_preserves_what_introspection_reads(browser):
    for attribute_name, keyword_name in [
        ("click", "click"),
        ("evaluate_javascript", "Evaluate JavaScript"),
    ]:
        wrapper = browser.attributes[attribute_name]
        original = browser.keywords[keyword_name]
        assert wrapper.__name__ == original.__name__
        assert wrapper.__doc__ == original.__doc__
        assert wrapper.robot_name == original.robot_name
        assert inspect.signature(wrapper) == inspect.signature(original)


def test_wrapping_survives_a_translated_keyword_table(tmpdir):
    Browser._output_dir = tmpdir
    sys.path.append(str(Path(__file__).parent.absolute()))
    library = Browser(language="ENG")
    assert "1_click" in library.keywords, "keyword names were not translated"
    assert library.attributes["1_click"].__wrapped__ is library.keywords["1_click"]
    assert len(library.attributes) > len(library.keywords)
    distinct_entries = {id(entry) for entry in library.attributes.values()}
    assert len(distinct_entries) == len(library.keywords)
    for name, keyword in library.keywords.items():
        entry = library.attributes[name]
        assert entry is keyword or entry.__wrapped__ is keyword


def test_timedelta_converts_from_a_time_string(spy):
    spy.spy_delay("1.5s")
    assert last_call(spy) == ("spy_delay", (timedelta(seconds=1.5),), {})


def test_timedelta_converts_from_a_number(spy):
    spy.spy_delay(2)
    assert last_call(spy) == ("spy_delay", (timedelta(seconds=2),), {})


@pytest.mark.parametrize("value", ["==", "contains"])
def test_assertion_operator_converts_from_a_string(spy, value):
    spy.spy_operator(value)
    assert last_call(spy) == ("spy_operator", (AssertionOperator[value],), {})


def test_an_already_typed_value_passes_through_unchanged(spy):
    spy.spy_enum(MouseButton.middle)
    spy.spy_delay(timedelta(seconds=3))
    assert spy.spy_calls == [
        ("spy_enum", (MouseButton.middle,), {}),
        ("spy_delay", (timedelta(seconds=3),), {}),
    ]


def test_none_reaches_the_body_as_none_on_an_optional_str_hint(spy):
    spy.spy_optional_text(None)
    assert last_call(spy) == ("spy_optional_text", (None,), {})


def test_the_string_none_stays_a_string_on_an_optional_str_hint(spy):
    spy.spy_optional_text("None")
    assert last_call(spy) == ("spy_optional_text", ("None",), {})


def test_a_str_parameter_converts_an_int(spy):
    spy.spy_text(5)
    assert last_call(spy) == ("spy_text", ("5",), {})


def test_a_typed_dict_parameter_converts(spy):
    spy.spy_proxy({"server": "http://localhost:8080", "bypass": "localhost"})
    assert last_call(spy) == (
        "spy_proxy",
        ({"server": "http://localhost:8080", "bypass": "localhost"},),
        {},
    )


def test_a_dict_argument_is_not_rewritten_under_the_caller(spy):
    options = {"dir": Path("videos")}
    spy.spy_record_video(options)
    assert last_call(spy) == ("spy_record_video", ({"dir": "videos"},), {})
    assert options == {"dir": Path("videos")}


def test_a_nested_dict_argument_is_not_rewritten_under_the_caller(spy):
    options = {"dir": "videos", "size": {"width": "400", "height": "200"}}
    spy.spy_record_video(options)
    assert last_call(spy) == (
        "spy_record_video",
        ({"dir": "videos", "size": {"width": 400, "height": 200}},),
        {},
    )
    assert options == {"dir": "videos", "size": {"width": "400", "height": "200"}}


def test_a_dict_inside_a_list_is_not_rewritten_under_the_caller(spy):
    certificates = [{"origin": "https://example.com", "certPath": Path("cert.pem")}]
    spy.spy_certificates(certificates)
    assert last_call(spy) == (
        "spy_certificates",
        ([{"origin": "https://example.com", "certPath": "cert.pem"}],),
        {},
    )
    assert certificates == [
        {"origin": "https://example.com", "certPath": Path("cert.pem")}
    ]


def test_a_mapping_that_cannot_be_rebuilt_is_not_rewritten_under_the_caller(spy):
    # defaultdict(items) raises TypeError -- the first argument is the factory, not a mapping.
    options = defaultdict(str, {"dir": Path("videos")})
    spy.spy_record_video(options)
    assert last_call(spy) == ("spy_record_video", ({"dir": "videos"},), {})
    assert options == {"dir": Path("videos")}


def test_a_str_or_secret_parameter_accepts_a_plain_string(spy):
    spy.spy_secret("plain string")
    assert last_call(spy) == ("spy_secret", ("plain string",), {})


def test_fill_secret_accepts_a_plain_string(browser):
    with pytest.raises(Exception, match="Could not find active page"):
        browser.fill_secret("//input", "plain string")


def test_rfbrowser_translate_reads_the_documentation_of_unwrapped_methods(tmpdir):
    Browser._output_dir = tmpdir
    translation = get_library_translation()
    library = Browser()
    documentation = {
        keyword.__name__: inspect.getdoc(keyword)
        for keyword in library.keywords.values()
    }
    for name, entry in translation.items():
        if name in ["__init__", "__intro__"]:
            continue
        assert entry["doc"] == documentation[name], name
