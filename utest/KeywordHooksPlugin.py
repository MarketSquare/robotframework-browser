from robot.api.deco import keyword

from Browser.base.librarycomponent import LibraryComponent


class KeywordHooksPlugin(LibraryComponent):
    @keyword(name="Plugin Login With Credentials")
    def plugin_login_with_credentials(self, selector: str, secret: str):
        return self.resolve_secret(secret, "secret")

    @keyword
    def plugin_without_secret(self, selector: str, text: str):
        return f"{selector}{text}"
