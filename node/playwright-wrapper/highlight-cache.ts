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

/**
 * Highlights made with `duration=0` that are waiting to be disposed.
 *
 * Its own module rather than `evaluation.ts` because `PlaywrightState` owns one
 * and `evaluation.ts` already imports `playwright-state.ts`. A module both can
 * import has no cycle, and a cycle would bite here: the cache is constructed in
 * the `PlaywrightState` constructor.
 */
export class HighlightDisposableCache {
    private disposables: Array<{ dispose: () => Promise<void> }>;

    constructor() {
        this.disposables = [];
    }

    add(disposable: { dispose: () => Promise<void> }) {
        this.disposables.push(disposable);
    }

    async disposeAll() {
        await Promise.all(this.disposables.map((d) => d.dispose()));
        this.disposables = [];
    }
}
