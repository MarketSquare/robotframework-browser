import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { BrowserContext, Cookie } from 'playwright';
import { exists } from './playwirght-invoke';

import { Response } from './generated/playwright_pb';
import { stringResponse } from './response-util';

export async function getCookies(callback: sendUnaryData<Response.String>, context?: BrowserContext) {
    exists(context, callback, `Tried to get all cookie's, but not context open.`);
    const allCookies = await context.cookies();
    console.log(allCookies);
    const cookieName = [];
    for (const cookie of allCookies as Array<Cookie>) {
        cookieName.push(cookie.name);
    }
    callback(null, stringResponse(JSON.stringify(allCookies), cookieName.toString()));
}
