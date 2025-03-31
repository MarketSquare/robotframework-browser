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

import json
from datetime import datetime, timezone
from typing import Optional, Union

from robot.libraries.DateTime import convert_date
from robot.utils import DotDict

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import CookieSameSite, CookieType, keyword, locals_to_params, logger


class Cookie(LibraryComponent):
    @keyword(tags=("Getter", "PageContent"))
    def get_cookies(
        self, return_type: CookieType = CookieType.dictionary
    ) -> Union[list[DotDict], str]:
        """Returns cookies from the current active browser context.

        If ``return_type`` is ``dictionary`` or ``dict`` then keyword returns list of Robot Framework
        [https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#accessing-list-and-dictionary-items|dot dictionaries]
        The dictionary contains all possible key value pairs of the cookie. See `Get Cookie` keyword documentation
        about the dictionary keys and values.

        If ``return_type`` is ``string`` or ``str``, then keyword returns the cookie as a string in format:
        ``name1=value1; name2=value2; name3=value3``. The return value contains only ``name`` and ``value`` keys of the
        cookie.

        [https://forum.robotframework.org/t//4266|Comment >>]
        """
        response, cookies = self._get_cookies()
        if not response.log:
            logger.info("No cookies found.")
            return []
        logger.info(f"Found cookies: {response.log}")
        if return_type is CookieType.dictionary:
            return self._format_cookies_as_dot_dict(cookies)
        return self._format_cookies_as_string(cookies)

    def _get_cookies(self):
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCookies(Request().Empty())
            return response, json.loads(response.json)

    def _format_cookies_as_string(self, cookies: list[dict]):
        pairs = []
        for cookie in cookies:
            pairs.append(self._cookie_as_string(cookie))
        return "; ".join(pairs)

    def _cookie_as_string(self, cookie: dict) -> str:
        return f"{cookie['name']}={cookie['value']}"

    def _format_cookies_as_dot_dict(self, cookies: list[dict]):
        as_list = []
        for cookie in cookies:
            as_list.append(self._cookie_as_dot_dict(cookie))
        return as_list

    def _cookie_as_dot_dict(self, cookie):
        dot_dict = DotDict()
        for key in cookie:
            if key == "expires":
                # In Windows OS, expires value might be -1 and it causes OSError.
                try:
                    dot_dict[key] = datetime.fromtimestamp(cookie[key], tz=timezone.utc)
                except OSError:
                    logger.debug(
                        f"Invalid expiry seen in: {cookie}, setting expiry as None"
                    )
                    dot_dict[key] = None
            else:
                dot_dict[key] = cookie[key]
        return dot_dict

    @keyword(tags=("Setter", "BrowserControl"))
    def add_cookie(
        self,
        name: str,
        value: str,
        url: Optional[str] = None,
        domain: Optional[str] = None,
        path: Optional[str] = None,
        expires: Optional[str] = None,
        httpOnly: Optional[bool] = None,
        secure: Optional[bool] = None,
        sameSite: Optional[CookieSameSite] = None,
    ):
        """Adds a cookie to currently active browser context.


        | =Arguments= | =Description= |
        | ``name`` | Name of the cookie. |
        | ``value`` | Given value for the cookie. |
        | ``url`` | Given url for the cookie. Defaults to None. Either ``url`` or ``domain`` / ``path`` pair must be set. |
        | ``domain`` | Given domain for the cookie. Defaults to None. Either ``url`` or ``domain`` / ``path`` pair must be set. |
        | ``path`` | Given path for the cookie. Defaults to None. Either ``url`` or ``domain`` / ``path`` pair must be set. |
        | ``expires`` | Given expiry for the cookie. Can be of date format or unix time. Supports the same formats as the [http://robotframework.org/robotframework/latest/libraries/DateTime.html|DateTime] library or an epoch timestamp. - example: 2027-09-28 16:21:35 |
        | ``httpOnly`` | Sets the httpOnly token. |
        | ``secure`` | Sets the secure token. |
        | ``samesite`` | Sets the samesite mode. |

        Example:
        | `Add Cookie`   foo   bar   http://address.com/path/to/site                                     # Using url argument.
        | `Add Cookie`   foo   bar   domain=example.com                path=/foo/bar                     # Using domain and url arguments.
        | `Add Cookie`   foo   bar   http://address.com/path/to/site   expires=2027-09-28 16:21:35       # Expires as timestamp.
        | `Add Cookie`   foo   bar   http://address.com/path/to/site   expires=1822137695                # Expires as epoch seconds.

        [https://forum.robotframework.org/t//4233|Comment >>]
        """
        params = locals_to_params(locals())
        if expires:
            params["expires"] = self._expiry(expires)
        cookie_json = json.dumps(params)
        logger.debug(f"Adding cookie: {cookie_json}")
        with self.playwright.grpc_channel() as stub:
            response = stub.AddCookie(Request.Json(body=cookie_json))
            logger.info(response.log)

    def _expiry(self, expiry: str) -> int:
        try:
            expiry_cleaned = str(expiry).replace(" ", "")
            if "," in expiry_cleaned and "." in expiry_cleaned:
                expiry_cleaned = expiry_cleaned[
                    : max(expiry_cleaned.find("."), expiry_cleaned.find(","))
                ]
            elif "," in expiry_cleaned:
                expiry_cleaned = expiry_cleaned.rsplit(",", maxsplit=1)[0]
            elif "." in expiry_cleaned:
                expiry_cleaned = expiry_cleaned.rsplit(".", maxsplit=1)[0]
            return int(expiry_cleaned)
        except ValueError:
            return int(convert_date(expiry, result_format="epoch"))

    @keyword(tags=("Setter", "BrowserControl"))
    def delete_all_cookies(self):
        """Deletes all cookies from the currently active browser context.

        [https://forum.robotframework.org/t//4244|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.DeleteAllCookies(Request.Empty())
        logger.info(response.log)

    @keyword
    def eat_all_cookies(self):
        """Eat all cookies for all easter.

        [https://forum.robotframework.org/t//4250|Comment >>]
        """
        self.delete_all_cookies()
        logger.info(
            """
        <iframe
        width="560" height="315"
        src="https://www.youtube.com/embed/I5e6ftNpGsU"
        frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen>
        </iframe>""",
            html=True,
        )
        logger.warn("Cookie monster ate all cookies!!")

    @keyword(tags=("Getter", "BrowserControl"))
    def get_cookie(
        self, cookie: str, return_type: CookieType = CookieType.dictionary
    ) -> Union[DotDict, str]:
        """Returns information of cookie with ``name`` as a Robot Framework dot dictionary or a string.

        | =Arguments= | =Description= |
        | ``cookie`` | Name of the cookie to be retrieved. |
        | ``return_type`` | Type of the return value. Can be either ``dictionary`` or ``string``. Defaults to ``dictionary``. |

        If ``return_type`` is ``dictionary`` or ``dict`` then keyword returns a of Robot Framework
        [https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#accessing-list-and-dictionary-items|dot dictionary]
        The dictionary contains all possible key value pairs of the cookie. If ``return_type`` is ``string`` or ``str``,
        then keyword returns the cookie as a string in format: ``name1=value1``. The return value contains only
        ``name`` and ``value`` keys of the cookie.

        If no cookie is found with ``name`` keyword fails. The cookie dictionary contains
        details about the cookie. Keys available in the dictionary are documented in the table below.

        | *Value*  | *Explanation*                                                                              |
        | name     | The name of a cookie, mandatory.                                                           |
        | value    | Value of the cookie, mandatory.                                                            |
        | url      | Define the scope of the cookie, what URLs the cookies should be sent to.                   |
        | domain   | Specifies which hosts are allowed to receive the cookie.                                   |
        | path     | Indicates a URL path that must exist in the requested URL, for example `/`.                |
        | expires  | Lifetime of a cookie. Returned as datatime object or None if not valid time received.      |
        | httpOnly | When true, the cookie is not accessible via JavaScript.                                    |
        | secure   | When true, the cookie is only used with HTTPS connections.                                 |
        | sameSite | Attribute lets servers require that a cookie shouldn't be sent with cross-origin requests. |

        See
        [https://playwright.dev/docs/api/class-browsercontext#browsercontextaddcookiescookies|playwright documentation]
        for details about each attribute.

        Example:
        | ${cookie}=        `Get Cookie`              Foobar
        | Should Be Equal   ${cookie.value}           Tidii
        | Should Be Equal   ${cookie.expires.year}     ${2020}

        [https://forum.robotframework.org/t//4265|Comment >>]
        """
        _, cookies = self._get_cookies()
        for cookie_dict in cookies:
            if cookie_dict["name"] == cookie:
                if return_type is CookieType.dictionary:
                    return self._cookie_as_dot_dict(cookie_dict)
                return self._cookie_as_string(cookie_dict)
        raise ValueError(f"Cookie with name {cookie} is not found.")
