import json
import sys
from unittest.mock import MagicMock

import pytest

import Browser.keywords as interaction
from Browser.keywords import PlaywrightState

WARN_MESSAGE = (
    "WARNING  RobotFramework:logger.py:95 Direct assignment of values as 'secret' is deprecated. "
    "Use special variable syntax to resolve variable. Example $var instead of ${var}.\n"
)


def test_fill_secret_in_plain_text(caplog):
    secrerts = interaction.Interaction(MagicMock())
    secrerts.fill_secret("selector", "password")
    assert caplog.text == WARN_MESSAGE


def test_type_secret_in_plain_text(caplog):
    secrerts = interaction.Interaction(MagicMock())
    secrerts.type_secret("selector", "password")
    assert caplog.text == WARN_MESSAGE


def test_type_secret_with_prefix(caplog):
    secrerts = interaction.Interaction(MagicMock())
    secrerts._replace_placeholder_variables = MagicMock(return_value="123")
    secrerts.type_secret("selector", "$password")
    assert caplog.text == ""
    secrerts.type_secret("selector", "%password")
    assert caplog.text == ""


def test_fill_secret_with_prefix(caplog):
    secrerts = interaction.Interaction(MagicMock())
    secrerts._replace_placeholder_variables = MagicMock(return_value="123")
    secrerts.fill_secret("selector", "$password")
    assert caplog.text == ""
    secrerts.fill_secret("selector", "%password")
    assert caplog.text == ""


@pytest.mark.skipif(sys.version_info.minor == 7, reason="Does not work with Python 3.7")
def test_http_credentials_in_new_context():
    class Response:
        contextOptions = json.dumps({'username': 'USERNAME', 'password': 'PWD'})
        log = "Something here"
        newBrowser = True
        id = 123
    ctx = MagicMock()
    dummy_new_context = MagicMock(return_value=Response())
    pw = PlaywrightState(ctx)
    pw._new_context = dummy_new_context
    pw.resolve_secret = MagicMock(
        return_value={"username": "USERNAME", "password": "PWD"}
    )
    pw.new_context(httpCredentials={"username": "$username", "password": "$pwd"})
    name, args, kwargs = dummy_new_context.mock_calls[0]
    result_raw_options = json.loads(args[0])
    assert result_raw_options["httpCredentials"]["username"] == "USERNAME"
    assert result_raw_options["httpCredentials"]["password"] == "PWD"
