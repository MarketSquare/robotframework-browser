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

import json
from typing import Dict

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import keyword, logger


class Devices(LibraryComponent):
    @keyword(tags=("Getter", "BrowserControl"))
    def get_devices(self) -> Dict:
        """Returns a dict of all playwright device descriptors.

        See Playwright's [https://github.com/Microsoft/playwright/blob/master/src/server/deviceDescriptors.ts | deviceDescriptors.ts]
        for a formatted list.
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDevices(Request().Empty())
            logger.debug(response.log)
            return json.loads(response.json)

    @keyword(tags=("Getter", "BrowserControl"))
    def get_device(self, name: str) -> Dict:
        """Get a single device decriptor with name exactly matching name.

        ``name`` Given name of the requested device. See Playwright's
        [https://github.com/Microsoft/playwright/blob/master/src/server/deviceDescriptors.ts | deviceDescriptors.ts]
        for a formatted list.

        Allows a concise syntax to set website testing values to exact matches of specific
        mobile devices.

        Use by passing to a context. After creating a context with devicedescriptor,
        before using ensure your active page is on that context.
        Usage:

        | ${device}=          Get Device       iPhone X
        | New Context         &{device}
        | New Page
        | Get Viewport Size   # returns { "width": 375, "height": 812 }
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.GetDevice(Request().Device(name=name))
            logger.debug(response.log)
            return json.loads(response.json)
