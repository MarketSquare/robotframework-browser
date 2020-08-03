from concurrent.futures import Future, ThreadPoolExecutor
from typing import Set

from robot.api.deco import keyword  # type: ignore
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS  # type: ignore

from ..base import LibraryComponent


class Promises(LibraryComponent):
    def __init__(self, library):
        LibraryComponent.__init__(self, library)
        self._executor = ThreadPoolExecutor(max_workers=256)
        self._unresolved_promises: Set[Future] = set()

    @keyword(tags=["Wait"])
    def promise_to(self, kw: str, *args):
        """
        *EXPERIMENTAL* *WORK IN PROGRESS*
        Wrap a Browser library keyword and make it a promise.
        Returns that promise and executes the keyword on background.
        """
        browser_lib = EXECUTION_CONTEXTS.current.namespace._kw_store.get_library(
            self.library
        )
        handler = browser_lib.handlers[kw]
        positional, named = handler.resolve_arguments(
            args, EXECUTION_CONTEXTS.current.variables
        )
        named = dict(named)

        promise = self._executor.submit(handler.current_handler(), *positional, **named)
        self._unresolved_promises.add(promise)
        return promise

    @keyword(tags=["Wait"])
    def wait_for(self, *promises: Future):
        """
        *EXPERIMENTAL* *WORK IN PROGRESS*
        Waits for promises to finish and returns results from them.
        Returns one result if one promise waited. Otherwise returns an array of results.
        If one fails, then this keyword will fail.
        """
        self._unresolved_promises -= {*promises}
        if len(promises) == 1:
            return promises[0].result()
        return [promise.result() for promise in promises]

    @keyword(tags=["Wait"])
    def wait_for_all_promises(self):
        """
        *EXPERIMENTAL* *WORK IN PROGRESS*
        Waits for all promises to finish.
        If one fails, then this keyword will fail.
        """
        self.wait_for(*self._unresolved_promises)
