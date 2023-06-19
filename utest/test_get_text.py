from unittest.mock import MagicMock

from Browser.keywords import Getters


class Response:
    log = "Log text"
    body = "element text"


def test_get_text(ctx: MagicMock):
    getter = Getters(ctx)
    getter._get_text = MagicMock(return_value=Response())  # type: ignore[assignment]
    text = getter.get_text("//div")
    assert text == "element text"
