// Copyright 2020-     Robot Framework Foundation
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

// Entry point for the child processes Playwright forks, most notably the out
// of process browser download in playwright-core/lib/entry/oopBrowserDownload.js.
//
// Playwright's own entry script is required only after the inspector shim has
// been installed, which node/build.wrapper.js injects ahead of this file. The
// script to run is passed in the environment by wrapFork() in inspector-shim.ts.
//
// Playwright talks to these children over the fork IPC channel, and requiring
// the target here keeps it in this process, so process.send() and the
// 'message' handlers it registers keep working.

import { FORK_TARGET_ENV } from './inspector-shim';

const target = process.env[FORK_TARGET_ENV];

if (!target) {
    throw new Error(`${FORK_TARGET_ENV} is not set, nothing to run.`);
}

// Not inherited by anything this child may fork itself; wrapFork() always sets
// it explicitly.
delete process.env[FORK_TARGET_ENV];

// module.require, not require, so that esbuild leaves the lookup to run time.
module.require(target);
