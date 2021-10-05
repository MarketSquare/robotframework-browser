from utils import get_normalized_keyword


def test_get_normalized_keyword():
    assert get_normalized_keyword("TiDii") == "tidii"
    assert get_normalized_keyword("TiDii something") == "tidii_something"
