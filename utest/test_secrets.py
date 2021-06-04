import json
import sys
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

import Browser.keywords as interaction
from Browser.keywords import PlaywrightState

WARN_MESSAGE = (
    "WARNING  RobotFramework:logger.py:95 Direct assignment of values as 'secret' is "
    "deprecated. Use variables or environment variables instead.\n"
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
    ctx = MagicMock()
    pw = MagicMock()
    grpc = MagicMock()
    new_context = MagicMock()
    response = MagicMock()
    msg = 'Successfully created context with  options: {"username": "USERNAME", "password": "PWD"}'
    type(response).log = PropertyMock(return_value=msg)
    context = MagicMock(return_value=response)
    new_context.NewContext = context
    enter = MagicMock(return_value=new_context)
    grpc.__enter__ = enter
    pw.grpc_channel.return_value = grpc
    ctx.playwright = pw
    pw = PlaywrightState(ctx)
    pw.resolve_secret = MagicMock(
        return_value={"username": "USERNAME", "password": "PWD"}
    )
    pw.new_context(httpCredentials={"username": "$username", "password": "$pwd"})
    args = new_context.NewContext.call_args_list
    result_raw_options = json.loads(args[0].args[0].rawOptions)
    assert result_raw_options["httpCredentials"]["username"] == "USERNAME"
    assert result_raw_options["httpCredentials"]["password"] == "PWD"
