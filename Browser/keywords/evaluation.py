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

from robot.utils import DotDict  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import DownloadedFile, keyword, logger


class Evaluation(LibraryComponent):
    @keyword(name="Execute JavaScript", tags=("Setter", "Getter", "PageContent"))
    def execute_javascript(self, function: str, selector: str = "") -> Any:
        """Executes given javascript on the page.

        ``function`` A valid javascript function or a javascript function body. For example
        ``() => true`` and ``true`` will behave similarly.

        ``selector`` Selector to resolve and pass to the JavaScript function. This will be the first
        argument the function receives. If given a selector a function is necessary, with an argument
        to capture the elementhandle. For example ``(element) => document.activeElement === element``
        See the `Finding elements` section for details about the selectors.

        [https://github.com/MarketSquare/robotframework-browser/tree/master/atest/test/06_Examples/js_evaluation.robot | Usage examples. ]
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.ExecuteJavascript(
                Request().JavascriptCode(script=function, selector=selector)
            )
            logger.info(response.log)
            if response.result:
                return json.loads(response.result)

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

        ``selector`` Selectors which shall be highlighted.
        See the `Finding elements` section for details about the selectors.

        ``duration`` Sets for how long the selector shall be highlighted. Defaults to ``5s`` => 5 seconds.

        ``width`` Sets the width of the higlight border. Defaults to 2px.

        ``style`` Sets the style of the border. Defaults to dotted.

        ``color`` Sets the color of the border. Valid colors i.e. are:
        ``red``, ``blue``, ``yellow``, ``pink``, ``black``
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.HighlightElements(
                Request().ElementSelectorWithDuration(
                    selector=selector,
                    duration=int(self.convert_timeout(duration)),
                    width=width,
                    style=style,
                    color=color,
                )
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "PageContent"))
    def add_style_tag(self, content: str):
        """Adds a <style type="text/css"> tag with the content.

        ``content`` Raw CSS content to be injected into frame.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.AddStyleTag(Request().StyleTag(content=content))
            logger.info(response.log)

    @keyword(tags=("Page Content",))
    def download(self, url: str) -> DownloadedFile:
        """Download given url content.

        Keyword returns dictionary which contains downloaded file path
        and suggested filename as keys (saveAs and suggestedFilename).
        See `Wait For Download` for more details.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.Download(Request().Url(url=url))
        logger.info(response.log)
        dot_dict = DotDict()
        for key, value in json.loads(response.json).items():
            dot_dict[key] = value
        return dot_dict
