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

import { Script } from 'vm';

import * as pb from './generated/playwright';
import { exists } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog } from './response-util';

export function initScriptSource(content: string, arg?: string): string {
    if (arg === undefined) return content;
    const expression = `(${content}\n)`;
    try {
        new Script(expression);
    } catch {
        throw new Error(`With arg, the init script must be a single function expression, got:\n${content}`);
    }
    return `${expression}(${arg})`;
}

export async function addContextInitScript(
    request: pb.Request_InitScript,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const context = state.getActiveContext();
    exists(context, 'Tried to add an init script, but no context was open.');
    await context.addInitScript({ content: initScriptSource(request.content, request.arg) });
    return emptyWithLog('Added init script to the active context.');
}

export async function addPageInitScript(
    request: pb.Request_InitScript,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const page = state.getActivePage();
    exists(page, 'Tried to add an init script, but no page was open.');
    await page.addInitScript({ content: initScriptSource(request.content, request.arg) });
    return emptyWithLog('Added init script to the active page.');
}
