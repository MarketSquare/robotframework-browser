# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import atexit
import contextlib
import os
import platform
import time
from functools import cached_property
from pathlib import Path
from subprocess import DEVNULL, STDOUT, CalledProcessError, Popen, run
from typing import TYPE_CHECKING, TextIO

import grpc  # type: ignore

try:
    from BrowserBatteries import start_grpc_server
except ImportError:
    start_grpc_server = None  # type: ignore[assignment]

from Browser.entry.constant import (
    PLAYWRIGHT_BROWSERS_PATH,
    ensure_playwright_browsers_path,
)
from Browser.generated import playwright_pb2_grpc
from Browser.generated.playwright_pb2 import Request

from .base import LibraryComponent
from .utils import (
    AutoClosingLevel,
    PlaywrightLogTypes,
    close_process_tree,
    find_free_port,
    logger,
)

if TYPE_CHECKING:
    from .browser import Browser


class Playwright(LibraryComponent):
    """A wrapper for communicating with nodejs Playwright process."""

    port: str | None

    def __init__(
        self,
        library: "Browser",
        enable_playwright_debug: PlaywrightLogTypes | bool,
        host: str | None = None,
        port: int | None = None,
        playwright_log: Path | TextIO | None = Path(Path.cwd()),
    ):
        LibraryComponent.__init__(self, library)
        self.enable_playwright_debug = enable_playwright_debug
        self.ensure_node_dependencies()
        self.host = str(host) if host else None
        self.port = str(port) if port else None
        self.playwright_log = playwright_log

    @cached_property
    def _playwright_process(self) -> Popen | None:
        process = self.start_playwright()
        atexit.register(self.close)
        self.wait_until_server_up()
        if platform.system() == "Darwin":
            time.sleep(1)  # To overcome problem with macOS Sonoma and hanging process
        return process

    @cached_property
    def _rfbrowser_dir(self) -> Path:
        return Path(__file__).parent

    @cached_property
    def _browser_wrapper_dir(self) -> Path:
        return self._rfbrowser_dir / "wrapper"

    def ensure_node_dependencies(self):
        """Ensure that node dependencies are installed.

        If BrowserBatteries is installed, does nothing.
        """
        if start_grpc_server is not None:
            logger.trace(
                "Running gRPC server from BrowserBatteries, no need to check node"
            )
            return
        try:
            run(["node", "-v"], stdout=DEVNULL, check=True)
        except (CalledProcessError, FileNotFoundError, PermissionError) as err:
            raise RuntimeError(
                "Couldn't execute node. Please ensure you have node.js installed and in PATH. "
                "See https://nodejs.org/ for instructions. "
                f"Original error is {err}"
            )

        # This second application of .parent is necessary to find out that a developer setup has node_modules correctly
        project_folder = self._rfbrowser_dir.parent
        if any(
            [
                (project_folder / "node_modules").is_dir(),
                (self._browser_wrapper_dir / "node_modules").is_dir(),
            ]
        ):
            return

        raise RuntimeError(
            "\n#############################################################"
            "\n#                                                           #"  # noqa: RUF001
            "\n#  RF-Browser dependencies not found in installation path!  #"  # noqa: RUF001
            "\n#           Run `rfbrowser init` to install.                #"  # noqa: RUF001
            "\n#                                                           #"  # noqa: RUF001
            "\n#############################################################"
            f"\nInstallation path: {self._browser_wrapper_dir}"
        )

    def _get_logfile(self) -> TextIO:
        if isinstance(self.playwright_log, Path):
            return self.playwright_log.open("w", encoding="utf-8")
        if self.playwright_log is None:
            return Path(os.devnull).open("w", encoding="utf-8")
        return self.playwright_log

    def start_playwright(self) -> Popen | None:
        env_node_port = os.environ.get("ROBOT_FRAMEWORK_BROWSER_NODE_PORT")
        existing_port = self.port or env_node_port
        if existing_port is not None:
            self.port = existing_port
            if self.host is None:
                self.host = "127.0.0.1"
            if env_node_port is None:
                logger.trace(
                    f"Using previously saved or imported port {existing_port}, skipping Browser process start"
                )
            else:
                logger.trace(
                    f"ROBOT_FRAMEWORK_BROWSER_NODE_PORT {existing_port} defined in env, skipping Browser process start"
                )
            return None
        host = str(self.host) if self.host is not None else "127.0.0.1"
        port = str(find_free_port())
        self.host = host
        self.port = port
        if start_grpc_server is None:
            return self._start_playwright_from_node(self._get_logfile(), host, port)
        ensure_playwright_browsers_path()

        return start_grpc_server(
            self._get_logfile(), host, port, self.enable_playwright_debug
        )

    def _start_playwright_from_node(
        self, logfile: TextIO, host: str, port: str
    ) -> Popen:
        """Start Playwright from nodejs wrapper."""
        playwright_script = self._browser_wrapper_dir / "index.js"
        if self.enable_playwright_debug == PlaywrightLogTypes.playwright:
            os.environ["DEBUG"] = "pw:api"
        logger.info(
            f"Starting Browser process {playwright_script} using at {host}:{port}"
        )
        node_args = ["node"]
        node_debug_options = os.environ.get(
            "ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS"
        )
        if node_debug_options:
            node_args.extend(node_debug_options.split(","))
        node_args.append(str(playwright_script))
        node_args.append(host)
        node_args.append(port)
        if not os.environ.get(PLAYWRIGHT_BROWSERS_PATH):
            os.environ[PLAYWRIGHT_BROWSERS_PATH] = "0"
        logger.trace(f"Node startup parameters: {node_args}")
        return Popen(
            node_args,
            shell=False,
            cwd=self._browser_wrapper_dir,
            env=os.environ,
            stdout=logfile,
            stderr=STDOUT,
        )

    def wait_until_server_up(self):
        for _ in range(150):  # About 15 seconds
            logger.debug(
                f"Waiting for Playwright server at {self.host}:{self.port} to start..."
            )
            with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
                try:
                    stub = playwright_pb2_grpc.PlaywrightStub(channel)
                    response = stub.Health(Request().Empty())
                    logger.trace(
                        f"Connected to the playwright process at {self.host}:{self.port}: {response}"
                    )
                    return
                except grpc.RpcError as err:
                    logger.debug(err)
                    time.sleep(0.1)
        raise RuntimeError(
            f"Could not connect to the playwright process at {self.host}:{self.port}."
        )

    @cached_property
    def _channel(self):
        return grpc.insecure_channel(f"{self.host}:{self.port}")

    @contextlib.contextmanager
    def grpc_channel(self, original_error=False):
        """Yields a PlayWrightstub on a newly initialized channel

        Acts as a context manager, so channel is closed automatically when control returns.
        """
        playwright_process = self._playwright_process
        if playwright_process:
            returncode = playwright_process.poll()
            if returncode is not None:
                raise ConnectionError(
                    f"Playwright process has been terminated with code {returncode}"
                )
        try:
            yield playwright_pb2_grpc.PlaywrightStub(self._channel)
        except grpc.RpcError as error:
            if original_error:
                raise error
            raise AssertionError(error.details())
        except Exception as error:
            logger.debug(f"Unknown error received: {error}")
            raise AssertionError(str(error))

    def close(self):
        if self._auto_closing_level == AutoClosingLevel.KEEP:
            logger.debug(
                "Not closing browsers, contexts and pages. Also leaving node process running. "
                "Remember to remove manually all process left running."
            )
            return
        logger.trace("Closing all open browsers, contexts and pages in Playwright")
        try:
            with self.grpc_channel() as stub:
                response = stub.CloseAllBrowsers(Request().Empty())
                logger.debug(response.log)
            self._channel.close()
        except Exception as exc:
            logger.debug(f"Failed to close browsers: {exc}")
        try:
            with self.grpc_channel() as stub:
                response = stub.CloseBrowserServer(Request().ConnectBrowser(url="ALL"))
                logger.debug(response.log)
        except Exception as exc:
            logger.debug(f"Failed to close browser servers: {exc}")
        # Access (possibly) cached property without actually invoking it
        playwright_process = self.__dict__.get("_playwright_process")
        if playwright_process:
            logger.trace("Closing Playwright process tree")
            close_process_tree(playwright_process)
        else:
            logger.trace("Disconnected from external Playwright process")
