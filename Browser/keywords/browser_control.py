# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import base64
from pathlib import Path

from robot.utils import get_link_path  # type: ignore
from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.time_conversion import timestr_to_millisecs


class Control(LibraryComponent):
    """Keywords to do things on the current browser page and modify the page"""

    @keyword(tags=["Setter", "BrowserControl"])
    def go_forward(self):
        """Navigates to the next page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoForward(Request.Empty())
            logger.info(response.log)

    @keyword(tags=["Setter", "BrowserControl"])
    def go_back(self):
        """Navigates to the previous page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoBack(Request.Empty())
            logger.info(response.log)

    @keyword(tags=["Setter", "BrowserControl"])
    def go_to(self, url: str):
        """Navigates to the given ``url``.

        ``url`` <str> URL to be navigated to. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GoTo(Request().Url(url=url))
            logger.info(response.log)

    def _get_screenshot_path(self, filename: str) -> Path:
        directory = self.library.outputdir
        # Filename didn't contain {index}
        if "{index}" not in filename:
            return Path(directory) / filename
        index = 0
        while True:
            index += 1
            indexed = Path(filename.replace("{index}", str(index)))
            logger.trace(indexed)
            path = Path(directory) / indexed
            # Unique path was found
            if not path.with_suffix(".png").is_file():
                return path

    @keyword(tags=["PageContent"])
    def take_screenshot(
        self,
        filename: str = "robotframework-browser-screenshot-{index}",
        selector: str = "",
    ):
        """Takes a screenshot of the current window and saves it to ``path``. Saves it as a png.

        ``filename`` <str> Filename into which to save. The file will be saved into the robot framework output
        directory by default. String ``{index}`` in path will be replaced with a rolling number. Use this to not
        override filenames. If filename equals to EMBED (case insensitive), then screenshot is embedded as
        Base64 image to the log.html. The image is saved temporally to the disk and warning is displayed
        if removing the temporary file fails.

        ``selector`` <str> Take a screenshot of the element matched by selector.
        If not provided take a screenshot of current viewport.
        """
        if self._is_embed(filename):
            logger.debug("Embedding image to log.html.")
        else:
            logger.debug(f"Using {filename} to take screenshot.")
        file_path = self._take_screenshot(filename, selector)
        if self._is_embed(filename):
            return self._emmed_to_log(file_path)
        return self._log_image_link(file_path)

    def _log_image_link(self, file_path: str) -> str:
        relative_path = get_link_path(file_path, self.library.outputdir)
        logger.info(
            f"Saved screenshot in <a href='{relative_path}'>{relative_path}</a>",
            html=True,
        )
        return file_path

    def _emmed_to_log(self, file_path):
        png = Path(file_path)
        with png.open("rb") as png_file:
            encoded_string = base64.b64encode(png_file.read())
        # log statement is copied from:
        # https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/keywords/screenshot.py
        logger.info(
            '</td></tr><tr><td colspan="3">'
            '<img alt="screenshot" class="robot-seleniumlibrary-screenshot" '
            f'src="data:image/png;base64,{encoded_string.decode()}" width="900px">',
            html=True,
        )
        try:
            png.unlink()
        except Exception:
            logger.warn(f"Could not remove {png}")
        return "EMBED"

    def _take_screenshot(self, filename: str, selector: str) -> str:
        string_path_no_extension = str(self._get_screenshot_path(filename))
        with self.playwright.grpc_channel() as stub:
            response = stub.TakeScreenshot(
                Request().ScreenshotOptions(
                    path=string_path_no_extension, selector=selector
                )
            )
        logger.debug(response.log)
        return response.body

    def _is_embed(self, filename: str) -> bool:
        return True if filename.upper() == "EMBED" else False

    @keyword(tags=["Setter", "Config"])
    def set_browser_timeout(self, timeout: str) -> str:
        """Sets the timeout used by most input and getter keywords.

        ``timeout`` <str> Timeout of it is for current playwright context. **Required**

        Returns the previous value of the timeout.
        """
        parsed_timeout = timestr_to_millisecs(timeout)
        old_timeout = self.timeout
        self.timeout = timeout
        with self.playwright.grpc_channel() as stub:
            response = stub.SetTimeout(Request().Timeout(timeout=parsed_timeout))
            logger.info(response.log)
        return old_timeout

    @keyword(tags=["Setter", "Config"])
    def set_retry_assertions_for(self, timeout: str) -> str:
        """Sets the timeout used in retrying assertions when they fail.

        ``timeout`` <str>

        Returns the previous value of the retry_assertions_until.
        """
        old_retry_assertions_for = self.retry_assertions_for
        self.retry_assertions_for = timeout
        return old_retry_assertions_for

    @keyword(tags=["Setter", "BrowserControl"])
    def set_viewport_size(self, width: int, height: int):
        """Sets current Pages viewport size to specified dimensions.

        In the case of multiple pages in a single browser,
        each page can have its own viewport size. However,
        `New Context` allows to set viewport size (and more) for all
        later opened pages in the context at once.

        `Set Viewport Size` will resize the page.
        A lot of websites don't expect phones to change size,
        so you should set the viewport size before navigating to
        the page with `New Context` before opening the page itself.

        ``width`` <int> Sets the width size. **Required**

        ``height`` <int> Sets the heigth size. **Required**
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SetViewportSize(
                Request().Viewport(height=height, width=width)
            )
            logger.info(response.log)

    @keyword(tags=["Setter", "BrowserControl"])
    def set_offline(self, offline: bool = True):
        """Toggles current Context's offline emulation.

        ``offline`` <bool> Toggles the offline mode. Set to False to switch back
        to online mode. Defaults to True.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SetOffline(Request().Bool(value=offline))
            logger.info(response.log)

    @keyword(tags=["Setter", "BrowserControl"])
    def reload(self):
        """Reloads current active page."""
        with self.playwright.grpc_channel() as stub:
            response = stub.Reload(Request().Empty())
            logger.info(response.log)
