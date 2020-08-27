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

from typing import Any

from robot.api import logger  # type: ignore


def info(msg: Any, html=False):
    logger.info(msg, html)


def debug(msg: Any, html=False):
    logger.debug(msg, html)


def trace(msg: Any, html=False):
    logger.trace(msg, html)


def warn(msg: Any, html=False):
    logger.warn(msg, html)


def error(msg: Any, html=False):
    logger.error(msg, html)


def console(msg: Any):
    logger.console(msg)
