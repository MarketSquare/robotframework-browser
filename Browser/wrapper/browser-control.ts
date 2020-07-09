import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { Browser, BrowserContext, Page } from 'playwright';

import { Response, Request } from './generated/playwright_pb';
import { invokePlaywright, exists } from './playwirght-util';
import { emptyWithLog } from './response-util';
import { BrowserState } from './server';

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
    await invokePlaywright(page, callback, 'goto', url);
    callback(null, emptyWithLog(`Succesfully opened URL ${url}`));
}

export async function goBack(callback: sendUnaryData<Response.Empty>, page?: Page): Promise<void> {
    await invokePlaywright(page, callback, 'goBack');
    callback(null, emptyWithLog('Did Go Back'));
}

export async function goForward(callback: sendUnaryData<Response.Empty>, page?: Page): Promise<void> {
    await invokePlaywright(page, callback, 'goForward');
    callback(null, emptyWithLog('Did Go Forward'));
}

export async function takeScreenshot(
    call: ServerUnaryCall<Request.ScreenshotPath>,
    callback: sendUnaryData<Response.Empty>,
    page?: Page,
) {
    // Add the file extension here because the image type is defined by playwrights defaults
    const path = call.request.getPath() + '.png';
    await invokePlaywright(page, callback, 'screenshot', { path: path });
    callback(null, emptyWithLog('Succesfully took screenshot'));
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

async function switchPage(
    browserState: BrowserState,
    pages: Array<Page>,
    index: number,
    callback: sendUnaryData<Response.Empty>,
) {
    console.log(`Changing active page to ${index}`);
    try {
        browserState.page = pages[index];
    } catch (e) {
        callback(e, null);
    }
}
export async function switchActivePage(
    call: ServerUnaryCall<Request.Index>,
    callback: sendUnaryData<Response.Empty>,
    browserState?: BrowserState,
) {
    exists(browserState, callback, "Tried to switch active page but browser wasn't open");
    const index = call.request.getIndex();
    const pages = browserState.context.pages();
    if (pages[index]) {
        switchPage(browserState, pages, index, callback);
    } else {
        try {
            await browserState.context.waitForEvent('page');
            switchPage(browserState, pages, index, callback);
        } catch (e) {
            // TODO: remove before merging or put behind --debug flag, debug prints
            console.log(`Existing contexts: ${browserState.browser.contexts().length}`);
            console.log(`Existing pages: ${pages.length}`);
            const mapped = pages.map((p) => p.url());
            const pageList = `Pages in current context: ${mapped.join(',')}`;
            const message = `No page for index ${index}. \n ` + pageList;
            const error = new Error(message);
            callback(error, null);
        }
    }
}
