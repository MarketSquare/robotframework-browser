import { BrowserContext, Cookie } from 'playwright';
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog, stringResponse } from './response-util';
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

export async function getCookies(callback: sendUnaryData<Response.String>, context?: BrowserContext) {
    const allCookies = await invokeOnContext(context, callback, 'cookies');
    logger.info({ 'Cookies: ': allCookies });
    const cookieName = [];
    for (const cookie of allCookies as Array<Cookie>) {
        cookieName.push(cookie.name);
    }
    callback(null, stringResponse(JSON.stringify(allCookies), cookieName.toString()));
}

export async function addCookie(
    call: ServerUnaryCall<Request.Json>,
    callback: sendUnaryData<Response.Empty>,
    context?: BrowserContext,
) {
    const cookie: CookieData = JSON.parse(call.request.getBody());
    logger.info({ 'Cookie data: ': call.request.getBody() });
    await invokeOnContext(context, callback, 'addCookies', [cookie]);
    callback(null, emptyWithLog('Cookie "' + cookie.name + '" added.'));
}

export async function deleteAllCookies(callback: sendUnaryData<Response.Empty>, context?: BrowserContext) {
    await invokeOnContext(context, callback, 'clearCookies');
    callback(null, emptyWithLog('All cookies deleted.'));
}
