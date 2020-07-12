from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent


class WebAppState(LibraryComponent):
    @keyword
    def localStorage_get(self, key: str) -> str:
        """
        Get saved data from from localStorage
        """
        return "Getting"

    @keyword
    def localStorage_set(self, key: str, value: str):
        """
        Save data to localStorage
        """
        pass

    @keyword
    def localStorage_remove(self, key: str):
        """
        Remove saved data with key from localStorage
        """
        pass

    @keyword
    def localStorage_clear(self):
        """
        Remove all saved data from localStorage
        """
        pass

    @keyword
    def sessionStorage_get(self, key: str) -> str:
        """
        Get saved data from from sessionStorage
        """
        return "Getting"

    @keyword
    def sessionStorage_set(self, key: str, value: str):
        """
        Save data to sessionStorage
        """
        pass

    @keyword
    def sessionStorage_remove(self, key: str):
        """
        Remove saved data with key from sessionStorage
        """
        pass

    @keyword
    def sessionStorage_clear(self):
        """
        Remove all saved data from sessionStorage
        """
        pass
