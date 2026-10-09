import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from subprocess import STDOUT, Popen
from typing import IO
from urllib.error import URLError
from urllib.request import urlopen

from Browser.utils import close_process_tree, find_free_port

POLL_INTERVAL_SECONDS = 0.1
STARTUP_TIMEOUT_SECONDS = 10
MAX_CRASH_RETRIES = 3
OVERALL_DEADLINE_SECONDS = 25

# For some reason, we need to have cwd at project root for the server to run properly.
ROOT_DIR = (Path(__file__).parent / ".." / "..").resolve()
SERVER_JS = ROOT_DIR / "node" / "dynamic-test-app" / "dist" / "server.js"

CommandBuilder = Callable[[str, str], list]
ReadinessCheck = Callable[[str, str, Path], bool]


@dataclass
class RunningTestApp:
    port: str
    process: Popen
    log_file: IO
    failed_attempts: list[str] = field(default_factory=list)

    def stop(self):
        close_process_tree(self.process)
        self.log_file.flush()
        self.log_file.close()


def read_log(log_path: Path) -> str:
    try:
        content = log_path.read_text(encoding="utf-8").strip()
    except OSError as error:
        return f"<could not read log {log_path}: {error}>"
    return content or "<log is empty>"


def http_ready(port: str, token: str, log_path: Path) -> bool:
    try:
        with urlopen(f"http://localhost:{port}/health", timeout=1) as response:
            body = response.read().decode("utf-8").strip()
    except (URLError, OSError):
        return False
    return body == token


def https_ready(port: str, token: str, log_path: Path) -> bool:
    for line in read_log(log_path).splitlines():
        if "server_start" in line and token in line:
            return True
    return False


def http_command(port: str, token: str) -> list:
    return ["node", str(SERVER_JS), "-p", port, "-i", token]


def start_test_app(
    log_dir: Path,
    cmd_builder: CommandBuilder = http_command,
    is_ready: ReadinessCheck = http_ready,
) -> RunningTestApp:
    """Start the Test App on a free port and wait until it answers as itself.

    A crashed start is retried on a new port. Every failed attempt is kept with
    the exit code and the app's log, so a retried crash stays visible.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + OVERALL_DEADLINE_SECONDS
    attempts: list[str] = []
    crash_retries_left = MAX_CRASH_RETRIES
    while True:
        port = str(find_free_port())
        token = uuid.uuid4().hex
        log_path = log_dir / f"test-app-{port}.log"
        log_file = open(log_path, "w", encoding="utf-8")
        try:
            process = Popen(
                cmd_builder(port, token),
                stdout=log_file,
                stderr=STDOUT,
                cwd=str(ROOT_DIR),
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
            return RunningTestApp(port, process, log_file, attempts)

        if process.poll() is None:
            close_process_tree(process)
        exit_code = process.poll()
        log_file.flush()
        log_file.close()
        reason = "crashed" if crashed else "did not become ready in time"
        attempts.append(
            f"attempt {len(attempts) + 1}: port {port} (instance {token}) {reason}, "
            f"exit code {exit_code}:\n{read_log(log_path)}"
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
