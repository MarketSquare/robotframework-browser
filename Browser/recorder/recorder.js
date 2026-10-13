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

// JS extension backing the `Record Keyword` / `Record Keywords` plugin.
//
// It drives Playwright's *programmatic* recorder (`recorderMode: 'api'`), which
// emits a structured, semantic action stream instead of generated code, and it
// hosts the Robot Framework toolbar injected into the page.
//
// The Python side calls `rfbRecorderPoll` repeatedly. Each call pushes the
// current toolbar state into the page and drains the recorder events and
// toolbar commands buffered since the previous call. Polling - rather than one
// long-lived stream - is what makes the channel bidirectional, which the
// toolbar's live step list requires.
//
// Four things here are load-bearing, established by testing against the pinned
// Playwright 1.62.1 (see `README.md`):
//
//  1. `_enableRecorder` must be called *once per context*. Playwright caches the
//     `Recorder` per context and ignores the params of any later call, while
//     `ProgrammaticRecorderApp.run` registers a *fresh* event listener every
//     time - so calling it twice delivers every action twice.
//  2. Never call `_disableRecorder()`: it drops the event sink. Re-arming a
//     later recording uses `__pw_recorderSetMode('recording')` instead.
//  3. The recorder sink delivers the whole `ActionInContext` on <= 1.62 and the
//     bare `Action` on >= 1.63; `toAction` accepts both.
//  4. Interactions with our own toolbar arrive as actions targeting the toolbar
//     host element (its shadow root is closed, so `composedPath()` cannot see
//     inside) and are dropped by `isToolbarAction`.

const { TOOLBAR_TAG, TOOLBAR_SOURCE } = require('./toolbar.js');

const RFB_STATE = Symbol.for('robotframework-browser.recorder.state');

// Modes that mean "the user is no longer recording". Everything else
// (`recording`, `recording-inspecting`, `asserting*`) is part of a recording.
const STOP_MODES = new Set(['none', 'standby']);

/**
 * Normalise a recorder payload to the bare `Action` and drop the bulky
 * `ariaSnapshot`, which we never use and which would otherwise be re-sent on
 * every keystroke.
 */
function toAction(payload) {
    if (!payload || typeof payload !== 'object') return null;
    const action = payload.action && typeof payload.action === 'object' ? payload.action : payload;
    if (typeof action.name !== 'string') return null;
    const { ariaSnapshot, ...rest } = action;
    return rest;
}

/** True when an action targets our own toolbar and must not be recorded. */
function isToolbarAction(action) {
    return !!action && typeof action.selector === 'string' && action.selector.includes(TOOLBAR_TAG);
}

/** Empty an array in place, returning what it held. */
function drain(list) {
    return list.splice(0, list.length);
}

/** Read the recorder's current mode, or undefined if it is not reachable yet. */
async function readMode(context) {
    for (const page of context.pages()) {
        try {
            const state = await page.evaluate(() =>
                // eslint-disable-next-line no-undef
                window.__pw_recorderState ? window.__pw_recorderState() : null,
            );
            if (state && state.mode) return state.mode;
        } catch (e) {
            // Page closed or navigating - try the next one.
        }
    }
    return undefined;
}

/** Ask the recorder to switch mode, using its own binding. */
async function writeMode(context, mode) {
    for (const page of context.pages()) {
        try {
            // eslint-disable-next-line no-undef
            await page.evaluate((m) => window.__pw_recorderSetMode && window.__pw_recorderSetMode(m), mode);
            return true;
        } catch (e) {
            // Page closed or navigating - try the next one.
        }
    }
    return false;
}

/** Install the permanent event sink and toolbar binding for this context. */
async function ensureRecorder(context) {
    if (context[RFB_STATE]) return context[RFB_STATE];

    if (typeof context._enableRecorder !== 'function')
        throw new Error(
            'This Playwright build does not expose the programmatic recorder ' +
                '(context._enableRecorder). Update Playwright to use the recorder plugin.',
        );

    const state = { events: [], commands: [], armed: false };
    const forward = (event) => (page, payload) => {
        const action = toAction(payload);
        if (!action || isToolbarAction(action)) return;
        state.events.push({ event, action });
    };
    await context._enableRecorder(
        { mode: 'recording', recorderMode: 'api' },
        {
            actionAdded: forward('added'),
            actionUpdated: forward('updated'),
            signalAdded: () => {},
        },
    );
    await context.exposeBinding('__rfbCommand', (source, command) => {
        state.commands.push(command);
    });
    // Deliberately *no* `context.addInitScript(TOOLBAR_SOURCE)`: an init script
    // cannot be un-registered, so the toolbar would keep re-appearing on every
    // navigation for the rest of the context's life, long after the session
    // ended. `renderToolbars` re-injects it on every poll instead, which covers
    // navigation and popups and stops by itself once polling stops.
    context[RFB_STATE] = state;
    return state;
}

/** Make sure every open page shows the toolbar and renders the given state. */
async function renderToolbars(context, toolbarState) {
    for (const page of context.pages()) {
        try {
            const installed = await page.evaluate(
                () =>
                    // eslint-disable-next-line no-undef
                    typeof window.__rfbToolbarRender === 'function',
            );
            if (!installed) await page.evaluate(TOOLBAR_SOURCE);
            // eslint-disable-next-line no-undef
            await page.evaluate((s) => window.__rfbToolbarRender && window.__rfbToolbarRender(s), toolbarState);
        } catch (e) {
            // Page closed or navigating - it picks the state up next poll.
        }
    }
}

async function rfbRecorderPoll(context, playwright, state, reset) {
    const recorder = await ensureRecorder(context);
    const toolbarState = typeof state === 'string' ? JSON.parse(state) : state || {};

    if (reset) {
        // A previous session leaves the recorder in `standby`, its `armed` flag
        // set, and possibly actions buffered in between. All three would end
        // this session on its very first poll.
        recorder.armed = false;
        drain(recorder.events);
        drain(recorder.commands);
        await writeMode(context, 'recording');
    }

    await renderToolbars(context, toolbarState);

    const mode = await readMode(context);
    // Only honour a stop once the recorder has actually been seen recording,
    // otherwise a slow start would end the session immediately.
    if (mode !== undefined && !STOP_MODES.has(mode)) recorder.armed = true;
    const stopped = recorder.armed && mode !== undefined && STOP_MODES.has(mode);

    return {
        mode: stopped ? 'stopped' : 'recording',
        pages: context.pages().length,
        events: drain(recorder.events),
        commands: drain(recorder.commands),
    };
}
rfbRecorderPoll.rfdoc = 'Internal: poll the Playwright api-mode recorder for the Record Keyword(s) plugin.';

async function rfbRecorderStop(context) {
    // Deliberately not `_disableRecorder()`: that drops the event sink, and
    // re-installing it would double every action of the next session.
    await writeMode(context, 'standby');
    for (const page of context.pages()) {
        try {
            // eslint-disable-next-line no-undef
            await page.evaluate(() => window.__rfbToolbarRemove && window.__rfbToolbarRemove());
        } catch (e) {
            // Page closed or navigating.
        }
    }
    return { stopped: true };
}
rfbRecorderStop.rfdoc = 'Internal: end a Record Keyword(s) session and remove the toolbar.';

exports.__esModule = true;
exports.rfbRecorderPoll = rfbRecorderPoll;
exports.rfbRecorderStop = rfbRecorderStop;
exports.toAction = toAction;
exports.isToolbarAction = isToolbarAction;
exports.drain = drain;
