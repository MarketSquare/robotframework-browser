import json
from typing import Any, Dict, List, Optional

from robot.libraries.DateTime import convert_date  # type: ignore
from robotlibcore import keyword  # type: ignore

from Browser.base import LibraryComponent
from Browser.generated.playwright_pb2 import Request
from Browser.utils import logger
from Browser.utils.meta_python import locals_to_params


class Cookie(LibraryComponent):
    @keyword(tags=["Getter", "PageContent"])
    def get_cookies(self) -> List[Dict[str, Any]]:
        """Returns cookies from the current active browser context.

        Return value contains list of dictionaries. See `Get Cookie` documentation about the dictionary keys.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCookies(Request().Empty())
            cookie_names = response.log
            if not cookie_names:
                logger.info("No cookies found.")
                return []
            else:
                logger.info(f"Found cookies: {response.log}")
        return json.loads(response.body)

    @keyword(tags=["Setter", "PageContent"])
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
        sameSite: Optional[str] = None,
    ):
        """Adds a cookie to currently active browser context.

        ``name`` and ``value`` are required.  ``url``, ``domain``, `path``, ``expiry``, `http_only``, ``secure``
        and ``same_site`` are optional, but cookie must contain either url or  domain/path pair. Expiry supports
        the same formats as the [http://robotframework.org/robotframework/latest/libraries/DateTime.html|DateTime]
        library or an epoch timestamp.

        Example:
        | `Add Cookie` | foo | bar | http://address.com/path/to/site |                                 |                            |
        | `Add Cookie` | foo | bar | domain=example.com              | path=/foo/bar                   |                            |
        | `Add Cookie` | foo | bar | http://address.com/path/to/site | expiry=2027-09-28 16:21:35      | # Expiry as timestamp.     |
        | `Add Cookie` | foo | bar | http://address.com/path/to/site | expiry=1822137695               | # Expiry as epoch seconds. |
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
            return int(expiry)
        except ValueError:
            return int(convert_date(expiry, result_format="epoch"))

    @keyword(tags=["Setter", "PageContent"])
    def delete_all_cookies(self):
        """Deletes all cookies from the currently active browser context."""
        with self.playwright.grpc_channel() as stub:
            response = stub.DeleteAllCookies(Request.Empty())
        logger.info(response.log)

    @keyword
    def eat_all_cookies(self):
        """Eat all cookies for all easter."""
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

    @keyword(tags=["Getter", "PageContent"])
    def get_cookie(self, cookie: str) -> Dict[str, Any]:
        """Returns information of cookie with name as an dictionary.

        If no cookie is found with name, keyword fails. The cookie dictionary contains
        details about the cookie. Keys available in the dictionary are documented in the table below.

        | Value    | Explanation                                                                                |
        | name     | The name of a cookie, mandatory.                                                           |
        | value    | Value of the cookie, mandatory.                                                            |
        | url      | Define the scope of the cookie, what URLs the cookies should be sent to.                   |
        | domain   | Specifies which hosts are allowed to receive the cookie.                                   |
        | path     | Indicates a URL path that must exist in the requested URL, for example `/`.                |
        | expiry   | Lifetime of a cookie.                                                                      |
        | httpOnly | When true, the cookie is not accessible via JavaScript.                                    |
        | secure   | When true, the cookie is only used with HTTPS connections.                                 |
        | sameSite | Attribute lets servers require that a cookie shouldn't be sent with cross-origin requests. |

        See
        [playwright documentation|https://github.com/microsoft/playwright/blob/master/docs/api.md#browsercontextaddcookiescookies]
        for details about each attribute.
        """
        for cookie_dict in self.get_cookies():
            if cookie_dict["name"] == cookie:
                return cookie_dict
        raise ValueError(f"Cookie with name {cookie} is not found.")
