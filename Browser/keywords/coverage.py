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

from os import PathLike
from pathlib import Path
from typing import Optional

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import CoverageType, SelectionType, keyword, logger


class Coverage(LibraryComponent):

    @keyword(tags=("Setter", "Coverage"))
    def start_coverage(self, coverage_type: CoverageType = CoverageType.all) -> str:
        """Starts the coverage for the current page.

        | =Arguments= | =Description= |
        | ``coverage_type`` | Type of coverage to start. Default is `all`. |

        The `coverage_type` can be one of the following:
        - `all`: Both [https://playwright.dev/docs/api/class-coverage/#coverage-start-css-coverage|CSS] and [https://playwright.dev/docs/api/class-coverage/#coverage-start-js-coverage|JS].
        - css: [https://playwright.dev/docs/api/class-coverage/#coverage-start-css-coverage|CSS].
        - js: [https://playwright.dev/docs/api/class-coverage/#coverage-start-js-coverage|JS].

        Coverage must started called when page is open and before any action is
        performed on the page. Coverage be stopped by calling `Stop Coverage` keyword
        and must be called before page is closed.

        Example:
        | `New Page`
        | `Start Coverage`
        | `Go To`    ${LOGIN_URL}
        | Do Something In The Page
        | `Stop Coverage`
        """
        logger.info(f"Starting coverage for {coverage_type.name}")
        with self.playwright.grpc_channel() as stub:
            response = stub.StartCoverage(
                Request.CoverateStart(
                    coverateType=coverage_type.name,
                )
            )
            logger.info(response.log)
            page_id = response.body
        self.coverage_types[page_id] = coverage_type
        return str(coverage_type)

    @keyword(tags=("Getter", "Coverage"))
    def stop_coverage(
        self,
        config_file: Optional[PathLike] = None,
    ) -> Path:
        """Stops the coverage for the current page.

        | =Arguments= | =Description= |
        | ``config_file`` | Optional path to [https://www.npmjs.com/package/monocart-coverage-reports#options|options file] |

        Creates a coverage report by using
        [https://www.npmjs.com/package/monocart-coverage-reports|monocart-coverage-reports]
        To see the default and all possible options, see
        [https://github.com/cenfun/monocart-coverage-reports/blob/HEAD/lib/default/options.js|options.js]
        file for more details. Returns the path to the folder where
        coverage reported."""
        catalog = self.library.get_page_ids(page=SelectionType.CURRENT)
        if not catalog:
            raise ValueError("No pages open")
        page = catalog[0]
        coverage_type = self.coverage_types.pop(page, CoverageType.all)
        coverage_dir = Path(self.outputdir) / "coverage_reports" / f"{page}_coverage"
        logger.info(
            f"Stopping coverage for {page} with {coverage_type.name} to {coverage_dir}"
        )
        with self.playwright.grpc_channel() as stub:
            response = stub.StopCoverage(
                Request.CoverageStop(
                    configFile=str(config_file) if config_file else "",
                    outputDir=str(coverage_dir),
                    coverateType=coverage_type.name,
                )
            )
            logger.info(response.log)
        return coverage_dir
