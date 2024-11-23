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
import {
    Browser,
    BrowserContext,
    BrowserServer,
    BrowserType,
    Download,
    Locator,
    Page,
    chromium,
    firefox,
    webkit,
} from 'playwright';
import { v4 as uuidv4 } from 'uuid';

import { Request, Response } from './generated/playwright_pb';
import {
    emptyWithLog,
    getConsoleLogResponse,
    getErrorMessagesResponse,
    jsonResponse,
    keywordsResponse,
    pageReportResponse,
    stringResponse,
} from './response-util';
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

export interface TimedError {
    name: string;
    message: string;
    stack?: string;
    time: Date;
}

export interface TimedConsoleMessage {
    type: string;
    text: string;
    location: { url: string; lineNumber: number; columnNumber: number };
    time: Date;
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
    logger.info(`Initializing extension: ${request.getPath()}`);
    const extension: Record<string, (...args: unknown[]) => unknown> = eval('require')(request.getPath());
    state.extensions.push(extension);
    const kws = Object.keys(extension).filter((key) => extension[key] instanceof Function && !key.startsWith('__'));
    logger.info(`Adding ${kws.length} keywords from JS Extension`);
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

const getArgumentNamesFromJavascriptKeyword = (keyword: CallableFunction) =>
    extractArgumentsStringFromJavascript(keyword.toString())
        .split(',')
        .map((s) => s.trim().match(/^\w*/)?.[0] || s.trim());

export async function extensionKeywordCall(
    request: Request.KeywordCall,
    call: ServerWritableStream<Request.KeywordCall, Response.Json>,
    state: PlaywrightState,
): Promise<Response.Json> {
    const keywordName = request.getName();
    const args = JSON.parse(request.getArguments()) as { arguments: [string, unknown][] };
    const extension = state.extensions.find((extension) => Object.keys(extension).includes(keywordName));
    if (!extension) throw Error(`Could not find keyword ${keywordName}`);
    const keyword = extension[keywordName];
    const namedArguments = Object.fromEntries(args['arguments']);
    const apiArguments = new Map();
    apiArguments.set('page', state.getActivePage());
    apiArguments.set('context', state.getActiveContext());
    apiArguments.set('browser', state.getActiveBrowser()?.browser);
    apiArguments.set('logger', (msg: string) => call.write(jsonResponse(JSON.stringify(''), msg)));
    apiArguments.set('playwright', playwright);
    const functionArguments = getArgumentNamesFromJavascriptKeyword(keyword).map(
        (argName) => apiArguments.get(argName) || namedArguments[argName],
    );
    const result = await keyword(...functionArguments);
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
    timeout: number | undefined,
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

async function _launchBrowserServer(
    browserType: 'chromium' | 'firefox' | 'webkit',
    headless: boolean,
    timeout: number | undefined,
    options?: Record<string, unknown>,
): Promise<BrowserServer> {
    let browser: BrowserServer;
    const launchOptions: playwright.LaunchOptions = { ...options, headless, timeout };
    if (browserType === 'firefox') {
        browser = await firefox.launchServer(launchOptions);
    } else if (browserType === 'chromium') {
        browser = await chromium.launchServer(launchOptions);
    } else if (browserType === 'webkit') {
        browser = await webkit.launchServer(launchOptions);
    } else {
        throw new Error('unsupported browser');
    }
    return browser;
}

async function _connectBrowser(browserName: string, url: string, connectCDP: boolean): Promise<BrowserAndConfs> {
    logger.info(`Connecting to browser: ${browserName} at ${url} via ${connectCDP ? 'CDP' : 'WebSocket'}`);
    let browserType: BrowserType;
    switch (browserName) {
        case 'firefox':
            browserType = firefox;
            break;
        case 'webkit':
            browserType = webkit;
            break;
        default:
            browserType = chromium;
            browserName = 'chromium';
            break;
    }
    const browser = connectCDP ? await browserType.connectOverCDP(url) : await browserType.connect(url);
    return {
        browser,
        browserType: browserName as 'chromium' | 'firefox' | 'webkit',
        headless: false,
    };
}

async function _newBrowserContext(
    browser: Browser,
    defaultTimeout: number | undefined,
    traceFile: string,
    options?: Record<string, unknown>,
): Promise<IndexedContext> {
    const context = await browser.newContext(options);
    if (defaultTimeout) {
        context.setDefaultTimeout(defaultTimeout);
    }
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

function indexedPage(newPage: Page): IndexedPage {
    const timestamp = new Date().getTime() / 1000;
    const pageErrors: TimedError[] = [];
    const consoleMessages: TimedConsoleMessage[] = [];
    newPage.on('pageerror', (error) => {
        const timedError = {
            name: error.name,
            message: error.message,
            stack: error.stack,
            time: new Date(),
        };
        pageErrors.push(timedError);
    });
    newPage.on('console', (message) => {
        const timedMessage = {
            type: message.type(),
            text: message.text(),
            location: message.location(),
            time: new Date(),
        };
        consoleMessages.push(timedMessage);
    });
    return {
        id: `page=${uuidv4()}`,
        p: newPage,
        timestamp,
        pageErrors,
        errorIndex: 0,
        consoleMessages,
        consoleIndex: 0,
        activeDownloads: new Map(),
        coverage: undefined,
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
        this.extensions = [];
        this.browserServer = [];
    }
    extensions: Record<string, (...args: unknown[]) => unknown>[];
    private browserStack: BrowserState[];
    private browserServer: BrowserServer[];
    get activeBrowser() {
        return lastItem(this.browserStack);
    }
    public getActiveBrowser = (): BrowserState => {
        const currentBrowser = this.activeBrowser;
        if (currentBrowser === undefined) {
            throw new Error('Browser has been closed.');
        }
        return currentBrowser;
    };

    public switchTo = (id: Uuid): BrowserState => {
        const browser = this.browserStack.find((b) => b.id === id);
        this.browserStack = this.browserStack.filter((b) => b.id !== id);
        exists(browser, `No browser for id '${id}'`);
        this.browserStack.push(browser);
        return this.getActiveBrowser();
    };

    public async getOrCreateActiveBrowser(
        browserType: 'chromium' | 'firefox' | 'webkit' | null,
        timeout: number | undefined,
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
            try {
                await browser.close();
            } catch (e) {} // eslint-disable-line
        }
        this.browserStack = [];
    }

    public async closeAllServers(): Promise<void> {
        const servers = this.browserServer;
        for (const server of servers) {
            try {
                await server.close();
            } catch (e) {} // eslint-disable-line
        }
        this.browserServer = [];
    }

    public getBrowserServer(wsEndpoint: string): BrowserServer | undefined {
        return this.browserServer.find((server) => server.wsEndpoint() === wsEndpoint);
    }

    public async closeServer(selectedServer: BrowserServer): Promise<void> {
        if (!this.browserServer.includes(selectedServer)) {
            throw new Error(`BrowserServer not found.`);
        }
        this.browserServer.splice(this.browserServer.indexOf(selectedServer), 1);
        await selectedServer.close();
    }

    public async getCatalog() {
        const pageToContents = async (page: IndexedPage) => {
            let title = null;
            const titlePromise = page.p.title();
            const titleTimeout = new Promise((_r, rej) => setTimeout(() => rej(null), 350));
            try {
                title = await Promise.race([titlePromise, titleTimeout]);
            } catch (e) {} // eslint-disable-line
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
        const adding_browser = browserAndConfs.browser;
        logger.info(`Adding browser to stack: ${browserAndConfs.browserType}, version: ${adding_browser?.version()}`);
        let browserState = this.browserStack.find((b) => b.browser === adding_browser);
        if (browserState !== undefined) {
            this.browserStack = this.browserStack.filter((b) => b.browser !== adding_browser);
        } else {
            browserState = new BrowserState(browserAndConfs);
        }
        const browserContexts = browserState.browser?.contexts();
        if (browserContexts !== undefined) {
            logger.info(`Adding ${browserContexts.length} contexts to browser`);
            for (const context of browserContexts) {
                const indexedPages = context.pages().map((page) => indexedPage(page));
                logger.info(`Adding ${indexedPages.length} pages to context`);
                const indexedContext = {
                    id: `context=${uuidv4()}`,
                    c: context,
                    pageStack: indexedPages,
                    options: {},
                    traceFile: '',
                };
                indexedContext.c.on('page', async (page) => {
                    indexedContext.pageStack.unshift(await _newPage(indexedContext, page));
                });
                browserState?.pushContext(indexedContext);
            }
        }
        this.browserStack.push(browserState);
        return browserState;
    }

    public addBrowserServer(browserServer: BrowserServer): void {
        this.browserServer.push(browserServer);
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
    public getActivePageId = (): string | undefined => {
        return this.activeBrowser?.page?.id;
    };
    public getCoverageOptions(): CoverageOptions | undefined {
        return this.activeBrowser?.page?.coverage;
    }
    public addCoverageOptions = (coverage: CoverageOptions): void => {
        if (this.activeBrowser?.page) {
            this.activeBrowser.page.coverage = coverage;
        }
    };
}

class LocatorCache {
    private cache: Map<string, playwright.Locator>;

    constructor() {
        this.cache = new Map<string, playwright.Locator>();
    }

    public add(key: string, locator: playwright.Locator): void {
        this.cache.set(key, locator);
    }

    public get(key: string): playwright.Locator | undefined {
        return this.cache.get(key);
    }

    public delete(key: string): boolean {
        return this.cache.delete(key);
    }

    public has(key: string): boolean {
        return this.cache.has(key);
    }

    public clear(): void {
        this.cache.clear();
    }
}

export const locatorCache = new LocatorCache();

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

export type DownloadInfo = {
    downloadObject: Download;
    saveAs: string;
    suggestedFilename: string;
};

export type CoverageOptions = {
    type: string;
    directory: string;
    folderPrefix: string;
    configFile: string;
    raw: boolean;
};

export type IndexedPage = {
    p: Page;
    id: Uuid;
    timestamp: number;
    pageErrors: TimedError[];
    errorIndex: number;
    consoleMessages: TimedConsoleMessage[];
    consoleIndex: number;
    activeDownloads: Map<Uuid, DownloadInfo>;
    coverage: CoverageOptions | undefined;
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

    public async getOrCreateActiveContext(defaultTimeout: number | undefined): Promise<IIndexedContext> {
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
            if (!newContext.c) {
                throw new Error('Tried to switch to context, which did not exist anymore.');
            }
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
            if (!newPage.p) {
                throw new Error('Tried to switch to page, which did not exist anymore.');
            }
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

export async function closeBrowserServer(
    request: Request.ConnectBrowser,
    openBrowsers: PlaywrightState,
): Promise<Response.Empty> {
    const wsEndpoint = request.getUrl();
    if (wsEndpoint === 'ALL') {
        await openBrowsers.closeAllServers();
        return emptyWithLog('Closed all browser servers');
    }
    const browserServer = openBrowsers.getBrowserServer(wsEndpoint);
    if (!browserServer) throw new Error(`BrowserServer with endpoint ${wsEndpoint} not found.`);
    openBrowsers.closeServer(browserServer);
    return emptyWithLog(`Closed browser server with endpoint: ${wsEndpoint}`);
}

export async function closeBrowser(openBrowsers: PlaywrightState): Promise<Response.String> {
    const currentBrowser = openBrowsers.activeBrowser;
    if (currentBrowser === undefined) {
        return stringResponse('no-browser', 'No browser open, doing nothing');
    }
    openBrowsers.popBrowser();
    try {
        await currentBrowser.close();
        return stringResponse(currentBrowser.id, 'Closed browser');
    } catch (e) { // eslint-disable-line
        return stringResponse('', `Browser ${currentBrowser.id} was already closed`);
    }
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

export async function closePage(
    request: Request.ClosePage,
    openBrowsers: PlaywrightState,
): Promise<Response.PageReportResponse> {
    const activeBrowser = openBrowsers.getActiveBrowser();
    const closedPage = activeBrowser.popPage();
    const unload = request.getRunbeforeunload();
    if (!closedPage) throw new Error('No open page');
    logger.info(`Closing page with runBeforeUnload ${unload}`);
    await closedPage.p.close({ runBeforeUnload: unload });
    return pageReportResponse(`Successfully closed Page with runBeforeUnload ${unload}`, closedPage);
}

export async function newPage(
    request: Request.UrlOptions,
    openBrowsers: PlaywrightState,
): Promise<Response.NewPageResponse> {
    const defaultTimeout = request.getUrl()?.getDefaulttimeout();
    const waitUntil = <'load' | 'domcontentloaded' | 'networkidle' | 'commit'>request.getWaituntil();
    const browserState = await openBrowsers.getOrCreateActiveBrowser(null, defaultTimeout);
    const newBrowser = browserState.newBrowser;
    const context = await browserState.browser.getOrCreateActiveContext(defaultTimeout);

    const page = await _newPage(context.context);
    let videoPath: string | undefined = '';
    try {
        videoPath = await page.p.video()?.path();
    } catch (e) { // eslint-disable-line
        logger.info('Suppress video().path() error');
    }
    logger.info('Video path: ' + videoPath);
    browserState.browser.pushPage(page);
    const url = request.getUrl()?.getUrl() || 'about:blank';
    try {
        const goToOptions: {
            timeout?: number;
            waitUntil?: 'load' | 'domcontentloaded' | 'networkidle' | 'commit';
        } = { timeout: defaultTimeout };
        if (waitUntil) {
            goToOptions.waitUntil = waitUntil;
        }
        await page.p.goto(url, goToOptions);
        const response = new Response.NewPageResponse();
        response.setBody(page.id);
        response.setLog(`Successfully initialized new page object and opened url: ${url}`);
        const video = { video_path: videoPath || null, contextUuid: context.context.id };
        response.setVideo(JSON.stringify(video));
        response.setNewbrowser(newBrowser);
        response.setNewcontext(context.newContext);
        return response;
    } catch (e) {
        browserState.browser.popPage()?.p.close();
        throw e;
    }
}

export async function newContext(
    request: Request.Context,
    openBrowsers: PlaywrightState,
): Promise<Response.NewContextResponse> {
    const options = JSON.parse(request.getRawoptions());
    logger.info('Creating new context with options: ' + JSON.stringify(options));
    const defaultTimeout = request.getDefaulttimeout();
    const browserState = await openBrowsers.getOrCreateActiveBrowser(options.defaultBrowserType, defaultTimeout);
    const traceFile = request.getTracefile();
    logger.info(`Trace file: ${traceFile}`);

    if (browserState.browser.browser === null) {
        throw new Error('Trying to create a new context when a persistentContext is active');
    }
    const context = await _newBrowserContext(browserState.browser.browser, defaultTimeout, traceFile, options);

    return await _finishContextResponse(context, browserState, traceFile, options);
}

async function _finishContextResponse(
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

export async function launchBrowserServer(
    request: Request.Browser,
    openBrowsers: PlaywrightState,
): Promise<Response.String> {
    const browserType = request.getBrowser() as 'chromium' | 'firefox' | 'webkit';
    const options = JSON.parse(request.getRawoptions()) as Record<string, unknown>;
    logger.info(`Launching browser server: ${browserType}`);
    logger.info('Launching browser server with options: ' + JSON.stringify(options));
    const browserServer = await _launchBrowserServer(
        browserType,
        options['headless'] as boolean,
        options['timeout'] as number,
        options,
    );
    logger.info(`Browser server launched. Endpoint: ${browserServer.wsEndpoint()}`);
    openBrowsers.addBrowserServer(browserServer);
    return stringResponse(
        browserServer.wsEndpoint(),
        'Successfully created browser server with options: ' + JSON.stringify(options),
    );
}

export async function newPersistentContext(
    request: Request.PersistentContext,
    openBrowsers: PlaywrightState,
): Promise<Response.NewContextResponse> {
    const traceFile = request.getTracefile();
    const timeout = request.getDefaulttimeout();
    const options = JSON.parse(request.getRawoptions()) as Record<string, unknown>;

    const userDataDir = options?.userDataDir as string;
    let browser: BrowserType;
    switch (options.defaultBrowserType || options.browser) {
        case 'chromium':
            browser = chromium;
            break;
        case 'firefox':
            browser = firefox;
            break;
        case 'webkit':
            browser = webkit;
            break;
        default:
            throw new Error(`"${options.browser} is an unsupported browser."`);
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

    persistentContext.setDefaultTimeout(timeout);
    const indexedContext = {
        id: `context=${uuidv4()}`,
        c: persistentContext,
        pageStack: [] as IndexedPage[],
        options: options,
        traceFile: traceFile,
    };
    indexedContext.c.on('page', async (page) => {
        indexedContext.pageStack.unshift(await _newPage(indexedContext, page));
    });
    if (traceFile) {
        logger.info('Tracing enabled with: { screenshots: true, snapshots: true }');
        persistentContext.tracing.start({ screenshots: true, snapshots: true });
    }

    const page = indexedContext.c.pages()[0];
    indexedContext.pageStack.unshift(await _newPage(indexedContext, page));

    browserState.browser.pushContext(indexedContext);
    const response = new Response.NewPersistentContextResponse();
    response.setId(indexedContext.id);
    if (traceFile) {
        response.setLog(`Successfully created context and trace file will be saved to: ${traceFile}`);
        options.trace = { screenshots: true, snapshots: true };
    } else {
        response.setLog('Successfully created context. ');
    }
    response.setContextoptions(JSON.stringify(options));
    response.setNewbrowser(browserState.newBrowser);
    const currentBrowser = openBrowsers.activeBrowser;
    const currentPage = indexedContext.pageStack[0];
    const videoPath = await currentPage.p.video()?.path();
    const video = { video_path: videoPath || null, contextUuid: indexedContext.id };
    response.setVideo(JSON.stringify(video));
    response.setPageid(currentPage.id);
    response.setBrowserid(currentBrowser?.id || '');
    return response;
}

export async function connectToBrowser(
    request: Request.ConnectBrowser,
    openBrowsers: PlaywrightState,
): Promise<Response.String> {
    const browserType = request.getBrowser();
    const url = request.getUrl();
    const connectCDP = request.getConnectcdp();
    const browserAndConfs = await _connectBrowser(browserType, url, connectCDP);
    const browserState = openBrowsers.addBrowser(browserAndConfs);
    return stringResponse(browserState.id, 'Successfully connected to browser');
}

async function _switchPage(id: Uuid, browserState: BrowserState) {
    const context = browserState.context?.c;
    if (!context) throw new Error('Tried to switch page, no open context');
    const pages = browserState.context?.pageStack;
    logger.info('Changing current active page: ' + id);
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
        browserState.page?.p.bringToFront();
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
    return stringResponse(previous, 'Successfully changed active page: ' + id);
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
        }
    } else {
        await _switchContext(id, browserState);
    }
    const page = browserState.page;
    if (page !== undefined) {
        await _switchPage(page.id, browserState);
    }
    return stringResponse(
        previous,
        id === 'CURRENT' ? 'Returned active context id: ' + id : 'Successfully changed active context: ' + id,
    );
}

export async function switchBrowser(request: Request.Index, openBrowsers: PlaywrightState): Promise<Response.String> {
    const id = request.getIndex();
    const previous = openBrowsers.activeBrowser;
    if (id !== 'CURRENT') {
        openBrowsers.switchTo(id);
    }
    openBrowsers.getActivePage()?.bringToFront();
    return stringResponse(
        previous?.id || 'NO BROWSER OPEN',
        id === 'CURRENT' ? 'Returned active browser id. ' + id : 'Successfully changed active browser: ' + id,
    );
}

export async function getBrowserCatalog(openBrowsers: PlaywrightState): Promise<Response.Json> {
    return jsonResponse(JSON.stringify(await openBrowsers.getCatalog()), 'Catalog received');
}

export async function getConsoleLog(request: Request.Bool, openBrowsers: PlaywrightState): Promise<Response.Json> {
    const activePage = openBrowsers.getActiveBrowser().page;
    if (!activePage) throw new Error('No open page');
    return getConsoleLogResponse(activePage, request.getValue(), 'Console log received');
}

export async function getErrorMessages(request: Request.Bool, openBrowsers: PlaywrightState): Promise<Response.Json> {
    const activePage = openBrowsers.getActiveBrowser().page;
    if (!activePage) throw new Error('No open page');
    return getErrorMessagesResponse(activePage, request.getValue(), 'Error messages received');
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
