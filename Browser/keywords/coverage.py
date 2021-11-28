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
from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import CoverageType, keyword, logger


class Coverage(LibraryComponent):
    @keyword(tags=("Setter", "PageContent"))
    def start_coverage(self, coverage_type=CoverageType.js):
        with self.playwright.grpc_channel() as stub:
            response = stub.StartCoverage(Request().StartCoverage())
        logger.info(f"Coverage: {response.log}")

    @keyword(tags=("Getter", "PageContent"))
    def stop_coverage(self):
        with self.playwright.grpc_channel() as stub:
            response = stub.StopCoverage(Request().Json())
        logger.info(f"Coverage: {response.log}")
