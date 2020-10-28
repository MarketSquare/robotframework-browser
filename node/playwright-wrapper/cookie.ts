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

import { BrowserContext, Cookie } from 'playwright';
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog, jsonResponse } from './response-util';
import { invokeOnContext } from './playwirght-invoke';

import * as pino from 'pino';
const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

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
}

export async function getCookies(context?: BrowserContext): Promise<Response.Json> {
    const allCookies = await invokeOnContext(context, 'cookies');
    logger.info({ 'Cookies: ': allCookies });
    const cookieName = [];
    for (const cookie of allCookies as Array<Cookie>) {
        cookieName.push(cookie.name);
    }
    return jsonResponse(JSON.stringify(allCookies), cookieName.toString());
}

export async function addCookie(request: Request.Json, context?: BrowserContext): Promise<Response.Empty> {
    const cookie: CookieData = JSON.parse(request.getBody());
    logger.info({ 'Cookie data: ': request.getBody() });
    await invokeOnContext(context, 'addCookies', [cookie]);
    return emptyWithLog('Cookie "' + cookie.name + '" added.');
}

export async function deleteAllCookies(context?: BrowserContext): Promise<Response.Empty> {
    await invokeOnContext(context, 'clearCookies');
    return emptyWithLog('All cookies deleted.');
}
