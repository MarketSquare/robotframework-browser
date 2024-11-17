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
import logging
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Union


def combine(
    input_folder: Path,
    output_folder: Path,
    config: Union[Path, None],
    logger: logging.Logger,
    shell: bool,
    install_dir: Path,
) -> None:
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
    raw_reports = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for file in input_folder.iterdir():
            if file.is_dir() and file.joinpath("raw").is_dir():
                raw_dir = file.joinpath("raw")
                logger.info(f"Folder {raw_dir} found")
                for raw_file in raw_dir.iterdir():
                    if raw_file.is_file():
                        shutil.copy(raw_file, tmp_path.joinpath(raw_file.name))
                        raw_reports.append(raw_file)
        if not raw_reports:
            logger.error(f"No raw reports found from {input_folder}")
            sys.exit(2)
        args = [
            "npx",
            "mcr",
            "--logging",
            "debug",
            "--inputDir",
            f"{tmp_path!s}",
            "--outputDir",
            f"{output_folder!s}",
            "command",
        ]
        if config is not None:
            args.extend(["--config", f"{config!s}"])
        subprocess.run(args, check=True, shell=shell, cwd=install_dir)
        logger.info(f"Combined coverage files to {output_folder}")
