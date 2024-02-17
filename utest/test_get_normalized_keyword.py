from Browser.utils import get_normalized_keyword


def test_get_normalized_keyword():
    assert get_normalized_keyword("Tidii") == "tidii"
    assert get_normalized_keyword("TiDii") == "ti_dii"
    assert get_normalized_keyword("Tidii SomeThing") == "tidii_something"
    assert get_normalized_keyword("ThisIsKeyword") == "this_is_keyword"
