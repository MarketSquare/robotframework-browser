import re
from unittest.mock import MagicMock

import pytest

from Browser.keywords.network import Network
from Browser.utils.data_types import ContextOrPage, RequestMethod
from Browser.utils.types import Secret


@pytest.fixture
def network() -> tuple[Network, MagicMock]:
    library = MagicMock()
    library.get_timeout.return_value = 7000.0
    stub = MagicMock()
    stub.AddContextRoute.return_value.id = "context-rule"
    library.playwright.grpc_channel.return_value.__enter__.return_value = stub
    network = Network.__new__(Network)
    network.library = library
    return network, stub


def sent_modify(stub: MagicMock):
    return stub.AddContextRoute.call_args.args[0].modify


def test_secret_values_are_revealed_before_the_rpc(network):
    network, stub = network
    network.modify_responses(
        "**/api",
        headers={"X-Token": Secret("response-token")},
        request_url=Secret("https://staging/api"),
        request_headers={"Authorization": Secret("Bearer abc")},
        request_body=Secret("payload"),
    )
    modify = sent_modify(stub)
    assert modify.headers["X-Token"] == "response-token"
    assert modify.url == "https://staging/api"
    assert modify.requestHeaders["Authorization"] == "Bearer abc"
    assert modify.postData == b"payload"


def test_log_has_header_names_and_hides_a_secret_url(network, monkeypatch):
    network, _ = network
    logged = []
    monkeypatch.setattr("Browser.keywords.network.logger.info", logged.append)
    network.modify_responses(
        "**/api",
        status=500,
        json_patch={"a": None},
        headers={"X-Real": "response-value"},
        request_url=Secret("https://staging/api"),
        request_headers={"Authorization": "Bearer abc"},
        request_body="payload",
    )
    assert logged == [
        "Added route rule context-rule: modify **/api, "
        "request: url=<secret>, headers=[Authorization], body; "
        "response: status=500, json_patch, headers=[X-Real], times=None, on=Context."
    ]


def test_only_the_given_changes_are_sent(network):
    network, stub = network
    network.modify_responses("**/api", status=404)
    modify = sent_modify(stub)
    assert modify.status == 404
    assert modify.timeout == 7000
    for field in ("url", "method", "postData", "body", "jsonPatch"):
        assert not modify.HasField(field)
    assert dict(modify.headers) == {}
    assert dict(modify.requestHeaders) == {}


def test_request_changes_are_sent(network):
    network, stub = network
    network.modify_responses(
        "**/api",
        request_url="/api/v2",
        request_method=RequestMethod.POST,
        request_body="päivää",
    )
    modify = sent_modify(stub)
    assert modify.url == "/api/v2"
    assert modify.method == "POST"
    assert modify.postData == "päivää".encode()
    assert not modify.HasField("status")


def test_json_patch_is_sent_as_json_text(network):
    network, stub = network
    network.modify_responses("**/api", json_patch={"order": {"note": None}})
    modify = sent_modify(stub)
    assert modify.jsonPatch == '{"order": {"note": null}}'
    assert dict(modify.headers) == {}


def test_replaced_body_gets_the_content_type_unless_headers_has_one(network):
    network, stub = network
    network.modify_responses("**/api", json=[1])
    assert sent_modify(stub).body == b"[1]"
    assert dict(sent_modify(stub).headers) == {"Content-Type": "application/json"}
    network.modify_responses("**/api", body="x", headers={"content-type": "text/csv"})
    assert dict(sent_modify(stub).headers) == {"content-type": "text/csv"}


def test_page_rule_uses_the_page_rpc(network):
    network, stub = network
    stub.AddPageRoute.return_value.id = "page-rule"
    assert (
        network.modify_responses("**/api", status=200, on=ContextOrPage.Page)
        == "page-rule"
    )


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        ({}, "Modify Responses needs at least one change."),
        (
            {"headers": {}, "request_headers": {}},
            "Modify Responses needs at least one change.",
        ),
        (
            {"body": "a", "json_patch": {"a": 1}},
            "Give at most one of body, json, path and json_patch, got body and json_patch.",
        ),
        ({"status": 600}, "status must be from 100 to 599, got 600."),
        ({"status": 200, "times": 0}, "times must be 1 or more, got 0."),
    ],
)
def test_invalid_arguments_fail_before_the_rpc(network, arguments, message):
    network, stub = network
    with pytest.raises(ValueError, match=re.escape(message)):
        network.modify_responses("**/api", **arguments)
    stub.AddContextRoute.assert_not_called()


def test_secret_body_is_revealed_before_the_rpc(network):
    network, stub = network
    network.modify_responses("**/api", body=Secret("response-secret"))
    modify = sent_modify(stub)
    assert modify.body == b"response-secret"
    assert dict(modify.headers) == {"Content-Type": "text/plain; charset=utf-8"}
