__version__ = "0.1.0"
import grpc  # type: ignore

from robot.api import logger  # type: ignore

import Playwright.generated.playwright_pb2 as playwright_pb2
import Playwright.generated.playwright_pb2_grpc as playwright_pb2_grpc

_SUPPORTED_BROWSERS = ["chrome", "firefox", "webkit"]


class Playwright:
    @staticmethod
    def open_browser(browser="Chrome", url=None):
        if url is None:
            url = "about:blank"
        browser_ = browser.lower().strip()
        if browser_ not in _SUPPORTED_BROWSERS:
            raise ValueError(
                f"{browser} is not supported, "
                f'it should be one of: {", ".join(_SUPPORTED_BROWSERS)}'
            )
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = playwright_pb2_grpc.PlaywrightStub(channel)
            for response in stub.OpenBrowser(
                playwright_pb2.openBrowserRequest(url=url, browser=browser_)
            ):
                logger.info(response.log)

    @staticmethod
    def close_browser():
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = playwright_pb2_grpc.PlaywrightStub(channel)
            response = stub.CloseBrowser(playwright_pb2.Empty())
            logger.info(response.log)
