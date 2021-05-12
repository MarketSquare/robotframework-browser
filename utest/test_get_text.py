from unittest.mock import MagicMock

from Browser.keywords import Getters


def test_get_text(ctx: MagicMock):
    getter = Getters(ctx)
    getter.get_text("//div")
