import json
from pathlib import Path

from robot.api.deco import keyword
from robot.api import logger

from Browser.base.librarycomponent import LibraryComponent
from Browser.generated.playwright_pb2 import Request


class ExamplePlugin(LibraryComponent):
    def __init__(self, ctx: LibraryComponent):
        super().__init__(ctx)
        with ctx.playwright.grpc_channel() as stub:
            response = stub.InitializeExtension(
                Request().FilePath(
                    path=str(Path(__file__).parent.resolve() / "jsplugin.js")
                )
            )

    @keyword
    def new_plugin_cookie_keyword(self) -> dict:
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCookies(Request().Empty())
            cookies = json.loads(response.json)
        assert len(cookies) == 1, "Too many cookies."
        return {"name": cookies[0]["name"], "value": cookies[0]["value"]}

    @keyword
    def mouse_wheel(self, x: int, y: int):
        with self.playwright.grpc_channel() as stub:
            responses = stub.CallExtensionKeyword(
                Request().KeywordCall(
                    name="mouseWheel",
                    arguments=json.dumps(
                        {
                            "arguments": [
                                ("x", x),
                                ("y", y),
                                ("logger", "RESERVED"),
                                ("page", "RESERVED"),
                            ]
                        }
                    ),
                )
            )
            for response in responses:
                logger.info(response.log)
            if not response.json:
                return response.json
            return json.loads(response.json)
