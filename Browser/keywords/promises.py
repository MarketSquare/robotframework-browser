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
import re
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import timedelta
from os import PathLike
from pathlib import Path
from sys import maxsize
from time import sleep
from typing import Any, Optional

from robot.api.deco import keyword
from robot.utils import DotDict

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import DownloadInfo, logger
from ..utils.data_types import RobotTypeConverter as TypeConverter


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

        | =Arguments= | =Description= |
        | ``kw`` | Keyword that will work async on background. |
        | ``*args`` | Keyword arguments as normally used. |

        Example:
        | ${promise}=     `Promise To`            Wait For Response     matcher=     timeout=3
        | `Click`           \\#delayed_request
        | ${body}=        `Wait For`              ${promise}

        [https://forum.robotframework.org/t//4312|Comment >>]
        """
        promise: Future = Future()
        known_keyword = self.get_known_keyword(kw)
        if not known_keyword:
            raise ValueError(
                f"Unknown keyword '{kw}'! 'Promise To' can only be used with Browser keywords."
            )
        positional, named = self.resolve_arguments(known_keyword, *args)
        promise = self._executor.submit(
            self.library.keywords[known_keyword], *positional, **(named or {})
        )
        self.unresolved_promises.add(promise)
        while not (promise.running() or promise.done()):
            sleep(0.01)
        return promise

    def get_known_keyword(self, kw: str) -> str:
        normalized_kw = self.normalized_keyword_name(kw)
        for keyword_name in self.library.get_keyword_names():
            if normalized_kw == self.normalized_keyword_name(keyword_name):
                return keyword_name
        return ""

    def normalized_keyword_name(self, kw: str) -> str:
        """Returns normalized keyword name.

        Keyword name is normalized by removing spaces and converting to lower case.
        """
        return kw.lower().replace(" ", "").replace("_", "")

    def resolve_arguments(self, kw: str, *args):
        positional: list[Any] = []
        named: dict[str, Any] = {}
        logger.debug(f"*args {args}")

        arg_names = []
        index_of_varargs = maxsize
        for index, argument in enumerate(self.library.get_keyword_arguments(kw)):
            arg_name = argument[0] if isinstance(argument, tuple) else argument
            match = re.fullmatch(r"^\*(\w.*)", arg_name)
            if match:
                index_of_varargs = index
                arg_name = match.group(1)
            arg_names.append(arg_name)

        for index, arg in enumerate(args):
            arg_name, has_equal, arg_value = arg.partition("=")
            arg_name = arg_name.strip()
            arg_value = arg_value.strip()

            if not named and (not has_equal or arg_name not in arg_names):
                positional.append(
                    self.convert_keyword_arg(
                        kw, arg_names[min(index, index_of_varargs)], arg
                    )
                )
            elif arg_name in arg_names:
                named[arg_name] = self.convert_keyword_arg(kw, arg_name, arg_value)
            else:
                raise ValueError(
                    f"Invalid argument '{arg_name}' for keyword '{kw}'. "
                    f"Valid arguments are: {', '.join(arg_names)}"
                )

        logger.debug(
            f"named arguments: {named}, positional arguments: {tuple(positional)}"
        )
        return tuple(positional), named

    def convert_keyword_arg(self, kw: str, arg_name: str, arg_value: Any) -> Any:
        argument_type = self.library.get_keyword_types(kw).get(arg_name)
        if argument_type is not None:
            converter = TypeConverter.converter_for(argument_type)
            return (
                converter.convert(name=arg_name, value=arg_value)
                if converter
                else arg_value
            )
        return arg_value

    @keyword(tags=("Wait", "BrowserControl"))
    def promise_to_wait_for_download(
        self,
        saveAs: str = "",
        wait_for_finished: bool = True,
        download_timeout: Optional[timedelta] = None,
    ) -> Future:
        """Returns a promise that waits for next download event on page.

        To enable downloads context's ``acceptDownloads`` needs to be true.

        With default filepath downloaded files are deleted when Context the download happened in is closed.

        If browser is connected remotely with `Connect To Browser` then ``saveAs`` must be set to store it locally where the browser runs!

        | =Arguments= | =Description= |
        | ``saveAs`` | Defines path where the file is saved persistently. File will also temporarily be saved in playwright context's default download location. If empty, generated unique path (GUID) is used and file is deleted when the context is closed. |
        | ``wait_for_finished`` | If true, promise will wait for download to finish. If false, promise will resolve immediately after download has started. |
        | ``download_timeout`` | Maximum time to wait for download to finish, if ``wait_for_finished`` is set to ``True``. If download is not finished during this time, keyword will be fail. |

        Keyword returns dictionary of type `DownloadInfo` which contains downloaded file path
        and suggested filename as well as state and downloadID.
        Example:
        | {
        |   "saveAs": "/tmp/robotframework-browser/downloads/2f1b3b7c-1b1b-4b1b-9b1b-1b1b1b1b1b1b",
        |   "suggestedFilename": "downloaded_file.txt"
        | }

        The keyword `New Browser` has a ``downloadsPath`` setting which can be used to set the default download directory.
        If `saveAs` is set to a relative path, the file will be saved relative to the browser's ``downloadsPath`` setting or if that is not set, relative to the
        Playwright's working directory. If ``saveAs`` is set to an absolute path, the file will be saved to that absolute path independent of ``downloadsPath``.

        If the URL for the file to download shall be used, `Download` keyword may be a simpler alternative way to download the file.

        Waited promise returns a dictionary which contains saveAs and suggestedFilename as keys. The saveAs contains
        where the file is downloaded and suggestedFilename contains the name suggested name for the download.
        The suggestedFilename is typically computed by the browser from the Content-Disposition response header
        or the download attribute. See the spec on [https://html.spec.whatwg.org/#downloading-resources|whatwg].
        Different browsers can use different logic for computing it.

        Example usage:
        | `New Context`            acceptDownloads=True
        | `New Page`               ${LOGIN_URL}
        | ${dl_promise}          `Promise To Wait For Download`    /path/to/download/file.name
        | `Click`                  id=file_download
        | ${file_obj}=           `Wait For`    ${dl_promise}
        | File Should Exist      ${file_obj}[saveAs]
        | Should Be True         ${file_obj.suggestedFilename}

        [https://forum.robotframework.org/t//4314|Comment >>]
        """
        timeout_ms = (
            int(download_timeout.total_seconds() * 1000) if download_timeout else 0
        )
        promise = self._executor.submit(
            self._wait_for_download,
            saveAs=saveAs,
            wait_for_finish=wait_for_finished,
            download_timeout=timeout_ms,
        )
        self.unresolved_promises.add(promise)
        return promise

    def _wait_for_download(
        self, saveAs: str = "", wait_for_finish: bool = True, download_timeout: int = 0
    ) -> DownloadInfo:
        with self.playwright.grpc_channel() as stub:
            if not saveAs:
                response = stub.WaitForDownload(
                    Request().DownloadOptions(
                        downloadTimeout=download_timeout, waitForFinish=wait_for_finish
                    )
                )
                logger.debug(response.log)
            else:
                file_path = Path(saveAs)
                file_path.resolve()
                response = stub.WaitForDownload(
                    Request().DownloadOptions(
                        path=str(file_path),
                        downloadTimeout=download_timeout,
                        waitForFinish=wait_for_finish,
                    )
                )
        logger.info(response.log)
        return DotDict(json.loads(response.json))

    @keyword(tags=("Wait",))
    def wait_for(self, *promises: Future):
        """Waits for promises to finish and returns results from them.

        Returns one result if one promise waited. Otherwise returns an array of
        results. If one fails, then this keyword will fail.

        See `Promise To` for more information about promises.

        For general waiting of elements please see `Implicit waiting`.

        | =Arguments= | =Description= |
        | ``promises`` | Promises to wait for. |

        Example:
        | ${promise}=    `Promise To`            `Wait For Response`     matcher=     timeout=3
        | `Click`         \\#delayed_request
        | ${body}=       `Wait For`              ${promise}

        [https://forum.robotframework.org/t//4342|Comment >>]
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

        [https://forum.robotframework.org/t//4344|Comment >>]
        """
        self.wait_for(*self.unresolved_promises)

    @keyword(tags=("Setter", "PageContent"))
    def promise_to_upload_file(self, path: PathLike):
        """Returns a promise that resolves when file from ``path`` has been uploaded.

        Fails if the upload has not happened during timeout.

        Upload file from ``path`` into next file chooser dialog on page.

        | =Arguments= | =Description= |
        | ``path`` | Path to file to be uploaded. |

        Example use:

        | ${promise}=    `Promise To Upload File`    ${CURDIR}/test_upload_file.txt
        | `Click`          id=open_file_chooser_button
        | ${upload_result}=    `Wait For`    ${promise}

        Alternatively, you can use `Upload File By Selector` keyword.

        [https://forum.robotframework.org/t//4313|Comment >>]
        """
        p = Path(path)
        if not p.is_file():
            raise ValueError(f"Nonexistent input file path '{p.resolve()}'")
        promise = self._executor.submit(self._upload_file, path=str(p.resolve()))
        self.unresolved_promises.add(promise)
        return promise

    def _upload_file(self, path: str):
        with self.playwright.grpc_channel() as stub:
            response = stub.UploadFile(Request().FilePath(path=path))
            logger.debug(response.log)
