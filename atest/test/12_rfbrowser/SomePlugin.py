from robot.api.deco import keyword

from Browser.base.librarycomponent import LibraryComponent


class SomePlugin(LibraryComponent):
    @keyword
    def this_is_plugin_keyword(self):
        """Docs"""
        return 1
