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

// Drives Playwright's *programmatic* recorder (`recorderMode: 'api'`), which
// emits a structured, semantic Action stream instead of generated code, and
// hosts the Robot Framework toolbar injected into the page.
//
// Python calls `recorderPoll` repeatedly. Each call pushes the current toolbar
// state into the page and drains the Actions, signals and toolbar commands
// buffered since the previous call. Polling rather than one long-lived stream
// is what makes the channel bidirectional, which the live Keyword Call list in
// the toolbar requires.
//
// Four things here are load-bearing, established by testing against Playwright
// 1.63, the version in use:
//
//  1. `_enableRecorder` must be called once per context. Playwright caches the
//     `Recorder` per context and ignores the params of any later call, while
//     `ProgrammaticRecorderApp.run` registers a fresh event listener every time,
//     so calling it twice delivers every Action twice.
//  2. Never call `_disableRecorder()`: it drops the event sink. Re-arming a
//     later recording uses `__pw_recorderSetMode('recording')` instead.
//  3. The recorder sink delivers the whole `ActionInContext` on <= 1.62 and the
//     bare `Action` on >= 1.63; `toAction` accepts both. `actionUpdated` still
//     exists in 1.63.
//  4. Interactions with our own toolbar arrive as Actions targeting the toolbar
//     host element (its shadow root is closed, so `composedPath()` cannot see
//     inside) and are dropped by `isToolbarAction`.

import * as fs from 'fs';
import * as path from 'path';
import { BrowserContext } from 'playwright';

import * as pb from './generated/playwright';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, jsonResponse } from './response-util';

export const TOOLBAR_TAG = 'rfb-recorder-toolbar';
const RECORDER = Symbol.for('robotframework-browser.recorder.state');
// Modes that mean "the user is no longer recording". Everything else
// (`recording`, `recording-inspecting`, `asserting*`) is part of a recording.
const STOP_MODES = new Set(['none', 'standby']);

export type Action = Record<string, unknown> & { name: string; selector?: string };
interface Buffered {
    event: 'added' | 'updated' | 'signal';
    action: Record<string, unknown>;
}
export interface RecorderBuffers {
    events: Buffered[];
    commands: unknown[];
    armed: boolean;
}

export function toAction(payload: unknown): Action | null {
    if (!payload || typeof payload !== 'object') return null;
    const record = payload as Record<string, unknown>;
    const inner =
        record.action && typeof record.action === 'object' ? (record.action as Record<string, unknown>) : record;
    if (typeof inner.name !== 'string') return null;
    const { ariaSnapshot: _ariaSnapshot, ...rest } = inner; // eslint-disable-line @typescript-eslint/no-unused-vars
    return rest as Action;
}

export function isToolbarAction(action: Action): boolean {
    return typeof action.selector === 'string' && action.selector.includes(TOOLBAR_TAG);
}

export function drain<T>(list: T[]): T[] {
    return list.splice(0, list.length);
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

async function readMode(context: BrowserContext): Promise<string | undefined> {
    for (const page of context.pages()) {
        try {
            const recorderState = await page.evaluate(() => {
                const w = window as unknown as { __pw_recorderState?: () => { mode?: string } | null };
                return w.__pw_recorderState ? w.__pw_recorderState() : null;
            });
            if (recorderState && recorderState.mode) return recorderState.mode;
        } catch {
            // Page closed or navigating - try the next one.
        }
    }
    return undefined;
}

async function writeMode(context: BrowserContext, mode: string): Promise<boolean> {
    for (const page of context.pages()) {
        try {
            await page.evaluate((m) => {
                const w = window as unknown as { __pw_recorderSetMode?: (mode: string) => unknown };
                return w.__pw_recorderSetMode && w.__pw_recorderSetMode(m);
            }, mode);
            return true;
        } catch {
            // Page closed or navigating - try the next one.
        }
    }
    return false;
}

export async function ensureRecorder(context: BrowserContext): Promise<RecorderBuffers> {
    const holder = context as unknown as Record<symbol, RecorderBuffers | undefined>;
    const existing = holder[RECORDER];
    if (existing) return existing;
    const enable = (context as unknown as { _enableRecorder?: (...args: unknown[]) => Promise<void> })._enableRecorder;
    if (typeof enable !== 'function') {
        throw new Error(
            'This Playwright version does not offer the programmatic recorder ' +
                '(BrowserContext._enableRecorder), which Record Keyword and Record Keywords need.',
        );
    }
    const buffers: RecorderBuffers = { events: [], commands: [], armed: false };
    const forward = (event: 'added' | 'updated') => (_page: unknown, payload: unknown) => {
        const action = toAction(payload);
        if (!action || isToolbarAction(action)) return;
        buffers.events.push({ event, action });
    };
    await enable.call(
        context,
        { mode: 'recording', recorderMode: 'api' },
        {
            actionAdded: forward('added'),
            actionUpdated: forward('updated'),
            signalAdded: (_page: unknown, signal: unknown) => {
                if (signal && typeof signal === 'object' && typeof (signal as Action).name === 'string') {
                    buffers.events.push({ event: 'signal', action: signal as Record<string, unknown> });
                }
            },
        },
    );
    await context.exposeBinding('__rfbCommand', (_source: unknown, command: unknown) => {
        buffers.commands.push(command);
    });
    // Deliberately no `context.addInitScript(toolbarScript())`: an init script
    // cannot be un-registered, so the toolbar would keep re-appearing on every
    // navigation long after the session ended. `renderToolbars` re-injects it
    // on every poll instead, which covers navigation and popups and stops by
    // itself once polling stops.
    holder[RECORDER] = buffers;
    return buffers;
}

async function renderToolbars(context: BrowserContext, toolbarState: unknown): Promise<void> {
    for (const page of context.pages()) {
        try {
            const installed = await page.evaluate(
                () => typeof (window as unknown as { __rfbToolbarRender?: unknown }).__rfbToolbarRender === 'function',
            );
            if (!installed) await page.evaluate(toolbarScript());
            await page.evaluate((s) => {
                const w = window as unknown as { __rfbToolbarRender?: (state: unknown) => void };
                return w.__rfbToolbarRender && w.__rfbToolbarRender(s);
            }, toolbarState);
        } catch {
            // Page closed or navigating - it picks the state up next poll.
        }
    }
}

export async function recorderPoll(request: pb.Request_Json, state: PlaywrightState): Promise<pb.Response_Json> {
    const context = state.getActiveContext();
    if (!context) throw new Error('No browser context is open. Open a page before recording.');
    const { state: toolbarState, reset } = JSON.parse(request.body || '{}');
    const buffers = await ensureRecorder(context);
    if (reset) {
        // A previous session leaves the recorder in `standby`, `armed` set and
        // possibly Actions buffered in between; all three would end this
        // session on its first poll.
        buffers.armed = false;
        drain(buffers.events);
        drain(buffers.commands);
        await writeMode(context, 'recording');
    }
    await renderToolbars(context, toolbarState ?? {});
    const mode = await readMode(context);
    // Only honour a stop once the recorder has actually been seen recording,
    // otherwise a slow start would end the session immediately.
    if (mode !== undefined && !STOP_MODES.has(mode)) buffers.armed = true;
    const stopped = buffers.armed && mode !== undefined && STOP_MODES.has(mode);
    return jsonResponse(
        JSON.stringify({
            mode: stopped ? 'stopped' : 'recording',
            pages: context.pages().length,
            events: drain(buffers.events),
            commands: drain(buffers.commands),
        }),
        '',
    );
}

export async function recorderStop(_request: pb.Request_Empty, state: PlaywrightState): Promise<pb.Response_Empty> {
    const context = state.getActiveContext();
    if (!context) return emptyWithLog('No context to stop recording in.');
    // Deliberately not `_disableRecorder()`: it drops the event sink, and
    // re-installing it would deliver every Action of the next session twice.
    await writeMode(context, 'standby');
    for (const page of context.pages()) {
        try {
            await page.evaluate(() => {
                const w = window as unknown as { __rfbToolbarRemove?: () => void };
                w.__rfbToolbarRemove?.();
            });
        } catch {
            // Page closed or navigating.
        }
    }
    return emptyWithLog('Recording stopped.');
}
