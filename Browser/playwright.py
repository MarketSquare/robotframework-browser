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

import contextlib
import os
import time
from pathlib import Path
from subprocess import DEVNULL, STDOUT, CalledProcessError, Popen, run
from typing import TYPE_CHECKING

import grpc  # type: ignore
from backports.cached_property import cached_property
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS, BuiltIn  # type: ignore

import Browser.generated.playwright_pb2_grpc as playwright_pb2_grpc
from Browser.generated.playwright_pb2 import Request

from .base import LibraryComponent

if TYPE_CHECKING:
    from .browser import Browser

from .utils import find_free_port, logger, timestr_to_millisecs


class Playwright(LibraryComponent):
    """A wrapper for communicating with nodejs Playwirght process."""

    def __init__(self, library: "Browser", enable_playwright_debug: bool):
        LibraryComponent.__init__(self, library)
        self.enable_playwright_debug = enable_playwright_debug
        self.ensure_node_dependencies()

    @property
    def outputdir(self):
        if EXECUTION_CONTEXTS.current:
            return BuiltIn().get_variable_value("${OUTPUTDIR}")
        else:
            return "."

    @cached_property
    def _playwright_process(self) -> Popen:
        process = self.start_playwright()
        self.wait_until_server_up()
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
        subfolders = os.listdir(project_folder) + os.listdir(installation_dir)

        if "node_modules" in subfolders:
            return
        raise RuntimeError(
            f"Could not find node dependencies in installation directory `{installation_dir}.` "
            "Run `rfbrowser init` to install the dependencies."
        )

    def start_playwright(self):
        workdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wrapper")
        playwright_script = os.path.join(workdir, "index.js")
        logfile = open(os.path.join(self.outputdir, "playwright-log.txt"), "w")
        port = str(find_free_port())
        env = dict(os.environ)
        env["PORT"] = port
        env["TIMEOUT"] = str(timestr_to_millisecs(self.timeout))
        if self.enable_playwright_debug:
            env["DEBUG"] = "pw:api"
        logger.info(f"Starting Browser process {playwright_script} using port {port}")
        self.port = port
        return Popen(
            ["node", playwright_script],
            shell=False,
            cwd=workdir,
            env=env,
            stdout=logfile,
            stderr=STDOUT,
        )

    def wait_until_server_up(self):
        for i in range(50):
            with grpc.insecure_channel(f"localhost:{self.port}") as channel:
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

    @contextlib.contextmanager
    def grpc_channel(self):
        """Yields a PlayWrightstub on a newly initialized channel

        Acts as a context manager, so channel is closed automatically when control returns.
        """
        returncode = self._playwright_process.poll()
        if returncode is not None:
            raise ConnectionError(
                "Playwright process has been terminated with code {}".format(returncode)
            )
        channel = grpc.insecure_channel(f"localhost:{self.port}")
        try:
            yield playwright_pb2_grpc.PlaywrightStub(channel)
        except Exception as e:
            raise AssertionError(self.get_reason(e))
        finally:
            channel.close()

    def get_reason(self, err):
        try:
            metadata = err.trailing_metadata()
            for element in metadata:
                if element.key == "reason":
                    return element.value
        except AttributeError:
            pass
        try:
            return err.details()
        except TypeError:
            return err.details
        except AttributeError:
            pass
        return str(err)

    def close(self):
        logger.debug("Closing all open browsers, contexts and pages in Playwright")
        with self.grpc_channel() as stub:
            response = stub.CloseAllBrowsers(Request().Empty())
            logger.info(response.log)

        logger.debug("Closing Playwright process")
        self._playwright_process.kill()
        logger.debug("Playwright process killed")
