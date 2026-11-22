from unittest.mock import MagicMock

import pytest

from Browser.keywords.network import Network
from Browser.utils import AbortErrorCode, ContextOrPage


def make_network() -> tuple[Network, MagicMock]:
    library = MagicMock()
    stub = MagicMock()
    stub.AddContextRoute.return_value.id = "context-rule"
    stub.AddPageRoute.return_value.id = "page-rule"
    library.playwright.grpc_channel.return_value.__enter__.return_value = stub
    network = Network.__new__(Network)
    network.library = library
    return network, stub


@pytest.mark.parametrize("times", [0, -1])
def test_times_below_one_fails_before_the_rpc(times):
    network, stub = make_network()
    with pytest.raises(ValueError, match=f"times must be 1 or more, got {times}."):
        network.abort_requests("**/api", times=times)
    stub.AddContextRoute.assert_not_called()
    stub.AddPageRoute.assert_not_called()


def test_context_rule_is_the_default():
    network, stub = make_network()
    assert network.abort_requests("**/api") == "context-rule"
    request = stub.AddContextRoute.call_args.args[0]
    assert request.url == "**/api"
    assert not request.HasField("times")
    assert request.abort.errorCode == "failed"
    stub.AddPageRoute.assert_not_called()


def test_page_rule_sends_times_and_error_code():
    network, stub = make_network()
    rule_id = network.abort_requests(
        "/api/",
        error_code=AbortErrorCode.timedout,
        times=2,
        on=ContextOrPage.Page,
    )
    assert rule_id == "page-rule"
    request = stub.AddPageRoute.call_args.args[0]
    assert request.times == 2
    assert request.abort.errorCode == "timedout"
    stub.AddContextRoute.assert_not_called()
