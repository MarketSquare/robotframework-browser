from robotlibcore import keyword  # type: ignore

from Browser.base import LibraryComponent
from Browser.generated.playwright_pb2 import Request
from Browser.utils import logger


class Cookie(LibraryComponent):
    @keyword
    def get_cookies(self):
        """Returns cookies from the current active browser context"""
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCookies(Request().Empty())
            cookie_names = response.log
            if not cookie_names:
                logger.info('No cookies found.')
            else:
                logger.info(f'Found cookies: {response.log}')
        return response.body
