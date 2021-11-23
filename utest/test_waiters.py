from unittest.mock import MagicMock, PropertyMock

from Browser import ElementState
from Browser.keywords import Waiter


class Response:
    log = "log message"


def test_wait_for_state(ctx: MagicMock, response: MagicMock):
    wait = Waiter(ctx)
    wait._wait_for_elements_state = MagicMock(return_value=Response())
    wait.wait_for_elements_state("id=myText")


def test_wait_for_state_error():
    ctx = MagicMock()
    ctx.timeout = 1000
    wait = Waiter(ctx)
    wait._wait_for_elements_state = MagicMock(side_effect=[AssertionError, "one"])
    wait.wait_for_elements_state("id=myText")


def test_wait_for_function():
    ctx = MagicMock()
    ctx.timeout = 1000
    wait = Waiter(ctx)
    wait._wait_for_function = MagicMock(side_effect=[AssertionError, "10"])
    wait.wait_for_elements_state("id=myText", ElementState.checked)
