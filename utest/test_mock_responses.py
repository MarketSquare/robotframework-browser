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


def test_json_string_is_encoded_as_a_json_string():
    network, stub = make_network()
    network.mock_responses("**/api", json='{"a": 1}')
    assert sent_fulfill(stub).body == b'"{\\"a\\": 1}"'


def test_empty_body_is_an_empty_text_body():
    network, stub = make_network()
    network.mock_responses("**/api", body="")
    fulfill = sent_fulfill(stub)
    assert fulfill.body == b""
    assert fulfill.headers["Content-Type"] == "text/plain; charset=utf-8"


def test_file_with_an_unknown_extension_is_octet_stream(tmp_path):
    file = tmp_path / "payload.robotmock"
    file.write_bytes(b"\x00\xff")
    network, stub = make_network()
    network.mock_responses("**/api", path=file)
    fulfill = sent_fulfill(stub)
    assert fulfill.body == b"\x00\xff"
    assert fulfill.headers["Content-Type"] == "application/octet-stream"


def test_three_payloads_are_named_in_the_error(tmp_path):
    network, stub = make_network()
    with pytest.raises(
        ValueError,
        match="Give at most one of body, json and path, got body, json and path.",
    ):
        network.mock_responses("**/api", body="a", json=1, path=tmp_path)
    stub.AddContextRoute.assert_not_called()


def test_bytes_body_is_sent_unchanged_as_octet_stream():
    network, stub = make_network()
    network.mock_responses("**/api", body=b"\x89P\xff\x00\xe9")
    fulfill = sent_fulfill(stub)
    assert fulfill.body == b"\x89P\xff\x00\xe9"
    assert fulfill.headers["Content-Type"] == "application/octet-stream"


def test_json_body_is_compact():
    network, stub = make_network()
    network.mock_responses("**/api", json={"a": [1, 2]})
    assert sent_fulfill(stub).body == b'{"a":[1,2]}'


@pytest.mark.parametrize("value", [float("nan"), float("inf"), {1, 2}])
def test_json_that_is_not_json_fails_with_a_value_error(value):
    network, stub = make_network()
    with pytest.raises(ValueError, match="^json cannot be sent as JSON: "):
        network.mock_responses("**/api", json={"a": value})
    stub.AddContextRoute.assert_not_called()
