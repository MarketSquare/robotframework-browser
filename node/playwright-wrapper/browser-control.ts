import { BrowserContext, Page } from 'playwright';
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { PlaywrightState } from './playwright-state';
import { Request, Response } from './generated/playwright_pb';
import { determineElement, exists, invokeOnPage } from './playwirght-invoke';
import { emptyWithLog, stringResponse } from './response-util';

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
    call: ServerUnaryCall<Request.ScreenshotOptions>,
    callback: sendUnaryData<Response.String>,
    state: PlaywrightState,
) {
    // Add the file extension here because the image type is defined by playwrights defaults
    const path = call.request.getPath() + '.png';
    const selector = call.request.getSelector();
    if (selector) {
        const elem = await determineElement(state, selector, callback);
        exists(elem, callback, `Tried to capture element screenshot, element '${selector}' wasn't found`);
        await elem.screenshot({ path: path });
    } else {
        const page = state.getActivePage();
        exists(page, callback, 'Tried to take screenshot, no page was open');
        await invokeOnPage(page, callback, 'screenshot', { path: path });
    }
    const message = 'Screenshot succesfully captured to: ' + path;
    callback(null, stringResponse(path, message));
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

export async function setOffline(
    call: ServerUnaryCall<Request.Bool>,
    callback: sendUnaryData<Response.Empty>,
    context?: BrowserContext,
) {
    exists(context, callback, 'Tried to toggle context to offline, no open context');
    const offline = call.request.getValue();
    await context.setOffline(offline);
    callback(null, emptyWithLog(`Set context to ${offline}`));
}
