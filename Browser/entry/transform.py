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

import subprocess
from pathlib import Path

TIDY_TRANSFORMER_DIR = Path(__file__).parent.parent / "tidy_transformer"


def transform(
    path: Path,
    wait_until_network_is_idle: bool,
) -> None:
    cmd = ["robotidy"]
    if wait_until_network_is_idle:
        wait_until_network_is_idle_file = TIDY_TRANSFORMER_DIR / "network_idle.py"
        cmd.append("--transform")
        cmd.append(str(wait_until_network_is_idle_file))
    cmd.extend([str(item) for item in path])  # type: ignore
    subprocess.run(cmd, check=False)
