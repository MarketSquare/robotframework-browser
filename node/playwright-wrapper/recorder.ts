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

// Playwright's programmatic recorder and the toolbar injected into the page;
// see Browser/recorder/README.md. Load-bearing, established against Playwright 1.64:
//  1. `_startRecording` once per context, never `_stopRecording`: a second start
//     throws, a stop drops the event sink. Sessions switch `__pw_recorderSetMode`.
//  2. The sink delivers the whole `ActionInContext` on <= 1.62, the bare `Action`
//     from 1.63; `toAction` accepts both.
//  3. The toolbar sits in an `x-pw-glass` element. The injected recorder ignores
//     every event whose composed path holds one (`_ignoreOverlayEvent`), so a
//     toolbar click is never an Action - nor Playwright's last Action, which
//     would swallow a navigation in the next 5 s.

import * as fs from 'fs';
import * as path from 'path';
import { BrowserContext, Page } from 'playwright';

import { logger } from './browser_logger';
import * as pb from './generated/playwright';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, jsonResponse } from './response-util';

const RECORDER = Symbol.for('robotframework-browser.recorder.state');
const COMMANDS = Symbol.for('robotframework-browser.recorder.commands');
// Modes that mean "the user is no longer recording". Everything else
// (`recording`, `recording-inspecting`, `asserting*`) is part of a recording.
const STOP_MODES = new Set(['none', 'standby']);
// The mode written when a session ends: in Playwright 1.64 only `none` hides its overlay.
const STOPPED_MODE = 'none';

// The command binding is callable by any page script (ADR 0010), and one poll
// reply must stay well below gRPC's 4 MB message limit. Sizes are UTF-8 bytes
// of JSON. A command quotes the value it makes an argument of, which the
// session bounds to 64 KiB of ASCII-escaped JSON (`MAX_RAW_LENGTH`).
export const MAX_COMMAND_BYTES = 256 * 1024;
export const MAX_BUFFERED_COMMANDS = 100;
export const MAX_EVENT_BYTES = 1024 * 1024;
export const MAX_ENTRIES_PER_POLL = 500;
export const MAX_REPLY_BYTES = 3 * 1024 * 1024;

export type Action = Record<string, unknown> & { name: string; selector?: string };
interface EventEntry {
    event: 'added' | 'updated' | 'signal';
    action: Record<string, unknown>;
}
interface CommandEntry {
    command: unknown;
}
export type Entry = EventEntry | CommandEntry;
export interface RecorderBuffers {
    // Actions, signals and toolbar commands in the order they happened: an Undo
    // clicked before an Action must not undo that Action.
    entries: Entry[];
    commandCount: number;
    armed: boolean;
    // A Recording Session is running: set by the reset poll, cleared by `recorderStop`.
    active: boolean;
    // The toolbar state each page shows, so an unchanged state is not sent again.
    rendered: WeakMap<Page, string>;
}

export function toAction(payload: unknown): Action | null {
    if (!payload || typeof payload !== 'object') return null;
    const record = payload as Record<string, unknown>;
    const inner =
        record.action && typeof record.action === 'object' ? (record.action as Record<string, unknown>) : record;
    if (typeof inner.name !== 'string') return null;
    // The snapshot of every Action is large and unused; only `assertSnapshot` needs it.
    if (inner.name === 'assertSnapshot') return { ...inner } as Action;
    const { ariaSnapshot: _ariaSnapshot, ...rest } = inner; // eslint-disable-line @typescript-eslint/no-unused-vars
    return rest as Action;
}

// Playwright's "Pick locator" overlay button toggles these modes. While on, the
// recorder is disabled: no Actions, no signals, and the pick is not delivered.
const PICKING_MODES = new Set(['recording-inspecting', 'inspecting']);

export function isPicking(mode: string | undefined): boolean {
    return mode !== undefined && PICKING_MODES.has(mode);
}

function jsonLength(value: unknown): number {
    try {
        const json = JSON.stringify(value);
        return json === undefined ? Infinity : Buffer.byteLength(json, 'utf8');
    } catch {
        return Infinity;
    }
}

const isCommand = (entry: Entry): entry is CommandEntry => 'command' in entry;

// The oldest entries that fit one poll reply; the rest wait for the next poll.
export function drainEntries(buffers: RecorderBuffers): Entry[] {
    let count = 0;
    let bytes = 0;
    while (count < buffers.entries.length && count < MAX_ENTRIES_PER_POLL) {
        bytes += jsonLength(buffers.entries[count]);
        if (count > 0 && bytes > MAX_REPLY_BYTES) break;
        count += 1;
    }
    const drained = buffers.entries.splice(0, count);
    buffers.commandCount -= drained.filter(isCommand).length;
    return drained;
}

function clearEntries(buffers: RecorderBuffers): void {
    buffers.entries.length = 0;
    buffers.commandCount = 0;
}

export function newBuffers(): RecorderBuffers {
    return { entries: [], commandCount: 0, armed: false, active: false, rendered: new WeakMap() };
}

export function acceptCommand(buffers: RecorderBuffers, command: unknown): void {
    if (!buffers.active || buffers.commandCount >= MAX_BUFFERED_COMMANDS) return;
    if (jsonLength(command) > MAX_COMMAND_BYTES) {
        logger.info('recorder: ignoring an oversized toolbar command');
        return;
    }
    buffers.entries.push({ command });
    buffers.commandCount += 1;
}

let toolbarSource: string | undefined;
export function toolbarScript(): string {
    if (toolbarSource === undefined) {
        // `__dirname` is Browser/wrapper at runtime (static/ is copied next to
        // index.js by `inv node-build`) and node/playwright-wrapper under jest.
        toolbarSource = fs.readFileSync(path.join(__dirname, 'static', 'recorder-toolbar.js'), 'utf8');
    }
    return toolbarSource;
}

// Runs `fn` on each page until it returns a value. A page that closed or is
// navigating throws and is skipped, as is one where `fn` returns undefined.
async function firstOnPages<T>(
    context: BrowserContext,
    fn: (page: Page) => Promise<T | undefined>,
): Promise<T | undefined> {
    for (const page of context.pages()) {
        try {
            const result = await fn(page);
            if (result !== undefined) return result;
        } catch {
            // Page closed or navigating.
        }
    }
    return undefined;
}

async function onEveryPage(context: BrowserContext, fn: (page: Page) => Promise<unknown>): Promise<void> {
    await firstOnPages(context, async (page) => {
        await fn(page);
        return undefined;
    });
}

function readMode(context: BrowserContext): Promise<string | undefined> {
    return firstOnPages(context, async (page) => {
        const recorderState = await page.evaluate(() => {
            const w = window as unknown as { __pw_recorderState?: () => { mode?: string } | null };
            return w.__pw_recorderState ? w.__pw_recorderState() : null;
        });
        return recorderState?.mode || undefined;
    });
}

export async function writeMode(context: BrowserContext, mode: string): Promise<boolean> {
    const written = await firstOnPages(context, async (page) => {
        const present = await page.evaluate((m) => {
            const w = window as unknown as { __pw_recorderSetMode?: (mode: string) => unknown };
            if (!w.__pw_recorderSetMode) return false;
            w.__pw_recorderSetMode(m);
            return true;
        }, mode);
        return present || undefined;
    });
    return written === true;
}

// `__rfbCommand` can be exposed only once per context, but Record Keyword(s)
// and Record Selector both talk through it: each registers its buffers, and a
// command goes to those of the session that is running.
export function commandListeners(context: BrowserContext): Promise<Set<RecorderBuffers>> {
    const store = context as unknown as Record<symbol, Promise<Set<RecorderBuffers>> | undefined>;
    const existing = store[COMMANDS];
    if (existing) return existing;
    const listeners = new Set<RecorderBuffers>();
    const exposed = context
        .exposeBinding('__rfbCommand', (_source: unknown, command: unknown) => {
            listeners.forEach((buffers) => acceptCommand(buffers, command));
        })
        .then(() => listeners);
    store[COMMANDS] = exposed;
    return exposed;
}

// The in-flight promise is stored on the context, so concurrent calls and a
// retry after a partial failure can never run `_startRecording` twice.
export function ensureRecorder(context: BrowserContext): Promise<RecorderBuffers> {
    const existing = existingRecorder(context);
    if (existing) return existing;
    const created = createRecorder(context);
    (context as unknown as Record<symbol, Promise<RecorderBuffers>>)[RECORDER] = created;
    return created;
}

export function existingRecorder(context: BrowserContext): Promise<RecorderBuffers> | undefined {
    return (context as unknown as Record<symbol, Promise<RecorderBuffers> | undefined>)[RECORDER];
}

async function createRecorder(context: BrowserContext): Promise<RecorderBuffers> {
    const start = (context as unknown as { _startRecording?: (...args: unknown[]) => Promise<void> })._startRecording;
    if (typeof start !== 'function') {
        throw new Error(
            'This Playwright version does not offer the programmatic recorder ' +
                '(BrowserContext._startRecording), which Record Keyword and Record Keywords need.',
        );
    }
    const buffers = newBuffers();
    const buffer = (entry: EventEntry) => {
        if (!buffers.active) return;
        if (jsonLength(entry) > MAX_EVENT_BYTES) {
            logger.info(`recorder: ignoring an oversized '${String(entry.action.name)}' event`);
            return;
        }
        buffers.entries.push(entry);
    };
    const forward = (event: 'added' | 'updated') => (_page: unknown, payload: unknown) => {
        const action = toAction(payload);
        if (action) buffer({ event, action });
    };
    // `language` only selects the generator of the `code` Playwright passes
    // along with every event, which is not used.
    await start.call(
        context,
        { language: 'python' },
        {
            actionAdded: forward('added'),
            actionUpdated: forward('updated'),
            signalAdded: (_page: unknown, signal: unknown) => {
                if (signal && typeof signal === 'object' && typeof (signal as Action).name === 'string') {
                    buffer({ event: 'signal', action: signal as Record<string, unknown> });
                }
            },
        },
    );
    (await commandListeners(context)).add(buffers);
    // Deliberately no `context.addInitScript(toolbarScript())`: an init script
    // cannot be un-registered, so the toolbar would keep re-appearing on every
    // navigation long after the session ended. `renderToolbars` re-injects it
    // on every poll instead, which covers navigation and popups and stops by
    // itself once polling stops.
    return buffers;
}

// The state can hold up to a MiB of recorded values; a page gets it only when it
// changed, or when the page lost the toolbar by navigating.
function renderToolbars(context: BrowserContext, buffers: RecorderBuffers, toolbarState: unknown): Promise<void> {
    const json = JSON.stringify(toolbarState);
    return onEveryPage(context, (page) => renderToolbar(page, buffers, json));
}

export async function renderToolbar(page: Page, buffers: RecorderBuffers, json: string): Promise<void> {
    // `missing` after a navigation, `detached` when the page dropped the
    // toolbar from its DOM; rendering re-attaches it, even with an unchanged state.
    const toolbar = await page.evaluate(() => {
        const w = window as unknown as { __rfbToolbarRender?: unknown; __rfbToolbarConnected?: () => boolean };
        if (typeof w.__rfbToolbarRender !== 'function') return 'missing';
        return w.__rfbToolbarConnected && !w.__rfbToolbarConnected() ? 'detached' : 'shown';
    });
    const installed = toolbar !== 'missing';
    if (toolbar === 'shown' && buffers.rendered.get(page) === json) return;
    if (!installed) await page.evaluate(toolbarScript());
    await page.evaluate((s) => {
        const w = window as unknown as { __rfbToolbarRender?: (state: unknown) => void };
        return w.__rfbToolbarRender && w.__rfbToolbarRender(JSON.parse(s));
    }, json);
    buffers.rendered.set(page, json);
}

export function removeToolbar(page: Page): Promise<void> {
    return page.evaluate(() => {
        const w = window as unknown as { __rfbToolbarRemove?: () => void };
        w.__rfbToolbarRemove?.();
    });
}

// Playwright holds a navigation (and a left click) back for 500 ms before it
// reports it, so a page opened or navigated right before a session starts
// would otherwise arrive as the session's first Action.
export const HELD_BACK_MS = 600;
const delay = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

export async function resetSession(
    context: BrowserContext,
    buffers: RecorderBuffers,
    wait: (ms: number) => Promise<void> = delay,
): Promise<void> {
    // A previous session leaves the recorder stopped (`none`), `armed` set and
    // possibly Actions buffered in between; all three would end this
    // session on its first poll. The wait happens while still stopped, and
    // recording starts only after the drain, so no Action made after the
    // switch to `recording` can be dropped with the stale ones.
    buffers.armed = false;
    buffers.active = true;
    await wait(HELD_BACK_MS);
    clearEntries(buffers);
    await writeMode(context, 'recording');
}

export async function recorderPoll(request: pb.Request_Json, state: PlaywrightState): Promise<pb.Response_Json> {
    const context = state.getActiveContext();
    const { state: toolbarState, reset, allowHeadless } = JSON.parse(request.body || '{}');
    if (!context) {
        if (reset) throw new Error('No browser context is open. Open a page before recording.');
        // Closed during the session, with its pages: ends it like closing the last page.
        return jsonResponse(JSON.stringify({ mode: 'recording', picking: false, pages: 0, entries: [] }), '');
    }
    if (reset && !allowHeadless && state.activeBrowser?.headless) {
        throw new Error(
            'Recording needs a visible browser, but the active browser runs headless. ' +
                'Open it with New Browser    headless=False.',
        );
    }
    const buffers = await ensureRecorder(context);
    if (reset) await resetSession(context, buffers);
    if (toolbarState) await renderToolbars(context, buffers, toolbarState);
    const mode = await readMode(context);
    // Only honour a stop once the recorder has actually been seen recording,
    // otherwise a slow start would end the session immediately.
    if (mode !== undefined && !STOP_MODES.has(mode)) buffers.armed = true;
    // The reset finds no page to switch when the only one is navigating; until
    // the recorder is seen recording, every poll tries again.
    else if (!buffers.armed) await writeMode(context, 'recording');
    const stopped = buffers.armed && mode !== undefined && STOP_MODES.has(mode);
    return jsonResponse(
        JSON.stringify({
            mode: stopped ? 'stopped' : 'recording',
            picking: isPicking(mode),
            pages: context.pages().length,
            entries: drainEntries(buffers),
        }),
        '',
    );
}

export async function recorderStop(_request: pb.Request_Empty, state: PlaywrightState): Promise<pb.Response_Empty> {
    const context = state.getActiveContext();
    if (!context) return emptyWithLog('No context to stop recording in.');
    try {
        const recorder = existingRecorder(context);
        if (recorder) (await recorder).active = false;
    } catch {
        // The recorder never started; nothing buffers commands.
    }
    // Deliberately not `_stopRecording()`: it drops the event sink, and the
    // next session would have to start a new recording.
    await writeMode(context, STOPPED_MODE);
    await onEveryPage(context, removeToolbar);
    return emptyWithLog('Recording stopped.');
}
