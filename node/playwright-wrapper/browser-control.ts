import { BrowserContext, Page } from 'playwright';
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog, stringResponse } from './response-util';
import { exists, invokeOnPage } from './playwirght-invoke';

export async function goTo(
    call: ServerUnaryCall<Request.Url>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
): Promise<void> {
    const url = call.request.getUrl();
    await invokeOnPage(page, callback, 'goto', url);
    callback(null, emptyWithLog(`Succesfully opened URL ${url}`));
}

export async function goBack(callback: sendUnaryData<Response.Empty>, page?: Page): Promise<void> {
    await invokeOnPage(page, callback, 'goBack');
    callback(null, emptyWithLog('Did Go Back'));
}

export async function goForward(callback: sendUnaryData<Response.Empty>, page?: Page): Promise<void> {
    await invokeOnPage(page, callback, 'goForward');
    callback(null, emptyWithLog('Did Go Forward'));
}

export async function takeScreenshot(
    call: ServerUnaryCall<Request.ScreenshotPath>,
    callback: sendUnaryData<Response.String>,
    page?: Page,
) {
    // Add the file extension here because the image type is defined by playwrights defaults
    const path = call.request.getPath() + '.png';
    await invokeOnPage(page, callback, 'screenshot', { path: path });
    callback(null, stringResponse(path));
}

export function setTimeout(
    call: ServerUnaryCall<Request.Timeout>,
    callback: sendUnaryData<Response.Empty>,
    context?: BrowserContext,
) {
    exists(context, callback, 'Tried to set timeout, no open context');
    const timeout = call.request.getTimeout();
    context.setDefaultTimeout(timeout);
    callback(null, emptyWithLog(`Set timeout to: ${timeout}`));
}

export async function setViewportSize(
    call: ServerUnaryCall<Request.Viewport>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    const size = { width: call.request.getWidth(), height: call.request.getHeight() };
    await invokeOnPage(page, callback, 'setViewportSize', size);
    callback(null, emptyWithLog(`Set viewport size to: ${size}`));
}
