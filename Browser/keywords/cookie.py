from robotlibcore import keyword  # type: ignore

from Browser.base import LibraryComponent
from Browser.generated.playwright_pb2 import Request


class Cookie(LibraryComponent):
    @keyword
    def get_cookies(self):
        """Returns cookies from the current active browser context"""
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCookies(Request().Empty())
            self.info(response.log)
        return response.body
