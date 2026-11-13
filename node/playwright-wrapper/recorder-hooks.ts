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

// The recorder hooks a JS extension can export; see the `Record Keyword`
// documentation and Browser/recorder/README.md. Exports starting with `__` are
// never keywords (`initializeExtension`).

import { BrowserContext, Page } from 'playwright';

import { logger } from './browser_logger';

export type Extension = Record<string, unknown>;

export const RECORDING_STARTED = '__recordingStarted';
export const RECORDED_SELECTOR = '__recordedSelector';

// How long a poll or a pick waits for the hooks to rewrite a selector; a
// selector that takes longer is used as Playwright made it.
export const REWRITE_WAIT_MS = 2000;

const started = new WeakMap<BrowserContext, WeakSet<Extension>>();

// Runs each extension's `__recordingStarted({ context })` once per context,
// before its first recording session, in load order.
export async function startRecordingHooks(context: BrowserContext, extensions: Extension[]): Promise<void> {
    const done = started.get(context) ?? new WeakSet<Extension>();
    started.set(context, done);
    for (const extension of extensions) {
        const hook = extension[RECORDING_STARTED];
        if (typeof hook !== 'function' || done.has(extension)) continue;
        done.add(extension);
        try {
            await hook({ context });
        } catch (error) {
            done.delete(extension);
            throw new Error(`The ${RECORDING_STARTED} hook of a JS extension failed: ${String(error)}`, {
                cause: error,
            });
        }
    }
}

export function hasSelectorHook(extensions: Extension[]): boolean {
    return extensions.some((extension) => typeof extension[RECORDED_SELECTOR] === 'function');
}

// Each extension's `__recordedSelector({ selector, action, page, context })`, in
// load order, each seeing the previous one's result; `action` is null for a pick.
// A hook may return a promise. A string replaces the selector, `undefined` keeps
// it; anything else or a failure is logged and ignored, so a broken extension
// never loses an Action or a pick.
export async function recordedSelector(
    selector: string,
    action: Record<string, unknown> | null,
    page: Page | undefined,
    context: BrowserContext | undefined,
    extensions: Extension[],
): Promise<string> {
    let current = selector;
    for (const extension of extensions) {
        const hook = extension[RECORDED_SELECTOR];
        if (typeof hook !== 'function') continue;
        let result: unknown;
        try {
            result = await hook({
                selector: current,
                action: action && { ...action, selector: current },
                page,
                context,
            });
        } catch (error) {
            logger.info(`recorder: ${RECORDED_SELECTOR} failed, the selector is kept: ${String(error)}`);
            continue;
        }
        if (result === undefined || result === null) continue;
        if (typeof result === 'string' && result.trim()) current = result;
        else logger.info(`recorder: ${RECORDED_SELECTOR} returned ${typeof result}, the selector is kept`);
    }
    return current;
}

// The picked selector after the hooks, or Playwright's when they take longer than REWRITE_WAIT_MS.
export async function pickedSelector(
    selector: string,
    page: Page,
    extensions: Extension[],
    waitMs = REWRITE_WAIT_MS,
): Promise<string> {
    if (!hasSelectorHook(extensions)) return selector;
    let timer: NodeJS.Timeout | undefined;
    const late = new Promise<string>((resolve) => {
        timer = setTimeout(() => {
            logger.info(`recorder: ${RECORDED_SELECTOR} took longer than ${waitMs} ms, the picked selector is kept`);
            resolve(selector);
        }, waitMs);
    });
    let context: BrowserContext | undefined;
    try {
        context = page.context();
    } catch {
        context = undefined;
    }
    try {
        return await Promise.race([recordedSelector(selector, null, page, context, extensions), late]);
    } finally {
        clearTimeout(timer);
    }
}
