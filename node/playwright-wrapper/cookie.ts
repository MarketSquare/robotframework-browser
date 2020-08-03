import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { BrowserContext, Cookie } from 'playwright';
import { invokeOnContext } from './playwirght-invoke';

import { Request, Response } from './generated/playwright_pb';
import { stringResponse, emptyWithLog } from './response-util';

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
    console.log(allCookies);
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
    console.log('Cookie data: ' + call.request.getBody());
    await invokeOnContext(context, callback, 'addCookies', [cookie]);
    callback(null, emptyWithLog('Cookie "' + cookie.name + '" added.'));
}

export async function deleteAllCookies(callback: sendUnaryData<Response.Empty>, context?: BrowserContext) {
    await invokeOnContext(context, callback, 'clearCookies');
    callback(null, emptyWithLog('All cookies deleted.'));
}
