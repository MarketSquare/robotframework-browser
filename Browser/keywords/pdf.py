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
import sys
from os import PathLike
from pathlib import Path

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger
from ..utils.data_types import (
    ColorScheme,
    ForcedColors,
    Media,
    NotSet,
    PdfFormat,
    PdfMarging,
    ReducedMotion,
)

PdfMargingDefault: PdfMarging = {
    "top": "0px",
    "right": "0px",
    "bottom": "0px",
    "left": "0px",
}


class Pdf(LibraryComponent):
    @keyword(tags=("Getter", "PageContent"))
    def save_page_as_pdf(
        self,
        path: PathLike,
        *,
        displayHeaderFooter: bool = False,
        footerTemplate: str = "",
        format: PdfFormat = PdfFormat.Letter,  # noqa: A002
        headerTemplate: str = "",
        height: str = "0px",
        landscape: bool = False,
        margin: PdfMarging = PdfMargingDefault,
        outline: bool = False,
        pageRanges: str = "",
        preferCSSPageSize: bool = False,
        printBackground: bool = False,
        scale: float = 1,
        tagged: bool = False,
        width: str = "0px",
    ) -> str:
        """Saves page as PDF.

        Saving a PDF is currently only supported in Chromium and only when the
        browser is running in headless mode.

        | =Arguments= | =Description= |
        | ``path`` | Where the PDF is saved. If the path is not absolute, the file is saved relative to ${OUTPUT_DIR}. |
        | ``displayHeaderFooter`` | Display header and footer. Defaults to false. |
        | ``footerTemplate`` | HTML template for the print footer. Should use the same format as the ``headerTemplate``. |
        | ``format`` | Paper format. If set, takes priority over the ``width`` and ``height`` arguments. Defaults to ``Letter``. |
        | ``headerTemplate`` | HTML template for the print header. Both templates are only rendered when ``displayHeaderFooter`` is true. See the detailed explanation below. |
        | ``height`` | Paper height, accepts values labeled with units. |
        | ``landscape`` | Paper orientation. Defaults to false. |
        | ``margin`` | Defines the PDF margins, see `PdfMarging` for more details. Defaults to ``0px`` on all sides. |
        | ``outline`` | Whether or not to embed the document outline into the PDF. Defaults to false. |
        | ``pageRanges`` | Paper ranges to print, e.g. ``1-5, 8, 11-13``. Defaults to the empty string, which means print all pages. |
        | ``preferCSSPageSize`` | Give any CSS ``@page`` size declared in the page priority over what is declared in the ``width`` and ``height`` or ``format`` arguments. Defaults to false, which will scale the content to fit the paper size. |
        | ``printBackground`` | Print background graphics. Defaults to false. |
        | ``scale`` | Scale of the webpage rendering. Defaults to 1. Scale amount must be between 0.1 and 2. |
        | ``tagged`` | Whether or not to generate a tagged (accessible) PDF. Defaults to false. |
        | ``width`` | Paper width, accepts values labeled with units. |

        ``headerTemplate`` and ``footerTemplate`` should be valid HTML markup. The following
        classes can be used to inject printing values into them:
        - ``date`` formatted print date
        - ``title`` document title
        - ``url`` document location
        - ``pageNumber`` current page number
        - ``totalPages`` total pages in the document

        All possible units are:
        - ``px`` - pixel
        - ``in`` - inch
        - ``cm`` - centimeter
        - ``mm`` - millimeter

        ``headerTemplate`` and ``footerTemplate`` markup have the following limitations:
        - Script tags inside the templates are not evaluated.
        - Page styles are not visible inside the templates.

        Returns the path to the saved PDF file.

        More details can be found in the
        [https://playwright.dev/docs/api/class-page#page-pdf|Playwright pdf documentation].

        Example:
        | `New Browser`        Chromium              headless=True
        | `New Page`           ${URL}
        | `Emulate Media`      media=screen
        | ${pdf_path} =      `Save Page As Pdf`    page.pdf
        | Should Be Equal    ${pdf_path}           ${OUTPUT_DIR}${/}page.pdf
        """
        if not self._is_relative_to(path):
            path = Path(self.outputdir) / str(path)
        format_ = format.value
        margin_ = json.dumps(margin)
        logger.debug(
            f"Saving page as PDF with options: displayHeaderFooter: {displayHeaderFooter} "
            f"footerTemplate: {footerTemplate} format: {format_} headerTemplate: {headerTemplate} "
            f"height: {height} landscape: {landscape} margin: {margin_} outline: {outline} "
            f"pageRanges: {pageRanges} path: {path} preferCSSPageSize: {preferCSSPageSize} "
            f"printBackground: {printBackground} scale: {scale} tagged: {tagged} width: {width}"
        )
        with self.playwright.grpc_channel() as stub:
            response = stub.Pdf(
                Request().Pdf(
                    displayHeaderFooter=displayHeaderFooter,
                    footerTemplate=footerTemplate,
                    format=format_,
                    headerTemplate=headerTemplate,
                    height=height,
                    landscape=landscape,
                    margin=margin_,
                    outline=outline,
                    pageRanges=pageRanges,
                    path=str(path),
                    preferCSSPageSize=preferCSSPageSize,
                    printBackground=printBackground,
                    scale=scale,
                    tagged=tagged,
                    width=width,
                )
            )
        logger.info(response.log)
        return response.body

    def _is_relative_to(self, path) -> bool:
        if sys.version_info[1] == 8:
            try:
                return path.relative_to(self.outputdir)
            except ValueError:
                return False
        return path.is_relative_to(self.outputdir)

    @keyword(tags=("Setter", "PageContent"))
    def emulate_media(
        self,
        colorScheme: ColorScheme | None = None,
        forcedColors: ForcedColors | NotSet = NotSet.not_set,
        media: Media | None = None,
        reducedMotion: ReducedMotion | None = None,
    ) -> dict:
        """Changes the CSS media type.

        It changes the CSS media type through the ``media`` argument, and/or the
        ``prefers-color-scheme`` media feature, using the ``colorScheme`` argument.
        This is useful to render the page in the correct format before using the
        `Save Page As Pdf` keyword.

        | =Arguments= | =Description= |
        | ``colorScheme`` | Emulates the ``prefers-color-scheme`` media feature, supported values are ``light`` and ``dark``. Passing ``null`` disables color scheme emulation. ``no-preference`` is deprecated. |
        | ``forcedColors`` | Emulates the ``forced-colors`` media feature, supported values are ``active`` and ``none``. Passing ``null`` disables forced colors emulation. |
        | ``media`` | Changes the CSS media type of the page. The only allowed values are ``screen``, ``print`` and ``null``. Passing ``null`` disables CSS media emulation. |
        | ``reducedMotion`` | Emulates the ``prefers-reduced-motion`` media feature, supported values are ``reduce`` and ``no-preference``. Passing ``null`` disables reduced motion emulation. |

        Arguments which are left to their default value are not sent to Playwright at
        all and therefore the corresponding emulation is left unchanged.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.EmulateMedia(
                Request().EmulateMedia(
                    colorScheme=(
                        str(NotSet.not_set.name)
                        if colorScheme is None
                        else str(colorScheme.name)
                    ),
                    forcedColors=str(forcedColors.name),
                    media=(
                        str(NotSet.not_set.name) if media is None else str(media.name)
                    ),
                    reducedMotion=(
                        str(NotSet.not_set.name)
                        if reducedMotion is None
                        else reducedMotion.value
                    ),
                )
            )
        logger.info(response.log)
        return json.loads(response.body)
