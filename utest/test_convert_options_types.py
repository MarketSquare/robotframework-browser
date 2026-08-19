from datetime import timedelta

import pytest
from robot.api import TypeInfo

from Browser import Browser
from Browser.entry.__main__ import convert_options_types
from Browser.utils.data_types import RobotTypeConverter


@pytest.fixture(scope="module")
def browser() -> Browser:
    return Browser()


def test_no_options_converts_to_empty_params(browser: Browser):
    assert convert_options_types([], browser) == {}


def test_converts_values_to_the_keyword_argument_types(browser: Browser):
    params = convert_options_types(
        ["headless=True", "timeout=10 sec", "port=8282"], browser
    )

    assert params == {
        "headless": True,
        "timeout": timedelta(seconds=10),
        "port": 8282,
    }


def test_converts_a_typed_dict_option(browser: Browser):
    params = convert_options_types(["proxy={'server': 'http://localhost:1'}"], browser)

    assert params == {"proxy": {"server": "http://localhost:1"}}


def test_only_the_first_equals_sign_separates_name_from_value(browser: Browser):
    params = convert_options_types(["wsPath=chromium/1?token=abc=def"], browser)

    assert params == {"wsPath": "chromium/1?token=abc=def"}


def test_every_launch_browser_server_option_is_convertible(browser: Browser):
    keyword_types = browser.get_keyword_types("launch_browser_server")

    unconvertible = [
        name
        for name, type_ in keyword_types.items()
        if RobotTypeConverter.converter_for(type_) is None
    ]

    assert not unconvertible, f"No converter for options: {unconvertible}"


def test_option_without_equals_sign_raises_runtime_error(browser: Browser):
    with pytest.raises(
        RuntimeError,
        match=r"Invalid option headless\. Options must be in the form of argument_name=value",
    ):
        convert_options_types(["headless"], browser)


def test_unknown_option_name_raises_runtime_error(browser: Browser):
    with pytest.raises(
        RuntimeError,
        match=r"Invalid argument name nosuchoption\. Argument names must be one of ",
    ):
        convert_options_types(["nosuchoption=1"], browser)


def test_bad_option_value_raises_robot_frameworks_value_error(browser: Browser):
    # The two error shapes are the contract: a bad name is this command's own
    # RuntimeError naming the CLI option, a bad value is Robot Framework's
    # ValueError naming the keyword argument. See
    # docs/research/rfbrowser-cli-coverage.md section 7 before changing either.
    with pytest.raises(
        ValueError,
        match=r"Argument 'timeout' got value 'notatime' that cannot be converted to timedelta",
    ):
        convert_options_types(["timeout=notatime"], browser)


def test_unconvertible_option_type_raises_runtime_error_not_attribute_error(
    browser: Browser, monkeypatch: pytest.MonkeyPatch
):
    # No real option reaches this branch on any supported Robot Framework version,
    # so converter_for is forced to return None to drive it.
    monkeypatch.setattr(
        RobotTypeConverter, "converter_for", staticmethod(lambda *args, **kwargs: None)
    )

    with pytest.raises(RuntimeError, match=r"Invalid option timeout\."):
        convert_options_types(["timeout=10 sec"], browser)


def test_converter_accepts_a_type_info():
    converter = RobotTypeConverter.converter_for(TypeInfo.from_type(int))

    assert converter is not None
    assert converter.convert(name="port", value="8282") == 8282
