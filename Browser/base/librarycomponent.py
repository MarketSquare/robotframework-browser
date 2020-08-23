from concurrent.futures._base import Future
from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from ..browser import Browser


class LibraryComponent:
    def __init__(self, library: "Browser") -> None:
        """Base class exposing attributes from the common context.

        :param library: The library itself as a context object.
        """
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @property
    def timeout(self) -> str:
        return self.library.timeout

    @timeout.setter
    def timeout(self, value: str):
        self.library.timeout = value

    @property
    def retry_assertions_until(self) -> str:
        return self.library.retry_assertions_until

    @retry_assertions_until.setter
    def retry_assertions_until(self, value: str):
        self.library.retry_assertions_until = value

    @property
    def unresolved_promises(self):
        return self.library._unresolved_promises

    @unresolved_promises.setter
    def unresolved_promises(self, value: Set[Future]):
        self.library._unresolved_promises = value
