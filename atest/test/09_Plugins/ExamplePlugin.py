import json
from pathlib import Path

from robot.api import logger
from robot.api.deco import keyword

from Browser import Browser
from Browser.base.librarycomponent import LibraryComponent
from Browser.generated.playwright_pb2 import Request


class ExamplePlugin(LibraryComponent):
    def __init__(self, ctx: Browser):
        super().__init__(ctx)
        self.initialize_js_extension(Path(__file__).parent.resolve() / "jsplugin.js")

    @keyword
    def new_plugin_cookie_keyword(self) -> dict:
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCookies(Request().Empty())
            cookies = json.loads(response.json)
        assert len(cookies) == 1, "Too many cookies."
        return {"name": cookies[0]["name"], "value": cookies[0]["value"]}

    @keyword
    def mouse_wheel(self, x: int, y: int):
        return self.call_js_keyword("mouseWheel", x=x, y=y, logger=None, page=None)
