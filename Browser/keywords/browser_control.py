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
import json
import os
from datetime import timedelta
from pathlib import Path
from typing import Optional

from robot.utils import get_link_path  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger
from ..utils.data_types import ScreenshotFileTypes


class Control(LibraryComponent):
    """Keywords to do things on the current browser page and modify the page"""

    @keyword(tags=("Setter", "BrowserControl"))
    def go_forward(self):
        """Navigates to the next page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoForward(Request.Empty())
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def go_back(self):
        """Navigates to the previous page in history."""
        with self.playwright.grpc_channel() as stub:
            response = stub.GoBack(Request.Empty())
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def go_to(self, url: str, timeout: Optional[timedelta] = None):
        """Navigates to the given ``url``.

        ``url`` <str> URL to be navigated to.
        ``timeout`` <str> time to wait page to load. If not defined
        will use the the library default timeout.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GoTo(
                Request().Url(url=url, defaultTimeout=int(self.get_timeout(timeout)))
            )
            logger.info(response.log)

    def _get_screenshot_path(self, filename: str, fileType: str) -> Path:
        if os.path.isabs(filename):
            d, file = os.path.split(filename)
            directory = Path(d)
            filename = os.path.splitext(file)[0]
        else:
            directory = self.screenshots_output
        # Filename didn't contain {index}
        if "{index}" not in filename:
            return directory / filename
        index = 0
        while True:
            index += 1
            indexed = Path(filename.replace("{index}", str(index)))
            logger.trace(indexed)
            path = directory / indexed
            # Unique path was found
            if not path.with_suffix(f".{fileType}").is_file():
                return path

    @keyword(tags=("PageContent",))
    def take_screenshot(
        self,
        filename: str = "robotframework-browser-screenshot-{index}",
        selector: str = "",
        fullPage: bool = False,
        fileType: ScreenshotFileTypes = ScreenshotFileTypes.png,
        quality: str = "",
        timeout: Optional[timedelta] = None,
    ) -> str:
        """Takes a screenshot of the current window and saves it.

        ``filename`` Filename into which to save. The file will be saved into the robot framework
         ${OUTPUTDIR}/browser/screenshot directory by default, but it can overwritten by providing
         custom path or filename. String ``{index}`` in filename will be replaced with a rolling
         number. Use this to not override filenames. If filename equals to EMBED (case insensitive),
         then screenshot is embedded as Base64 image to the log.html. The image is saved temporally
         to the disk and warning is displayed if removing the temporary file fails.
         If the filename is an absolute path, then filename is considered as an absolute path.

         The ${OUTPUTDIR}/browser/ is removed at the first suite startup.

        ``selector`` Take a screenshot of the element matched by selector.
        See the `Finding elements` section for details about the selectors.
        If not provided take a screenshot of current viewport.

        ``fullPage`` When True, takes a screenshot of the full scrollable page,
        instead of the currently visible viewport. Defaults to False.

        ``fileType`` <"png"|"jpeg"> Specify screenshot type, defaults to png.

        ``quality`` The quality of the image, between 0-100. Not applicable to png images.

        ``timeout`` Maximum time in milliseconds, defaults to 30 seconds, pass 0 to disable timeout.
        The default value can be changed by using the `Set Browser Timeout` keyword.
        """
        if self._is_embed(filename):
            logger.debug("Embedding image to log.html.")
        else:
            logger.debug(f"Using {filename} to take screenshot.")
        file_path = self._take_screenshot(
            filename, selector, fullPage, fileType, quality, timeout
        )
        if self._is_embed(filename):
            return self._embed_to_log(file_path)
        return self._log_image_link(file_path)

    def _log_image_link(self, file_path: str) -> str:
        relative_path = get_link_path(file_path, self.outputdir)
        logger.info(
            '</td></tr><tr><td colspan="3">'
            f'<a href="{relative_path}"><img src="{relative_path}" width="800px"></a>',
            html=True,
        )
        return file_path

    def _embed_to_log(self, file_path) -> str:
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

    def _take_screenshot(
        self,
        filename: str,
        selector: str = "",
        fullPage: bool = False,
        fileType: ScreenshotFileTypes = ScreenshotFileTypes.png,
        quality: str = "",
        timeout: Optional[timedelta] = None,
    ) -> str:
        string_path_no_extension = str(
            self._get_screenshot_path(filename, fileType.name)
        )
        with self.playwright.grpc_channel() as stub:
            response = stub.TakeScreenshot(
                Request().ScreenshotOptions(
                    path=string_path_no_extension,
                    selector=selector,
                    fullPage=fullPage,
                    fileType=fileType.name,
                    quality=quality,
                    timeout=int(self.get_timeout(timeout)),
                )
            )
        logger.debug(response.log)
        return response.body

    def _is_embed(self, filename: str) -> bool:
        return True if filename.upper() == "EMBED" else False

    @keyword(tags=("Setter", "Config"))
    def set_browser_timeout(self, timeout: timedelta) -> str:
        """Sets the timeout used by most input and getter keywords.

        ``timeout`` Timeout of it is for current playwright context.

        Returns the previous value of the timeout.
        """
        old_timeout = self.millisecs_to_timestr(self.timeout)
        self.timeout = self.convert_timeout(timeout)
        try:
            with self.playwright.grpc_channel() as stub:
                response = stub.SetTimeout(Request().Timeout(timeout=self.timeout))
                logger.info(response.log)
        except Exception as error:  # Suppress  all errors
            if "Browser has been closed" in str(error):
                logger.debug(f"Suppress error {error} when setting timeout.")
            else:
                raise
        return old_timeout

    @keyword(tags=("Setter", "Config"))
    def set_retry_assertions_for(self, timeout: timedelta) -> str:
        """Sets the timeout used in retrying assertions when they fail.

        ``timeout``

        Returns the previous value of the retry_assertions_until.
        """
        old_retry_assertions_for = self.millisecs_to_timestr(self.retry_assertions_for)
        self.retry_assertions_for = self.convert_timeout(timeout)
        return old_retry_assertions_for

    @keyword(tags=("Setter", "BrowserControl"))
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

        ``width`` Sets the width size.

        ``height`` Sets the heigth size.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SetViewportSize(
                Request().Viewport(height=height, width=width)
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def set_offline(self, offline: bool = True):
        """Toggles current Context's offline emulation.

        ``offline`` Toggles the offline mode. Set to False to switch back
        to online mode. Defaults to True.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SetOffline(Request().Bool(value=offline))
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def set_geolocation(
        self, latitude: float, longitude: float, accuracy: Optional[float] = None
    ):
        """Updated the correct Context's geolocation.

        Latitude can be between -90 and 90 and longitude can be between -180 and 180.
        """
        geolocation_dict = {"latitude": latitude, "longitude": longitude}
        if accuracy:
            geolocation_dict["accuracy"] = accuracy
        geolocation = json.dumps(geolocation_dict)
        logger.info(geolocation)
        with self.playwright.grpc_channel() as stub:
            response = stub.SetGeolocation(Request().Json(body=geolocation))
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def reload(self):
        """Reloads current active page."""
        with self.playwright.grpc_channel() as stub:
            response = stub.Reload(Request().Empty())
            logger.info(response.log)
