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
#
# Derived from https://github.com/robotframework/SeleniumLibrary and modified by Tatu Aalto

import re
from typing import List


class LocatorParse:

    _strategies_light = ("css:light", "text:light")
    _strategies = ("css", "xpath", "id", "text", *_strategies_light)

    def parse_locator(self, locator: str) -> str:
        full_locator = ""
        for part in self._split_locator(locator):
            if part != " >> ":
                part = self._parse_locator(part)
            full_locator = f"{full_locator}{part}"
        return full_locator

    def _split_locator(self, locator: str) -> List[str]:
        locator_parts = []
        while True:
            parts = re.search(r"(.*)(\s>>\s)(xpath:|css:|id:|text:)(.*)", locator)
            if parts:
                locator = parts.group(1)
                locator_parts.append(f"{parts.group(3)}{parts.group(4)}")
                locator_parts.append(parts.group(2))
            if not parts:
                locator_parts.append(locator)
                break
        locator_parts.reverse()
        return locator_parts

    def _parse_locator(self, locator: str) -> str:
        if locator.startswith(("//", "(//")):
            return f"xpath={locator}"
        index = self._strategy_index(locator)
        if index != -1:
            strategy = locator[:index].strip()
            if strategy in self._strategies:
                return f"{strategy}={locator[index + 1:].lstrip()}"
        return f"css={locator}"

    def _strategy_index(self, locator: str) -> int:
        if locator.lower().startswith(self._strategies_light):
            strategy = ":".join(locator.split(":", 2)[:2])
            return len(strategy)
        return locator.find(":")
