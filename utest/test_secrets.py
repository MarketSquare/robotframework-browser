import json
import os
import subprocess
import sys
from unittest.mock import MagicMock

import pytest
from robot.libraries.BuiltIn import RobotNotRunningError

import Browser
import Browser.keywords as interaction
from Browser.base.librarycomponent import LibraryComponent
from Browser.keywords import PlaywrightState

ERROR_MESSAGE = (
    "Direct assignment of values or variables as 'secret' is not allowed. "
    "Use special variable syntax ($var instead of ${var}) "
    "to prevent variable values from being spoiled."
)


class Response:
    log = "log message"


@pytest.fixture
def application_server():
    process = subprocess.Popen(
        ["node", "./node/dynamic-test-app/dist/server.js", "-p", "7272"]
    )
    yield
    process.terminate()


@pytest.fixture
def browser(tmpdir):
    Browser.Browser._output_dir = tmpdir
    browser = Browser.Browser()
    yield browser
    browser.close_browser("ALL")


def test_fill_secret_in_plain_text(caplog):
    ctx = MagicMock()
    ctx.presenter_mode = False
    secrets = interaction.Interaction(ctx)
    secrets._fill_text = MagicMock(return_value=Response())
    try:
        secrets.fill_secret("selector", "password")
    except ValueError as e:
        assert str(e) == ERROR_MESSAGE


def test_type_secret_in_plain_text(caplog):
    ctx = MagicMock()
    ctx.presenter_mode = False
    secrets = interaction.Interaction(ctx)
    secrets._type_text = MagicMock(return_value=Response())
    try:
        secrets.type_secret("selector", "password")
    except ValueError as e:
        assert str(e) == ERROR_MESSAGE


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

    assert str(excinfo.value) == "Failure filling: ***"


def test_type_secret_reformat_error():
    ctx = MagicMock()
    secrets = interaction.Interaction(ctx)

    def raiser(*args, **kwargs):
        raise Exception("Failure typing: PWD")

    secrets._type_text = raiser
    secrets.resolve_secret = lambda *args: "PWD"

    with pytest.raises(Exception) as excinfo:
        secrets.type_secret("selector", "$password")

    assert str(excinfo.value) == "Failure typing: ***"


@pytest.mark.skipif(sys.version_info.minor == 7, reason="Does not work with Python 3.7")
def test_http_credentials_in_new_context():
    class Response:
        contextOptions = json.dumps({"username": "USERNAME", "password": "PWD"})
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


def test_creds_from_python(application_server, browser):
    with pytest.raises(RobotNotRunningError):
        browser.new_context(
            httpCredentials={"username": "$name}", "password": "$password"}
        )

    ctx_id = browser.new_context(
        httpCredentials={"username": "name}", "password": "password"}
    )
    assert ctx_id

    ctx_id = browser.new_context(
        httpCredentials={"username": "%name", "password": "%password"}
    )
    assert ctx_id


def test_robot_running():
    lib = MagicMock()
    component = LibraryComponent(lib)
    assert component.robot_running is False


def test_resolve_secret():
    arg_name = "httpCredentials"
    secret_variable = {"password": "%password", "username": "%name"}
    lib = MagicMock()
    component = LibraryComponent(lib)
    secret = component.resolve_secret(secret_variable, arg_name)
    assert secret == secret_variable

    os.environ["name"] = "foo"
    os.environ["password"] = "bar"
    secret = component.resolve_secret(secret_variable, arg_name)
    assert secret == {"password": "bar", "username": "foo"}
