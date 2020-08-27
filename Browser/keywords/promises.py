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

from concurrent.futures import Future, ThreadPoolExecutor

from robot.api.deco import keyword  # type: ignore
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS  # type: ignore

from ..base import LibraryComponent


class Promises(LibraryComponent):
    def __init__(self, library):
        LibraryComponent.__init__(self, library)
        self._executor = ThreadPoolExecutor(max_workers=256)

    @keyword(tags=["Wait"])
    def promise_to(self, kw: str, *args):
        """
        Wrap a Browser library keyword and make it a promise.
        Returns that promise and executes the keyword on background.

        ``kw`` <str> Keyword that will work async on background.

        Example:
        | ${promise}=     Promise To            Wait For Response     matcher=     timeout=3
        | Click           \\#delayed_request
        | ${body}=        Wait For              ${promise}
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
        self.unresolved_promises.add(promise)
        return promise

    @keyword(tags=["Wait"])
    def wait_for(self, *promises: Future):
        """
        Waits for promises to finish and returns results from them.
        Returns one result if one promise waited. Otherwise returns an array of results.
        If one fails, then this keyword will fail.

        ``promises`` *Work in progress*

        Example:
        | ${promise}=     Promise To            Wait For Response     matcher=     timeout=3
        | Click           \\#delayed_request
        | ${body}=        Wait For              ${promise}
        """
        self.unresolved_promises -= {*promises}
        if len(promises) == 1:
            return promises[0].result()
        return [promise.result() for promise in promises]

    @keyword(tags=["Wait"])
    def wait_for_all_promises(self):
        """
        Waits for all promises to finish.
        If one fails, then this keyword will fail.
        """
        self.wait_for(*self.unresolved_promises)
