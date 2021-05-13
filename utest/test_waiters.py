from unittest.mock import MagicMock, PropertyMock

import pytest

from Browser import ElementState
from Browser.keywords import Waiter


def test_wait_for_state(ctx: MagicMock, response: MagicMock):
    wait = Waiter(ctx)
    wait.wait_for_elements_state("id=myText")


def test_wait_for_state_error():
    ctx = MagicMock()
    ctx.timeout = 10000
    pw = MagicMock()
    grpc = MagicMock()
    get_text = MagicMock()
    response = MagicMock()
    type(response).log = PropertyMock(side_effect=[AssertionError, "one"])
    get_text.WaitForElementsState = MagicMock(return_value=response)
    enter = MagicMock(return_value=get_text)
    grpc.__enter__ = enter
    pw.grpc_channel.return_value = grpc
    ctx.playwright = pw
    wait = Waiter(ctx)
    # pytest.set_trace()
    wait.wait_for_elements_state("id=myText")


def test_wait_for_function():
    ctx = MagicMock()
    ctx.timeout = 10000
    pw = MagicMock()
    grpc = MagicMock()
    get_text = MagicMock()
    response = MagicMock()
    type(response).log = PropertyMock(side_effect=[AssertionError, "10"])
    get_text.WaitForFunction = MagicMock(return_value=response)
    enter = MagicMock(return_value=get_text)
    grpc.__enter__ = enter
    pw.grpc_channel.return_value = grpc
    ctx.playwright = pw
    wait = Waiter(ctx)
    wait.wait_for_elements_state("id=myText", ElementState.checked)
