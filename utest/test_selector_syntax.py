import pytest

from Browser.utils.selector_syntax import crosses_frames, split_selector


@pytest.mark.parametrize(
    ("selector", "clauses", "separators"),
    [
        ("css=a", ["css=a"], []),
        ("a >>> b", ["a ", " b"], [">>>"]),
        ("a>>b>>>c", ["a", "b", ">c"], [">>", ">>"]),
        (">>> b", ["", " b"], [">>>"]),
        ('text="a >>> b"', ['text="a >>> b"'], []),
        ("text=it's >>> b", ["text=it's ", " b"], [">>>"]),
        ("label=Customer's name >>> b", ["label=Customer's name ", " b"], [">>>"]),
        ('text="say \\" >>> no" >>> c', ['text="say \\" >>> no" ', " c"], [">>>"]),
    ],
)
def test_split_selector_follows_the_node_splitter(selector, clauses, separators):
    assert split_selector(selector) == (clauses, separators)


@pytest.mark.parametrize(
    ("selector", "frames"),
    [
        ("id=f >>> id=b", True),
        (">>> id=b", True),
        ("internal:control=any-frame >> id=cc", True),
        ("id=f >> internal:control=enter-frame >> id=b", True),
        ('text="Save >>> later"', False),
        ("div>>>span", False),
        ("css=button", False),
    ],
)
def test_crosses_frames(selector, frames):
    assert crosses_frames(selector) is frames
