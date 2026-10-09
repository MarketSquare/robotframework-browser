import warnings
from unittest.mock import MagicMock

import pytest

from atest.library.test_app_server import ROOT_DIR, start_test_app


@pytest.fixture
def response():
    response = MagicMock()
    response.log = ""
    response.body = ""
    return response


@pytest.fixture
def ctx(response):
    ctx = MagicMock()
    pw = MagicMock()
    grpc = MagicMock()
    get_text = MagicMock()
    get_text.GetText = MagicMock(return_value=response)
    enter = MagicMock(return_value=get_text)
    grpc.__enter__ = enter
    pw.grpc_channel.return_value = grpc
    ctx.playwright = pw
    return ctx


@pytest.fixture(scope="session")
def test_app_url():
    server = start_test_app(ROOT_DIR / "utest" / "output" / "test-app")
    for attempt in server.failed_attempts:
        warnings.warn(f"Test App start was retried, {attempt}", stacklevel=1)
    yield f"http://localhost:{server.port}"
    server.stop()
