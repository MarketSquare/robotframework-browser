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

import * as playwright from 'playwright';
import { Browser, BrowserContext, ConsoleMessage, Locator, Page, chromium, firefox, webkit } from 'playwright';
import { v4 as uuidv4 } from 'uuid';

import { Request, Response } from './generated/playwright_pb';
import { emptyWithLog, jsonResponse, keywordsResponse, pageReportResponse, stringResponse } from './response-util';
import { exists } from './playwright-invoke';

import { ServerWritableStream } from '@grpc/grpc-js';
import { pino } from 'pino';
import strip from 'strip-comments';

const logger = pino({ timestamp: pino.stdTimeFunctions.isoTime });

function lastItem<T>(array: T[]): T | undefined {
    return array[array.length - 1];
}

interface IBrowserState {
    browser: BrowserState;
    newBrowser: boolean;
}

interface IIndexedContext {
    context: IndexedContext;
    newContext: boolean;
}

export interface LocatorCount {
    locator: Locator;
    nth: number;
}

const extractArgumentsStringFromJavascript = (javascript: string): string => {
    const regex = /\((.*?)\)/;
    const match = regex.exec(strip(javascript).replace(/\r?\n/g, ''));
    if (match) {
        return match[1];
    }
    logger.error(`Could not extract arguments from javascript:\n${javascript}\ndefaulting to *args`);
    return '*args';
};

export async function initializeExtension(
    request: Request.FilePath,
    state: PlaywrightState,
): Promise<Response.Keywords> {
    const extension: Record<string, (...args: unknown[]) => unknown> = eval('require')(request.getPath());
    state.extension = extension;
    const kws = Object.keys(extension).filter((key) => extension[key] instanceof Function && !key.startsWith('__'));
    return keywordsResponse(
        kws,
        kws.map((v) => {
            return extractArgumentsStringFromJavascript(extension[v].toString());
        }),
        kws.map((v) => {
            const typedV = extension[v] as { rfdoc?: string };
            return typedV.rfdoc ?? 'TODO: Add rfdoc string to exposed function to create documentation';
        }),
        'ok',
    );
}

export async function extensionKeywordCall(
    request: Request.KeywordCall,
    call: ServerWritableStream<Request.KeywordCall, Response.Json>,
    state: PlaywrightState,
): Promise<Response.Json> {
    const methodName = request.getName();
    const args = JSON.parse(request.getArguments()) as { arguments: [string, unknown][] };
    const func = (state.extension as Record<string, (...args: unknown[]) => unknown>)[methodName];
    const result = await func(
        ...args['arguments'].map((v) => {
            if (v[0] === 'page') {
                return state.getActivePage();
            }
            if (v[0] === 'logger') {
                return (msg: string) => {
                    call.write(jsonResponse(JSON.stringify(''), msg));
                };
            }
            if (v[0] === 'playwright') {
                return playwright;
            }
            return v[1];
        }),
    );
    return jsonResponse(JSON.stringify(result), 'ok');
}

interface BrowserAndConfs {
    browser: Browser | null;
    browserType: 'chromium' | 'firefox' | 'webkit';
    headless: boolean;
}

async function _newBrowser(
    browserType: 'chromium' | 'firefox' | 'webkit',
    headless: boolean,
    timeout: number,
    options?: Record<string, unknown>,
): Promise<BrowserAndConfs> {
    let browser;
    const launchOptions: playwright.LaunchOptions = { ...options, headless, timeout };
    if (browserType === 'firefox') {
        browser = await firefox.launch(launchOptions);
    } else if (browserType === 'chromium') {
        browser = await chromium.launch(launchOptions);
    } else if (browserType === 'webkit') {
        browser = await webkit.launch(launchOptions);
    } else {
        throw new Error('unsupported browser');
    }
    return {
        browser,
        browserType,
        headless,
    };
}

async function _connectBrowser(browserType: string, url: string): Promise<BrowserAndConfs> {
    browserType = browserType || 'chromium';
    let browser;
    if (browserType === 'firefox') {
        browser = await firefox.connect({ wsEndpoint: url });
    } else if (browserType === 'chromium') {
        browser = await chromium.connect({ wsEndpoint: url });
    } else if (browserType === 'webkit') {
        browser = await webkit.connect({ wsEndpoint: url });
    } else {
        throw new Error('unsupported browser');
    }
    return {
        browser,
        browserType,
        headless: false,
    };
}

async function _newBrowserContext(
    browser: Browser,
    defaultTimeout: number,
    traceFile: string,
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
    const c = {
        id: `context=${uuidv4()}`,
        c: context,
        pageStack: [] as IndexedPage[],
        options: options,
        traceFile: traceFile,
    };
    if (traceFile) {
        logger.info('Tracing enabled with: { screenshots: true, snapshots: true }');
        context.tracing.start({ screenshots: true, snapshots: true });
    }
    c.c.on('page', async (page) => {
        c.pageStack.unshift(await _newPage(c, page));
    });
    return c;
}

function indexedPage(newPage: Page) {
    const timestamp = new Date().getTime() / 1000;
    const pageErrors: Error[] = [];
    const consoleMessages: ConsoleMessage[] = [];
    newPage.on('pageerror', (error) => {
        pageErrors.push(error);
    });
    newPage.on('console', (message) => {
        consoleMessages.push(message);
    });
    return {
        id: `page=${uuidv4()}`,
        p: newPage,
        timestamp,
        pageErrors,
        consoleMessages,
    };
}

async function _newPage(context: IndexedContext, page: Page | undefined = undefined): Promise<IndexedPage> {
    const newPage = page === undefined ? await context.c.newPage() : page;
    const contextPage = indexedPage(newPage);
    newPage.on('close', () => {
        const oldPageStackLength = context.pageStack.length;
        const filteredPageStack = context.pageStack.filter((page: IndexedPage) => page.p != contextPage.p);

        if (oldPageStackLength != filteredPageStack.length) {
            context.pageStack = filteredPageStack;
            logger.info('Removed ' + contextPage.id + ' from ' + context.id + ' page stack');
        }
    });
    return contextPage;
}

export class PlaywrightState {
    constructor() {
        this.browserStack = [];
        this.locatorHandles = new Map();
    }
    extension: unknown;
    private browserStack: BrowserState[];
    get activeBrowser() {
        return lastItem(this.browserStack);
    }
    locatorHandles: Map<string, LocatorCount>;
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

    public async getOrCreateActiveBrowser(
        browserType: 'chromium' | 'firefox' | 'webkit' | null,
        timeout: number,
    ): Promise<IBrowserState> {
        const currentBrowser = this.activeBrowser;
        logger.info('currentBrowser: ' + currentBrowser);
        if (currentBrowser === undefined) {
            const browserAndConfs = await _newBrowser(browserType || 'chromium', true, timeout);
            const newState = new BrowserState(browserAndConfs);
            this.browserStack.push(newState);
            return { browser: newState, newBrowser: true };
        } else {
            return { browser: currentBrowser, newBrowser: false };
        }
    }

    public async closeAll(): Promise<void> {
        const browsers = this.browserStack;
        for (const browser of browsers) {
            await browser.close();
        }
        this.browserStack = [];
    }

    public async getCatalog() {
        const pageToContents = async (page: IndexedPage) => {
            let title = null;
            const titlePromise = page.p.title();
            const titleTimeout = new Promise((_r, rej) => setTimeout(() => rej(null), 350));
            try {
                title = await Promise.race([titlePromise, titleTimeout]);
            } catch (e) {}
            return {
                type: 'page',
                title,
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

    public addBrowser(browserAndConfs: BrowserAndConfs): BrowserState {
        const browserState = new BrowserState(browserAndConfs);
        this.browserStack.push(browserState);
        return browserState;
    }

    public popBrowser(): BrowserState | undefined {
        return this.browserStack.pop();
    }

    public getActiveContext = (): BrowserContext | undefined => {
        return this.activeBrowser?.context?.c;
    };

    public getTraceFile = (): string | undefined => {
        return this.activeBrowser?.context?.traceFile;
    };
    public getActivePage = (): Page | undefined => {
        return this.activeBrowser?.page?.p;
    };

    public addLocator(id: string, pwLocator: Locator, nth: number): void {
        this.locatorHandles.set(id, { locator: pwLocator, nth: nth });
    }

    public getLocator(id: string): LocatorCount {
        const locator = this.locatorHandles.get(id);
        if (locator) {
            return locator;
        }
        throw new Error(`No locator handle found with "${id}".`);
    }
}

/*
 * Pagestack's last item should be the current active page and the first item should be the lastly added page
 * */
type IndexedContext = {
    c: BrowserContext;
    id: Uuid;
    traceFile: string;
    pageStack: IndexedPage[];
    options?: Record<string, unknown>;
};

export type IndexedPage = {
    p: Page;
    id: Uuid;
    timestamp: number;
    pageErrors: Error[];
    consoleMessages: ConsoleMessage[];
};

type Uuid = string;

/*
 * contextStacks's last item should be the current active page and the first item should be the lastly added page.
 * User opened items should get pushed and page opened unshifted
 * */
export class BrowserState {
    constructor(browserAndConfs: BrowserAndConfs) {
        this.name = browserAndConfs.browserType;
        this.browser = browserAndConfs.browser;
        this.headless = browserAndConfs.headless;
        this._contextStack = [];
        this.id = `browser=${uuidv4()}`;
    }
    private _contextStack: IndexedContext[];
    browser: Browser | null;
    name?: string;
    id: Uuid;
    headless: boolean;

    public async close(): Promise<void> {
        for (const context of this.contextStack) {
            const traceFile = context.traceFile;
            if (traceFile) {
                await context.c.tracing.stop({ path: traceFile });
            }
            await context.c.close();
        }
        this._contextStack = [];
        if (this.browser === null) {
            return;
        }
        await this.browser.close();
    }

    public async getOrCreateActiveContext(defaultTimeout: number): Promise<IIndexedContext> {
        if (this.context) {
            return { context: this.context, newContext: false };
        } else if (this.browser === null) {
            throw new Error('Invalid persistent context browser without context');
        } else {
            const activeBrowser = this.browser;
            const context = await _newBrowserContext(activeBrowser, defaultTimeout, '');
            this.pushContext(context);
            return { context: context, newContext: true };
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
    public popPage(): IndexedPage | undefined {
        const pageStack = this.context?.pageStack || [];
        return pageStack.pop();
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
    openBrowsers.popBrowser();
    await currentBrowser.close();
    return stringResponse(currentBrowser.id, 'Closed browser');
}

export async function closeAllBrowsers(openBrowsers: PlaywrightState): Promise<Response.Empty> {
    await openBrowsers.closeAll();
    return emptyWithLog('Closed all browsers');
}

export async function closeContext(openBrowsers: PlaywrightState): Promise<Response.Empty> {
    const activeBrowser = openBrowsers.getActiveBrowser();
    const traceFile = openBrowsers.getTraceFile();
    if (traceFile) {
        await openBrowsers.getActiveContext()?.tracing.stop({ path: traceFile });
    }
    await openBrowsers.getActiveContext()?.close();
    activeBrowser.popContext();
    return emptyWithLog('Successfully closed Context');
}

export async function closePage(openBrowsers: PlaywrightState): Promise<Response.PageReportResponse> {
    const activeBrowser = openBrowsers.getActiveBrowser();
    const closedPage = activeBrowser.popPage();
    if (!closedPage) throw new Error('No open page');
    await closedPage.p.close();
    return pageReportResponse('Successfully closed Page', closedPage);
}

export async function newPage(request: Request.Url, openBrowsers: PlaywrightState): Promise<Response.NewPageResponse> {
    const defaultTimeout = request.getDefaulttimeout();
    const browserState = await openBrowsers.getOrCreateActiveBrowser(null, defaultTimeout);
    const newBrowser = browserState.newBrowser;
    const context = await browserState.browser.getOrCreateActiveContext(defaultTimeout);

    const page = await _newPage(context.context);
    const videoPath = await page.p.video()?.path();
    logger.info('Video path: ' + videoPath);
    browserState.browser.pushPage(page);
    const url = request.getUrl() || 'about:blank';
    try {
        await page.p.goto(url);
        const response = new Response.NewPageResponse();
        response.setBody(page.id);
        response.setLog(`Successfully initialized new page object and opened url: ${url}`);
        const video = { video_path: videoPath || null, contextUuid: context.context.id };
        response.setVideo(JSON.stringify(video));
        response.setNewbrowser(newBrowser);
        response.setNewcontext(context.newContext);
        return response;
    } catch (e) {
        browserState.browser.popPage();
        throw e;
    }
}

export async function newContext(
    request: Request.Context,
    openBrowsers: PlaywrightState,
): Promise<Response.NewContextResponse> {
    const hideRfBrowser = request.getHiderfbrowser();
    const options = JSON.parse(request.getRawoptions());
    const defaultTimeout = request.getDefaulttimeout();
    const browserState = await openBrowsers.getOrCreateActiveBrowser(options.defaultBrowserType, defaultTimeout);
    const traceFile = request.getTracefile();
    logger.info(`Trace file: ${traceFile}`);

    if (browserState.browser.browser === null) {
        throw new Error('Trying to create a new context when a persistentContext is active');
    }
    const context = await _newBrowserContext(
        browserState.browser.browser,
        defaultTimeout,
        traceFile,
        options,
        hideRfBrowser,
    );

    return _finishContextResponse(context, browserState, traceFile, options);
}

function _finishContextResponse(
    context: IndexedContext,
    browserState: IBrowserState,
    traceFile: string,
    options: Record<string, unknown>,
) {
    browserState.browser.pushContext(context);
    const response = new Response.NewContextResponse();
    response.setId(context.id);
    if (traceFile) {
        response.setLog(`Successfully created context and trace file will be saved to: ${traceFile}`);
        options.trace = { screenshots: true, snapshots: true };
    } else {
        response.setLog('Successfully created context. ');
    }
    response.setContextoptions(JSON.stringify(options));
    response.setNewbrowser(browserState.newBrowser);
    return response;
}

export async function newBrowser(request: Request.Browser, openBrowsers: PlaywrightState): Promise<Response.String> {
    const browserType = request.getBrowser() as 'chromium' | 'firefox' | 'webkit';
    const options = JSON.parse(request.getRawoptions()) as Record<string, unknown>;
    const browserAndConfs = await _newBrowser(
        browserType,
        options['headless'] as boolean,
        options['timeout'] as number,
        options,
    );
    const browserState = openBrowsers.addBrowser(browserAndConfs);
    return stringResponse(browserState.id, 'Successfully created browser with options: ' + JSON.stringify(options));
}

export async function newPersistentContext(
    request: Request.PersistentContext,
    openBrowsers: PlaywrightState,
): Promise<Response.NewContextResponse> {
    const traceFile = request.getTracefile();
    const timeout = request.getDefaulttimeout();
    const options = JSON.parse(request.getRawoptions()) as Record<string, unknown>;

    const userDataDir = options?.userDataDir as string;

    let browser;
    if (options.browser === 'chromium') {
        browser = chromium;
    } else if (options.browser === 'firefox') {
        browser = firefox;
    } else {
        throw new Error('Invalid browserType for New Persistent Context');
    }

    const persistentContext = await browser.launchPersistentContext(userDataDir, options);

    const browserAndConfs = {
        browserType: options.browser,
        browser: null,
        headless: options?.headless || true,
    } as BrowserAndConfs;
    openBrowsers.addBrowser(browserAndConfs);

    const browserState = await openBrowsers.getOrCreateActiveBrowser(null, timeout);
    if (browserState.newBrowser === true) {
        throw new Error('A new browser was created in error while trying to create a persistent context');
    }

    if (!options.hideRfBrowser) {
        await persistentContext.addInitScript(function () {
            window.__SET_RFBROWSER_STATE__ = function (state: any) {
                window.__RFBROWSER__ = state;
                return state;
            };
        });
    }
    persistentContext.setDefaultTimeout(timeout);
    const indexedContext = {
        id: `context=${uuidv4()}`,
        c: persistentContext,
        pageStack: [] as IndexedPage[],
        options: options,
        traceFile: traceFile,
    };
    if (traceFile) {
        logger.info('Tracing enabled with: { screenshots: true, snapshots: true }');
        persistentContext.tracing.start({ screenshots: true, snapshots: true });
    }

    return _finishContextResponse(indexedContext, browserState, traceFile, options);
}

export async function connectToBrowser(
    request: Request.ConnectBrowser,
    openBrowsers: PlaywrightState,
): Promise<Response.String> {
    const browserType = request.getBrowser();
    const url = request.getUrl();
    const browserAndConfs = await _connectBrowser(browserType, url);
    const browserState = openBrowsers.addBrowser(browserAndConfs);
    return stringResponse(browserState.id, 'Successfully connected to browser');
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
    const page = browserState.page;
    if (page !== undefined) {
        await _switchPage(page.id, browserState);
    }
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

export async function saveStorageState(
    request: Request.FilePath,
    browserState?: BrowserState,
): Promise<Response.Empty> {
    exists(browserState, "Tried to save storage state but browser wasn't open");
    const context = browserState.context;
    exists(context, 'Tried to save storage state butno context was open');
    const stateFile = request.getPath();
    await context.c.storageState({ path: stateFile });
    return emptyWithLog('Current context state is saved to: ' + stateFile);
}
