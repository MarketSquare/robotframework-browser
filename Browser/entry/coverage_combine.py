# Copyright 2024-     Robot Framework Foundation
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
from pathlib import Path
from typing import Optional, Union

from .constant import get_browser_lib, logger


def combine(
    input_folder: Path,
    output_folder: Path,
    config: Union[Path, None],
    name: Optional[str] = None,
    reports: str = "v8",
) -> None:
    cwd = Path(Path.cwd())
    if not cwd.is_relative_to(output_folder):
        output_folder = cwd.joinpath(output_folder)
    logger.info(f"Combining coverage files from {input_folder} to {output_folder}")
    browser_lib = get_browser_lib()
    reports_list = reports.split(";") if ";" in reports else [reports]
    folder = browser_lib.merge_coverage_reports(
        input_folder=input_folder,
        output_folder=output_folder,
        config_file=config,
        name=name,
        reports=reports_list,
    )
    logger.info(f"Combined coverage files to {folder}")
