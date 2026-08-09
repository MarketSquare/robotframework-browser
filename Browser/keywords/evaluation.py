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
from datetime import timedelta
from typing import Any

from robot.utils import DotDict

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import (
    ROBOT_FRAMEWORK_BROWSER_NO_SET,
    DownloadInfo,
    HighlightMode,
    keyword,
    logger,
)


class Evaluation(LibraryComponent):
    @keyword(name="Evaluate JavaScript", tags=("Setter", "Getter", "PageContent"))
    def evaluate_javascript(
        self,
        selector: str | None = None,
        *function: str,
        arg: Any = None,
        all_elements: bool = False,
    ) -> Any:
        """Executes the given JavaScript in the browser page.

        The JavaScript is evaluated in the context of the page, not in the Node process
        of the library. Therefore browser globals like ``window`` and ``document`` are
        available, but Robot Framework variables and Python objects are not. Only ``arg``
        and the resolved element(s) are passed into the page.

        | =Arguments= | =Description= |
        | ``selector`` | Selector to resolve and pass to the JavaScript function. This will be the first argument the function receives if not ``${None}``. ``selector`` is optional and can be omitted. If given a selector, a function is necessary, with an argument to capture the element. For example ``(element) => document.activeElement === element`` See the `Finding elements` section for details about the selectors. |
        | ``*function`` | A valid javascript function or a javascript function body. These arguments can be used to write readable multiline JavaScript. |
        | ``arg`` | an additional argument that can be handed over to the JavaScript function. It is the second argument of the function when a ``selector`` is given, otherwise the first one. This argument must be JSON serializable. ElementHandles are not supported. |
        | ``all_elements`` | defines if only the single element found by ``selector`` is handed over to the function or if set to ``True`` all found elements are handed over as array. |

        The value returned by the JavaScript is transferred as JSON and must therefore be
        JSON serializable. DOM nodes and other non serializable objects can not be returned.
        If the JavaScript does not return anything, the keyword returns an empty string.

        Example with ``all_elements=True``:
        |  ${texts}=    Evaluate JavaScript    button
        |  ...    (elements, arg) => {
        |  ...        let text = []
        |  ...            for (e of elements) {
        |  ...                console.log(e.innerText)
        |  ...                text.push(e.innerText)
        |  ...            }
        |  ...        text.push(arg)
        |  ...        return text
        |  ...    }
        |  ...    all_elements=True
        |  ...    arg=Just another Text

        Keyword uses strict mode only if ``all_elements`` is ``False``. See `Finding elements` for more details
        about strict mode.

        [https://github.com/MarketSquare/robotframework-browser/tree/main/atest/test/06_Examples/js_evaluation.robot | Usage examples. ]

        [https://forum.robotframework.org/t//4251|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.EvaluateJavascript(
                Request().EvaluateAll(
                    selector=selector or "",
                    script="\n".join(function),
                    arg=json.dumps(arg),
                    allElements=all_elements,
                    strict=self.strict_mode,
                )
            )
        if response.log:
            logger.info(response.log)
        if response.result:
            return json.loads(response.result)
        return response.result

    @keyword(tags=("Setter", "PageContent"))
    def highlight_elements(
        self,
        selector: str,
        duration: timedelta = timedelta(seconds=5),
        width: str = "2px",
        style: str = "dotted",
        color: str = "blue",
        *,
        mode: HighlightMode = HighlightMode.border,
    ):
        """Adds a highlight to elements matched by the ``selector``. Provides a style adjustment.

        Returns the number of highlighted elements. Keyword does not fail, if the ``selector`` matched zero
        elements in the page. Keyword does not scroll elements to viewport and highlighted element might be
        outside the viewport. Use `Scroll To Element` keyword to scroll element in viewport.

        | =Arguments= | =Description= |
        | ``selector`` | Selectors which shall be highlighted. See the `Finding elements` section for details about the selectors. |
        | ``duration`` | Sets for how long the selector shall be highlighted. Defaults to ``5s`` => 5 seconds. If set to 0 seconds, the highlighting is not deleted. |
        | ``width`` | Sets the width of the highlight border. Defaults to 2px. |
        | ``style`` | Sets the style of the border. Defaults to dotted. |
        | ``color`` | Sets the color of the border. Valid colors i.e. are: ``red``, ``blue``, ``yellow``, ``pink``, ``black`` |
        | ``mode`` | Sets the mode of the highlight. Valid modes are: ``border`` (classic mode), ``playwright`` (Playwright's native one) and ``both``. Defaults to ``border``. If ``playwright`` is used, ``width``, ``style`` and ``color`` are ignored and only one highlighting can happen at the same time. |

        Keyword does not fail if selector resolves to multiple elements.

        Highlights which are created with ``duration=0`` stay in the page until they are removed. Calling this
        keyword with an empty ``selector``, for example ``Highlight Elements    ${EMPTY}``, removes all such
        highlights that were made with Playwright's native highlighting, in other words with ``mode=playwright``
        or ``mode=both``. Highlights drawn in ``border`` mode can not be removed that way.

        Example:
        | `Highlight Elements`    input#login_button    duration=200ms
        | ${count} =    `Highlight Elements`    input#login_button    duration=200ms    width=4px    style=solid    color=\\#FF00FF
        | Should Be Equal    ${count}    ${5}

        [https://forum.robotframework.org/t//4294|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.HighlightElements(
                Request().ElementSelectorWithDuration(
                    selector=self.resolve_selector(selector)
                    if selector
                    else ROBOT_FRAMEWORK_BROWSER_NO_SET,
                    duration=int(self.convert_timeout(duration)),
                    width=width,
                    style=style,
                    color=color,
                    strict=False,
                    mode=mode.name,
                )
            )
        count: int = response.body
        if selector:
            if count == 0:
                logger.info("Could not find elements to highlight.")
            else:
                logger.info(response.log)
        return count

    @keyword(tags=("Setter", "PageContent"))
    def add_style_tag(self, content: str):
        """Adds a <style type="text/css"> tag with the content.

        The tag is added to the currently active page and it is lost when the page is
        navigated to a new url.

        | =Arguments= | =Description= |
        | ``content`` | Raw CSS content to be injected into the current page. |

        Example:
        | `Add Style Tag`    \\#username_field:focus {background-color: aqua;}

        [https://forum.robotframework.org/t//4234|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.AddStyleTag(Request().StyleTag(content=content))
            logger.info(response.log)

    @keyword(tags=("Page Content",))
    def download(
        self,
        url: str,
        saveAs: str = "",
        wait_for_finished: bool = True,
        download_timeout: timedelta | None = None,
    ) -> DownloadInfo:
        """Download given url content.

        | =Arguments= | =Description= |
        | ``url`` | URL to the file that shall be downloaded. |
        | ``saveAs`` | Path where the file shall be saved persistently. If empty, generated unique path (GUID) is used and file is deleted when the context is closed. |
        | ``wait_for_finished`` | If set to ``False`` keyword returns immediately after the download has started. Defaults to ``True``. |
        | ``download_timeout`` | Timeout for the download itself if ``wait_for_finished`` is set to ``True``. By default no timeout is set. |

        Keyword returns dictionary of type `DownloadInfo`.

        Example:
        | {
        |   "saveAs": "/tmp/robotframework-browser/downloads/2f1b3b7c-1b1b-4b1b-9b1b-1b1b1b1b1b1b",
        |   "suggestedFilename": "downloaded_file.txt",
        |   "state": "finished",
        |   "downloadID": None,
        | }

        When ``wait_for_finished`` is ``False``, the returned dictionary has an empty ``saveAs``,
        the ``state`` is ``in_progress`` and ``downloadID`` contains the id of the download. The
        download can then be followed with the `Get Download State` keyword, which also saves the
        file to ``saveAs`` when the download is finished.

        If the download should be started by an interaction with an element on the page,
        `Promise To Wait For Download` keyword may be a better choice.

        The keyword `New Browser` has a ``downloadsPath`` setting which can be used to set the default download directory.
        If ``saveAs`` is set to a relative path, the file will be saved relative to the browser's ``downloadsPath`` setting or if that is not set, relative to the
        Playwright's working directory. If ``saveAs`` is set to an absolute path, the file will be saved to that absolute path independent of ``downloadsPath``.

        To enable downloads context's ``acceptDownloads`` needs to be true, otherwise the
        keyword fails. This keyword requires that there is currently an open page and that
        the page has been navigated to an url, downloading from ``about:blank`` fails. The
        download is done by a ``fetch`` call inside the page and therefore it uses the
        current page's local state (cookies, sessionstorage, localstorage) to avoid
        authentication problems. Because of that, a relative ``url`` is resolved against the
        current page url and the page's cross-origin restrictions apply.

        Example:
        | ${file_object}=    `Download`    ${url}
        | ${actual_size}=    Get File Size    ${file_object.saveAs}

        Example 2:
        | ${href}=          `Get Property`    text="Download File"    href
        | `Download`    ${href}    saveAs=${OUTPUT DIR}/downloads/downloaded_file.txt
        | File Should Exist    ${OUTPUT DIR}/downloads/downloaded_file.txt

        [https://forum.robotframework.org/t//4246|Comment >>]
        """
        timeout_ms = (
            int(download_timeout.total_seconds() * 1000) if download_timeout else 0
        )
        with self.playwright.grpc_channel() as stub:
            response = stub.Download(
                Request().DownloadOptions(
                    url=url,
                    path=saveAs,
                    waitForFinish=wait_for_finished,
                    downloadTimeout=timeout_ms,
                )
            )
        logger.info(response.log)
        dot_dict = DotDict()
        for key, value in json.loads(response.json).items():
            dot_dict[key] = value
        return dot_dict
