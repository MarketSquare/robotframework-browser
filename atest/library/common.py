import json
import os
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from subprocess import STDOUT, Popen
from typing import IO, Dict, NamedTuple
from urllib.parse import urlparse

from robot.api import logger
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn

from Browser.utils import FormatterKeywords, close_process_tree, find_free_port


@library(scope='GLOBAL', listener='SELF')
class common:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self._servers: Dict = {}
        self._log_files: Dict[str, IO] = {}

    @keyword
    def parse_url(self, url: str) -> NamedTuple:
        return urlparse(url)

    @keyword
    def start_test_server(self) -> str:
        external_port = self._get_external_server_port()
        if external_port:
            logger.info(
                f"Using externally provided SERVER, skipping local test app startup (port {external_port})."
            )
            return external_port

        port = str(find_free_port())
        # For some reason, we need to have cwd at project root for the server to run properly.
        root_dir = Path(os.path.dirname(__file__)) / ".." / ".."
        root_dir = root_dir.resolve()
        test_app_path = root_dir / "node" / "dynamic-test-app" / "dist" / "server.js"
        print(test_app_path)
        log_file = self._open_log_file(root_dir, port)
        try:
            process = Popen(
                ["node", test_app_path, "-p", port],
                stdout=log_file,
                stderr=STDOUT,
                cwd=str(root_dir),
            )
        except Exception:
            log_file.close()
            raise
        self._servers[port] = process
        self._log_files[port] = log_file
        self._wait_for_server_startup(process, root_dir, port)
        return port

    @keyword
    def start_test_https_server(
        self,
        server_cert_path: str,
        server_key_path: str,
        ca_cert_path: str,
        mutual_tls: bool = False,
    ) -> str:
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
        log_file = self._open_log_file(root_dir, port)
        try:
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
                stdout=log_file,
                stderr=STDOUT,
                cwd=str(root_dir),
            )
        except Exception:
            log_file.close()
            raise
        self._servers[port] = process
        self._log_files[port] = log_file
        self._wait_for_server_startup(process, root_dir, port)
        return port

    @keyword
    def stop_test_server(self, port: str):
        external_port = self._get_external_server_port()
        if external_port and port == external_port and port not in self._servers:
            logger.info(
                f"Using externally provided SERVER, skipping local test app shutdown (port {port})."
            )
            return

        if port in self._servers:
            p: Popen = self._servers[port]
            close_process_tree(p)
            del self._servers[port]
        else:
            logger.warn(f"Server with port {port} not found")
        if port in self._log_files:
            self._log_files[port].flush()
            self._log_files[port].close()
            del self._log_files[port]

    @keyword
    def get_current_scope_from_lib(self, keyword: FormatterKeywords) -> list:
        browser = BuiltIn().get_library_instance("Browser")
        stack = browser.scope_stack["assertion_formatter"].get()
        return [formatter.__name__ for formatter in stack.get(keyword.name, list())]

    def start_test(self, data, result):
        self._write_rf_marker('test_start', data.id, data.name, '', post_context=True)

    def end_test(self, data, result):
        self._write_rf_marker('test_end', data.id, result.name, result.status, post_context=True)

    def _open_log_file(self, root_dir: Path, port: str):
        log_dir = root_dir / "atest" / "output" / "test-app"
        log_dir.mkdir(parents=True, exist_ok=True)
        return open(log_dir / f"test-app-{port}.log", "a", encoding="utf-8")

    def _wait_for_server_startup(self, process: Popen, root_dir: Path, port: str, timeout_s: float = 15.0):
        deadline = time.time() + timeout_s
        last_error = ""
        while time.time() < deadline:
            exit_code = process.poll()
            if exit_code is not None:
                tail = self._read_server_log_tail(root_dir, port)
                raise RuntimeError(
                    f"Test app exited before becoming ready (port {port}, code {exit_code}).\n{tail}"
                )
            try:
                with socket.create_connection(("127.0.0.1", int(port)), timeout=0.5):
                    return
            except OSError as err:
                last_error = str(err)
            time.sleep(0.1)

        raise RuntimeError(
            f"Timed out waiting for test app on port {port} after {timeout_s:.1f}s. Last error: {last_error}"
        )

    def _read_server_log_tail(self, root_dir: Path, port: str, max_lines: int = 30) -> str:
        log_path = root_dir / "atest" / "output" / "test-app" / f"test-app-{port}.log"
        if not log_path.exists():
            return "<no server log available>"
        try:
            lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
            tail = "\n".join(lines[-max_lines:])
            return tail if tail else "<server log is empty>"
        except Exception as err:
            return f"<failed to read server log: {err}>"

    def _current_port(self) -> str | None:
        try:
            return BuiltIn().get_variable_value('${SERVER_PORT}')
        except Exception:
            return None

    def _get_external_server_port(self) -> str | None:
        try:
            server = BuiltIn().get_variable_value('${SERVER}')
        except Exception:
            return None
        if not server:
            return None

        # SERVER is expected as host:port. Treat non-localhost hosts as external.
        if ':' not in server:
            return None
        host, port = server.rsplit(':', 1)
        host = host.strip().lower()
        port = port.strip()
        if host in {'localhost', '127.0.0.1', '::1'}:
            return None
        if not port.isdigit():
            return None
        return port

    def _write_rf_marker(self, event: str, test_id: str, name: str, status: str, post_context: bool):
        record = json.dumps({
            'ts': datetime.now(timezone.utc).isoformat(),
            'type': 'rf',
            'event': event,
            'test_id': test_id,
            'name': name,
            'status': status,
        })
        port = self._current_port()
        line = record + '\n'
        if port and port in self._log_files:
            self._log_files[port].write(line)
            self._log_files[port].flush()
        if post_context and port and port in self._servers:
            ctx = json.dumps({'test_id': test_id, 'kw_name': name})
            self._post_rf_context(port, ctx)

    def _post_rf_context(self, port: str, payload: str):
        try:
            import logging
            import requests
            logging.getLogger('urllib3').setLevel(logging.WARNING)
            requests.post(
                f'http://localhost:{port}/rf-context',
                data=payload,
                headers={'Content-Type': 'application/json'},
                timeout=0.5,
            )
        except Exception:
            pass

    @keyword
    def numbers_are_close(self, number1: int, number2: int, difference: int) -> bool:
        """Compares that numbers difference is smaller than difference"""
        size_difference = abs(number1 - number2)
        logger.info(f"Numbers difference is {size_difference}")
        if size_difference <= difference:
            return True
        raise ValueError(
            f"Numbers difference is {size_difference} {type(size_difference)}, but it should have been {difference} {type(difference)}"
        )
