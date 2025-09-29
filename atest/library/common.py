import contextlib
import os
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from typing import Dict, NamedTuple
from urllib.parse import urlparse

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import psutil

from Browser.utils import find_free_port, FormatterKeywords, close_process_tree

SERVERS: Dict = {}


def parse_url(url: str) -> NamedTuple:
    return urlparse(url)


def start_test_server():
    global SERVERS
    port = str(find_free_port())
    # For some reason, we need to have cwd at project root for the server to run properly.
    root_dir = Path(os.path.dirname(__file__)) / ".." / ".."
    root_dir = root_dir.resolve()
    test_app_path = root_dir / "node" / "dynamic-test-app" / "dist" / "server.js"
    print(test_app_path)
    process = Popen(
        ["node", test_app_path, "-p", port],
        stdout=PIPE,
        stderr=STDOUT,
        cwd=str(root_dir),
    )
    SERVERS[port] = process
    return port


def start_test_https_server(
    server_cert_path: str,
    server_key_path: str,
    ca_cert_path: str,
    mutual_tls: bool = False,
):
    global SERVERS
    port = str(find_free_port())

    root_dir = Path(os.path.dirname(__file__)) / ".." / ".."
    root_dir = root_dir.resolve()
    test_app_dir = root_dir / "node" / "dynamic-test-app" / "dist"
    test_app_path = test_app_dir / "server.js"

    # This seems to be a very strange behaviour: if we start the server with absolute paths, it prepends
    # them with its own path and is unable to find the file. Therefore we have to count the relative path from its directory.
    server_cert_path = os.path.relpath(
        os.path.abspath(server_cert_path), start=test_app_dir
    )
    server_key_path = os.path.relpath(
        os.path.abspath(server_key_path), start=test_app_dir
    )
    ca_cert_path = os.path.relpath(os.path.abspath(ca_cert_path), start=test_app_dir)

    print(test_app_path)
    process = Popen(
        [
            "node",
            test_app_path,
            "-p",
            port,
            "-c",
            server_cert_path,
            "-k",
            server_key_path,
            "-C",
            ca_cert_path,
            "-M" if mutual_tls else "-T",
        ],
        text=True,
        cwd=str(root_dir),
    )
    SERVERS[port] = process
    return port


def stop_test_server(port: str):
    global SERVERS
    if port in SERVERS:
        p: Popen = SERVERS[port]
        close_process_tree(p)
        del SERVERS[port]
    else:
        logger.warn(f"Server with port {port} not found")


def _close_process(proc: Popen):
    try:
        parent = psutil.Process(proc.pid)
    except psutil.NoSuchProcess:
        logger.trace("Process already closed")
        return

    to_close = parent.children(recursive=True)
    to_close.append(parent)
    for p in to_close:
        logger.trace(f"Closing process <name={p.name()} pid={p.pid}>")
        with contextlib.suppress(psutil.NoSuchProcess):
            p.kill()
    _gone, alive = psutil.wait_procs(
        to_close,
        timeout=3,
        callback=lambda p: logger.trace(f"Process {p.pid} closed"),
    )

    if len(alive) == 0:
        logger.trace("Process tree closed")
        return

    for p in alive:
        logger.warn(f"Failed to close process. pid={p.pid}")


def get_current_scope_from_lib(keyword: FormatterKeywords) -> list:
    browser = BuiltIn().get_library_instance("Browser")
    stack = browser.scope_stack["assertion_formatter"].get()
    return [formatter.__name__ for formatter in stack.get(keyword.name, list())]


def numbers_are_close(number1: int, number2, difference: int) -> bool:
    """Compares that numbers difference is smaller than difference"""
    size_difference = abs(number1 - number2)
    logger.info(f"Numbers difference is {size_difference}")
    if size_difference < difference:
        return True
    raise ValueError(
        f"Numbers differece is {size_difference}, but it should have been {difference}"
    )
