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
from typing import Any, Optional

from robot.utils import DotDict  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import DownloadedFile, keyword, logger


class Evaluation(LibraryComponent):
    @keyword(name="Execute JavaScript", tags=("Setter", "Getter", "PageContent"))
    def execute_javascript(self, function: str, selector: str = "") -> Any:
        """*DEPRECATED!!* Use keyword `Evaluate JavaScript` instead. This keyword will be removed end of 2022.

        Executes given javascript on the page.

        | =Arguments= | =Description= |
        | ``function`` | A valid javascript function or a javascript function body. For example ``() => true`` and ``true`` will behave similarly. |
        | ``selector`` | Selector to resolve and pass to the JavaScript function. This will be the first argument the function receives. If given a selector a function is necessary, with an argument to capture the elementhandle. For example ``(element) => document.activeElement === element`` See the `Finding elements` section for details about the selectors. |

        Same functionality can be replaced with newer ``Evaluate JavaScript`` Keyword:
        | -    Execute JavaScript    (elem) => elem.innerText = "abc"    h1
        | +    Evaluate JavaScript    h1    (elem) => elem.innerText = "abc"

        Example for replacement without Selector:
        | -    Execute JavaScript    () => document.location.hostname
        | +    Evaluate JavaScript    ${None}    () => document.location.hostname

        Keyword uses strict mode if selector is defined. See `Finding elements` for more details
        about strict mode.

        [https://github.com/MarketSquare/robotframework-browser/tree/main/atest/test/06_Examples/js_evaluation.robot | Usage examples. ]

        [https://forum.robotframework.org/t//4252|Comment >>]
        """
        selector = self.resolve_selector(selector)
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(
                    script=function, selector=selector, strict=self.strict_mode
                )
            )
        if response.log:
            logger.info(response.log)
        if response.result:
            return json.loads(response.result)
        return response.result

    @keyword(name="Evaluate JavaScript", tags=("Setter", "Getter", "PageContent"))
    def evaluate_javascript(
        self,
        selector: Optional[str] = None,
        *function: str,
        arg: Any = None,
        all_elements: bool = False,
    ) -> Any:
        """Executes given javascript on the selected element(s) or on page.

        | =Arguments= | =Description= |
        | ``selector`` | Selector to resolve and pass to the JavaScript function. This will be the first argument the function receives if not ``${None}``. ``selector`` is optional and can be omitted. If given a selector, a function is necessary, with an argument to capture the elementHandle. For example ``(element) => document.activeElement === element`` See the `Finding elements` section for details about the selectors. |
        | ``*function`` | A valid javascript function or a javascript function body. These arguments can be used to write readable multiline JavaScript. |
        | ``arg`` | an additional argument that can be handed over to the JavaScript function. This argument must be JSON serializable. ElementHandles are not supported. |
        | ``all_elements`` | defines if only the single elementHandle found by ``selector`` is handed over to the function or if set to ``True`` all found elements are handed over as array. |

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

        Keyword uses strict mode if ``all_elements`` is ``False``. See `Finding elements` for more details
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
    ):
        """Adds a highlight to elements matched by the ``selector``. Provides a style adjustment.

        | =Arguments= | =Description= |
        | ``selector`` | Selectors which shall be highlighted. See the `Finding elements` section for details about the selectors. |
        | ``duration`` | Sets for how long the selector shall be highlighted. Defaults to ``5s`` => 5 seconds. |
        | ``width`` | Sets the width of the higlight border. Defaults to 2px. |
        | ``style`` | Sets the style of the border. Defaults to dotted. |
        | ``color`` | Sets the color of the border. Valid colors i.e. are: ``red``, ``blue``, ``yellow``, ``pink``, ``black`` |

        Keyword does not fail if selector resolves to multiple elements.

        Example:
        | `Highlight Elements`    input#login_button    duration=200ms
        | `Highlight Elements`    input#login_button    duration=200ms    width=4px    style=solid    color=\\#FF00FF

        [https://forum.robotframework.org/t//4294|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.HighlightElements(
                Request().ElementSelectorWithDuration(
                    selector=self.resolve_selector(selector),
                    duration=int(self.convert_timeout(duration)),
                    width=width,
                    style=style,
                    color=color,
                    strict=False,
                )
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def add_style_tag(self, content: str):
        """Adds a <style type="text/css"> tag with the content.

        | =Arguments= | =Description= |
        | ``content`` | Raw CSS content to be injected into frame. |

        Example:
        | `Add Style Tag`    \\#username_field:focus {background-color: aqua;}

        [https://forum.robotframework.org/t//4234|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.AddStyleTag(Request().StyleTag(content=content))
            logger.info(response.log)

    @keyword(tags=("Page Content",))
    def download(self, url: str) -> DownloadedFile:
        """Download given url content.

        Keyword returns dictionary which contains downloaded file path
        and suggested filename as keys (saveAs and suggestedFilename).
        If the file URL cannot be found (the download is triggered by event handlers)
        use `Wait For Download`keyword.

        To enable downloads context's ``acceptDownloads`` needs to be true.

        To configure download directory use New Browser's ``downloadsPath`` settings

        With default filepath downloaded files are deleted when Context the download happened in is closed.

        This keyword requires that there is currently an open page. The keyword uses
        the current pages local state (cookies, sessionstorage, localstorage) for the
        download to avoid authentication problems.

        Example:
        | ${file_object}=    `Download`    ${url}
        | ${actual_size}=    Get File Size    ${file_object.saveAs}

        Example 2:
        | ${elem}=          Get Element   text="Download File"
        | ${href}=          Get Property  ${elem}  href
        | ${file_object}=   Download  ${href}
        | ${file_path}=     Set Variable  ${file_object.saveAs}

        [https://forum.robotframework.org/t//4246|Comment >>]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.Download(Request().Url(url=url))
        logger.info(response.log)
        dot_dict = DotDict()
        for key, value in json.loads(response.json).items():
            dot_dict[key] = value
        return dot_dict
