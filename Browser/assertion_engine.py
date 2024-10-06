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
import time
from typing import Optional, Union, get_args, get_origin

import wrapt  # type: ignore
from assertionengine import AssertionOperator

from .utils import logger


def assertion_operator_is_set(wrapped, args, kwargs):
    assertion_operator = None
    assertion_op_name = None
    assertion_op_index = None
    for index, (_arg, typ) in enumerate(wrapped.__annotations__.items()):
        if get_origin(typ) is Union and AssertionOperator in get_args(typ):
            assertion_op_index = index
            break
        if typ is AssertionOperator:
            assertion_op_index = index
            break
    if assertion_op_index is not None:
        if len(args) > assertion_op_index:
            assertion_operator = args[assertion_op_index]
        elif assertion_op_name in kwargs:
            assertion_operator = kwargs[assertion_op_name]
    return assertion_operator


@wrapt.decorator
def with_assertion_polling(wrapped, instance, args, kwargs):
    start = time.time()
    timeout = instance.timeout / 1000
    retry_assertions_until = instance.retry_assertions_for / 1000
    retries_start: Optional[float] = None
    tries = 1
    try:
        logger.stash_this_thread()
        while True:
            try:
                return wrapped(*args, **kwargs)
            except AssertionError as e:
                if retries_start is None:
                    retries_start = time.time()
                elapsed = time.time() - start
                elapsed_retries = time.time() - retries_start
                if elapsed >= timeout or elapsed_retries >= retry_assertions_until:
                    raise e
                tries += 1
                if timeout - elapsed > 0.01:  # noqa: PLR2004
                    time.sleep(0.01)
                logger.clear_thread_stash()
    finally:
        logger.flush_and_delete_thread_stash()
        if retry_assertions_until and assertion_operator_is_set(wrapped, args, kwargs):
            now = time.time()
            logger.debug(
                f"Assertion polling statistics:\n"
                f"First element asserted in: {(retries_start or now) - start} seconds\n"
                f"Total tries: {tries}\n"
                f"Elapsed time in retries {now - (retries_start or now)} seconds"
            )


def assertion_formatter_used(func):
    func.assertion_formatter_used = True
    return func
