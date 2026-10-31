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

// Picking one element with Playwright's public `page.pickLocator()`, shared by
// Record Selector and the Pick button of Record Keyword(s). Python polls: each
// poll says whether to keep picking and which selector to count; the shown
// selector stays highlighted with Playwright's highlight until the pick ends.

import * as fs from 'fs';
import * as path from 'path';
import { ElementHandle, Locator, Page } from 'playwright';

import { findLocator } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';

export interface Picked {
    // Playwright's selector, in its internal syntax; Python translates it.
    selector?: string;
    css?: string;
    error?: string;
}

interface Disposable {
    dispose(): Promise<void>;
}

export interface Pick {
    page: Page;
    picking: boolean;
    picked?: Picked;
    highlight?: Disposable;
}

// What Python asks of a pick in one poll.
export interface PickRequest {
    pick?: unknown;
    count?: unknown;
    // `false` switches the highlight off; anything else leaves it on.
    highlight?: unknown;
}

let cssSource: string | undefined;
function cssSelectorScript(): string {
    if (cssSource === undefined) {
        cssSource = fs.readFileSync(path.join(__dirname, 'static', 'css-selector.js'), 'utf8');
    }
    return cssSource;
}

// The `css` selector of the picked element: one per frame, from the outermost
// iframe element inward, joined by Browser's frame-piercing ` >>> `.
export async function cssSelectorOf(locator: Locator): Promise<string> {
    const parts: string[] = [];
    // The element may be gone right after the pick; then there is no css selector.
    let element: ElementHandle<Node> = await locator.elementHandle({ timeout: 1000 });
    for (;;) {
        const frame = await element.ownerFrame();
        if (!frame) break;
        await frame.evaluate(cssSelectorScript());
        parts.unshift(
            await element.evaluate((e) =>
                (window as unknown as { __rfbCssSelector: (e: Node) => string }).__rfbCssSelector(e),
            ),
        );
        if (!frame.parentFrame()) break;
        element = await frame.frameElement();
    }
    return parts.join(' >>> ');
}

function internalSelector(locator: Locator): string {
    // `pickLocator` returns `page.locator(selector)`; the selector is not public.
    const selector = (locator as unknown as { _selector?: unknown })._selector;
    if (typeof selector !== 'string') throw new Error('Playwright returned a locator without a selector.');
    return selector;
}

// Playwright switches the pointer to a hand for Pick locator and its assertion
// tools (`body[data-pw-cursor=pointer]`), but leaves it when switching to a tool
// without a cursor, such as recording in api mode or none (Playwright 1.64).
export async function resetPlaywrightCursor(page: Page): Promise<void> {
    let frames;
    try {
        frames = page.frames();
    } catch {
        return;
    }
    await Promise.all(
        frames.map((frame) =>
            frame.evaluate(() => document.body?.removeAttribute('data-pw-cursor')).catch(() => undefined),
        ),
    );
}

// The longest selector a pick hands on. The css generator runs in the page under
// test (ADR 0010); a reply must stay within gRPC's message limit. Mirrors
// MAX_SELECTOR_LENGTH in Browser/recorder/picker.py.
export const MAX_PICKED_LENGTH = 10_000;
const MAX_ERROR_LENGTH = 1_000;

const errorText = (e: unknown) => String(e).slice(0, MAX_ERROR_LENGTH);

export function startPick(pick: Pick): void {
    pick.picking = true;
    pick.page
        .pickLocator()
        .then(async (locator) => {
            // Stopped meanwhile (Reselect, Cancel, Stop): the pick is not wanted any more.
            if (!pick.picking) return;
            const selector = internalSelector(locator);
            if (selector.length > MAX_PICKED_LENGTH) {
                pick.picked = { error: 'The picked selector is too long.' };
                return;
            }
            const css = await cssSelectorOf(locator).then(
                (generated) =>
                    generated.length > MAX_PICKED_LENGTH ? { error: 'The css selector is too long.' } : generated,
                (e: unknown) => ({ error: `The css selector could not be generated: ${errorText(e)}` }),
            );
            pick.picked = typeof css === 'string' ? { selector, css } : { selector, ...css };
        })
        .catch((e: unknown) => {
            // A cancel (Reselect, Stop, a closed page) is not a result.
            if (pick.picking) pick.picked = { error: errorText(e) };
        })
        .finally(() => {
            pick.picking = false;
            void resetPlaywrightCursor(pick.page);
        });
}

export async function stopPick(pick: Pick): Promise<void> {
    if (!pick.picking) return;
    pick.picking = false;
    await pick.page.cancelPickLocator().catch(() => undefined);
}

export async function clearHighlight(pick: Pick): Promise<void> {
    const highlight = pick.highlight;
    pick.highlight = undefined;
    await highlight?.dispose().catch(() => undefined);
}

export async function countOf(state: PlaywrightState, selector: string): Promise<{ count?: number; error?: string }> {
    try {
        return { count: await (await findLocator(state, selector, false, false)).count() };
    } catch (e) {
        return { error: e instanceof Error ? e.message.split('\n')[0] : String(e) };
    }
}

// The counted selector replaces the highlighted one; one that finds nothing,
// or does not parse, leaves nothing highlighted.
async function highlightSelector(state: PlaywrightState, pick: Pick, selector: string, count?: number) {
    await clearHighlight(pick);
    if (!count) return;
    try {
        const locator = await findLocator(state, selector, false, false);
        pick.highlight = await locator.highlight();
    } catch {
        // The page navigated or the selector stopped matching meanwhile.
    }
}

// One poll of a pick: start or stop it, hand over a result, count and highlight.
export async function drivePick(state: PlaywrightState, pick: Pick, request: PickRequest) {
    if (request.pick === true && !pick.picking && !pick.picked) {
        await clearHighlight(pick);
        startPick(pick);
    }
    if (request.pick !== true) await stopPick(pick);
    const reply: Record<string, unknown> = {};
    if (pick.picked) {
        reply.picked = pick.picked;
        pick.picked = undefined;
    }
    if (request.highlight === false) await clearHighlight(pick);
    if (typeof request.count === 'string') {
        const counted = await countOf(state, request.count);
        reply.count = { selector: request.count, ...counted };
        if (request.highlight !== false) await highlightSelector(state, pick, request.count, counted.count);
    }
    return reply;
}

export async function endPick(pick: Pick): Promise<void> {
    await stopPick(pick);
    await clearHighlight(pick);
}
