import { Browser, BrowserContext, ElementHandle, Page, chromium, firefox, webkit } from 'playwright';
import { ServerUnaryCall, sendUnaryData } from 'grpc';

import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog, intResponse } from './response-util';
import { exists, invokeOnPage } from './playwirght-invoke';

function lastItem<T>(array: T[]): T | undefined {
    return array[array.length - 1];
}

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
    return { index: index, c: context, pageStack: [] };
}

async function _newPage(context: BrowserContext): Promise<IndexedPage> {
    const index = context.pages().length;
    const newPage = await context.newPage();
    return { index: index, p: newPage };
}

export class PlaywrightState {
    constructor() {
        this.activeBrowser = undefined;
        this._browserStack = [];
        this.elementHandles = new Map();
    }
    _browserStack: BrowserState[];
    _ids = 0;
    activeBrowser: BrowserState | undefined;
    elementHandles: Map<string, ElementHandle>;
    public getActiveBrowser = <T>(callback: sendUnaryData<T>): BrowserState => {
        const currentBrowser = this.activeBrowser;
        if (currentBrowser === undefined) {
            const error = new Error('Browser has been closed.');
            callback(error, null);
            throw error;
        } else {
            return currentBrowser;
        }
    };

    public switchTo = <T>(id: number, callback: sendUnaryData<T>): BrowserState => {
        this.activeBrowser = this._browserStack.filter((b) => b.id === id)[0];
        this._browserStack = this._browserStack.filter((b) => b.id !== id);
        this._browserStack.push(this.activeBrowser);
        return this.getActiveBrowser(callback);
    };

    public async getOrCreateActiveBrowser(): Promise<BrowserState> {
        const currentBrowser = this.activeBrowser;
        if (currentBrowser === undefined) {
            const [newBrowser, name] = await _newBrowser();
            const newState = new BrowserState(name, newBrowser);
            this.activeBrowser = newState;
            this._browserStack.push(newState);
            return newState;
        } else {
            return currentBrowser;
        }
    }

    public async closeAll(): Promise<void> {
        const browsers = this._browserStack;
        for (const b of browsers) {
            await b.close();
        }
        this._browserStack = [];
        this.activeBrowser = undefined;
    }

    public async getCatalog() {
        const pageToContents = async (page: IndexedPage) => {
            return {
                type: 'page',
                title: await page.p.title(),
                url: page.p.url(),
                id: page.index,
            };
        };

        const contextToContents = async (context: IndexedContext) => {
            return {
                type: 'context',
                id: context.index,
                pages: await Promise.all(context.pageStack.map(pageToContents)),
            };
        };

        return Promise.all(
            this._browserStack.map(async (browser) => {
                return {
                    type: browser.name,
                    id: browser.id,
                    contexts: await Promise.all(browser.contextStack.map(contextToContents)),
                    activePage: browser.page?.index,
                    activeContext: browser.context?.index,
                    activeBrowser: this.activeBrowser === browser,
                };
            }),
        );
    }

    public addBrowser(name: string, browser: Browser): BrowserState {
        const browserState = new BrowserState(name, browser);
        browserState.id = this._ids++;
        this._browserStack.push(browserState);
        this.activeBrowser = browserState;
        return browserState;
    }

    public popBrowser(): void {
        this._browserStack.pop();
        if (this._browserStack.length > 0) {
            this.activeBrowser = lastItem(this._browserStack);
        } else {
            this.activeBrowser = undefined;
        }
    }

    public getActiveContext = (): BrowserContext | undefined => {
        return this.activeBrowser?.context?.c;
    };

    public getActivePage = (): Page | undefined => {
        return this.activeBrowser?.page?.p;
    };

    public addElement(id: string, handle: ElementHandle): void {
        this.elementHandles.set(id, handle);
    }

    public getElement(id: string): ElementHandle {
        const elem = this.elementHandles.get(id);
        if (elem) {
            return elem;
        }
        throw new Error(`No element handle found with id \`${id}\`.`);
    }
}

type IndexedContext = {
    c: BrowserContext;
    index: number;
    pageStack: IndexedPage[];
};

type IndexedPage = {
    p: Page;
    index: number;
};

export class BrowserState {
    constructor(name: string, browser: Browser, context?: BrowserContext, page?: Page) {
        this.name = name;
        this.browser = browser;
        this._contextStack = [];
        this.context = context ? { c: context, index: 0, pageStack: [] } : undefined;
        this.page = page ? { p: page, index: 0 } : undefined;
        this.id = -1;
    }
    private _contextStack: IndexedContext[];
    browser: Browser;
    name?: string;
    id: number;

    public async close(): Promise<void> {
        this.context = undefined;
        this.page = undefined;
        this._contextStack = [];
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
    get context(): IndexedContext | undefined {
        return lastItem(this._contextStack);
    }
    set context(newContext: IndexedContext | undefined) {
        if (newContext !== undefined) {
            // prevent duplicates
            this._contextStack = this._contextStack.filter((c) => c.c !== newContext.c);
            this._contextStack.push(newContext);
            console.log('Changed active context');
        } else console.log('Set active context to undefined');
    }
    get page(): IndexedPage | undefined {
        const context = this.context;
        if (context) return lastItem(context.pageStack);
        else return undefined;
    }
    set page(newPage: IndexedPage | undefined) {
        const currentContext = this.context;
        if (newPage !== undefined && currentContext !== undefined) {
            // prevent duplicates
            currentContext.pageStack = currentContext.pageStack.filter((p) => p.p !== newPage.p);
            currentContext.pageStack.push(newPage);
            console.log('Changed active page');
        } else {
            console.log('Set active page to undefined');
        }
    }
    get contextStack(): IndexedContext[] {
        return this._contextStack;
    }
    public popPage(): void {
        const pageStack = this.context?.pageStack || [];
        pageStack.pop();
    }
    public popContext(): void {
        this._contextStack.pop();
        const context = lastItem(this._contextStack);
        if (context) {
            this.context = context;
        } else {
            this.context = undefined;
        }
    }
}

export async function closeBrowser(callback: sendUnaryData<Response.Empty>, openBrowsers: PlaywrightState) {
    const index = openBrowsers.activeBrowser;
    const currentBrowser = openBrowsers.activeBrowser;
    if (currentBrowser === undefined) {
        callback(new Error(`Tried to close Browser ${index}, was already closed.`), null);
        return;
    }
    await currentBrowser.close();
    openBrowsers.popBrowser();
    callback(null, emptyWithLog('Closed browser'));
}

export async function closeAllBrowsers(callback: sendUnaryData<Response.Empty>, openBrowsers: PlaywrightState) {
    await openBrowsers.closeAll();
    callback(null, emptyWithLog('Closed all browsers'));
}

export async function closeContext(
    callback: sendUnaryData<Response.Empty>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const activeBrowser = openBrowsers.getActiveBrowser(callback);
    await openBrowsers.getActiveContext()?.close();
    activeBrowser.popContext();
    callback(null, emptyWithLog('Succesfully closed Context'));
}

export async function closePage(callback: sendUnaryData<Response.Empty>, openBrowsers: PlaywrightState): Promise<void> {
    const activeBrowser = openBrowsers.getActiveBrowser(callback);
    await openBrowsers.getActivePage()?.close();
    activeBrowser.popPage();
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
        const browserState = openBrowsers.addBrowser(name, browser);
        const response = intResponse(browserState.id);
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

async function _switchPage(index: number, browserState: BrowserState, waitForPage: boolean) {
    const context = browserState.context?.c;
    if (!context) throw new Error('Tried to switch page, no open context');
    const pages = context.pages();

    if (pages[index]) {
        browserState.page = { index: index, p: pages[index] };
        return;
    } else if (waitForPage) {
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
    } else {
        throw new Error(`Couldn't switch page`);
    }
}

async function _switchContext(index: number, browserState: BrowserState) {
    const contexts = browserState.browser.contexts();
    if (contexts && contexts[index]) {
        browserState.context = { index: index, c: contexts[index], pageStack: [] };
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
    await _switchPage(index, browserState, true).catch((error) => callback(error, null));
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
    await _switchPage(browserState.page?.index || 0, browserState, false).catch(console.log);
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
    openBrowsers.switchTo(index, callback);
    const response = intResponse(previous?.id || -1);
    response.setLog('Succesfully changed active browser');
    callback(null, response);
}

export async function getBrowserCatalog(
    callback: sendUnaryData<Response.String>,
    openBrowsers: PlaywrightState,
): Promise<void> {
    const response = new Response.String();
    response.setBody(JSON.stringify(await openBrowsers.getCatalog()));
    callback(null, response);
}
