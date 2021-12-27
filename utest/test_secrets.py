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


class Response:
    log = "log message"


def test_fill_secret_in_plain_text(caplog):
    ctx = MagicMock()
    ctx.presenter_mode = False
    secrets = interaction.Interaction(ctx)
    secrets._fill_text = MagicMock(return_value=Response())
    secrets.fill_secret("selector", "password")
    assert caplog.text == WARN_MESSAGE


def test_type_secret_in_plain_text(caplog):
    ctx = MagicMock()
    ctx.presenter_mode = False
    secrets = interaction.Interaction(ctx)
    secrets._type_text = MagicMock(return_value=Response())
    secrets.type_secret("selector", "password")
    assert caplog.text == WARN_MESSAGE


def test_type_secret_with_prefix(caplog):
    ctx = MagicMock()
    ctx.presenter_mode = False
    secrets = interaction.Interaction(ctx)
    secrets._replace_placeholder_variables = MagicMock(return_value="123")
    secrets._type_text = MagicMock(return_value=Response())
    secrets.type_secret("selector", "$password")
    assert caplog.text == ""
    secrets.type_secret("selector", "%password")
    assert caplog.text == ""


def test_fill_secret_with_prefix(caplog):
    ctx = MagicMock()
    ctx.presenter_mode = False
    secrets = interaction.Interaction(ctx)
    secrets._fill_text = MagicMock(return_value=Response())
    secrets._replace_placeholder_variables = MagicMock(return_value="123")
    secrets.fill_secret("selector", "$password")
    assert caplog.text == ""
    secrets.fill_secret("selector", "%password")
    assert caplog.text == ""


def test_fill_secret_reformat_error():
    ctx = MagicMock()
    secrets = interaction.Interaction(ctx)

    def raiser(*args, **kwargs):
        raise Exception("Failure filling: PWD")

    secrets._fill_text = raiser
    secrets.resolve_secret = lambda *args: "PWD"

    with pytest.raises(Exception) as excinfo:
        secrets.fill_secret("selector", "$password")

    assert "Failure filling: ***" == str(excinfo.value)


def test_type_secret_reformat_error():
    ctx = MagicMock()
    secrets = interaction.Interaction(ctx)

    def raiser(*args, **kwargs):
        raise Exception("Failure typing: PWD")

    secrets._type_text = raiser
    secrets.resolve_secret = lambda *args: "PWD"

    with pytest.raises(Exception) as excinfo:
        secrets.type_secret("selector", "$password")

    assert "Failure typing: ***" == str(excinfo.value)


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
