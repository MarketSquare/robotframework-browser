import { sendUnaryData, ServerUnaryCall } from 'grpc';
import { chromium, firefox, webkit, Browser, BrowserContext, Page } from 'playwright';

import { Response, Request } from './generated/playwright_pb';
import { invokeOnPage, exists } from './playwirght-util';
import { emptyWithLog, intResponse } from './response-util';

async function _newBrowser(
    browserType?: string,
    headless?: boolean,
    options?: Record<string, unknown>,
): Promise<[Browser, string]> {
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
    return [browser, browserType];
}

async function _newBrowserContext(
    browser: Browser,
    options?: Record<string, unknown>,
    hideRfBrowser?: boolean,
): Promise<IndexedContext> {
    const context = await browser.newContext(options);
    if (!hideRfBrowser) {
        await context.addInitScript(function () {
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
    return { index: index, p: newPage };
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
            const mapped = this.browsers.map((browserState) => {
                if (typeof browserState === 'string') return browserState;
                else return browserState?.name;
            });
            const message = `No browser for index ${this.activeBrowser}. Open browsers: ` + mapped;
            const error = new Error(message);
            callback(error, null);
            throw error;
        } else {
            return currentBrowser;
        }
    };

    public async getOrCreateActiveBrowser(): Promise<BrowserState> {
        const currentBrowser = this.browsers[this.activeBrowser];
        if (currentBrowser == 'CLOSED' || !currentBrowser) {
            const [newBrowser, name] = await _newBrowser();
            const newState = new BrowserState(name, newBrowser);
            this.browsers[this.activeBrowser] = newState;
            return newState;
        } else {
            return currentBrowser;
        }
    }

    public getActiveContext = (): BrowserContext | undefined => {
        const currentBrowser = this.browsers[this.activeBrowser];
        if (currentBrowser === 'CLOSED') return undefined;
        return currentBrowser?.context?.c;
    };

    public getActivePage = (): Page | undefined => {
        const currentBrowser = this.browsers[this.activeBrowser];
        if (currentBrowser === 'CLOSED') return undefined;
        return currentBrowser?.page?.p;
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
    constructor(name: string, browser: Browser, context?: BrowserContext, page?: Page) {
        this.name = name;
        this.browser = browser;
        this.context = context ? { c: context, index: 0 } : undefined;
        this.page = page ? { p: page, index: 0 } : undefined;
    }
    private _context?: IndexedContext;
    private _page?: IndexedPage;
    browser: Browser;
    name?: string;

    public async close() {
        this.context = undefined;
        this.page = undefined;
        await this.browser.close();
    }

    public async getOrCreateActiveContext(): Promise<IndexedContext> {
        if (this.context) {
            return this.context;
        } else {
            const browser = this.browser;
            const context = await _newBrowserContext(browser);
            this.context = context;
            return context;
        }
    }
    get context() {
        return this._context;
    }
    set context(newContext: IndexedContext | undefined) {
        this._context = newContext;
        if (!newContext) console.log('Undefined active page');
        else console.log('Changed active context');
    }
    get page() {
        return this._page;
    }
    set page(newPage: IndexedPage | undefined) {
        this._page = newPage;
        if (!newPage) console.log('Undefined active page');
        else console.log('Changed active page');
    }
}

export async function closeBrowser(callback: sendUnaryData<Response.Empty>, openBrowsers: PlaywrightState) {
    const index = openBrowsers.activeBrowser;
    const currentBrowser = openBrowsers.browsers[index];
    if (currentBrowser === 'CLOSED') {
        callback(new Error(`Tried to close Browser ${index}, was already closed.`), null);
        return;
    }
    await currentBrowser.close();
    openBrowsers.browsers[index] = 'CLOSED';

    const newIndex = openBrowsers.browsers.findIndex((element) => element !== 'CLOSED');
    openBrowsers.activeBrowser = newIndex;
    const activeBrowser = openBrowsers.browsers[newIndex];
    if (activeBrowser && activeBrowser !== 'CLOSED') {
        await _switchContext(0, activeBrowser).catch((_) =>
            console.log("Couldn't change active Context after closing browser"),
        );
        await _switchPage(0, activeBrowser).catch((_) =>
            console.log("Couldn't change active Page after closing browser"),
        );
    }
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

export async function closeContext(
    callback: sendUnaryData<Response.Empty>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const activeBrowser = openBrowsers.getActiveBrowser(callback);
    await openBrowsers.getActiveContext()?.close();

    await _switchContext(0, activeBrowser).catch((_) => console.log("Couldn't change active Context after closing"));
    await _switchPage(0, activeBrowser).catch((_) => console.log("Couldn't change active Page after closing Context"));
    callback(null, emptyWithLog('Succesfully closed Context'));
}

export async function closePage(callback: sendUnaryData<Response.Empty>, openBrowsers: PlaywrightState): Promise<void> {
    const activeBrowser = openBrowsers.getActiveBrowser(callback);
    await openBrowsers.getActivePage()?.close();
    await _switchPage(0, activeBrowser).catch((_) => console.log("Couldn't change active Page after closing Page"));
    callback(null, emptyWithLog('Succesfully closed Page'));
}

export async function newPage(
    call: ServerUnaryCall<Request.Url>,
    callback: sendUnaryData<Response.Int>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const browserState = await openBrowsers.getOrCreateActiveBrowser();
    const context = await browserState.getOrCreateActiveContext();

    const page = await _newPage(context.c);
    browserState.page = page;
    const url = call.request.getUrl() || 'about:blank';
    await invokeOnPage(page.p, callback, 'goto', url, { timeout: 10000 });
    const response = intResponse(page.index);
    response.setLog('Succesfully initialized new page object and opened url');
    callback(null, response);
}

export async function newContext(
    call: ServerUnaryCall<Request.Context>,
    callback: sendUnaryData<Response.Int>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const hideRfBrowser = call.request.getHiderfbrowser();
    const browserState = await openBrowsers.getOrCreateActiveBrowser();
    try {
        const options = JSON.parse(call.request.getRawoptions());
        const context = await _newBrowserContext(browserState.browser, options, hideRfBrowser);
        browserState.context = context;

        const response = intResponse(context.index);
        response.setLog(`Succesfully created context with options ${options}`);
        callback(null, response);
    } catch (error) {
        callback(error, null);
        return;
    }
}

export async function newBrowser(
    call: ServerUnaryCall<Request.Browser>,
    callback: sendUnaryData<Response.Int>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const browserType = call.request.getBrowser();
    const headless = call.request.getHeadless();

    try {
        const options = JSON.parse(call.request.getRawoptions());
        const [browser, name] = await _newBrowser(browserType, headless, options);
        const browserState = new BrowserState(name, browser);

        const newIndex = openBrowsers.browsers.push(browserState) - 1;
        openBrowsers.activeBrowser = newIndex;
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
    const context = browserState.context?.c;
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
    const contexts = browserState.browser.contexts();
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
    browserState: BrowserState,
): Promise<void> {
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
    openBrowsers.activeBrowser = index;
    const switchedBrowser = openBrowsers.getActiveBrowser(callback);
    try {
        // Try to switch to page and context in target browser
        await _switchContext(switchedBrowser.context?.index || 0, switchedBrowser);
        await _switchPage(switchedBrowser.page?.index || 0, switchedBrowser);
    } catch (pwError) {
        console.log(pwError);
    }
    const response = intResponse(previous);
    response.setLog('Succesfully changed active browser');
    callback(null, response);
}

export async function getBrowserCatalog(
    callback: sendUnaryData<Response.String>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const response = new Response.String();

    const mappedBrowsers = openBrowsers.browsers.map((browser, index) => {
        if (browser !== 'CLOSED') {
            const contexts = browser.browser.contexts().map((context, i) => {
                return {
                    type: 'context',
                    id: i,
                    pages: context.pages(),
                };
            });
            return {
                type: browser.name,
                id: index,
                contexts: contexts,
            };
        } else {
            return {
                type: 'browser',
                id: index,
                state: 'CLOSED',
            };
        }
    });

    // This for looping is done instead of a .map on the pages() lists to avoid needing to handle deeply nested page.title() promises.
    for (const b of mappedBrowsers) {
        const contextList = b.contexts;
        if (contextList) {
            for (const c of contextList) {
                for (const i in c.pages) {
                    const page = c.pages[i];
                    const t = await page.title();
                    const url = page.url();
                    c.pages[i] = {
                        type: 'page',
                        title: t,
                        url: url,
                        id: i,
                    } as any;
                }
            }
        }
    }

    response.setBody(JSON.stringify(mappedBrowsers));

    callback(null, response);
}
