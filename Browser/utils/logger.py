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
import threading
from typing import Any, Callable, Dict, List

from robot.api import logger

_THREAD_STASHES: Dict[int, List[List[Callable]]] = {}


def _stashing_logger(funk: Callable):
    def func(msg: Any, html=False):
        if threading.get_ident() in _THREAD_STASHES:
            _THREAD_STASHES[threading.get_ident()][-1].append(lambda: funk(msg, html))
        else:
            funk(msg, html)

    return func


@_stashing_logger
def info(msg: Any, html=False):
    logger.info(msg, html)


@_stashing_logger
def debug(msg: Any, html=False):
    logger.debug(msg, html)


@_stashing_logger
def trace(msg: Any, html=False):
    logger.trace(msg, html)


@_stashing_logger
def warn(msg: Any, html=False):
    logger.warn(msg, html)


@_stashing_logger
def error(msg: Any, html=False):
    logger.error(msg, html)


def console(msg: Any):
    logger.console(msg)


def stash_this_thread():
    identifier = threading.get_ident()
    if identifier in _THREAD_STASHES:
        _THREAD_STASHES[identifier].append([])
    else:
        _THREAD_STASHES[threading.get_ident()] = [[]]


def clear_thread_stash():
    _THREAD_STASHES[threading.get_ident()][-1] = []


def flush_and_delete_thread_stash():
    stashes = _THREAD_STASHES[threading.get_ident()]
    if len(stashes) == 1:
        for logging_call in stashes[0]:
            logging_call()
        del _THREAD_STASHES[threading.get_ident()]
    else:
        last = stashes.pop()
        stashes[-1].extend(last)
