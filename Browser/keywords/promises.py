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
from concurrent.futures import Future, ThreadPoolExecutor
from os import PathLike
from pathlib import Path
from time import sleep

from robot.api.deco import keyword  # type: ignore
from robot.libraries.BuiltIn import EXECUTION_CONTEXTS  # type: ignore
from robot.utils import DotDict  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import DownloadedFile, logger


class Promises(LibraryComponent):
    def __init__(self, library):
        LibraryComponent.__init__(self, library)
        self._executor = ThreadPoolExecutor(max_workers=256)

    @keyword(tags=("Wait",))
    def promise_to(self, kw: str, *args) -> Future:
        """
        Wrap a Browser library keyword and make it a promise.
        Returns that promise and executes the keyword on background.

        ``kw`` Keyword that will work async on background.

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
        while not (promise.running() or promise.done()):
            sleep(0.01)
        return promise

    @keyword(tags=("Wait", "BrowserControl"))
    def promise_to_wait_for_download(self, saveAs: str = "") -> Future:
        """Returns a promise that waits for next download event on page.

        To enable downloads context's ``acceptDownloads`` needs to be true.

        With default filepath downloaded files are deleted when Context the download happened in is closed.

        ``saveAs`` defines path where the file is saved. File will also temporarily be saved in playwright context's
        default download location.

        Waited promise returns a dictionary which contains saveAs and suggestedFilename as keys. The saveAs contains
        where the file is downloaded and suggestedFilename contains the name suggested name for the download.
        The suggestedFilename is typically computed by the browser from the Content-Disposition response header
        or the download attribute. See the spec on [https://html.spec.whatwg.org/#downloading-resources|whatwg].
        Different browsers can use different logic for computing it.

        Example usage:
        | New Context          acceptDownloads=True
        | New Page             ${LOGIN_URL}
        | ${dl_promise}        Promise To Wait For Download    /path/to/download/folder
        | Click                \\#file_download
        | ${file_obj}=         Wait For  ${dl_promise}
        | File Should Exist    ${file_obj}[saveAs]
        | Should Be True       ${file_obj.suggestedFilename}
        """
        promise = self._executor.submit(self._wait_for_download, **{"saveAs": saveAs})
        self.unresolved_promises.add(promise)
        return promise

    @keyword(tags=("Wait", "BrowserControl"))
    def wait_for_download(self, saveAs: str = "") -> DownloadedFile:
        """*DEPRECATED!!* Use keyword `Promise To Wait For Download` instead."""
        return self._wait_for_download(saveAs)

    def _wait_for_download(self, saveAs: str = "") -> DownloadedFile:
        with self.playwright.grpc_channel() as stub:
            if not saveAs:
                response = stub.WaitForDownload(Request().FilePath())
                logger.debug(response.log)
            else:
                file_path = Path(saveAs)
                file_path.resolve()
                response = stub.WaitForDownload(Request().FilePath(path=str(file_path)))
        logger.info(response.log)
        dot_dict = DotDict()
        for key, value in json.loads(response.json).items():
            dot_dict[key] = value
        return dot_dict

    @keyword(tags=("Wait",))
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

    @keyword(tags=("Wait",))
    def wait_for_all_promises(self):
        """
        Waits for all promises to finish.
        If one fails, then this keyword will fail.
        """
        self.wait_for(*self.unresolved_promises)

    @keyword(tags=("Setter", "PageContent"))
    def promise_to_upload_file(self, path: PathLike):
        """Returns a promise that resolves when file from ``path`` has been uploaded.
        Fails if the upload has not happened during timeout.

        Upload file from ``path`` into next file chooser dialog on page.

        ``path`` Path to file to be uploaded.

        Example use:

        | ${promise}=  Promise To Upload File    ${CURDIR}/test_upload_file
        | Click          \\#file_chooser
        | ${upload_result}=  Wait For  ${promise}

        """

        promise = self._executor.submit(self._upload_file, **{"path": path})
        self.unresolved_promises.add(promise)
        return promise

    @keyword(tags=("Setter", "PageContent"))
    def upload_file(self, path: PathLike):
        """*DEPRECATED!!* Use keyword `Promise To Upload File` instead.
        Upload file from ``path`` into next file chooser dialog on page.

        ``path`` Path to file to be uploaded.

        Example use:

        | Upload File    ${CURDIR}/test_upload_file
        | Click          \\#file_chooser

        """
        return self._upload_file(path)

    def _upload_file(self, path: PathLike):
        p = Path(path)
        p.resolve(strict=True)
        with self.playwright.grpc_channel() as stub:
            response = stub.UploadFile(Request().FilePath(path=str(p)))
            logger.debug(response.log)
