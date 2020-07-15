import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { chromium, firefox, webkit, Browser, BrowserContext, Page } from 'playwright';

import { Response, Request } from './generated/playwright_pb';
import { invokeOnPage, exists } from './playwirght-util';
import { emptyWithLog, intResponse } from './response-util';

async function _newBrowser(
    browserType?: string,
    headless?: boolean,
    options?: Record<string, unknown>,
): Promise<[string, Browser]> {
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
    return [browserType, browser];
}

async function _newBrowserContext(browser: Browser, hideRfBrowser?: boolean): Promise<IndexedContext> {
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
    const index = browser.contexts().length - 1;
    return { index: index, c: context };
}

async function _newPage(context: BrowserContext): Promise<IndexedPage> {
    const index = context.pages().length;
    const newPage = await context.newPage();
    const page = { index: index, p: newPage };
    return page;
}

async function initializeBrowser(browserState: BrowserState): Promise<Browser> {
    if (browserState.browser) {
        return browserState.browser;
    } else {
        const [name, browser] = await _newBrowser();
        browserState.browser = browser;
        browserState.name = name;
        return browser;
    }
}

async function initializeContext(browserState: BrowserState): Promise<BrowserContext> {
    if (browserState.context?.c) {
        return browserState.context.c;
    } else {
        const browser = await initializeBrowser(browserState);
        const context = await _newBrowserContext(browser!);
        browserState.context = context;
        return context.c;
    }
}

export class PlaywrightState {
    constructor() {
        this.activeBrowser = 0;
        this.browsers = [];
    }
    browsers: (BrowserState | 'CLOSED')[];
    activeBrowser: number;
    public getActiveBrowser = <T>(callback: sendUnaryData<T>): BrowserState => {
        const currentBrowser = this.browsers[this.activeBrowser];
        if (currentBrowser === 'CLOSED') {
            const error = new Error('Browser has been closed.');
            callback(error, null);
            throw error;
        } else if (currentBrowser === undefined) {
            const newBrowser = new BrowserState();
            this.browsers[this.activeBrowser] = newBrowser;
            return newBrowser;
        } else {
            return currentBrowser;
        }
    };
    public getActivePage = <T>(callback: sendUnaryData<T>): Page | undefined => {
        const currentBrowser = this.getActiveBrowser(callback);
        return currentBrowser.page?.p;
    };
}

type IndexedContext = {
    c: BrowserContext;
    index: number;
};

type IndexedPage = {
    p: Page;
    index: number;
};

export class BrowserState {
    constructor(browser?: Browser, context?: BrowserContext, page?: Page, name?: string) {
        this.browser = browser;
        this.context = context ? { c: context, index: 0 } : undefined;
        this.page = page ? { p: page, index: 0 } : undefined;
        this.name = name;
    }
    browser?: Browser;
    context?: IndexedContext;
    page?: IndexedPage;
    name?: string;

    public async close() {
        await this.browser?.close();
        this.browser = undefined;
        this.context = undefined;
        this.page = undefined;
    }
}

export async function closeBrowser(callback: sendUnaryData<Response.Empty>, openBrowsers: PlaywrightState) {
    // FIXME: this can actually initialize a new browser and then close it ...
    const index = openBrowsers.activeBrowser;
    const currentBrowser = openBrowsers.browsers[index];
    if (currentBrowser === 'CLOSED') {
        callback(new Error(`Tried to close Browser ${index}, was already closed.`), null);
        return;
    }

    // TODO: Set next browser in list as active here
    currentBrowser.close();
    callback(null, emptyWithLog('Closed browser'));
}

export async function closeAllBrowsers(callback: sendUnaryData<Response.Empty>, openBrowsers: PlaywrightState) {
    const browsers = openBrowsers.browsers;
    for (let i = 0; i < browsers.length; i++) {
        const b = browsers[i];
        if (b !== 'CLOSED') {
            await b.close();
        }
        openBrowsers.browsers[i] = 'CLOSED';
    }
    openBrowsers.activeBrowser = 0;
    callback(null, emptyWithLog('Closed all browsers'));
}

export async function createPage(
    call: ServerUnaryCall<Request.Url>,
    callback: sendUnaryData<Response.Int>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const browserState = openBrowsers.getActiveBrowser(callback);
    await initializeBrowser(browserState);
    const context = await initializeContext(browserState);

    const pageIndex = context.pages().length;
    const page = await _newPage(context);
    browserState.page = page;
    const url = call.request.getUrl() || 'about:blank';
    await invokeOnPage(page.p, callback, 'goto', url, { timeout: 10000 });
    const response = intResponse(pageIndex);
    response.setLog('Succesfully initialized new page object and opened url');
    callback(null, response);
}

export async function createContext(
    call: ServerUnaryCall<Request.Context>,
    callback: sendUnaryData<Response.Int>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const browserState = openBrowsers.getActiveBrowser(callback);
    const browser = await initializeBrowser(browserState);
    try {
        const options = JSON.parse(call.request.getRawoptions());
        const contextIndex = browser.contexts().length;
        browserState.context = await _newBrowserContext(browser);
        const response = intResponse(contextIndex);
        response.setLog(`Succesfully created context with options ${options}`);
        callback(null, response);
    } catch (error) {
        callback(error, null);
        return;
    }
}

export async function createBrowser(
    call: ServerUnaryCall<Request.Browser>,
    callback: sendUnaryData<Response.Int>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const browserType = call.request.getBrowser();
    const headless = call.request.getHeadless();

    try {
        const options = JSON.parse(call.request.getRawoptions());
        const [name, browser] = await _newBrowser(browserType, headless, options);
        const browserState = new BrowserState();
        browserState.name = name;
        browserState.browser = browser;

        const newIndex = openBrowsers.browsers.push(browserState);
        openBrowsers.activeBrowser = newIndex - 1;
        const response = intResponse(newIndex);
        response.setLog('Succesfully created browser with options ${options}');
        callback(null, response);
    } catch (error) {
        callback(error, null);
    }
}

export async function autoActivatePages(
    call: ServerUnaryCall<Request.Empty>,
    callback: sendUnaryData<Response.Empty>,
    browserState?: BrowserState,
) {
    exists(
        browserState?.context?.c,
        callback,
        'Tried to focus next opened page, no context was open in current Browser',
    );

    browserState.context.c.on('page', (page) => {
        const pageIndex = browserState?.context?.c?.pages().length;
        browserState.page = { index: pageIndex || 0, p: page };
        console.log('Changed active page');
    });
    callback(null, emptyWithLog('Will focus future ``pages`` in this context'));
}

async function _switchPage(index: number, browserState: BrowserState) {
    const context = browserState?.context?.c;
    if (!context) throw new Error('Tried to switch page, no open context');
    const pages = context.pages();

    if (pages[index]) {
        browserState.page = { index: index, p: pages[index] };
        return;
    } else {
        try {
            console.log('Started waiting for a page to pop up');
            const page = await context.waitForEvent('page');
            browserState.page = { index: index, p: page };
            return;
        } catch (pwError) {
            console.log('Wait was not fulfilled');
            console.log(pwError);
            const mapped = pages?.map((p) => p.url()).join(',');
            const message = `No page for index ${index}. Open pages: ${mapped}`;
            const error = new Error(message);
            throw error;
        }
    }
}

async function _switchContext(index: number, browserState: BrowserState) {
    const contexts = browserState.browser?.contexts();
    if (contexts && contexts[index]) {
        browserState.context = { index: index, c: contexts[index] };
        return;
    } else {
        const mapped = contexts
            ?.map((c) => c.pages())
            .reduce((acc, val) => acc.concat(val), [])
            .map((p) => p.url());

        const message = `No context for index ${index}. Open contexts: ${mapped}`;
        const error = new Error(message);
        throw error;
    }
}

export async function switchPage(
    call: ServerUnaryCall<Request.Index>,
    callback: sendUnaryData<Response.Int>,
    browserState?: BrowserState,
) {
    exists(browserState, callback, "Tried to switch Page but browser wasn't open");
    console.log('Changing current active page');
    const index = call.request.getIndex();
    const previous = browserState.page?.index || 0;
    await _switchPage(index, browserState).catch((error) => callback(error, null));
    const response = intResponse(previous);
    response.setLog('Succesfully changed active page');
    callback(null, response);
}

export async function switchContext(
    call: ServerUnaryCall<Request.Index>,
    callback: sendUnaryData<Response.Int>,
    browserState?: BrowserState,
): Promise<void> {
    exists(browserState?.browser, callback, "Tried to switch Context but browser wasn't open");
    const index = call.request.getIndex();
    const previous = browserState.context?.index || 0;

    await _switchContext(index, browserState).catch((error) => callback(error, null));
    await _switchPage(browserState.page?.index || 0, browserState).catch(console.log);
    const response = intResponse(previous);
    response.setLog('Succesfully changed active context');
    callback(null, response);
}

export async function switchBrowser(
    call: ServerUnaryCall<Request.Index>,
    callback: sendUnaryData<Response.Int>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const index = call.request.getIndex();
    const previous = openBrowsers.activeBrowser;
    const switchedBrowser = openBrowsers.getActiveBrowser(callback);
    if (switchedBrowser) {
        openBrowsers.activeBrowser = index;
        try {
            // Try to switch to page and context in target browser
            await _switchContext(switchedBrowser.context?.index || 0, switchedBrowser);
            await _switchPage(switchedBrowser.page?.index || 0, switchedBrowser);
        } catch (pwError) {
            console.log(pwError);
        }
    } else {
        const mapped = openBrowsers.browsers.map((browserState) => {
            if (typeof browserState === 'string') return browserState;
            else return browserState?.name;
        });
        const message = `No browser for index ${index}. Open browsers: ` + mapped;
        const error = new Error(message);
        callback(error, null);
    }
    const response = intResponse(previous);
    response.setLog('Succesfully changed active browser');
    callback(null, response);
}
