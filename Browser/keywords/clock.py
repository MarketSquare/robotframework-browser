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
from datetime import datetime

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import ClockType, keyword, logger


class Clock(LibraryComponent):

    @keyword(tags=("Setter", "Clock"))
    def clock_set_time(self, time: datetime, clock_type: ClockType = ClockType.install):
        """Sets the time of the browser's internal clock.

        | Argument | Description |
        | time     | The time to set. Suppots Robot Framework date and time format |
        | clock_type | The clock type to set. Default is `install`. |

        The fixed makes Date.now and new Date() return fixed fake
        time at all times, keeps all the timers running.

        The system sets current system time but does not trigger any timers.

        The install fake timers are used to manually control the flow of time in tests.
        They allow you to advance time, fire timers, and control the behavior
        of time-dependent functions.

        How to use clock related keywords, see
        [https://playwright.dev/docs/clock|Playwright clock documentation].
        Also reviewing the Playwright
        [https://playwright.dev/docs/api/class-clock|Clock API] is recommended.
        """
        logger.info(
            f"Setting clock to {time} {time.timestamp()} with type {clock_type.name}"
        )
        with self.playwright.grpc_channel() as stub:
            response = stub.SetTime(
                Request.ClockSetTime(
                    time=time.timestamp(),
                    setType=clock_type.name,
                )
            )
            logger.info(response.log)

    @keyword(tags=("Setter", "Clock"))
    def clock_resume(self):
        """Resumes the clock.

        Once keyword method is called, time resumes flowing,
        timers are fired as usual.
        """
        logger.info("Resuming clock")
        with self.playwright.grpc_channel() as stub:
            respose = stub.ClockResume(Request.Empty())
            logger.info(respose.log)
