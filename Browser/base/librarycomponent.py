class LibraryComponent:
    def __init__(self, library):
        """Base class exposing attributes from the common context.

        :param library: The library itself as a context object.
        :type library: Browser.Browser
        """
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright
