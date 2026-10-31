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

// Record Selector: the element is picked as in element-picker.ts, the recorder
// toolbar shows the result in its `selector` mode. Python drives the session by
// polling, as for Record Keyword(s), and translates Playwright's selector.

import { drivePick, endPick, Pick } from './element-picker';
import * as pb from './generated/playwright';
import { PlaywrightState } from './playwright-state';
import {
    commandListeners,
    drainEntries,
    newBuffers,
    otherSessionRuns,
    RecorderBuffers,
    removeToolbar,
    renderToolbar,
} from './recorder';
import { emptyWithLog, jsonResponse } from './response-util';

// One picker per library instance: pabot workers share this Node process.
const sessions = new WeakMap<PlaywrightState, PickerSession>();

export interface PickerSession extends Pick {
    buffers: RecorderBuffers;
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
    const previous = sessions.get(state);
    if (previous) await endSession(state, previous);
    if (await otherSessionRuns(context)) {
        throw new Error(
            'A Record Keyword(s) session or another Record Selector is running in this browser context. ' +
                'Record Selector can run only after it ended.',
        );
    }
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
    await endPick(session);
    if (!session.page.isClosed()) await removeToolbar(session.page).catch(() => undefined);
}

export async function selectorPickerPoll(request: pb.Request_Json, state: PlaywrightState): Promise<pb.Response_Json> {
    const body = JSON.parse(request.body || '{}');
    const session = body.reset ? await startSession(state, body.allowHeadless === true) : sessions.get(state);
    if (!session || session.page.isClosed()) {
        return jsonResponse(JSON.stringify({ pages: 0, entries: [] }), '');
    }
    if (body.state) await renderToolbar(session.page, session.buffers, JSON.stringify(body.state));
    const picked = await drivePick(state, session, body);
    return jsonResponse(JSON.stringify({ pages: 1, entries: drainEntries(session.buffers), ...picked }), '');
}

export async function selectorPickerStop(
    _request: pb.Request_Empty,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    const session = sessions.get(state);
    if (session) await endSession(state, session);
    return emptyWithLog('Selector recording stopped.');
}
