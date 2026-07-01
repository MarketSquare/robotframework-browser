from unittest.mock import MagicMock

from Browser.keywords import Getters


class Response:
    log = "Log text"
    items = ["element text"]


class SelectResponse:
    log = "Log text"
    items = ["Dog"]


def test_get_text(ctx: MagicMock):
    getter = Getters(ctx)
    getter._get_text = MagicMock(return_value=Response())  # type: ignore[assignment]
    text = getter.get_text("//div")
    assert text == "element text"


def test_get_text_select_returns_option_text(ctx: MagicMock):
    getter = Getters(ctx)
    getter._get_text = MagicMock(return_value=SelectResponse())  # type: ignore[assignment]
    text = getter.get_text("id=pet-select")
    assert text == "Dog"
