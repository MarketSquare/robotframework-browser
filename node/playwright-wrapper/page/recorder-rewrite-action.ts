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

// Runs the `__rewriteAction` hooks of JS extensions in the page, before an
// Action changes it; see Browser/recorder/README.md, "Extension hooks".
// Playwright's injected recorder reports every Action by calling
// `window.__pw_recorderRecordAction(action)` synchronously in its capture
// listener, before the page's click handlers run. The wrapper of that binding
// runs the hooks and reports the Action with what they changed; Playwright
// then puts the frames before its selector. What the hooks log goes to Node
// through Browser's own binding, `LOG_BINDING`.

// Only a type from recorder.ts: the page script takes no Node code.
import type { Action } from '../recorder';
import {
    Log,
    LOG_BINDING,
    Query,
    REWRITE_PICKED_SELECTOR_FUNCTION,
    Rewriter,
    REWRITERS_PROPERTY,
} from '../recorder-rewrite-action-contract';

export const PW_RECORD_ACTION_BINDING = '__pw_recorderRecordAction';

// Playwright's binding through which the injected recorder reports each Action
// to the recorder in Node.
type ReportAction = (action: Action, preconditionSelector?: string) => unknown;

// Replaces `window.__pw_recorderRecordAction`, the function that reports each
// Action to the recorder in Node, with one that reports the Action as
// `reuseClick` or else `rewriteAction` gives it.
export function patchReportAction(window: Record<string, unknown>): void {
    let lastAction: Action | undefined;
    let lastPlaywrightSelector: string | undefined;
    monkeyPatch<ReportAction>(window, PW_RECORD_ACTION_BINDING, (reportAction) => (action, preconditionSelector) => {
        lastAction = reuseClick(lastPlaywrightSelector, lastAction, action) ?? rewriteAction(window, action);
        lastPlaywrightSelector = action.selector;
        return reportAction(lastAction, preconditionSelector);
    });
}

// Defines `window.__rfbRewritePickedSelector`, the function that rewrites the
// selector of a pick with `rewriteAction`. The Node half calls it on the picked
// element (`rewritePickedSelector`).
export function defineRewritePickedSelector(window: Record<string, unknown>): void {
    window[REWRITE_PICKED_SELECTOR_FUNCTION] = (selector: string) =>
        rewriteAction(window, { name: 'pick', selector }).selector as string;
}

// A later click of a double or triple click replaces the click before
// (`RecorderSignalProcessor._supersedes`), which already changed the page.
function reuseClick(selector: string | undefined, lastAction: Action | undefined, action: Action): Action | undefined {
    return lastAction?.name === 'click' && action.selector === selector && Number(action.clickCount) > 1
        ? { ...lastAction, clickCount: action.clickCount }
        : undefined;
}

// Monkey-patches the function `name` of `window` with what `patch` makes of it,
// whether it is set before or after this runs: every function set there later
// is patched too. Patches once, however often it runs.
function monkeyPatch<F extends (...args: never[]) => unknown>(
    window: Record<string, unknown>,
    name: string,
    patch: (original: F) => F,
): void {
    if (Object.getOwnPropertyDescriptor(window, name)?.get) return;
    const original = window[name] as F | undefined;
    let patched = original && patch(original);
    Object.defineProperty(window, name, {
        configurable: true,
        enumerable: true,
        get: () => patched,
        set: (value: F) => {
            patched = patch(value);
        },
    });
}

// `action` as the rewriters on `window` rewrite it; as it is when there are
// none, when it has no selector, or when they cannot run, which is logged.
function rewriteAction(window: Record<string, unknown>, action: Action): Action {
    const rewriters = (window[REWRITERS_PROPERTY] as Rewriter[] | undefined) ?? [];
    const actionSelector = action.selector;
    if (rewriters.length === 0 || typeof actionSelector !== 'string') return action;
    const log: Log = (message) => (window[LOG_BINDING] as Log | undefined)?.(message);
    try {
        const playwright = window.playwright as { $$: Query };
        const query: Query = (selector) => playwright.$$(selector);
        return runRewriters({ ...action, selector: actionSelector }, query, log, rewriters);
    } catch (error) {
        log(`the Action is kept: ${String(error)}`);
        return action;
    }
}

// `action` as the rewriters rewrite it, each the Action the one before gave.
// Unchanged when Playwright's own selector does not find exactly one element.
function runRewriters(action: Action & { selector: string }, query: Query, log: Log, rewriters: Rewriter[]): Action {
    const elements = query(action.selector);
    if (elements.length !== 1) {
        log(`${action.selector} finds ${elements.length} elements here, the Action is kept`);
        return action;
    }
    const element = elements[0];
    return rewriters.reduce<Action>(
        (rewrittenAction, rewriter) => applyRewriter(rewriter, rewrittenAction, element, query, log),
        action,
    );
}

// `action` with the parts `rewriter` changes, its name always Playwright's; or
// `action` as it is, when the rewriter fails or gives what cannot be recorded,
// and why is logged. The rewriter gets and gives copies, as data: it cannot
// change Playwright's Action, and what it gives always reaches Node.
function applyRewriter(rewriter: Rewriter, action: Action, element: Element, query: Query, log: Log): Action {
    const logAsRewriter: Log = (message) => log(`${rewriter.name}: ${message}`);
    try {
        const actionUpdates = copyOf(
            rewriter.rewriteAction({ action: copyOf(action), element, query, log: logAsRewriter }),
        );
        if (actionUpdates === undefined) return action;
        if (typeof actionUpdates !== 'object' || actionUpdates === null || Array.isArray(actionUpdates)) {
            throw new Error(`expected an object, received a ${typeof actionUpdates}`);
        }
        if ('selector' in actionUpdates && actionUpdates.selector !== action.selector) {
            validateSelector(actionUpdates.selector, element, query);
        }
        return { ...action, ...actionUpdates, name: action.name };
    } catch (error) {
        logAsRewriter(`${String(error)}, its changes are not recorded`);
        return action;
    }
}

// A deep copy of `value` with only what JSON keeps; `undefined` stays
// `undefined`.
function copyOf<T>(value: T): T {
    if (value === undefined) return value;
    return JSON.parse(JSON.stringify(value)) as T;
}

// Throws, saying why, unless `selector` finds exactly `element`, so that it is
// recorded for it only then.
function validateSelector(selector: unknown, element: Element, query: Query): void {
    const selectorStr = JSON.stringify(selector);
    if (typeof selector !== 'string' || selector.trim() === '') {
        throw new Error(`${selectorStr} is not a selector`);
    }
    let elements: Element[];
    try {
        elements = query(selector);
    } catch (error) {
        throw new Error(`${selectorStr} cannot be checked: ${String(error).split('\n')[0]}`, {
            cause: error,
        });
    }
    if (elements.length === 0) throw new Error(`${selectorStr} finds no element`);
    if (elements.length > 1) throw new Error(`${selectorStr} finds ${elements.length} elements`);
    if (elements[0] !== element) throw new Error(`${selectorStr} finds another element`);
}
