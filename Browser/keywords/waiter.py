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

import json
from pathlib import Path
from typing import Dict

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import ElementState, logger, timestr_to_millisecs


class Waiter(LibraryComponent):
    @keyword(tags=["Wait", "PageContent"])
    def wait_for_elements_state(
        self,
        selector: str,
        state: ElementState = ElementState.visible,
        timeout: str = "",
    ):
        """Waits for the element found by ``selector`` to satisfy state option.

        State options could be either appear/disappear from dom, or become visible/hidden.
        If at the moment of calling the keyword, the selector already satisfies the condition,
        the keyword will return immediately.

        If the selector doesn't satisfy the condition within the timeout the keyword will FAIL.

        ``selector`` <str> Selector of the corresponding object. **Required**

        ``state`` Defaults to visible. Possible states are:
        - ``attached``: to be present in DOM.
        - ``detached``: to not be present in DOM.
        - ``visible``: to have non-empty bounding box and no visibility:hidden.
        - ``hidden``: to be detached from DOM, or have an empty bounding box or visibility:hidden.
        - ``enabled``: to not be ``disabled``.
        - ``disabled``: to be ``disabled``. Can be used on <button>, <fieldset>, <input>, <optgroup>, <option>, <select> and <textarea>.
        - ``editable``: to not be ``readOnly``.
        - ``readonly``: to be ``readOnly``. Can be used on <input> and <textarea>.
        - ``selected``: to be ``selected``. Can be used on <option>.
        - ``deselected``: to not be ``selected``.
        - ``focused``: to be the ``activeElement``.
        - ``defocused``: to not be the ``activeElement``.
        - ``checked``: to be ``checked``. Can be used on <input>.
        - ``unchecked``: to not be ``checked``.

        Note that element without any content or with display:none has an empty bounding box
        and is not considered visible.

        ``timeout`` <str> (optional) uses default timeout of 10 seconds if not set.
        """
        funct = {
            ElementState.enabled: "e => !e.disabled",
            ElementState.disabled: "e => e.disabled",
            ElementState.editable: "e => !e.readOnly",
            ElementState.readonly: "e => e.readOnly",
            ElementState.selected: "e => e.selected",
            ElementState.deselected: "e => !e.selected",
            ElementState.focused: "e => document.activeElement === e",
            ElementState.defocused: "e => document.activeElement !== e",
            ElementState.checked: "e => e.checked",
            ElementState.unchecked: "e => !e.checked",
        }

        with self.playwright.grpc_channel() as stub:
            if state in [
                ElementState.attached,
                ElementState.detached,
                ElementState.visible,
                ElementState.hidden,
            ]:
                options: Dict[str, object] = {"state": state.name}
                if timeout:
                    timeout_ms = timestr_to_millisecs(timeout)
                    options["timeout"] = timeout_ms
                options_json = json.dumps(options)
                response = stub.WaitForElementsState(
                    Request().ElementSelectorWithOptions(
                        selector=selector, options=options_json
                    )
                )
                logger.info(response.log)
            else:
                self.wait_for_function(funct[state], selector=selector, timeout=timeout)

    @keyword(tags=["Wait", "PageContent"])
    def wait_for_function(
        self,
        function: str,
        selector: str = "",
        polling: str = "raf",
        timeout: str = "",
    ):
        """Polls JavaScript expression or function in browser until it returns a
        (JavaScript) truthy value.

        ``function`` <str> A valid javascript function or a javascript function body. For example
        ``() => true`` and ``true`` will behave similarly. **Required**

        ``selector`` <str> Selector to resolve and pass to the JavaScript function. This will be the first
        argument the function receives. If given a selector a function is necessary, with an argument
        to capture the elementhandle. For example ``(element) => document.activeElement === element``

        ``polling`` <str> Default polling value of "raf" polls in a callback for ``requestAnimationFrame``.
        Any other value for polling will be parsed as a robot framework time for interval between polls.

        ``timeout`` <str> Uses default timeout of 10 seconds if not set.

        Example usage:
        | ${promise}    Promise To      Wait For Function    element => element.style.width=="100%"    selector=\\#progress_bar    timeout=4s
        | Click         \\#progress_bar
        | Wait For      ${promise}
        """
        with self.playwright.grpc_channel() as stub:
            options: Dict[str, int] = {}
            if polling != "raf":
                options["polling"] = timestr_to_millisecs(polling)
            if timeout:
                options["timeout"] = timestr_to_millisecs(timeout)
            options_json = json.dumps(options)
            response = stub.WaitForFunction(
                Request().WaitForFunctionOptions(
                    script=function,
                    selector=selector,
                    options=options_json,
                )
            )
            logger.debug(response.json)
            logger.info(response.log)

    @keyword(tags=["Wait", "BrowserControl"])
    def wait_for_download(self, saveAs: str = ""):
        """Waits for next download event on page. Returns file path to downloaded file.

        To enable downloads context's ``acceptDownloads`` needs to be true.

        With default filepath downloaded files are deleted when Context the download happened in is closed.

        ``saveAs`` <str> Filename to save as. File will also temporarily be saved in playwright context's default download location.

        Example usage:
        | New Context      acceptDownloads=True
        | New Page         ${LOGIN_URL}
        | ${dl_promise}    Promise To  Wait For Download
        | Click            \\#file_download
        | ${file_path}=    Wait For  ${dl_promise}
        """
        with self.playwright.grpc_channel() as stub:
            if not saveAs:
                response = stub.WaitForDownload(Request().FilePath())
                logger.debug(response.log)
                return json.loads(response.json)
            else:
                p = Path(saveAs)
                p.resolve()
                response = stub.WaitForDownload(Request().FilePath(path=str(p)))
                logger.debug(response.log)
                return json.loads(response.json)
