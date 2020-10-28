// Copyright 2020-     Robot Framework Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { Browser, BrowserContext, ElementHandle, Page, chromium, firefox, webkit } from 'playwright';
import { ServerUnaryCall, sendUnaryData } from '@grpc/grpc-js';
import { v4 as uuidv4 } from 'uuid';

import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog, jsonResponse, stringResponse } from './response-util';
import { exists, invokeOnPage } from './playwirght-invoke';

import * as pino from 'pino';

const logger = pino.default({ timestamp: pino.stdTimeFunctions.isoTime });

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
    defaultTimeout: number,
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
    context.setDefaultTimeout(defaultTimeout);
    const c = { id: `context=${uuidv4()}`, c: context, pageStack: [] as IndexedPage[], options: options };
    c.c.on('page', (page) => {
        const timestamp = new Date().getTime() / 1000;
        const newPage = { id: `page=${uuidv4()}`, p: page, timestamp: timestamp };
        c.pageStack.unshift(newPage);
    });
    return c;
}

async function _newPage(context: BrowserContext): Promise<IndexedPage> {
    const newPage = await context.newPage();
    const timestamp = new Date().getTime() / 1000;
    return { id: `page=${uuidv4()}`, p: newPage, timestamp: timestamp };
}

export class PlaywrightState {
    constructor() {
        this.browserStack = [];
        this.elementHandles = new Map();
    }
    private browserStack: BrowserState[];
    get activeBrowser() {
        return lastItem(this.browserStack);
    }
    elementHandles: Map<string, ElementHandle>;
    public getActiveBrowser = (): BrowserState => {
        const currentBrowser = this.activeBrowser;
        if (currentBrowser === undefined) {
            throw new Error('Browser has been closed.');
        }
        return currentBrowser;
    };

    public switchTo = (id: Uuid): BrowserState => {
        const browser = this.browserStack.find((b) => b.id === id);
        exists(browser, `No browser for id '${id}'`);
        this.browserStack = this.browserStack.filter((b) => b.id !== id);
        this.browserStack.push(browser);
        return this.getActiveBrowser();
    };

    public async getOrCreateActiveBrowser(): Promise<BrowserState> {
        const currentBrowser = this.activeBrowser;
        if (currentBrowser === undefined) {
            const [newBrowser, name] = await _newBrowser();
            const newState = new BrowserState(name, newBrowser);
            this.browserStack.push(newState);
            return newState;
        } else {
            return currentBrowser;
        }
    }

    public async closeAll(): Promise<void> {
        const browsers = this.browserStack;
        for (const b of browsers) {
            await b.close();
        }
        this.browserStack = [];
    }

    public async getCatalog() {
        const pageToContents = async (page: IndexedPage) => {
            return {
                type: 'page',
                title: await page.p.title(),
                url: page.p.url(),
                id: page.id,
                timestamp: page.timestamp,
            };
        };

        const contextToContents = async (context: IndexedContext) => {
            const activePage = lastItem(context.pageStack)?.id;
            return {
                type: 'context',
                id: context?.id,
                activePage: activePage,
                pages: await Promise.all(context.pageStack.map(pageToContents)),
            };
        };

        return Promise.all(
            this.browserStack.map(async (browser) => {
                return {
                    type: browser.name,
                    id: browser.id,
                    contexts: await Promise.all(browser.contextStack.map(contextToContents)),
                    activeContext: browser.context?.id,
                    activeBrowser: this.activeBrowser === browser,
                };
            }),
        );
    }

    public addBrowser(name: string, browser: Browser): BrowserState {
        const browserState = new BrowserState(name, browser);
        this.browserStack.push(browserState);
        return browserState;
    }

    public popBrowser(): void {
        this.browserStack.pop();
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

/*
 * Pagestack's last item should be the current active page and the first item should be the lastly added page
 * */
type IndexedContext = {
    c: BrowserContext;
    id: Uuid;
    pageStack: IndexedPage[];
    options?: Record<string, unknown>;
};

type IndexedPage = {
    p: Page;
    id: Uuid;
    timestamp: number;
};

type Uuid = string;

/*
 * contextStacks's last item should be the current active page and the first item should be the lastly added page.
 * User opened items should get pushed and page opened unshifted
 * */
export class BrowserState {
    constructor(name: string, browser: Browser) {
        this.name = name;
        this.browser = browser;
        this._contextStack = [];
        this.id = `browser=${uuidv4()}`;
    }
    private _contextStack: IndexedContext[];
    browser: Browser;
    name?: string;
    id: Uuid;

    public async close(): Promise<void> {
        this._contextStack = [];
        await this.browser.close();
    }

    public async getOrCreateActiveContext(defaultTimeout: number): Promise<IndexedContext> {
        if (this.context) {
            return this.context;
        } else {
            const activeBrowser = this.browser;
            const context = await _newBrowserContext(activeBrowser, defaultTimeout);
            this.pushContext(context);
            return context;
        }
    }
    get context(): IndexedContext | undefined {
        return lastItem(this._contextStack);
    }
    pushContext(newContext: IndexedContext | undefined) {
        if (newContext !== undefined) {
            if (newContext.options === undefined) {
                // copy known options
                newContext.options = this._contextStack.find((c) => c.c === newContext.c)?.options;
            }
            // prevent duplicates
            this._contextStack = this._contextStack.filter((c) => c.c !== newContext.c);
            this._contextStack.push(newContext);
            logger.info('Changed active context');
        } else logger.info('Set active context to undefined');
    }

    unshiftContext(newContext: IndexedContext) {
        this._contextStack.unshift(newContext);
    }

    get page(): IndexedPage | undefined {
        const context = this.context;
        if (context) return lastItem(context.pageStack);
        else return undefined;
    }

    async activatePage(page: IndexedPage) {
        this.pushPage(page);
        await page.p.bringToFront();
    }

    pushPage(newPage: IndexedPage | undefined) {
        const currentContext = this.context;
        if (newPage !== undefined && currentContext !== undefined) {
            // prevent duplicates
            currentContext.pageStack = currentContext.pageStack.filter((p) => p.p !== newPage.p);
            currentContext.pageStack.push(newPage);
            logger.info('Changed active page');
        } else {
            logger.info('Set active page to undefined');
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
    }
}

export async function closeBrowser(openBrowsers: PlaywrightState): Promise<Response.String> {
    const currentBrowser = openBrowsers.activeBrowser;
    if (currentBrowser === undefined) {
        return stringResponse('no-browser', 'No browser open, doing nothing');
    }
    await currentBrowser.close();
    openBrowsers.popBrowser();
    return stringResponse(currentBrowser.id, 'Closed browser');
}

export async function closeAllBrowsers(openBrowsers: PlaywrightState): Promise<Response.Empty> {
    await openBrowsers.closeAll();
    return emptyWithLog('Closed all browsers');
}

export async function closeContext(openBrowsers: PlaywrightState): Promise<Response.Empty> {
    const activeBrowser = openBrowsers.getActiveBrowser();
    await openBrowsers.getActiveContext()?.close();
    activeBrowser.popContext();
    return emptyWithLog('Successfully closed Context');
}

export async function closePage(openBrowsers: PlaywrightState): Promise<Response.Empty> {
    const activeBrowser = openBrowsers.getActiveBrowser();
    await openBrowsers.getActivePage()?.close();
    activeBrowser.popPage();
    return emptyWithLog('Successfully closed Page');
}

export async function newPage(request: Request.Url, openBrowsers: PlaywrightState): Promise<Response.String> {
    const browserState = await openBrowsers.getOrCreateActiveBrowser();
    const defaultTimeout = request.getDefaulttimeout();
    const context = await browserState.getOrCreateActiveContext(defaultTimeout);

    const page = await _newPage(context.c);
    browserState.pushPage(page);
    const url = request.getUrl() || 'about:blank';
    try {
        await page.p.goto(url);
        return stringResponse(page.id, 'Successfully initialized new page object and opened url: ' + url);
    } catch (e) {
        browserState.popPage();
        throw e;
    }
}

export async function newContext(request: Request.Context, openBrowsers: PlaywrightState): Promise<Response.String> {
    const hideRfBrowser = request.getHiderfbrowser();
    const browserState = await openBrowsers.getOrCreateActiveBrowser();
    const options = JSON.parse(request.getRawoptions());
    const defaultTimeout = request.getDefaulttimeout();
    const context = await _newBrowserContext(browserState.browser, defaultTimeout, options, hideRfBrowser);
    browserState.pushContext(context);

    return stringResponse(context.id, 'Successfully created context with options: ' + JSON.stringify(options));
}

export async function newBrowser(request: Request.Browser, openBrowsers: PlaywrightState): Promise<Response.String> {
    const browserType = request.getBrowser();
    const headless = request.getHeadless();
    const options = JSON.parse(request.getRawoptions());
    const [browser, name] = await _newBrowser(browserType, headless, options);
    const browserState = openBrowsers.addBrowser(name, browser);
    return stringResponse(browserState.id, 'Successfully created browser with options: ' + JSON.stringify(options));
}

async function _switchPage(id: Uuid, browserState: BrowserState) {
    const context = browserState.context?.c;
    if (!context) throw new Error('Tried to switch page, no open context');
    const pages = browserState.context?.pageStack;
    logger.info('Changing current active page');
    const page = pages?.find((elem) => elem.id == id);
    if (page) {
        await browserState.activatePage(page);
        return;
    } else {
        const mapped = pages?.map((page) => `{ id: ${page.id}, url: ${page.p.url()} }`).join(',');
        const message = `No page for id ${id}. Open pages: ${mapped}`;
        const error = new Error(message);
        throw error;
    }
}

async function _switchContext(id: Uuid, browserState: BrowserState) {
    const contexts = browserState.contextStack;
    const context = contexts.find((context) => context.id === id);
    if (contexts && context) {
        browserState.pushContext(context);
        return;
    } else {
        const mapped = contexts.map((context) => context.id);

        const message = `No context for id ${id}. Open contexts: ${mapped}`;
        throw new Error(message);
    }
}

export async function switchPage(
    request: Request.IdWithTimeout,
    browserState?: BrowserState,
): Promise<Response.String> {
    exists(browserState, "Tried to switch Page but browser wasn't open");
    const context = browserState.context;
    exists(context, 'Tried to switch Page but no context was open');
    const id = request.getId();
    if (id === 'CURRENT') {
        const previous = browserState.page?.id || 'NO PAGE OPEN';
        return stringResponse(previous, 'Returned active page id');
    } else if (id === 'NEW') {
        const previous = browserState.page?.id || 'NO PAGE OPEN';
        const previousTime = browserState.page?.timestamp || 0;
        const latest = await findLatestPageAfter(previousTime, request.getTimeout(), context);
        exists(latest, 'Tried to activate a new page but no new pages were detected in context.');
        await browserState.activatePage(latest);
        return stringResponse(previous, `Activated new page ${latest.id}`);
    }

    const previous = browserState.page?.id || '';
    await _switchPage(id, browserState);
    return stringResponse(previous, 'Successfully changed active page');
}

async function findLatestPageAfter(
    timestamp: number,
    timeout: number,
    context: IndexedContext,
): Promise<IndexedPage | null> {
    if (timeout < 0) {
        return null;
    }
    const latest = context.pageStack.reduce((acc, val) => {
        if (acc === undefined || acc.timestamp < val.timestamp) {
            return val;
        }
        return acc;
    });
    if (!latest || (timestamp && latest.timestamp <= timestamp)) {
        await new Promise((resolve) => setTimeout(resolve, Math.min(15, timeout)));
        return findLatestPageAfter(timestamp, timeout - 15, context);
    }
    return latest;
}

export async function switchContext(request: Request.Index, browserState: BrowserState): Promise<Response.String> {
    const id = request.getIndex();
    const previous = browserState.context?.id || '';

    if (id === 'CURRENT') {
        if (!previous) {
            return stringResponse('NO CONTEXT OPEN', 'Returned info that no contexts are open');
        } else {
            return stringResponse(previous, 'Returned active context id');
        }
    }

    await _switchContext(id, browserState);
    await _switchPage(browserState.page?.id || '', browserState);
    return stringResponse(previous, 'Successfully changed active context');
}

export async function switchBrowser(request: Request.Index, openBrowsers: PlaywrightState): Promise<Response.String> {
    const id = request.getIndex();
    const previous = openBrowsers.activeBrowser;
    if (id === 'CURRENT') {
        return stringResponse(previous?.id || 'NO BROWSER OPEN', 'Active context id');
    }
    openBrowsers.switchTo(id);
    return stringResponse(previous?.id || '', 'Successfully changed active browser');
}

export async function getBrowserCatalog(openBrowsers: PlaywrightState): Promise<Response.Json> {
    return jsonResponse(JSON.stringify(await openBrowsers.getCatalog()), 'Catalog received');
}
