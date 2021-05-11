from unittest.mock import MagicMock, Mock

from Browser.keywords import Getters


def test_get_text():
    ctx = MagicMock()
    pw = MagicMock()
    grpc = MagicMock()
    get_text = MagicMock()
    response = MagicMock()
    response.log = ""
    response.body = ""
    get_text.GetText = Mock(return_value=response)
    enter = MagicMock(return_value=get_text)
    grpc.__enter__ = enter
    pw.grpc_channel.return_value = grpc
    ctx.playwright = pw
    getter = Getters(ctx)
    getter.get_text("//div")
