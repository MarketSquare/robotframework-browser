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

import shutil
import tempfile
from collections.abc import Iterator
from os import PathLike
from pathlib import Path

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import CoverageType, keyword, logger


class Coverage(LibraryComponent):
    @keyword(tags=("Setter", "Coverage", "Experimental"))
    def start_coverage(
        self,
        *,
        config_file: PathLike | None = None,
        coverage_type: CoverageType = CoverageType.all,
        path: Path = Path(),
        raw: bool = False,
        reportAnonymousScripts: bool = False,
        resetOnNavigation: bool = True,
    ) -> str:
        """Starts the coverage for the current page.

        | =Arguments= | =Description= |
        | ``config_file`` | Optional path to [https://www.npmjs.com/package/monocart-coverage-reports#options|options file] |
        | ``coverage_type`` | Type of coverage to start. Default is `all`. |
        | ``path`` | Absolute or relative directory path (relative to ``${OUTPUT_DIR}/browser/coverage/``) where the coverage is store in a directory with the page id name. |
        | ``raw`` | Whether to save raw coverage data. Default is `False`. |
        | ``reportAnonymousScripts`` | Whether to report anonymous scripts. Default is `False`. Only valid for JS coverage. |
        | ``resetOnNavigation`` | Whether to reset coverage on navigation. Default is `True`. |

        The `coverage_type` can be one of the following:
        - ``all``: Both [https://playwright.dev/docs/api/class-coverage/#coverage-start-css-coverage|CSS] and [https://playwright.dev/docs/api/class-coverage/#coverage-start-js-coverage|JS].
        - ``css``: [https://playwright.dev/docs/api/class-coverage/#coverage-start-css-coverage|CSS].
        - ``js``: [https://playwright.dev/docs/api/class-coverage/#coverage-start-js-coverage|JS].

        Coverage must started when page is open and before any action is
        performed on the page. Coverage will be stored when calling `Stop Coverage` keyword
        or page or context is closed. This is done automatically when using the auto closing.

        The `raw` argument saves the raw coverage data in the coverage folder. The raw data
        is needed to combine multiple coverage reports to single report. Singel report can
        be created with `rfbrowser coverage /path/to/basefolder/ /path/to/outputfolder/`
        command. Pleaee note that the `raw` argument is ignored if the `config_file`
        is defined. In this case user is responsible to also set the raw reporter
        in the config file. To see more details about combining coverage data, run:
        `rfbrowser coverage --help` command.

        Example:
        | `New Page`
        | `Start Coverage`
        | `Go To`    ${LOGIN_URL}
        | Do Something In The Page
        | `Stop Coverage`
        """
        logger.info(f"Starting coverage for {coverage_type.name}")
        if config_file and not config_file.is_file():  # type: ignore[attr-defined]
            logger.info(f"Config file {config_file} not found. Ignoring the file.")
        with self.playwright.grpc_channel() as stub:
            response = stub.StartCoverage(
                Request.CoverageStart(
                    coverageType=coverage_type.name,
                    resetOnNavigation=resetOnNavigation,
                    reportAnonymousScripts=reportAnonymousScripts,
                    configFile=str(config_file) if config_file else "",
                    coverageDir=str(self.coverage_ouput / path),
                    raw=raw,
                )
            )
            logger.info(response.log)
        return str(coverage_type)

    @keyword(tags=("Getter", "Coverage"))
    def stop_coverage(
        self,
    ) -> Path:
        """Stops the coverage for the current page.

        Creates a coverage report by using
        [https://www.npmjs.com/package/monocart-coverage-reports|monocart-coverage-reports]
        To see the default and all possible options, see
        [https://github.com/cenfun/monocart-coverage-reports/blob/HEAD/lib/default/options.js|options.js]
        file for more details. Returns the path to the folder where
        coverage reported.
        """
        logger.info("Stopping coverage")
        with self.playwright.grpc_channel() as stub:
            response = stub.StopCoverage(Request.Empty())
            logger.info(response.log)
        coverage_dir = Path(response.body)
        coverage_index_html = list(coverage_dir.glob("*.html"))
        if not coverage_index_html:
            logger.info(
                f"No coverage report found from  {coverage_dir}. Default folder or file type "
                "could have been changed by {config_file}, return the coverage folder."
            )
            return coverage_dir
        file_path = coverage_index_html[0]
        logger.info(f"Coverage report saved to {file_path.as_uri()}")
        return file_path

    @keyword(tags=("Setter", "Coverage"))
    def merge_coverage_reports(
        self,
        input_folder: Path,
        output_folder: Path,
        config_file: Path | None = None,
        name: str | None = None,
        reports: list[str] | None = None,
    ) -> Path:
        """Combines multiple raw coverage reports to single report.

        | =Arguments= | =Description= |
        | ``input_folder`` | Path to the base folder where the raw coverage reports are located. |
        | ``output_folder`` | Path to the folder where the combined report is stored. |
        | ``config_file`` | Optional path to [https://www.npmjs.com/package/monocart-coverage-reports#options|options file] |
        | ``name`` | Optional name for the combined report. |
        | ``reports`` | Optional report format (default is "v8"). |

        The input_folder argument is the base folder where the coverage reports are
        located. Keyword will look into each subfolder and if the subfolder
        contains "raw" folder, it will use data from the "raw" folder for
        combined reports.

        The output_folder argument is the folder where the combined report is saved.
        If folder does not exist, it is created. If folder exists, it's content
        is deleted before report is created.

        The output_folder and input_folder must be full paths to the folders.

        The config_file argument is optional and can be used to provide a path to a
        monocart-coverage-reports options file. For more details see:
        https://www.npmjs.com/package/monocart-coverage-reports#config-file

        The name argument is optional and can be used to provide a name for the
        combined report.

        The reports argument is optional and can be used to provide a list of
        reporters to create. Default is 'v8'.

        The keyword combines only the raw reports. To get raw reports,
        `Start Coverage` keyword must be called with `raw=True` argument.
        Keyword should be used when there is a need to combine multiple reports
        to single report. For example, when tests are run in multiple pages, the
        example in below demonstrates how to use the keyword.

        Example:
        | `New Page`
        | `Start Coverage`
        | `Go To`    ${LOGIN_URL}
        | Test Feature X In The Page
        | `Stop Coverage`
        | `New Page`
        | `Start Coverage`
        | `Go To`    ${LOGIN_URL}
        | Test Feature Y In The Page
        | `Stop Coverage`
        | `Merge Coverage Reports`    ${OUTPUT_DIR}/browser/coverage    ${OUTPUT_DIR}/browser/combined-coverage
        """
        logger.info(
            f"Combining coverage reports from {input_folder} to {output_folder}"
        )
        if config_file is not None and config_file.is_file():
            logger.info(f"Using configuration from {config_file}")
        if config_file is not None and not config_file.is_file():
            raise FileNotFoundError(f"Configuration file {config_file} does not exist")
        if output_folder.exists():
            logger.warn(
                f"Output folder {output_folder} already exists, deleting it first"
            )
            shutil.rmtree(output_folder)
        raw_reports = False
        reports = reports or ["v8"]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for raw_file in _find_coverage_files(input_folder):
                shutil.copy(raw_file, tmp_path.joinpath(raw_file.name))
                raw_reports = True
            if not raw_reports:
                logger.error(f"No raw reports found from {input_folder}")
                raise FileNotFoundError(f"No raw reports found from {input_folder}")
            with self.playwright.grpc_channel() as stub:
                response = stub.MergeCoverage(
                    Request.CoverageMerge(
                        input_folder=str(tmp_path),
                        output_folder=str(output_folder),
                        config=str(config_file) if config_file else "",
                        name=name if name else "",
                        reports=reports,
                    )
                )
                logger.info(response.log)
        return output_folder


def _find_coverage_files(input_folder: Path) -> Iterator:
    for file in input_folder.rglob("*"):
        if file.is_dir() and file.joinpath("raw").is_dir():
            raw_dir = file.joinpath("raw")
            logger.debug(f"Raw folder {raw_dir} found")
            for raw_file in raw_dir.iterdir():
                if raw_file.is_file():
                    yield raw_file
