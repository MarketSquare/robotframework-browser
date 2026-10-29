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

// Record Selector: Playwright's public `page.pickLocator()` picks the element,
// the recorder toolbar shows the result in its `selector` mode. Python drives
// the session by polling, as for Record Keyword(s), and translates Playwright's
// selector; Node picks, generates the `css` selector, counts and highlights.

import * as fs from 'fs';
import * as path from 'path';
import { BrowserContext, ElementHandle, Locator, Page } from 'playwright';

import { highlightAll } from './evaluation';
import * as pb from './generated/playwright';
import { findLocator } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';
import {
    commandListeners,
    drainEntries,
    existingRecorder,
    newBuffers,
    RecorderBuffers,
    removeToolbar,
    renderToolbar,
} from './recorder';
import { emptyWithLog, jsonResponse } from './response-util';

// One picker per library instance: pabot workers share this Node process.
const sessions = new WeakMap<PlaywrightState, PickerSession>();

export interface Picked {
    // Playwright's selector, in its internal syntax; Python translates it.
    selector?: string;
    css?: string;
    error?: string;
}

export interface PickerSession {
    page: Page;
    buffers: RecorderBuffers;
    picking: boolean;
    picked?: Picked;
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
    let element: ElementHandle<Node> = await locator.elementHandle();
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

export function startPick(session: PickerSession): void {
    session.picking = true;
    session.page
        .pickLocator()
        .then(async (locator) => {
            const selector = internalSelector(locator);
            const css = await cssSelectorOf(locator).catch((e: unknown) => {
                return { error: `The css selector could not be generated: ${String(e)}` };
            });
            session.picked = typeof css === 'string' ? { selector, css } : { selector, ...css };
        })
        .catch((e: unknown) => {
            // A cancel (Reselect, Stop, a closed page) is not a result.
            if (session.picking) session.picked = { error: String(e) };
        })
        .finally(() => {
            session.picking = false;
        });
}

export async function stopPick(session: PickerSession): Promise<void> {
    if (!session.picking) return;
    session.picking = false;
    await session.page.cancelPickLocator().catch(() => undefined);
}

export async function countOf(state: PlaywrightState, selector: string): Promise<{ count?: number; error?: string }> {
    try {
        return { count: await (await findLocator(state, selector, false, false)).count() };
    } catch (e) {
        return { error: e instanceof Error ? e.message.split('\n')[0] : String(e) };
    }
}

async function recordingRuns(context: BrowserContext): Promise<boolean> {
    const recorder = existingRecorder(context);
    if (!recorder) return false;
    try {
        return (await recorder).active;
    } catch {
        return false;
    }
}

async function startSession(state: PlaywrightState, allowHeadless: boolean): Promise<PickerSession> {
    const page = state.getActivePage();
    if (!page) throw new Error('No page is open. Open a page before recording a selector.');
    if (!allowHeadless && state.activeBrowser?.headless) {
        throw new Error(
            'Record Selector needs a visible browser, but the active browser runs headless. ' +
                'Open it with New Browser    headless=False.',
        );
    }
    const context = page.context();
    if (await recordingRuns(context)) {
        throw new Error(
            'A Record Keyword(s) session is running in this browser context. ' +
                'Record Selector can run only after it ended.',
        );
    }
    const previous = sessions.get(state);
    if (previous) await endSession(state, previous);
    const session: PickerSession = { page, buffers: newBuffers(), picking: false };
    session.buffers.active = true;
    (await commandListeners(context)).add(session.buffers);
    sessions.set(state, session);
    await page.bringToFront();
    return session;
}

async function endSession(state: PlaywrightState, session: PickerSession): Promise<void> {
    session.buffers.active = false;
    (await commandListeners(session.page.context())).delete(session.buffers);
    if (sessions.get(state) === session) sessions.delete(state);
    await stopPick(session);
    if (!session.page.isClosed()) await removeToolbar(session.page).catch(() => undefined);
}

export async function selectorPickerPoll(request: pb.Request_Json, state: PlaywrightState): Promise<pb.Response_Json> {
    const { state: toolbarState, reset, allowHeadless, pick, count, highlight } = JSON.parse(request.body || '{}');
    const session = reset ? await startSession(state, allowHeadless === true) : sessions.get(state);
    if (!session || session.page.isClosed()) {
        return jsonResponse(JSON.stringify({ pages: 0, entries: [] }), '');
    }
    if (toolbarState) await renderToolbar(session.page, session.buffers, JSON.stringify(toolbarState));
    if (pick && !session.picking && !session.picked) startPick(session);
    if (!pick) await stopPick(session);
    const reply: Record<string, unknown> = { pages: 1, entries: drainEntries(session.buffers) };
    if (session.picked) {
        reply.picked = session.picked;
        session.picked = undefined;
    }
    if (typeof count === 'string') reply.count = { selector: count, ...(await countOf(state, count)) };
    if (typeof highlight === 'string') await highlightAll(highlight, 1500, '2px', 'dotted', '#ff6b5e', false, state);
    return jsonResponse(JSON.stringify(reply), '');
}

export async function selectorPickerStop(
    _request: pb.Request_Empty,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const session = sessions.get(state);
    if (session) await endSession(state, session);
    return emptyWithLog('Selector recording stopped.');
}
