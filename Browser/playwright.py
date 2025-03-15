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
from typing import TYPE_CHECKING, Optional, Union

import grpc  # type: ignore

from Browser.generated import playwright_pb2_grpc
from Browser.generated.playwright_pb2 import Request

from .base import LibraryComponent
from .utils import AutoClosingLevel

if TYPE_CHECKING:
    from .browser import Browser

from .utils import PlaywrightLogTypes, find_free_port, logger


class Playwright(LibraryComponent):
    """A wrapper for communicating with nodejs Playwirght process."""

    port: Optional[str]

    def __init__(
        self,
        library: "Browser",
        enable_playwright_debug: Union[PlaywrightLogTypes, bool],
        port: Optional[int] = None,
        playwright_log: Union[Path, None] = Path(Path.cwd()),
    ):
        LibraryComponent.__init__(self, library)
        self.enable_playwright_debug = enable_playwright_debug
        self.ensure_node_dependencies()
        self.port = str(port) if port else None
        self.playwright_log = playwright_log

    @cached_property
    def _playwright_process(self) -> Optional[Popen]:
        process = self.start_playwright()
        atexit.register(self.close)
        self.wait_until_server_up()
        if platform.system() == "Darwin":
            time.sleep(1)  # To overcome problem with macOS Sonoma and hanging process
        return process

    def ensure_node_dependencies(self):
        # Checks if node is in PATH, errors if it isn't
        try:
            run(["node", "-v"], stdout=DEVNULL, check=True)
        except (CalledProcessError, FileNotFoundError, PermissionError) as err:
            raise RuntimeError(
                "Couldn't execute node. Please ensure you have node.js installed and in PATH. "
                "See https://nodejs.org/ for instructions. "
                f"Original error is {err}"
            )

        rfbrowser_dir = Path(__file__).parent
        installation_dir = rfbrowser_dir / "wrapper"
        # This second application of .parent is necessary to find out that a developer setup has node_modules correctly
        project_folder = rfbrowser_dir.parent
        if any(
            [
                (project_folder / "node_modules").is_dir(),
                (installation_dir / "node_modules").is_dir(),
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
            f"\nInstallation path: {installation_dir}"
        )

    def start_playwright(self) -> Optional[Popen]:
        env_node_port = os.environ.get("ROBOT_FRAMEWORK_BROWSER_NODE_PORT")
        existing_port = self.port or env_node_port
        if existing_port is not None:
            self.port = existing_port
            if env_node_port is None:
                logger.info(
                    f"Using previously saved or imported port {existing_port}, skipping Browser process start"
                )
            else:
                logger.info(
                    f"ROBOT_FRAMEWORK_BROWSER_NODE_PORT {existing_port} defined in env, skipping Browser process start"
                )
            return None
        current_dir = Path(__file__).parent
        workdir = current_dir / "wrapper"
        playwright_script = workdir / "index.js"
        if self.playwright_log:
            logfile = self.playwright_log.open("w", encoding="utf-8")
        else:
            logfile = Path(os.devnull).open("w", encoding="utf-8")  # noqa: SIM115
        port = str(find_free_port())
        if self.enable_playwright_debug == PlaywrightLogTypes.playwright:
            os.environ["DEBUG"] = "pw:api"
        logger.info(f"Starting Browser process {playwright_script} using port {port}")
        self.port = port
        node_args = ["node"]
        node_debug_options = os.environ.get(
            "ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS"
        )
        if node_debug_options:
            node_args.extend(node_debug_options.split(","))
        node_args.append(str(playwright_script))
        node_args.append(port)
        if not os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
        logger.info(f"Node startup parameters: {node_args}")
        return Popen(
            node_args,
            shell=False,
            cwd=workdir,
            env=os.environ,
            stdout=logfile,
            stderr=STDOUT,
        )

    def wait_until_server_up(self):
        for _ in range(150):  # About 15 seconds
            with grpc.insecure_channel(f"127.0.0.1:{self.port}") as channel:
                try:
                    stub = playwright_pb2_grpc.PlaywrightStub(channel)
                    response = stub.Health(Request().Empty())
                    logger.debug(
                        f"Connected to the playwright process at port {self.port}: {response}"
                    )
                    return
                except grpc.RpcError as err:
                    logger.debug(err)
                    time.sleep(0.1)
        raise RuntimeError(
            f"Could not connect to the playwright process at port {self.port}."
        )

    @cached_property
    def _channel(self):
        return grpc.insecure_channel(f"127.0.0.1:{self.port}")

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
        logger.debug("Closing all open browsers, contexts and pages in Playwright")
        try:
            with self.grpc_channel() as stub:
                response = stub.CloseAllBrowsers(Request().Empty())
                logger.info(response.log)
            self._channel.close()
        except Exception as exc:
            logger.debug(f"Failed to close browsers: {exc}")
        try:
            with self.grpc_channel() as stub:
                response = stub.CloseBrowserServer(Request().ConnectBrowser(url="ALL"))
                logger.info(response.log)
        except Exception as exc:
            logger.debug(f"Failed to close browser servers: {exc}")
        # Access (possibly) cached property without actually invoking it
        playwright_process = self.__dict__.get("_playwright_process")
        if playwright_process:
            logger.debug("Closing Playwright process")
            playwright_process.kill()
            logger.debug("Playwright process killed")
        else:
            logger.debug("Disconnected from external Playwright process")
