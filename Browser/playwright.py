import contextlib
import functools
import os
import socket
import time
from subprocess import STDOUT, Popen

import grpc  # type: ignore
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS, BuiltIn  # type: ignore

import Browser.generated.playwright_pb2_grpc as playwright_pb2_grpc
from Browser.generated.playwright_pb2 import Request
from Browser.utils import logger
from Browser.utils.time_conversion import timestr_to_millisecs


class Playwright:
    """A wrapper for communicating with nodejs Playwirght process."""

    def __init__(self, timeout: str, enable_playwright_debug: bool):
        self.timeout = timeout
        self.enable_playwright_debug = enable_playwright_debug

    @property
    def outputdir(self):
        if EXECUTION_CONTEXTS.current:
            return BuiltIn().get_variable_value("${OUTPUTDIR}")
        else:
            return "."

    @functools.cached_property
    def _playwright_process(self) -> Popen:
        process = self.start_playwright()
        self.wait_until_server_up()
        return process

    def start_playwright(self):
        workdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wrapper")
        playwright_script = os.path.join(workdir, "index.js")
        logfile = open(os.path.join(self.outputdir, "playwright-log.txt"), "w")
        port = str(self.find_free_port())
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

    def find_free_port(self) -> str:
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(("", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]
