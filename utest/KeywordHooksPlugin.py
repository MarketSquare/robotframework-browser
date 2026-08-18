from robot.api.deco import keyword

from Browser.base.librarycomponent import LibraryComponent


class KeywordHooksPlugin(LibraryComponent):
    """Plugin used to prove the keyword hooks also cover plugin keywords.

    `Plugin Login With Credentials` takes a secret while neither its Robot name
    nor its Python name contains the word secret, so a hook that decides on the
    keyword name cannot protect it.
    """

    @keyword(name="Plugin Login With Credentials")
    def plugin_login_with_credentials(self, selector: str, secret: str):
        return self.resolve_secret(secret, "secret")

    @keyword
    def plugin_without_secret(self, selector: str, text: str):
        return f"{selector}{text}"
