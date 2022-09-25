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
from collections.abc import Iterable
from datetime import timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union

from robot.utils import get_link_path  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import Scope, keyword, logger
from ..utils.data_types import BoundingBox, Permission, ScreenshotFileTypes


class Control(LibraryComponent):
    """Keywords to do things on the current browser page and modify the page"""

    @keyword(tags=("Setter", "BrowserControl"))
    def go_forward(self):
        """Navigates to the next page in history.

        [https://forum.robotframework.org/t//4290|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GoForward(Request.Empty())
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def go_back(self):
        """Navigates to the previous page in history.

        [https://forum.robotframework.org/t//4289|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GoBack(Request.Empty())
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def go_to(self, url: str, timeout: Optional[timedelta] = None):
        """Navigates to the given ``url``.

        | =Arguments= | =Description= |
        | ``url`` | <str> URL to be navigated to. |
        | ``timeout`` | <str> time to wait page to load. If not defined will use the library default timeout. |

        [https://forum.robotframework.org/t//4291|Comment >>]
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
        selector: Optional[str] = None,
        fullPage: bool = False,
        fileType: ScreenshotFileTypes = ScreenshotFileTypes.png,
        quality: Optional[int] = None,
        timeout: Optional[timedelta] = None,
        crop: Optional[BoundingBox] = None,
        disableAnimations: bool = False,
        mask: Union[List[str], str] = "",
        omitBackground: bool = False,
    ) -> str:
        """Takes a screenshot of the current window or element and saves it to disk.

        | =Arguments= | =Description= |
        | ``filename`` | Filename into which to save. The file will be saved into the robot framework  ${OUTPUTDIR}/browser/screenshot directory by default, but it can overwritten by providing  custom path or filename. String ``{index}`` in filename will be replaced with a rolling  number. Use this to not override filenames. If filename equals to EMBED (case insensitive),  then screenshot is embedded as Base64 image to the log.html. The image is saved temporally  to the disk and warning is displayed if removing the temporary file fails. The ${OUTPUTDIR}/browser/ is removed at the first suite startup. |
        | ``selector`` | Take a screenshot of the element matched by selector. See the `Finding elements` section for details about the selectors. If not provided take a screenshot of current viewport. |
        | ``fullPage`` | When True, takes a screenshot of the full scrollable page, instead of the currently visible viewport. Defaults to False. |
        | ``fileType`` | <"png"|"jpeg"> Specify screenshot type, defaults to png. |
        | ``quality`` | The quality of the image, between 0-100. Not applicable to png images. |
        | ``timeout`` | Maximum time how long taking screenshot can last, defaults to library timeout. Supports Robot Framework time format, like 10s or 1 min, pass 0 to disable timeout. The default value can be changed by using the `Set Browser Timeout` keyword. |
        | ``crop`` | Crops the taken screenshot to the given box. It takes same dictionary as returned from `Get BoundingBox`. Cropping only works on page screenshot, so if no selector is given. |
        | ``disableAnimations`` | When set to ``True``, stops CSS animations, CSS transitions and Web Animations. Animations get different treatment depending on their duration:  - finite animations are fast-forwarded to completion, so they'll fire transitionend event.  - infinite animations are canceled to initial state, and then played over after the screenshot. |
        | ``mask`` | Specify selectors that should be masked when the screenshot is taken. Masked elements will be overlayed with a pink box ``#FF00FF`` that completely covers its bounding box. Argument can take a single selector string or a list of selector strings if multiple different elements should be masked. |
        | ``omitBackground`` | Hides default white background and allows capturing screenshots with transparency. Not applicable to jpeg images. |

        Keyword uses strict mode if selector is defined. See `Finding elements` for more details
        about strict mode.

        Example
        | `Take Screenshot`                                 # Takes screenshot from page with default filename
        | `Take Screenshot`   selector=id=username_field    # Captures element in image
        | # Takes screenshot with jpeg extension, defines image quality and timeout how long taking screenhost should last
        | `Take Screenshot`   fullPage=True    fileType=jpeg    quality=50    timeout=10s

        [https://forum.robotframework.org/t//4337|Comment >>]
        """
        if self._is_embed(filename):
            logger.debug("Embedding image to log.html.")
        else:
            logger.debug(f"Using {filename} to take screenshot.")
        string_path_no_extension = str(
            self._get_screenshot_path(filename, fileType.name)
        )
        with self.playwright.grpc_channel() as stub:
            options = {
                "path": f"{string_path_no_extension}.{fileType.name}",
                "fileType": fileType.name,
                "fullPage": fullPage,
                "timeout": int(self.get_timeout(timeout)),
                "omitBackground": omitBackground,
            }
            if mask:
                mask_selectors: Optional[List[str]]
                if isinstance(mask, str):
                    mask_selectors = [self.resolve_selector(mask)]
                elif isinstance(mask, Iterable):
                    mask_selectors = [self.resolve_selector(str(s)) for s in mask]
                else:
                    raise ValueError(
                        f"'mask' argument is neither string nor list of string. It is {type(mask)}"
                    )
            else:
                mask_selectors = None

            if quality is not None:
                options["quality"] = max(min(100, quality), 0)
            if disableAnimations:
                options["animations"] = "disabled"
            if crop:
                options["clip"] = crop
            response = stub.TakeScreenshot(
                Request().ScreenshotOptions(
                    selector=self.resolve_selector(selector) or "",
                    mask=json.dumps(mask_selectors),
                    options=json.dumps(options),
                    strict=self.strict_mode,
                )
            )
            logger.debug(response.log)
            file_path = response.body

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

    def _is_embed(self, filename: str) -> bool:
        return True if filename.upper() == "EMBED" else False

    @keyword(tags=("Setter", "Config"))
    def set_browser_timeout(
        self, timeout: timedelta, scope: Scope = Scope.Suite
    ) -> str:
        """Sets the timeout used by most input and getter keywords.

        | =Arguments= | =Description= |
        | ``timeout`` | Timeout of it is for current playwright context and for new contexts. Supports Robot Framework [https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#time-format|time format] . Returns the previous value of the timeout. |
        | ``scope``   | Scope defines the live time of that setting. Available values are ``Global``, ``Suite`` or ``Test``/``Task``. See `Scope Settings` for more details. |

        Example:
        | ${old_timeout} =    `Set Browser Timeout`    1m 30 seconds
        | Click     //button
        | `Set Browser Timeout`    ${old_timeout}

        [https://forum.robotframework.org/t//4328|Comment >>]
        """
        old_timeout = self.millisecs_to_timestr(self.timeout)
        self.timeout_stack.set(self.convert_timeout(timeout), scope)
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
    def set_retry_assertions_for(
        self, timeout: timedelta, scope: Scope = Scope.Suite
    ) -> str:
        """Sets the timeout used in retrying assertions when they fail.

        | =Arguments= | =Description= |
        | ``timeout`` | Assertion retry timeout will determine how long Browser library will retry an assertion to be true. |
        | ``scope``   | Scope defines the live time of that setting. Available values are ``Global``, ``Suite`` or ``Test``/``Task``. See `Scope` for more details. |

        The other keyword `Set Browser timeout` controls how long Playwright
        will perform waiting in the node side for Elements to fulfill the
        requirements of the specific keyword.

        Returns the previous value of the assertion retry timeout.

        Example:
        | `Set Browser Timeout`    10 seconds
        | ${old} =    `Set Retry Assertions For`    30s
        | `Get Title`    ==    Login Page
        | `Set Retry Assertions For`    ${old}

        Example waits 10 seconds on Playwright to get the page title and library
        will retry 30 seconds to make sure that title is correct.

        [https://forum.robotframework.org/t//4331|Comment >>]
        """
        old_retry_assertions_for = self.millisecs_to_timestr(self.retry_assertions_for)
        self.retry_assertions_for_stack.set(self.convert_timeout(timeout), scope)
        return old_retry_assertions_for

    @keyword(tags=("Setter", "Config"))
    def set_selector_prefix(
        self, prefix: Optional[str], scope: Scope = Scope.Suite
    ) -> str:
        """Sets the prefix for all selectors in the given scope.

        | =Arguments= | =Description= |
        | ``prefix``   | Prefix for all selectors. Prefix and selector will be separated by a single space. |
        | ``scope``   | Scope defines the live time of that setting. Available values are ``Global``, ``Suite`` or ``Test``/``Task``. See `Scope` for more details. |

        Returns the previous value of the prefix.

        Example:
        | ${old} =    `Set Selector Prefix`    iframe#embedded_page >>>
        | `Click`    button#login_btn       # Clicks on button inside iframe with the selector ``iframe#embedded_page >>> button#login_btn``
        | `Set Selector Prefix`    ${old}

        Example will click on button with id ``login_btn`` inside iframe with id ``embedded_page``.
        The resulting selector will be ``iframe#embedded_page >>> button#login_btn``.

        [https://forum.robotframework.org/t//4330|Comment >>]
        """
        old_prefix = self.selector_prefix
        self.selector_prefix_stack.set(prefix or "", scope)
        return old_prefix

    @keyword(tags=("Setter", "Config"))
    def show_keyword_banner(
        self, show: bool = True, style: str = ""
    ) -> Dict[str, Union[None, bool, str]]:
        """Controls if the keyword banner is shown on page or not.

        Keyword call banner is a css overlay that shows the currently executed keyword directly on page.
        This is useful for debugging and for showing the test execution on video recordings.
        By default, the banner is not shown on page except when running in presenter mode.

        The banner can be controlled by an import setting of Browser library. (see `Importing` section)

        | =Arguments= | =Description= |
        | ``show`` | If `True` banner is shown on page. If `False` banner is not shown on page. If `None` banner is shown on page only when running in presenter mode. |
        | ``style`` | Additional css styles to be applied to the banner. These styles are css settings and may override the existing ones for the banner. |


        Example:
        | Show Keyword Banner     True    top: 5px; bottom: auto; left: 5px; background-color: #00909077; font-size: 9px; color: black;   # Show banner on top left corner with custom styles
        | Show Keyword Banner     False   # Hide banner

        [https://forum.robotframework.org/t//4716|Comment >>]
        """
        original_state = self.library.show_keyword_call_banner
        original_style = self.library.keyword_call_banner_add_style
        self.library.show_keyword_call_banner = show
        self.library.keyword_call_banner_add_style = style
        if not show:
            self.library.set_keyword_call_banner()
        return {"show": original_state, "style": original_style}

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

        | =Arguments= | =Description= |
        | ``width`` | Sets the width size. |
        | ``height`` | Sets the height size. |

        [https://forum.robotframework.org/t//4333|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SetViewportSize(
                Request().Viewport(height=height, width=width)
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def set_offline(self, offline: bool = True):
        """Toggles current Context's offline emulation.

        | =Arguments= | =Description= |
        | ``offline`` | Toggles the offline mode. Set to False to switch back to online mode. Defaults to True. |

        [https://forum.robotframework.org/t//4330|Comment >>]
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
        Accuracy of the location must be positive number and defaults to 0. When
        creating context, grant ``geolocation`` permission for pages to read its geolocation.

        | =Arguments= | =Description= |
        | ``latitude`` | Latitude between -90 and 90. |
        | ``longitude`` | Longitude between -180 and 180. |
        | ``accuracy`` | Non-negative accuracy value. Defaults to 0. |

        Example:
        | ${permissions} =    Create List    geolocation
        | `New Context`    permissions=${permissions}
        | `Set Geolocation`    60.173708, 24.982263    3    # Points to Korkeasaari in Helsinki.

        [https://forum.robotframework.org/t//4329|Comment >>]
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
        """Reloads current active page.

        [https://forum.robotframework.org/t//4317|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.Reload(Request().Empty())
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def grant_permissions(self, *permissions: Permission, origin: Optional[str] = None):
        """Grants permissions to the current context.

        | =Arguments= | =Description= |
        | ``permissions`` | is a list of permissions to grant. Permissions can be one of the following: geolocation, notifications, camera, microphone, |
        | ``origin`` | The origin to grant permissions to, e.g. "https://example.com". |

        Example:
        | `New Context`
        | `Grant Permissions`    geolocation

        [https://forum.robotframework.org/t//4292|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GrantPermissions(
                Request().Permissions(
                    permissions=[p.name for p in permissions], origin=origin or ""
                )
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "BrowserControl"))
    def clear_permissions(self):
        """Clears all permissions from the current context.

        [https://forum.robotframework.org/t//4236|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ClearPermissions(Request().Empty())
            logger.info(response.log)
