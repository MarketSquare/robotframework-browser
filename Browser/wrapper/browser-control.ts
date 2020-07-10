import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { Browser, BrowserContext, Page } from 'playwright';

import { Response, Request } from './generated/playwright_pb';
import { BrowserState } from './server';
import { invokeOnPage, exists } from './playwirght-util';
import { emptyWithLog, stringResponse } from './response-util';

export async function closeBrowser(callback: sendUnaryData<Response.Empty>, browser?: Browser) {
    exists(browser, callback, 'Tried to close browser but none was open');
    await browser.close();
}

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
    exists(context, callback, 'Tried to set timeout, no open browser');
    const timeout = call.request.getTimeout();
    context.setDefaultTimeout(timeout);
    callback(null, emptyWithLog(`Set timeout to: ${timeout}`));
}

export async function autoActivatePages(
    call: ServerUnaryCall<Request.Empty>,
    callback: sendUnaryData<Response.Empty>,
    browserState?: BrowserState,
) {
    exists(browserState, callback, 'Tried to focus next opened page');

    browserState.context.on('page', (page) => {
        browserState.page = page;
        console.log('Changed active page');
    });
    callback(null, emptyWithLog('Will focus future ``pages`` in this context'));
}

export async function switchActivePage(
    call: ServerUnaryCall<Request.Index>,
    callback: sendUnaryData<Response.Empty>,
    browserState?: BrowserState,
) {
    exists(browserState, callback, "Tried to switch active page but browser wasn't open");
    console.log('Changing current active page');
    const index = call.request.getIndex();
    const pages = browserState.context.pages();
    if (pages[index]) {
        browserState.page = pages[index];
        callback(null, emptyWithLog('Succesfully changed active page'));
    } else {
        try {
            const page = await browserState.context.waitForEvent('page');
            // const page = await browserState.page.waitForEvent('popup')
            browserState.page = page;
            callback(null, emptyWithLog('Succesfully changed active page'));
        } catch (e) {
            // TODO: put behind --debug flag, debug prints
            const mapped = pages.map((p) => p.url());
            const pageList = `Pages in current context: ${mapped.join(',')}`;
            const message = `No page for index ${index}. \n ` + pageList;
            const error = new Error(message);
            callback(error, null);
        }
    }
}
