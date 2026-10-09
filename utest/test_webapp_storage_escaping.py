import json
from unittest.mock import MagicMock

import pytest

from Browser.keywords.webapp_state import WebAppState


def make_state() -> tuple[WebAppState, MagicMock]:
    library = MagicMock()
    library.scope_stack = {
        "timeout": MagicMock(get=MagicMock(return_value=10_000.0)),
        "retry_assertions_for": MagicMock(get=MagicMock(return_value=0.0)),
    }
    library._get_assertion_formatter.return_value = []

    state = WebAppState.__new__(WebAppState)
    state.library = library
    eval_js = MagicMock(return_value=MagicMock(log="", result="null"))
    state.eval_js = eval_js  # type: ignore[method-assign]
    return state, eval_js


def script_of(eval_js: MagicMock) -> str:
    """The script argument of the single recorded call."""
    eval_js.assert_called_once()
    return eval_js.call_args.args[0]


AWKWARD_KEYS = [
    pytest.param("plain", id="plain"),
    pytest.param("it's", id="single-quote"),
    pytest.param('say "hi"', id="double-quote"),
    pytest.param("back\\slash", id="backslash"),
    pytest.param("line\nbreak", id="newline"),
    pytest.param("tab\there", id="tab"),
    pytest.param("null\x00byte", id="nul"),
    pytest.param("line\u2028separator", id="u2028"),
    pytest.param("para\u2029separator", id="u2029"),
    pytest.param("rtl\u202eoverride", id="bidi-override"),
    pytest.param("emoji\U0001f600", id="astral-printable"),
    # The class repr() gets wrong: astral and non-printable.
    pytest.param("tag\U000e0001char", id="astral-tag"),
    pytest.param("private\U000f0000use", id="astral-private-use"),
    # The class bare interpolation gets wrong: it closes the literal and runs.
    pytest.param('x"), (evil = 1), S.getItem("y', id="injection"),
]

GETTERS = [
    pytest.param("local_storage_get_item", "localStorage", "getItem", id="local-get"),
    pytest.param(
        "session_storage_get_item", "sessionStorage", "getItem", id="session-get"
    ),
]

REMOVERS = [
    pytest.param(
        "local_storage_remove_item", "localStorage", "removeItem", id="local-remove"
    ),
    pytest.param(
        "session_storage_remove_item",
        "sessionStorage",
        "removeItem",
        id="session-remove",
    ),
]

SETTERS = [
    pytest.param("local_storage_set_item", "localStorage", id="local-set"),
    pytest.param("session_storage_set_item", "sessionStorage", id="session-set"),
]


@pytest.mark.parametrize("key", AWKWARD_KEYS)
@pytest.mark.parametrize(("method", "store", "op"), GETTERS + REMOVERS)
def test_key_is_escaped(method: str, store: str, op: str, key: str) -> None:
    state, eval_js = make_state()
    getattr(state, method)(key)
    assert script_of(eval_js) == f"window.{store}.{op}({json.dumps(key)})"


@pytest.mark.parametrize("key", AWKWARD_KEYS)
@pytest.mark.parametrize(("method", "store"), SETTERS)
def test_key_and_value_are_escaped(method: str, store: str, key: str) -> None:
    value = 'v"\\\n\U000f0000'
    state, eval_js = make_state()
    getattr(state, method)(key, value)
    expected = f"window.{store}.setItem({json.dumps(key)}, {json.dumps(value)})"
    assert script_of(eval_js) == expected


@pytest.mark.parametrize("key", AWKWARD_KEYS)
@pytest.mark.parametrize(("method", "store", "op"), GETTERS + REMOVERS)
def test_script_carries_no_escape_javascript_misreads(
    method: str, store: str, op: str, key: str
) -> None:
    "`\\U` is an identity escape in JavaScript -- the backslash is dropped."
    state, eval_js = make_state()
    getattr(state, method)(key)
    assert "\\U" not in script_of(eval_js)


@pytest.mark.parametrize("key", AWKWARD_KEYS)
def test_script_is_ascii(key: str) -> None:
    """Pure ASCII, so U+2028/U+2029 cannot reach the page as raw characters.

    They are legal in JSON but were illegal inside a JavaScript string literal
    before ES2019, and the script also has to survive a protobuf hop.
    """
    state, eval_js = make_state()
    state.local_storage_get_item(key)
    script_of(eval_js).encode("ascii")


@pytest.mark.parametrize("key", AWKWARD_KEYS)
def test_the_embedded_literal_parses_back_to_the_key(key: str) -> None:
    state, eval_js = make_state()
    state.local_storage_get_item(key)
    literal = (
        script_of(eval_js)
        .removeprefix("window.localStorage.getItem(")
        .removesuffix(")")
    )
    assert json.loads(literal) == key


def test_repr_would_not_pass_these_tests() -> None:
    """Pins why the keywords do not use `repr()`, which is the obvious choice."""
    key = "tag\U000e0001char"
    assert "\\U" in repr(key)
    assert "\\U" not in json.dumps(key)
    assert json.loads(json.dumps(key)) == key
