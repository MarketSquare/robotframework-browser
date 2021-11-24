import os
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from typing import Dict, NamedTuple
from urllib.parse import urlparse

from Browser.utils import find_free_port

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
    # TODO: remove str() when Python 3.7 support is dropped.
    process = Popen(
        ["node", str(test_app_path), port],
        stdout=PIPE,
        stderr=STDOUT,
        cwd=str(root_dir),
    )
    SERVERS[port] = process
    return port


def stop_test_server(port: str):
    global SERVERS
    if port in SERVERS:
        SERVERS[port].kill()
        del SERVERS[port]
