import base64
import os
from typing import NamedTuple
from urllib.parse import urlparse

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from test_app_server import (
    ROOT_DIR,
    SERVER_JS,
    RunningTestApp,
    https_ready,
    start_test_app,
)

from Browser.utils import FormatterKeywords

SERVERS: dict[str, RunningTestApp] = {}
TEST_APP_LOG_DIR = ROOT_DIR / "atest" / "output" / "test-app"


def _start(**kwargs) -> str:
    server = start_test_app(TEST_APP_LOG_DIR, **kwargs)
    for attempt in server.failed_attempts:
        logger.warn(f"Test server start was retried, {attempt}")
    SERVERS[server.port] = server
    return server.port


def parse_url(url: str) -> NamedTuple:
    return urlparse(url)


def parse_url_netloc(url: str) -> str:
    """Returns netloc from url"""
    return urlparse(url).netloc


def start_test_server():
    return _start()


def start_test_https_server(
    server_cert_path: str,
    server_key_path: str,
    ca_cert_path: str,
    mutual_tls: bool = False,
):
    test_app_dir = SERVER_JS.parent

    # This seems to be a very strange behaviour: if we start the server with absolute paths, it prepends
    # them with its own path and is unable to find the file. Therefore we have to count the relative path from its directory.
    server_cert_path = os.path.relpath(
        os.path.abspath(server_cert_path), start=test_app_dir
    )
    server_key_path = os.path.relpath(
        os.path.abspath(server_key_path), start=test_app_dir
    )
    ca_cert_path = os.path.relpath(os.path.abspath(ca_cert_path), start=test_app_dir)

    def cmd_builder(port: str, token: str) -> list:
        return [
            "node",
            str(SERVER_JS),
            "-p",
            port,
            "-c",
            server_cert_path,
            "-k",
            server_key_path,
            "-C",
            ca_cert_path,
            "-M" if mutual_tls else "-T",
            "-i",
            token,
        ]

    return _start(cmd_builder=cmd_builder, is_ready=https_ready)


def stop_test_server(port: str):
    server = SERVERS.pop(port, None)
    if server is None:
        logger.warn(f"Server with port {port} not found")
        return
    server.stop()


def get_current_scope_from_lib(keyword: FormatterKeywords) -> list:
    browser = BuiltIn().get_library_instance("Browser")
    stack = browser.scope_stack["assertion_formatter"].get()
    return [formatter.__name__ for formatter in stack.get(keyword.name, list())]


def numbers_are_close(number1: int, number2: int, difference: int) -> bool:
    """Compares that numbers difference is smaller than difference"""
    size_difference = abs(number1 - number2)
    logger.info(f"Numbers difference is {size_difference}")
    if size_difference <= difference:
        return True
    raise ValueError(
        f"Numbers difference is {size_difference} {type(size_difference)}, but it should have been {difference} {type(difference)}"
    )


def base64url_encode(data: str) -> str:
    """Encodes string to base64url string"""
    return base64.urlsafe_b64encode(data.encode("utf-8")).rstrip(b"=").decode("utf-8")
