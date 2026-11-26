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

// Puts the `__rewriteAction` hooks of JS extensions into the page
// (`installRewritingScript`), where page/recorder-rewrite-action.ts runs them
// (`runRewriters`) and reports the Action with what they changed, and
// rewrites a picked selector with them (`rewritePickedSelector`); see
// Browser/recorder/README.md, "Extension hooks".
// What Playwright does not promise is used here and in
// page/recorder-rewrite-action.ts only. Exports starting with `__` are never
// keywords (`initializeExtension`).

import * as fs from 'fs';
import * as path from 'path';
import { BrowserContext, Page } from 'playwright';

import { logger } from './browser_logger';
import {
    LOG_BINDING,
    REWRITE_PICKED_SELECTOR_FUNCTION,
    Rewriter,
    rewritersScript,
} from './recorder-rewrite-action-contract';

// A module loaded with the `jsextension` import argument.
export type JsExtension = Record<string, unknown>;

const REWRITE_ACTION_HOOK = '__rewriteAction';

const FRAME_ENTRY = ' >> internal:control=enter-frame >> ';

// Puts the hooks of `extensions` into every frame of `context`, as one init
// script, now and after every navigation, unless they are there already.
// Without hooks the pages are left alone. Never fails: when Playwright does not
// offer what this needs, the Actions are recorded as Playwright reports them,
// and the reason is logged.
export async function installRewritingScript(context: BrowserContext, extensions: JsExtension[]): Promise<void> {
    const hooks = getHooks(extensions);
    if (hooks.length === 0) return;
    const exposeConsoleApi = (context as unknown as { _exposeConsoleApi?: () => Promise<void> })._exposeConsoleApi;
    if (!exposeConsoleApi) {
        log(
            'hooks cannot run, Actions are recorded as Playwright reports them: this Playwright version has no BrowserContext._exposeConsoleApi',
        );
        return;
    }
    const rewriters = hooks.map((hook) => ({ name: hook.name, rewriteAction: hook }));
    await installInitScript(context, rewriters, exposeConsoleApi);
}

// `selector`, picked, as the hooks rewrite it in the frame of the picked element,
// which must still be there within `timeout` ms.
export async function rewritePickedSelector(
    selector: string,
    page: Page,
    timeout: number,
    extensions: JsExtension[] = [],
): Promise<string> {
    const hooks = getHooks(extensions);
    if (hooks.length === 0) return selector;
    // The hooks see only the selector inside the picked element's frame, so the
    // frames go before what they give.
    const frames = framesOf(selector);
    const selectorInFrame = selector.slice(frames.length);
    try {
        const rewrittenSelector = await page
            .locator(selector)
            .evaluate(rewriteInPage, [REWRITE_PICKED_SELECTOR_FUNCTION, selectorInFrame] as const, {
                timeout,
            });
        return frames + rewrittenSelector;
    } catch (error) {
        log(`could not run on the pick, it is kept: ${String(error)}`);
        return selector;
    }
}

// The `__rewriteAction` hook of each extension that has one, in load order. A
// hook must be written as `function name(...) {...}`: the page runs its source,
// which a method, an arrow or an `async` function would break for every hook,
// and logs by its name, which one that only got the name of the export it is
// assigned to does not have. Any other hook is left out and logged, by its
// place among the hooks.
function getHooks(extensions: JsExtension[]): Rewriter['rewriteAction'][] {
    return extensions
        .map((extension) => extension[REWRITE_ACTION_HOOK])
        .filter((hook) => hook !== undefined)
        .filter((hook, index): hook is Rewriter['rewriteAction'] => {
            if (isNamedFunctionExpression(hook)) return true;
            log(`number ${index + 1} is not a named function, left out`);
            return false;
        });
}

function isNamedFunctionExpression(hook: unknown): boolean {
    if (typeof hook !== 'function') return false;
    if (hook.name === '' || hook.name === REWRITE_ACTION_HOOK) return false;
    return /^function\b/.test(Function.prototype.toString.call(hook));
}

// Writes `message` to playwright-log.txt, as a line about the hooks.
function log(message: string): void {
    logger.info(`recorder: ${REWRITE_ACTION_HOOK} ${message}`);
}

// The hooks each context has, as the script that gives them to the page.
const installedScripts = new WeakMap<BrowserContext, string>();

// Puts `rewriters` into every frame of `context`, by their names and in order,
// together with the page script that runs them, as one init script, unless the
// hooks are there already, once the context is prepared for it with
// `exposeConsoleApi`.
async function installInitScript(
    context: BrowserContext,
    rewriters: Rewriter[],
    exposeConsoleApi: () => Promise<void>,
): Promise<void> {
    const script = rewritersScript(rewriters);
    if (script === installedScripts.get(context)) return;
    try {
        await prepareContext(context, exposeConsoleApi);
        // A later script overrides the hooks an earlier one gave the page; the
        // page script installs itself only once.
        await addScriptToEveryFrame(context, `${script}\n${pageScript()}`);
        installedScripts.set(context, script);
    } catch (error) {
        log(`hooks cannot run, Actions are recorded as Playwright reports them: ${String(error)}`);
    }
}

// The contexts that have the console API and the binding the page logs through.
const preparedContexts = new WeakSet<BrowserContext>();

// Gives `context` what the hooks' init script needs, once: the console API, and
// the binding the page logs through, which cannot be exposed twice in a context.
async function prepareContext(context: BrowserContext, exposeConsoleApi: () => Promise<void>): Promise<void> {
    if (preparedContexts.has(context)) return;
    await exposeConsoleApi.call(context);
    await context.exposeBinding(LOG_BINDING, (_source, line: unknown) => {
        log(String(line));
    });
    preparedContexts.add(context);
}

// The page side, page/recorder-rewrite-action.ts as built into static/, which
// is next to index.js at runtime and to this file under Jest.
function pageScript(): string {
    return fs.readFileSync(path.join(__dirname, 'static', 'recorder-rewrite-action.js'), 'utf8');
}

async function addScriptToEveryFrame(context: BrowserContext, script: string): Promise<void> {
    await context.addInitScript({ content: script });
    const frames = context.pages().flatMap((page) => page.frames());
    await Promise.all(frames.map((frame) => frame.evaluate(script).catch(() => undefined)));
}

// The frames a selector enters, up to the selector inside the last of them.
function framesOf(selector: string): string {
    const entered = selector.lastIndexOf(FRAME_ENTRY);
    if (entered === -1) return '';
    return selector.slice(0, entered + FRAME_ENTRY.length);
}

// Runs in the frame of the picked element: `selector`, the picked selector
// inside that frame, as the page script's rewrite function gives it.
// Playwright runs only this function's source in the page, so the name of that
// function, `REWRITE_PICKED_SELECTOR_FUNCTION`, comes as an argument.
function rewriteInPage(_element: Element, [functionName, selector]: readonly [string, string]): string {
    const rewrite = (window as unknown as Record<string, (selector: string) => string>)[functionName];
    return rewrite(selector);
}
