import json

from robot.api.deco import keyword

from Browser.base.librarycomponent import LibraryComponent
from Browser.generated.playwright_pb2 import Request


class ExamplePlugin(LibraryComponent):

    @keyword
    def new_plugin_cookie_keyword(self) -> dict:
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCookies(Request().Empty())
            cookies = json.loads(response.json)
        assert len(cookies) == 1, "Too many cookies."
        return {
            "name": cookies[0]["name"],
            "value": cookies[0]["value"]
        }
