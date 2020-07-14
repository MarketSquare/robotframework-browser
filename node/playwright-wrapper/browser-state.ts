import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { chromium, firefox, webkit, Browser, BrowserContext, Page } from 'playwright';

import { Response, Request } from './generated/playwright_pb';
import { invokeOnPage, exists } from './playwirght-util';
import { emptyWithLog, stringResponse } from './response-util';

async function newBrowser(
    browserType?: string,
    headless?: boolean,
    options?: Record<string, unknown>,
): Promise<Browser> {
    browserType = browserType || 'chromium';
    headless = headless || true;
    let browser;
    if (browserType === 'firefox') {
        browser = await firefox.launch({ headless: headless, ...options });
    } else if (browserType === 'chromium') {
        browser = await chromium.launch({ headless: headless, ...options });
    } else if (browserType === 'webkit') {
        browser = await webkit.launch({ headless: headless, ...options });
    } else {
        throw new Error('unsupported browser');
    }
    return browser;
}

async function newBrowserContext(browser: Browser, hideRfBrowser?: boolean): Promise<BrowserContext> {
    hideRfBrowser = hideRfBrowser || false;
    const context = await browser.newContext();
    if (!hideRfBrowser) {
        context.addInitScript(function () {
            window.__SET_RFBROWSER_STATE__ = function (state: any) {
                window.__RFBROWSER__ = state;
                return state;
            };
        });
    }
    context.setDefaultTimeout(parseFloat(process.env.TIMEOUT || '10000'));
    return context;
}

export class BrowserState {
    constructor(browser?: Browser, context?: BrowserContext, page?: Page) {
        this.browser = browser;
        this.context = context;
        this.page = page;
    }
    browser?: Browser;
    context?: BrowserContext;
    page?: Page;
}

async function initializeBrowser(browserState: BrowserState): Promise<Browser> {
    if (browserState.browser) {
        return browserState.browser;
    } else {
        const browser = await newBrowser();
        browserState.browser = browser;
        return browser;
    }
}

async function initializeContext(browserState: BrowserState): Promise<BrowserContext> {
    if (browserState?.context) {
        return browserState.context;
    } else {
        if (!browserState?.browser) {
            await initializeBrowser(browserState);
        }
        const browser = browserState.browser;
        const context = await newBrowserContext(browser!);
        browserState.context = context;
        return context;
    }
}

export async function closeBrowser(callback: sendUnaryData<Response.Empty>, browserState: BrowserState) {
    exists(browserState?.browser, callback, 'Tried to close browser but none was open');
    await browserState.browser.close();
    browserState.context = undefined;
    browserState.page = undefined;
}

export async function createPage(
    call: ServerUnaryCall<Request.Url>,
    callback: sendUnaryData<Response.Empty>,
    browserState: BrowserState,
): Promise<void> {
    const context = await initializeContext(browserState);

    const page = await context?.newPage();
    browserState.page = page;
    const url = call.request.getUrl() || 'about:blank';
    await invokeOnPage(page, callback, 'goto', url, { timeout: 10000 });
    callback(null, emptyWithLog('Succesfully initialized new page object and opened url'));
}

export async function createContext(
    call: ServerUnaryCall<Request.Context>,
    callback: sendUnaryData<Response.Empty>,
    browserState: BrowserState,
): Promise<void> {
    const browser = await initializeBrowser(browserState);
    try {
        const options = JSON.parse(call.request.getRawoptions());
        browserState.context = await newBrowserContext(browser);
        callback(null, emptyWithLog(`Succesfully created context with options ${options}`));
    } catch (error) {
        callback(error, null);
        return;
    }
}

export async function createBrowser(
    call: ServerUnaryCall<Request.Browser>,
    callback: sendUnaryData<Response.Empty>,
    browserState: BrowserState,
): Promise<void> {
    const browserType = call.request.getBrowser();
    const headless = call.request.getHeadless();

    try {
        const options = JSON.parse(call.request.getRawoptions());
        browserState.browser = await newBrowser(browserType, headless, options);
        callback(null, emptyWithLog(`Succesfully opened browser ${browserType}`));
    } catch (error) {
        callback(error, null);
        return;
    }
}

export async function autoActivatePages(
    call: ServerUnaryCall<Request.Empty>,
    callback: sendUnaryData<Response.Empty>,
    browserState: BrowserState,
) {
    exists(browserState?.context, callback, 'Tried to focus next opened page');

    browserState.context.on('page', (page) => {
        browserState.page = page;
        console.log('Changed active page');
    });
    callback(null, emptyWithLog('Will focus future ``pages`` in this context'));
}

export async function switchPage(
    call: ServerUnaryCall<Request.Index>,
    callback: sendUnaryData<Response.Empty>,
    browserState: BrowserState,
) {
    exists(browserState.context, callback, "Tried to switch active page but wasn't open");
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

export async function switchContext(
    call: ServerUnaryCall<Request.Index>,
    callback: sendUnaryData<Response.Empty>,
    browserState: BrowserState,
): Promise<void> {
    exists(browserState.browser, callback, "Tried to switch active context but browser wasn't open");
    const index = call.request.getIndex();
    const contexts = browserState.browser.contexts();

    if (contexts[index]) {
        browserState.context = contexts[index];
        callback(null, emptyWithLog('Succesfully changed active context'));
    } else {
        const mapped = contexts
            .map((c) => c.pages())
            .reduce((acc, val) => acc.concat(val), [])
            .map((p) => p.url());

        const message = `No context for index ${index}. \n ` + mapped;
        const error = new Error(message);
        callback(error, null);
        return;
    }
    const error = new Error('Functionality not implemented yet');
    callback(error, null);
}

export async function switchBrowser(
    call: ServerUnaryCall<Request.Index>,
    callback: sendUnaryData<Response.Empty>,
    browsers: BrowserState[],
    setBrowser: (newBrowser: BrowserState) => void,
): Promise<void> {
    const index = call.request.getIndex();
    if (browsers[index]) {
        setBrowser(browsers[index]);
        callback(null, emptyWithLog('Succesfully changed active page'));
    } else {
        // TODO: put behind --debug flag, debug prints
        const message = `No browser for index ${index}. \n ` + browsers;
        const error = new Error(message);
        callback(error, null);
        return;
    }
}
