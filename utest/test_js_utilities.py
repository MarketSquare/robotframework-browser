import pytest

from Browser.utils import get_abs_scroll_coordinates, get_rel_scroll_coordinates


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        (120, 120),
        ("120", 120),
        ("top", 0),
        ("BOTTOM", 800),
        ("50%", 400),
        ("12.5%", 100),
    ],
)
def test_absolute_scroll_coordinates(query, expected):
    assert get_abs_scroll_coordinates(query, 800, "top", "bottom") == expected


@pytest.mark.parametrize("query", ["1_5%", "1,5%", "50%\n", "-50%", "%", "middle"])
def test_absolute_scroll_coordinates_reject_other_strings(query):
    with pytest.raises(ValueError, match="percentage"):
        get_abs_scroll_coordinates(query, 800, "top", "bottom")


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        (-30, -30),
        ("height", 300),
        ("-Height", -300),
        ("+height", 300),
        ("25%", 200),
        ("-25%", -200),
        ("+12.5%", 100),
    ],
)
def test_relative_scroll_coordinates(query, expected):
    assert get_rel_scroll_coordinates(query, 800, 300, "height") == expected


@pytest.mark.parametrize("query", ["1_5%", "-1,5%", "25%\n", "--25%", "%", "width"])
def test_relative_scroll_coordinates_reject_other_strings(query):
    with pytest.raises(ValueError, match="percentage"):
        get_rel_scroll_coordinates(query, 800, 300, "height")
