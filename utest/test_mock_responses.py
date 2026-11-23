from unittest.mock import MagicMock

import pytest

from Browser.keywords.network import Network


def make_network() -> tuple[Network, MagicMock]:
    library = MagicMock()
    stub = MagicMock()
    stub.AddContextRoute.return_value.id = "context-rule"
    library.playwright.grpc_channel.return_value.__enter__.return_value = stub
    network = Network.__new__(Network)
    network.library = library
    return network, stub


def sent_fulfill(stub: MagicMock):
    return stub.AddContextRoute.call_args.args[0].fulfill


def test_body_and_its_content_type_are_sent_in_the_fulfill():
    network, stub = make_network()
    network.mock_responses("**/api", json={"a": [1, 2]}, headers={"X-A": "1"})
    fulfill = sent_fulfill(stub)
    assert fulfill.body == b'{"a":[1,2]}'
    assert dict(fulfill.headers) == {"X-A": "1", "Content-Type": "application/json"}


def test_three_payloads_are_named_in_the_error(tmp_path):
    network, stub = make_network()
    with pytest.raises(
        ValueError,
        match="Give at most one of body, json and path, got body, json and path.",
    ):
        network.mock_responses("**/api", body="a", json=1, path=tmp_path)
    stub.AddContextRoute.assert_not_called()


def test_json_that_is_not_json_fails_before_the_rpc():
    network, stub = make_network()
    with pytest.raises(ValueError, match="^json cannot be sent as JSON: "):
        network.mock_responses("**/api", json={"a": float("nan")})
    stub.AddContextRoute.assert_not_called()
