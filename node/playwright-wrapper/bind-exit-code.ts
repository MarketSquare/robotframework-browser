// Copyright 2026-     Robot Framework Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// The library starts the wrapper on a port it found free. Another process can
// take that port before the wrapper listens. Exiting with this code tells the
// library so, and it starts the wrapper again on a fresh port.
export const PORT_TAKEN_EXIT_CODE = 3;

// grpc-js names the cause only in the message of the error bindAsync passes.
export function bindErrorExitCode(error: Error): number {
    return error.message.includes('EADDRINUSE') ? PORT_TAKEN_EXIT_CODE : 1;
}
