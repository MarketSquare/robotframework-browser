import contextlib
import functools
import os
import socket
from subprocess import Popen, STDOUT
import time

import grpc  # type: ignore
from robot.api import logger  # type: ignore
from robot.libraries.BuiltIn import BuiltIn  # type: ignore

from Browser.generated.playwright_pb2 import Empty
import Browser.generated.playwright_pb2_grpc as playwright_pb2_grpc


class Playwright:
    """A wrapper for communicating with nodejs Playwirght process."""

    @property
    def outputdir(self):
        return BuiltIn().get_variable_value("${OUTPUTDIR}")

    @functools.cached_property
    def _playwright_process(self) -> Popen:
        process = self.start_playwright()
        self.wait_until_server_up()
        return process

    def start_playwright(self):
        workdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wrapper")
        playwright_script = os.path.join(workdir, "index.js")
        logfile = open(os.path.join(self.outputdir, "playwright-log.txt"), "w",)
        port = str(self.find_free_port())
        env = dict(os.environ)
        env["PORT"] = port
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
        for i in range(30):
            with grpc.insecure_channel(f"localhost:{self.port}") as channel:
                try:
                    stub = playwright_pb2_grpc.PlaywrightStub(channel)
                    response = stub.Health(Empty())
                    logger.info(
                        f"Connected to the playwright process at port {self.port}: {response}"
                    )
                    return
                except grpc.RpcError as err:
                    logger.info(err)
                    time.sleep(0.1)
        raise RuntimeError(
            f"Could not connect to the playwright process at port {self.port}"
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
        yield playwright_pb2_grpc.PlaywrightStub(channel)
        channel.close()

    def close(self):
        logger.debug("Closing Playwright process")
        self._playwright_process.kill()
        logger.debug("Playwright process killed")

    def find_free_port(self) -> str:
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(("", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]
