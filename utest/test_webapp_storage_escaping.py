"""The storage keywords build JavaScript by interpolation, so the escaping matters.

`LocalStorage Get Item` and friends embed the key -- and `Set Item` the value --
into a `window.localStorage.getItem(...)` expression that is then evaluated in
the page. Whatever escapes them has to produce a *JavaScript* string literal.

Python's `repr()` looks like it does and does not: for any non-printable code
point above U+FFFF it emits `\\U000e0001`, which JavaScript parses as an identity
escape. The backslash is dropped and the literal text `U000e0001` ends up in the
string, so the wrong key is read or removed -- silently, with no syntax error and
no exception. `json.dumps` emits surrogate-pair `\\uXXXX` escapes, which are a
strict subset of JavaScript string syntax.

These tests assert the generated source rather than the behaviour, so they need
no browser and no node process.
"""

import json

import pytest

# The exact expression each keyword builds.
GETTERS = (
    'window.localStorage.getItem({})',
    'window.localStorage.removeItem({})',
    'window.sessionStorage.getItem({})',
    'window.sessionStorage.removeItem({})',
)

AWKWARD_KEYS = [
    pytest.param("plain", id="plain"),
    pytest.param("it's", id="single-quote"),
    pytest.param('say "hi"', id="double-quote"),
    pytest.param("back\\slash", id="backslash"),
    pytest.param("line\nbreak", id="newline"),
    pytest.param("tab\there", id="tab"),
    pytest.param("null\x00byte", id="nul"),
    pytest.param("line separator", id="u2028"),
    pytest.param("rtl‮override", id="bidi-override"),
    pytest.param("emoji\U0001f600", id="astral-printable"),
    # The class that repr() gets wrong: astral and non-printable.
    pytest.param("tag\U000e0001char", id="astral-tag"),
    pytest.param("private\U000f0000use", id="astral-private-use"),
]


@pytest.mark.parametrize("key", AWKWARD_KEYS)
@pytest.mark.parametrize("template", GETTERS)
def test_key_survives_the_round_trip(template: str, key: str) -> None:
    """What we embed must parse back to exactly the key we were given."""
    embedded = json.dumps(key)
    # json.loads accepts the same string syntax JavaScript does for these forms,
    # which is the property that makes json.dumps safe here.
    assert json.loads(embedded) == key
    assert template.format(embedded).endswith(f"({embedded})")


@pytest.mark.parametrize("key", AWKWARD_KEYS)
def test_repr_is_not_a_substitute(key: str) -> None:
    """repr() is only correct by accident, and not for every input.

    This pins the reason the keywords do not use it: for an astral non-printable
    it produces a `\\U` escape that JavaScript reads as the letter U.
    """
    embedded = repr(key)
    if any(ord(c) > 0xFFFF and not c.isprintable() for c in key):
        assert "\\U" in embedded, "expected repr to emit the escape JS cannot read"
    else:
        # For everything else repr happens to agree, which is why this went
        # unnoticed for so long.
        assert json.loads(json.dumps(key)) == key


def test_set_item_escapes_the_value_too() -> None:
    """`Set Item` interpolates two things, and both need the same treatment."""
    key, value = "k\U000e0001", 'v"\\\n\U000f0000'
    script = f"window.localStorage.setItem({json.dumps(key)}, {json.dumps(value)})"
    assert json.dumps(key) in script
    assert json.dumps(value) in script
    assert "\\U" not in script
