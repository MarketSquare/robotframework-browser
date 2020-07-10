import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { chromium, firefox, webkit, Browser, BrowserContext, Page } from 'playwright';

import { Response, Request } from './generated/playwright_pb';
import { invokeOnPage, exists } from './playwirght-util';
import { emptyWithLog, stringResponse } from './response-util';
import { PlaywrightServer } from './server';

// Can't have an async constructor, this is a workaround
export async function createBrowserState(
    browserType: string,
    headless: boolean,
    hideRfBrowser: boolean,
): Promise<BrowserState> {
    let browser;
    if (browserType === 'firefox') {
        browser = await firefox.launch({ headless: headless });
    } else if (browserType === 'chromium') {
        browser = await chromium.launch({ headless: headless });
    } else if (browserType === 'webkit') {
        browser = await webkit.launch({ headless: headless });
    } else {
        throw new Error('unsupported browser');
    }
    const context = await browser.newContext();
    if (!hideRfBrowser) {
        context.addInitScript(function () {
            window.__SET_RFBROWSER__ = function (state: any) {
                window.__RFBROWSER__ = state;
                return state;
            };
        });
    }
    context.setDefaultTimeout(parseFloat(process.env.TIMEOUT || '10000'));
    const page = await context.newPage();
    return new BrowserState(browser, context, page);
}

export class BrowserState {
    constructor(browser: Browser, context: BrowserContext, page: Page) {
        this.browser = browser;
        this.context = context;
        this.page = page;
    }
    browser: Browser;
    context: BrowserContext;
    page: Page;
}

export async function openBrowser(
    call: ServerUnaryCall<Request.NewBrowser>,
    callback: sendUnaryData<Response.Empty>,
    playwrightServer: PlaywrightServer,
): Promise<void> {
    const browserType = call.request.getBrowser();
    const headless = call.request.getHeadless();

    playwrightServer.browserState = await createBrowserState(browserType, headless, false);
    callback(null, emptyWithLog(`Succesfully opened browser ${browserType}`));
}

export async function closeBrowser(callback: sendUnaryData<Response.Empty>, browser?: Browser) {
    exists(browser, callback, 'Tried to close browser but none was open');
    await browser.close();
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
