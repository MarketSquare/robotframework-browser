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
from typing import Any, List

from assertionengine import AssertionOperator
from robot.api.deco import keyword  # type: ignore
from robot.utils import DotDict  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import DownloadedFile, logger
from ..utils.data_types import DialogAction, ElementState


class Promises(LibraryComponent):
    def __init__(self, library):
        LibraryComponent.__init__(self, library)
        self._executor = ThreadPoolExecutor(max_workers=256)

    @keyword(tags=("Wait",))
    def promise_to(self, kw: str, *args) -> Future:
        """Wrap a Browser library keyword and make it a promise.

        Promised keyword is executed and started on background.
        Test execution continues without waiting for ``kw`` to finish.

        Returns reference to the promised keyword.

        ``kw`` Keyword that will work async on background.

        Example:
        | ${promise}=     `Promise To`            Wait For Response     matcher=     timeout=3
        | `Click`           \\#delayed_request
        | ${body}=        `Wait For`              ${promise}
        """
        promise: Future = Future()
        keyword_name = kw.strip().lower().replace(" ", "_")

        if keyword_name in self.library.get_keyword_names():
            positional, named = self.resolve_arguments(keyword_name, *args)
            promise = self._executor.submit(
                self.library.keywords[keyword_name], *positional, **(named or {})
            )
            self.unresolved_promises.add(promise)
            while not (promise.running() or promise.done()):
                sleep(0.01)

        return promise

    def resolve_arguments(self, kw: str, *args):
        positional: List[Any] = []
        named = {}
        logger.debug(f"*args {args}")

        keyword_arguments = [
            argument[0] if isinstance(argument, tuple) else argument
            for argument in self.library.get_keyword_arguments(kw)
        ]
        for arg in args:
            parts = arg.partition("=")
            if parts[0].strip() in keyword_arguments:
                if parts[2].strip() in DialogAction.__members__:
                    named[parts[0].strip()] = DialogAction[parts[2].strip()]
                else:
                    named[parts[0].strip()] = parts[2].strip()
            else:
                if arg.strip() in AssertionOperator.__members__:
                    positional.append(AssertionOperator[arg.strip()])
                elif arg.strip() in ElementState.__members__:
                    positional.append(ElementState.__members__[arg.strip()])
                elif arg.strip() in DialogAction.__members__:
                    positional.append(DialogAction[arg.strip()])
                else:
                    positional.append(arg)

        logger.debug(
            f"named arguments: {named}, positional arguments: {tuple(positional)}"
        )
        return tuple(positional), named

    @keyword(tags=("Wait", "BrowserControl"))
    def promise_to_wait_for_download(self, saveAs: str = "") -> Future:
        """Returns a promise that waits for next download event on page.

        If you can get the URL for the file to download, ``Download`` keyword should be a consistent way to download the file.

        To enable downloads context's ``acceptDownloads`` needs to be true.

        To configure download directory use New Browser's ``downloadsPath`` settings

        With default filepath downloaded files are deleted when Context the download happened in is closed.

        ``saveAs`` defines path where the file is saved. File will also temporarily be saved in playwright context's
        default download location.

        Waited promise returns a dictionary which contains saveAs and suggestedFilename as keys. The saveAs contains
        where the file is downloaded and suggestedFilename contains the name suggested name for the download.
        The suggestedFilename is typically computed by the browser from the Content-Disposition response header
        or the download attribute. See the spec on [https://html.spec.whatwg.org/#downloading-resources|whatwg].
        Different browsers can use different logic for computing it.

        Example usage:
        | `New Context`          acceptDownloads=True
        | `New Page`             ${LOGIN_URL}
        | ${dl_promise}          `Promise To Wait For Download`    /path/to/download/file.name
        | `Click`                \\#file_download
        | ${file_obj}=           `Wait For`  ${dl_promise}
        | File Should Exist    ${file_obj}[saveAs]
        | Should Be True       ${file_obj.suggestedFilename}
        """
        promise = self._executor.submit(self._wait_for_download, **{"saveAs": saveAs})
        self.unresolved_promises.add(promise)
        return promise

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
        """Waits for promises to finish and returns results from them.

        Returns one result if one promise waited. Otherwise returns an array of
        results. If one fails, then this keyword will fail.

        See `Promise To` for more information about promises.

        For general waiting of elements please see `Implicit waiting`.

        ``promises`` *Work in progress*

        Example:
        | ${promise}=    `Promise To`            `Wait For Response`     matcher=     timeout=3
        | `Click`         \\#delayed_request
        | ${body}=       `Wait For`              ${promise}
        """
        self.unresolved_promises -= {*promises}
        if len(promises) == 1:
            return promises[0].result()
        return [promise.result() for promise in promises]

    @keyword(tags=("Wait",))
    def wait_for_all_promises(self):
        """Waits for all promises to finish.

        If one promises fails, then this keyword will fail.

        Example:
        | `Promise To`               Wait For Response     matcher=     timeout=3
        | `Click`                    \\#delayed_request
        | `Wait For All Promises`
        """
        self.wait_for(*self.unresolved_promises)

    @keyword(tags=("Setter", "PageContent"))
    def promise_to_upload_file(self, path: PathLike):
        """*!!DEPRECATED!!* Use keyword `Upload File By Selector` instead if possible. If your use case _needs_ promise to upload file please let the Browser team know by creating an issue.

        Returns a promise that resolves when file from ``path`` has been uploaded.

        Fails if the upload has not happened during timeout.

        Upload file from ``path`` into next file chooser dialog on page.

        ``path`` Path to file to be uploaded.

        !! Due to a certain problem with Playwright library currently files over 74 MB will fail to upload. !!

        Example use:

        | ${promise}=    `Promise To Upload File`    ${CURDIR}/test_upload_file
        | `Click`          \\#file_chooser
        | ${upload_result}=  `Wait For`  ${promise}
        """
        promise = self._executor.submit(self._upload_file, **{"path": path})
        self.unresolved_promises.add(promise)
        return promise

    def _upload_file(self, path: PathLike):
        p = Path(path)
        p.resolve(strict=True)
        with self.playwright.grpc_channel() as stub:
            response = stub.UploadFile(Request().FilePath(path=str(p)))
            logger.debug(response.log)
