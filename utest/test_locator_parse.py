from __future__ import annotations
import pytest

from Browser.locators import LocatorParse


@pytest.fixture
def parse():
    return LocatorParse()


def test_parse_css_locator(parse: LocatorParse):
    assert parse.parse_locator("div") == "css=div"
    assert parse.parse_locator("css:div") == "css=div"
    assert parse.parse_locator("css  :  div") == "css=div"
    assert parse.parse_locator("css:light  :  div") == "css:light=div"


def test_parse_xpath(parse: LocatorParse):
    assert parse.parse_locator("//div") == "xpath=//div"
    assert parse.parse_locator("(//div)[0]") == "xpath=(//div)[0]"
    assert parse.parse_locator("xpath://div") == "xpath=//div"
    assert (
        parse.parse_locator('//div[text="some:text"]')
        == 'xpath=//div[text="some:text"]'
    )


def test_parse_text(parse: LocatorParse):
    assert parse.parse_locator('text:"foobar"') == 'text="foobar"'
    assert parse.parse_locator(r"text:/^\\s*Login$/i") == r"text=/^\\s*Login$/i"


def test_parse_id(parse: LocatorParse):
    assert parse.parse_locator("id:password") == "id=password"


def test_strategy_index(parse: LocatorParse):
    assert parse._strategy_index("id:password") == 2
    assert parse._strategy_index("password") == -1
    assert parse._strategy_index("css:light:div") == 9


def test_chained_locators(parse: LocatorParse):
    result = parse.parse_locator("xpath://html/body/div >> css:span")
    assert result == "xpath=//html/body/div >> css=span"
    result = parse.parse_locator('xpath://div[@text=" >> "]')
    assert result == 'xpath=//div[@text=" >> "]'
    result = parse.parse_locator('xpath://div[@text=">>"] >> xpath://div[@text=">>"]')
    assert result == 'xpath=//div[@text=">>"] >> xpath=//div[@text=">>"]'
    result = parse.parse_locator("xpath://html/body/div>>css:span")
    assert result == "xpath=//html/body/div>>css:span"


def test_split_locator(parse: LocatorParse):
    assert parse._split_locator("css:span") == ["css:span"]
    assert parse._split_locator("xpath://html/body/div >> css:span") == [
        "xpath://html/body/div",
        " >> ",
        "css:span",
    ]
    assert parse._split_locator('xpath://div[@text=" >> "]') == [
        'xpath://div[@text=" >> "]'
    ]
    assert parse._split_locator('text:" >> " >> text: " >> "') == [
        'text:" >> "',
        " >> ",
        'text: " >> "',
    ]
