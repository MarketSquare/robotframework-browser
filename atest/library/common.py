import base64
import os
import time
import uuid
from pathlib import Path
from subprocess import STDOUT, Popen
from typing import IO, Callable, Dict, List, NamedTuple
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from Browser.utils import FormatterKeywords, close_process_tree, find_free_port

SERVERS: Dict = {}
LOG_FILES: Dict[str, IO] = {}

POLL_INTERVAL_SECONDS = 0.1
STARTUP_TIMEOUT_SECONDS = 10
MAX_CRASH_RETRIES = 3
OVERALL_DEADLINE_SECONDS = 25


def _root_dir() -> Path:
    # For some reason, we need to have cwd at project root for the server to run properly.
    return (Path(os.path.dirname(__file__)) / ".." / "..").resolve()


def _test_app_log_path(root_dir: Path, port: str) -> Path:
    log_dir = root_dir / "atest" / "output" / "test-app"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / f"test-app-{port}.log"


def _read_log(log_path: Path) -> str:
    try:
        content = log_path.read_text(encoding="utf-8").strip()
    except OSError as error:
        return f"<could not read log {log_path}: {error}>"
    return content or "<log is empty>"


def _http_ready(port: str, token: str, log_path: Path) -> bool:
    try:
        with urlopen(f"http://localhost:{port}/health", timeout=1) as response:
            body = response.read().decode("utf-8").strip()
    except (URLError, OSError):
        return False
    return body == token


def _https_ready(port: str, token: str, log_path: Path) -> bool:
    for line in _read_log(log_path).splitlines():
        if "server_start" in line and token in line:
            return True
    return False


def _spawn_with_readiness(
    cmd_builder: Callable[[str, str], list],
    root_dir: Path,
    is_ready: Callable[[str, str, Path], bool],
) -> str:
    global SERVERS, LOG_FILES
    deadline = time.monotonic() + OVERALL_DEADLINE_SECONDS
    attempts: List[str] = []
    crash_retries_left = MAX_CRASH_RETRIES
    while True:
        port = str(find_free_port())
        token = uuid.uuid4().hex
        log_path = _test_app_log_path(root_dir, port)
        log_file = open(log_path, "w", encoding="utf-8")
        try:
            process = Popen(
                cmd_builder(port, token),
                stdout=log_file,
                stderr=STDOUT,
                cwd=str(root_dir),
            )
        except Exception:
            log_file.close()
            raise

        attempt_deadline = min(time.monotonic() + STARTUP_TIMEOUT_SECONDS, deadline)
        crashed = False
        ready = False
        while time.monotonic() < attempt_deadline:
            if process.poll() is not None:
                crashed = True
                break
            if is_ready(port, token, log_path):
                ready = True
                break
            time.sleep(POLL_INTERVAL_SECONDS)

        if ready:
            SERVERS[port] = process
            LOG_FILES[port] = log_file
            return port

        if process.poll() is None:
            close_process_tree(process)
        exit_code = process.poll()
        log_file.flush()
        log_file.close()
        reason = "crashed" if crashed else "did not become ready in time"
        attempts.append(
            f"attempt {len(attempts) + 1}: port {port} (instance {token}) {reason}, "
            f"exit code {exit_code}:\n{_read_log(log_path)}"
        )

        budget_left = time.monotonic() < deadline
        if crashed and crash_retries_left > 0 and budget_left:
            crash_retries_left -= 1
            continue
        if not crashed and budget_left:
            continue
        break

    raise RuntimeError(
        f"Test server failed to start after {len(attempts)} attempt(s):\n\n"
        + "\n\n".join(attempts)
    )


def parse_url(url: str) -> NamedTuple:
    return urlparse(url)


def parse_url_netloc(url: str) -> str:
    """Returns netloc from url"""
    return urlparse(url).netloc


def start_test_server():
    root_dir = _root_dir()
    test_app_path = root_dir / "node" / "dynamic-test-app" / "dist" / "server.js"
    print(test_app_path)

    def cmd_builder(port: str, token: str) -> list:
        return ["node", str(test_app_path), "-p", port, "-i", token]

    return _spawn_with_readiness(cmd_builder, root_dir, _http_ready)


def start_test_https_server(
    server_cert_path: str,
    server_key_path: str,
    ca_cert_path: str,
    mutual_tls: bool = False,
):
    root_dir = _root_dir()
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

    def cmd_builder(port: str, token: str) -> list:
        return [
            "node",
            str(test_app_path),
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

    return _spawn_with_readiness(cmd_builder, root_dir, _https_ready)


def stop_test_server(port: str):
    global SERVERS, LOG_FILES
    if port in SERVERS:
        p: Popen = SERVERS[port]
        close_process_tree(p)
        del SERVERS[port]
    else:
        logger.warn(f"Server with port {port} not found")
    if port in LOG_FILES:
        LOG_FILES[port].flush()
        LOG_FILES[port].close()
        del LOG_FILES[port]


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
