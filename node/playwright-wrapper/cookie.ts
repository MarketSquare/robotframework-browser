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

import { BrowserContext } from 'playwright';

import { logger } from './browser_logger';
import * as pb from './generated/playwright';
import { exists } from './playwright-invoke';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, jsonResponse } from './response-util';

type SameSite = 'Strict' | 'Lax' | 'None';
const SAME_SITE_VALUES: readonly string[] = ['Strict', 'Lax', 'None'] satisfies SameSite[];

function sameSite(value: string | undefined): SameSite | undefined {
    if (value === undefined || SAME_SITE_VALUES.includes(value)) {
        return value as SameSite | undefined;
    }
    throw new Error(`Invalid sameSite value "${value}", expected one of ${SAME_SITE_VALUES.join(', ')}.`);
}

function activeContext(state: PlaywrightState): BrowserContext {
    const context = state.getActiveContext();
    exists(context, 'no open context.');
    return context;
}

export async function getCookies(request: pb.Request_CookieQuery, state: PlaywrightState): Promise<pb.Response_Json> {
    const cookies = await activeContext(state).cookies(request.urls);
    logger.info({ 'Cookies: ': cookies });
    return jsonResponse(JSON.stringify(cookies), cookies.map((cookie) => cookie.name).toString());
}

export async function addCookie(request: pb.Request_Cookie, state: PlaywrightState): Promise<pb.Response_Empty> {
    const context = activeContext(state);
    const cookie = { ...request, sameSite: sameSite(request.sameSite) };
    logger.info({ 'Cookie data: ': cookie });
    await context.addCookies([cookie]);
    return emptyWithLog('Cookie "' + cookie.name + '" added.');
}

export async function deleteAllCookies(
    request: pb.Request_CookieFilter,
    state: PlaywrightState,
): Promise<pb.Response_Empty> {
    await activeContext(state).clearCookies(request);
    const filter = JSON.stringify(request);
    return emptyWithLog(filter === '{}' ? 'All cookies deleted.' : 'Cookies matching ' + filter + ' deleted.');
}
