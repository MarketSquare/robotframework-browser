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
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, jsonResponse } from './response-util';

interface CookieData {
    name: string;
    value: string;
    url?: string;
    domain?: string;
    path?: string;
    expires?: number;
    httpOnly?: boolean;
    secure?: boolean;
    sameSite?: 'Strict' | 'Lax' | 'None';
    partitionKey?: string;
}

interface CookieFilter {
    name?: string;
    domain?: string;
    path?: string;
}

function activeContext(state: PlaywrightState): BrowserContext {
    const context = state.getActiveContext();
    if (!context) throw Error('no open context.');
    return context;
}

async function readCookies(context: BrowserContext, urls?: string | string[]): Promise<pb.Response_Json> {
    const cookies = await context.cookies(urls);
    logger.info({ 'Cookies: ': cookies });
    return jsonResponse(JSON.stringify(cookies), cookies.map((cookie) => cookie.name).toString());
}

export async function getCookies(context: BrowserContext): Promise<pb.Response_Json> {
    return readCookies(context);
}

export async function getCookiesForUrls(request: pb.Request_Json, state: PlaywrightState): Promise<pb.Response_Json> {
    const urls: string | string[] = JSON.parse(request.body);
    return readCookies(activeContext(state), urls);
}

export async function addCookie(request: pb.Request_Json, context: BrowserContext): Promise<pb.Response_Empty> {
    const cookie: CookieData = JSON.parse(request.body);
    logger.info({ 'Cookie data: ': request.body });
    await context.addCookies([cookie]);
    return emptyWithLog('Cookie "' + cookie.name + '" added.');
}

export async function deleteAllCookies(context: BrowserContext): Promise<pb.Response_Empty> {
    await context.clearCookies();
    return emptyWithLog('All cookies deleted.');
}

export async function deleteCookies(request: pb.Request_Json, state: PlaywrightState): Promise<pb.Response_Empty> {
    const filter: CookieFilter = JSON.parse(request.body);
    await activeContext(state).clearCookies(filter);
    return emptyWithLog('Cookies matching ' + request.body + ' deleted.');
}
