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
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Optional, Union

from .constant import INSTALLATION_DIR, SHELL, logger


def _find_coverage_files(input_folder: Path) -> Iterator:
    for file in input_folder.rglob("*"):
        if file.is_dir() and file.joinpath("raw").is_dir():
            raw_dir = file.joinpath("raw")
            logger.info(f"Folder {raw_dir} found")
            for raw_file in raw_dir.iterdir():
                if raw_file.is_file():
                    yield raw_file


def combine(
    input_folder: Path,
    output_folder: Path,
    config: Union[Path, None],
    name: Optional[str] = None,
    reports="v8",
) -> None:
    cwd = Path(Path.cwd())
    if not cwd.is_relative_to(output_folder):
        output_folder = cwd.joinpath(output_folder)
    logger.info(f"Combining coverage files from {input_folder} to {output_folder}")
    if config is not None and config.is_file():
        logger.info(f"Using configuration from {config}")
    if config is not None and not config.is_file():
        logger.error(f"Configuration file {config} does not exist")
        sys.exit(2)
    if output_folder.exists():
        logger.error(f"Output folder {output_folder} already exists, deleting it first")
        shutil.rmtree(output_folder)
    output_folder.mkdir(parents=True)
    raw_reports = False
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for raw_file in _find_coverage_files(input_folder):
            shutil.copy(raw_file, tmp_path.joinpath(raw_file.name))
            raw_reports = True
        if not raw_reports:
            logger.error(f"No raw reports found from {input_folder}")
            sys.exit(2)
        args = [
            "npx",
            "mcr",
            "merge",
            "--reports",
            reports,
            "--inputDir",
            str(tmp_path),
            "--outputDir",
            str(output_folder),
        ]
        if config is not None:
            args.extend(["--config", str(config)])
        if name is not None:
            args.extend(["--name", name])
        logger.info(f"Running command: {args}")
        subprocess.run(args, check=True, shell=SHELL, cwd=INSTALLATION_DIR)
        logger.info(f"Combined coverage files to {output_folder}")
