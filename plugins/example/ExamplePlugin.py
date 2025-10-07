import json

from robot.api.deco import keyword  # Decorator to mark which methods are keyword

from Browser.base.librarycomponent import (
    LibraryComponent,  # Plugin class must always inherit LibraryComponent
)
from Browser.generated.playwright_pb2 import (
    Request,  # GRPC stub which is used to talk Playwright running in node side
)


class ExamplePlugin(LibraryComponent):  # Inherit LibraryComponent
    @keyword  # This method is keyword
    def new_plugin_cookie_keyword(self) -> dict:
        with self.playwright.grpc_channel() as stub:  # Open grpc channel.
            response = stub.GetCookies(
                Request().Empty()
            )  # Call the cookies implementation from Node side.
            cookies = json.loads(response.json)  # Get json payload from response.
        # Write Python code as you need, these lines are just examples.
        for cookie in cookies:
            if cookie["name"] == "Foo22":
                return {"name": cookie["name"], "value": cookie["value"]}
        return {}

    def now_keyword(self):  # This is not keyword
        print(1)
