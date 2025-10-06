import json
from pathlib import Path

from robot.api import logger
from robot.api.deco import keyword
from robot.utils import DotDict

from Browser import Browser
from Browser.base.librarycomponent import LibraryComponent
from Browser.generated.playwright_pb2 import Request
from Browser.utils import Scope, SettingsStack


class ExamplePlugin(LibraryComponent):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, library: Browser):
        super().__init__(library)
        self.initialize_js_extension(Path(__file__).parent.resolve() / "jsplugin.js")
        library.scope_stack["last_log_message"] = SettingsStack("", library)

    def end_keyword(self, _kw, _args):
        msg = self.library.scope_stack["last_log_message"].get()
        if msg:
            logger.info(msg)

    @keyword
    def set_last_log_message(self, msg: str, scope: Scope):
        self.library.scope_stack["last_log_message"].set(msg, scope)

    @keyword
    def new_plugin_cookie_keyword(self) -> dict:
        """Uses grpc to directly call node side function."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCookies(Request().Empty())
            cookies = json.loads(response.json)
        assert len(cookies) == 1, "Too many cookies."
        return {"name": cookies[0]["name"], "value": cookies[0]["value"]}

    @keyword
    def get_location_object(self) -> dict:
        """Returns the location object of the current page.

        This keyword calles the python keyword `Evaluate Javascript` to get the location object.
        """
        location_dict = self.library.evaluate_javascript(None, "window.location")
        logger.info(f"Location object:\n {json.dumps(location_dict, indent=2)}")
        return DotDict(location_dict)

    @keyword
    def mouse_wheel(self, x: int, y: int):
        """This keyword calls a custom javascript keyword from the file jsplugin.js."""
        return self.call_js_keyword("mouseWheel", y=y, x=x)
