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

import { randomUUID } from 'crypto';
import { Script } from 'vm';

import * as pb from './generated/playwright';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog } from './response-util';

export function initScriptSource(content: string, arg?: string): string {
    if (arg === undefined) return content;
    try {
        new Script(`(${content}\n);`);
    } catch (error) {
        throw new Error(`With arg, the init script must be one expression: ${String(error)}`, {
            cause: error,
        });
    }
    return `(${content}\n)(${arg});`;
}

export async function addInitScript(
    request: pb.Request_InitScript,
    state: PlaywrightState,
): Promise<pb.Response_InitScriptAdded> {
    const indexedContext = state.activeBrowser?.context;
    if (!indexedContext) throw new Error('No context open, can not add an init script');
    const content = initScriptSource(request.content, request.arg);
    const scriptId = `initScript=${randomUUID()}`;
    indexedContext.initScripts.set(scriptId, await indexedContext.c.addInitScript({ content }));
    return pb.Response_InitScriptAdded.create({
        log: `Added init script ${scriptId} to context ${indexedContext.id}`,
        contextId: indexedContext.id,
        scriptId,
    });
}

export async function removeInitScript(
    request: pb.Request_InitScriptId,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const initScripts = state.findContext(request.contextId)?.initScripts;
    const disposable = initScripts?.get(request.scriptId);
    if (!initScripts || !disposable) {
        return emptyWithLog(`Context ${request.contextId} is closed, init script ${request.scriptId} went with it`);
    }
    initScripts.delete(request.scriptId);
    await disposable.dispose();
    return emptyWithLog(`Removed init script ${request.scriptId} from context ${request.contextId}`);
}
