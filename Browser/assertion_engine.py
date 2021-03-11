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
from typing import Optional

import wrapt  # type: ignore

from .utils import logger


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
                if timeout - elapsed > 0.01:
                    time.sleep(0.01)
                logger.clear_thread_stash()
    finally:
        logger.flush_and_delete_thread_stash()
        now = time.time()
        logger.debug(
            f"""Assertion polling statistics:
First element asserted in: {(retries_start or now) - start} seconds
Total tries: {tries}
Elapsed time in retries {now - (retries_start or now)} seconds"""
        )
