import json

from robot.libraries.DateTime import convert_date  # type: ignore
from robotlibcore import keyword  # type: ignore

from Browser.base import LibraryComponent
from Browser.generated.playwright_pb2 import Request
from Browser.utils import logger


class Cookie(LibraryComponent):
    @keyword
    def get_cookies(self):
        """Returns cookies from the current active browser context"""
        with self.playwright.grpc_channel() as stub:
            response = stub.GetCookies(Request().Empty())
            cookie_names = response.log
            if not cookie_names:
                logger.info("No cookies found.")
            else:
                logger.info(f"Found cookies: {response.log}")
        return json.loads(response.body)

    @keyword
    def add_cookie(
        self, name, value, url=None, domain=None, path=None, expiry=None, http_only=None, secure=None, same_site=None
    ):
        """Adds a cookie to your current context.

        ``name`` and ``value`` are required.  ``url``, ``domain``, `path``, ``expiry``, `http_only``, ``secure``
        and ``same_site`` are optional, but cookie must contain either url or  domain/path pair. Expiry supports
        the same formats as the [http://robotframework.org/robotframework/latest/libraries/DateTime.html|DateTime]
        library or an epoch timestamp.

        Example:
        | `Add Cookie` | foo | bar | http://address.com/path/to/site |
        | `Add Cookie` | foo | bar | domain=example.com              |
        | `Add Cookie` | foo | bar | expiry=2027-09-28 16:21:35 | # Expiry as timestamp.     |
        | `Add Cookie` | foo | bar | expiry=1822137695          | # Expiry as epoch seconds. |
        """
        cookie = {"name": name, "value": value}
        if url:
            cookie["url"] = url
        if path:
            cookie["path"] = path
        if domain:
            cookie["domain"] = domain
        if http_only:
            cookie["httpOnly"] = http_only
        if expiry:
            cookie["expires"] = self._expiry(expiry)
        if secure:
            cookie["secure"] = secure
        if same_site:
            cookie["sameSite"] = same_site
        if not self._check_data(cookie):
            raise ValueError("Cookie should have a url or a domain/path pair.")
        cookie_json = json.dumps(cookie)
        logger.debug(f"Adding cookie: {cookie_json}")
        with self.playwright.grpc_channel() as stub:
            response = stub.AddCookie(Request.Json(body=cookie_json))
            logger.info(response.log)

    def _expiry(self, expiry: str):
        try:
            return int(expiry)
        except ValueError:
            return int(convert_date(expiry, result_format="epoch"))

    def _check_data(self, cookie: dict):
        if cookie.get("url"):
            return True
        if cookie.get("path") and cookie.get("domain"):
            return True
        return False
