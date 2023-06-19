from unittest.mock import MagicMock

import pytest


@pytest.fixture
def response():
    response = MagicMock()
    response.log = ""
    response.body = ""
    return response


@pytest.fixture
def ctx(response):
    ctx = MagicMock()
    pw = MagicMock()
    grpc = MagicMock()
    get_text = MagicMock()
    get_text.GetText = MagicMock(return_value=response)
    enter = MagicMock(return_value=get_text)
    grpc.__enter__ = enter
    pw.grpc_channel.return_value = grpc
    ctx.playwright = pw
    return ctx
