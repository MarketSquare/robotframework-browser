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

// The contract between the two halves of rewriting a recorded Action: the Node
// half (recorder-rewrite-action.ts) and the page half
// (page/recorder-rewrite-action.ts). It holds the names both use on the page's
// `window`, the Rewriter the Node half gives the page, and the script through
// which it gives it (`rewritersScript`). Both halves import it, and neither
// imports the other. It holds no code that needs Node or a page.

import type { Action } from './recorder';

// Browser's binding through which the page logs to playwright-log.txt.
export const LOG_BINDING = '__rfbRecorderLog';
// Where `rewritersScript` puts the Rewriters on the page's `window`.
export const REWRITERS_PROPERTY = '__rfbRecorderRewriters';
// The function that gives the selector of a pick as the hooks rewrite it.
export const REWRITE_PICKED_SELECTOR_FUNCTION = '__rfbRewritePickedSelector';

// Writes a line to playwright-log.txt.
export type Log = (message: string) => void;

// The elements a selector finds in the page, with Playwright's own engines.
export type Query = (selector: string) => Element[];

// A rewrite of the recorded Action, as the page runs it. `rewriteAction` is the
// function an extension exports as `__rewriteAction`, and `name` is that
// function's own name, which starts every line it logs.
export interface Rewriter {
    name: string;
    rewriteAction: (args: { action: Action; element: Element; query: Query; log: Log }) => unknown;
}

// The script that puts `rewriters` on the page's `window`, in order. Each
// `rewriteAction` is written into it as its source, so the page runs it as a
// function.
export function rewritersScript(rewriters: Rewriter[]): string {
    const entries = rewriters.map(
        ({ name, rewriteAction }) => `{ name: ${JSON.stringify(name)}, rewriteAction: (${rewriteAction.toString()}) }`,
    );
    return `window[${JSON.stringify(REWRITERS_PROPERTY)}] = [${entries.join(', ')}];`;
}
