/// <reference types="jest" />

import { beforeEach, describe, expect, it } from '@jest/globals';
import type { Browser } from 'playwright';

jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

jest.mock('uuid', () => ({
    v4: jest.fn().mockReturnValue('test-uuid'),
}));

import {
    BrowserState,
    closeAllBrowsers,
    closeBrowser,
    closeBrowserServer,
    closeContext,
    extensionKeywordCall,
    locatorCache,
    newPage,
    PlaywrightState,
    removeFailedPage,
} from '../playwright-state';

function makeBrowserState(id: string): BrowserState {
    const state = new BrowserState({
        browser: null,
        name: 'chromium',
        headless: true,
    });
    state.id = id;
    return state;
}

function makeIndexedPage(id: string) {
    return {
        p: {} as any,
        id,
        timestamp: Date.now() / 1000,
        pageErrors: [],
        errorIndex: 0,
        consoleMessages: [],
        consoleIndex: 0,
        activeDownloads: new Map(),
        coverage: undefined,
    } as any;
}

function attachSingleContextWithPage(browserState: BrowserState, pageId = 'page=1') {
    const context = {
        c: {} as any,
        id: 'context=1',
        traceFile: '',
        pageStack: [makeIndexedPage(pageId)],
        options: {},
    } as any;
    browserState.pushContext(context);
}

describe('PlaywrightState', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        locatorCache.clear();
    });

    it('throws from getActiveBrowser when browser stack is empty', () => {
        const state = new PlaywrightState();

        expect(() => state.getActiveBrowser()).toThrow('No Browser is open but needed for this operation.');
    });

    it('switches active browser by id', () => {
        const state = new PlaywrightState();
        const first = makeBrowserState('browser=first');
        const second = makeBrowserState('browser=second');
        state.browserStack.push(first, second);

        const active = state.switchTo('browser=first');

        expect(active.id).toBe('browser=first');
        expect(state.activeBrowser?.id).toBe('browser=first');
    });

    it('throws when switchTo receives unknown browser id', () => {
        const state = new PlaywrightState();
        state.browserStack.push(makeBrowserState('browser=known'));

        expect(() => state.switchTo('browser=missing')).toThrow("No browser for id 'browser=missing'");
    });

    it('returns active context page and id from browser stack', () => {
        const state = new PlaywrightState();
        const browserState = makeBrowserState('browser=with-page');
        attachSingleContextWithPage(browserState, 'page=active');
        state.browserStack.push(browserState);

        expect(state.getActiveContext()).toBeDefined();
        expect(state.getActivePage()).toBeDefined();
        expect(state.getActivePageId()).toBe('page=active');
    });

    it('adds coverage options to the active page', () => {
        const state = new PlaywrightState();
        const browserState = makeBrowserState('browser=coverage');
        attachSingleContextWithPage(browserState, 'page=coverage');
        state.browserStack.push(browserState);

        const coverage = {
            type: 'javascript',
            directory: 'coverage/raw',
            configFile: 'config.json',
            raw: true,
        };

        state.addCoverageOptions(coverage);

        expect(state.getCoverageOptions()).toEqual(coverage);
    });

    it('finds and closes a registered browser server', async () => {
        const state = new PlaywrightState();
        const close = jest.fn().mockResolvedValue(undefined);
        const server = {
            wsEndpoint: jest.fn().mockReturnValue('ws://127.0.0.1:1234/playwright'),
            close,
        } as any;
        state.addBrowserServer(server);

        expect(state.getBrowserServer('ws://127.0.0.1:1234/playwright')).toBe(server);

        await state.closeServer(server);

        expect(close).toHaveBeenCalledTimes(1);
        expect(state.getBrowserServer('ws://127.0.0.1:1234/playwright')).toBeUndefined();
    });

    it('throws when closing an unknown browser server', async () => {
        expect.assertions(1);
        const state = new PlaywrightState();
        const server = {
            wsEndpoint: jest.fn().mockReturnValue('ws://127.0.0.1:4321/playwright'),
            close: jest.fn().mockResolvedValue(undefined),
        } as any;

        await expect(state.closeServer(server)).rejects.toThrow('BrowserServer not found.');
    });
});

describe('locatorCache', () => {
    beforeEach(() => {
        locatorCache.clear();
    });

    it('adds gets deletes and clears locators', () => {
        const locator = { id: 'loc' } as any;

        locatorCache.add('first', locator);
        expect(locatorCache.has('first')).toBe(true);
        expect(locatorCache.get('first')).toBe(locator);

        expect(locatorCache.delete('first')).toBe(true);
        expect(locatorCache.has('first')).toBe(false);

        locatorCache.add('second', locator);
        locatorCache.clear();
        expect(locatorCache.has('second')).toBe(false);
    });
});

describe('BrowserState', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('copies options from previous context with same browser context object', () => {
        const browser = makeBrowserState('browser=context-options');
        const sharedContextObject = {} as any;
        const first = {
            c: sharedContextObject,
            id: 'context=first',
            traceFile: '',
            pageStack: [],
            options: { locale: 'fi-FI' },
        } as any;
        const second = {
            c: sharedContextObject,
            id: 'context=second',
            traceFile: '',
            pageStack: [],
            options: undefined,
        } as any;

        browser.pushContext(first);
        browser.pushContext(second);

        expect(browser.contextStack).toHaveLength(1);
        expect(browser.context?.id).toBe('context=second');
        expect(browser.context?.options).toEqual({ locale: 'fi-FI' });
    });

    it('activates page and brings it to front', async () => {
        const browser = makeBrowserState('browser=activate-page');
        const bringToFront = jest.fn().mockResolvedValue(undefined);
        const page = {
            p: { bringToFront },
            id: 'page=new',
            timestamp: Date.now() / 1000,
            pageErrors: [],
            errorIndex: 0,
            consoleMessages: [],
            consoleIndex: 0,
            activeDownloads: new Map(),
            coverage: undefined,
        } as any;
        const context = {
            c: {} as any,
            id: 'context=1',
            traceFile: '',
            pageStack: [],
            options: {},
        } as any;
        browser.pushContext(context);

        await browser.activatePage(page);

        expect(browser.page?.id).toBe('page=new');
        expect(bringToFront).toHaveBeenCalledTimes(1);
    });

    it('popPage returns the active page from current context', () => {
        const browser = makeBrowserState('browser=pop-page');
        const context = {
            c: {} as any,
            id: 'context=1',
            traceFile: '',
            pageStack: [makeIndexedPage('page=1'), makeIndexedPage('page=2')],
            options: {},
        } as any;
        browser.pushContext(context);

        const popped = browser.popPage();

        expect(popped?.id).toBe('page=2');
        expect(browser.page?.id).toBe('page=1');
    });

    it('closes traces contexts and browser on close', async () => {
        const tracingStop = jest.fn().mockResolvedValue(undefined);
        const contextClose = jest.fn().mockResolvedValue(undefined);
        const browserClose = jest.fn().mockResolvedValue(undefined);
        const browserMock = {
            close: browserClose,
            contexts: jest.fn().mockReturnValue([]),
        } as unknown as Browser;
        const browser = new BrowserState({
            browser: browserMock,
            name: 'chromium',
            headless: true,
        });
        browser.pushContext({
            c: {
                tracing: { stop: tracingStop },
                close: contextClose,
            } as any,
            id: 'context=1',
            traceFile: '/tmp/trace.zip',
            pageStack: [],
            options: {},
        });

        await browser.close();

        expect(tracingStop).toHaveBeenCalledWith({ path: '/tmp/trace.zip' });
        expect(contextClose).toHaveBeenCalledTimes(1);
        expect(browserClose).toHaveBeenCalledTimes(1);
        expect(browser.contextStack).toHaveLength(0);
    });
});

describe('close helpers', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('closeBrowser returns no-browser when stack is empty', async () => {
        const state = new PlaywrightState();

        const response = await closeBrowser(state);

        expect(response.body).toBe('no-browser');
    });

    it('closeBrowser closes the active browser and returns its id', async () => {
        const state = new PlaywrightState();
        const close = jest.fn().mockResolvedValue(undefined);
        state.browserStack.push({ id: 'browser=to-close', close } as any);

        const response = await closeBrowser(state);

        expect(close).toHaveBeenCalledTimes(1);
        expect(response.body).toBe('browser=to-close');
    });

    it('closeAllBrowsers delegates to PlaywrightState.closeAll', async () => {
        const state = new PlaywrightState();
        const spy = jest.spyOn(state, 'closeAll').mockResolvedValue(undefined);

        const response = await closeAllBrowsers(state);

        expect(spy).toHaveBeenCalledTimes(1);
        expect(response.log).toContain('Closed all browsers');
    });

    it('closeBrowserServer closes all servers when endpoint is ALL', async () => {
        const state = new PlaywrightState();
        const spy = jest.spyOn(state, 'closeAllServers').mockResolvedValue(undefined);

        const response = await closeBrowserServer({ url: 'ALL' } as any, state);

        expect(spy).toHaveBeenCalledTimes(1);
        expect(response.log).toContain('Closed all browser servers');
    });

    it('closeBrowserServer throws for unknown endpoint', async () => {
        expect.assertions(1);
        const state = new PlaywrightState();

        await expect(closeBrowserServer({ url: 'ws://missing' } as any, state)).rejects.toThrow(
            'BrowserServer with endpoint ws://missing not found.',
        );
    });
});

function makePlaywrightPage(goto: jest.Mock) {
    return {
        on: jest.fn(),
        video: jest.fn().mockReturnValue(null),
        goto,
        close: jest.fn().mockResolvedValue(undefined),
        isClosed: jest.fn().mockReturnValue(false),
    };
}

function stateWithOpenPage(openPageId = 'page=open') {
    const state = new PlaywrightState();
    const browser = makeBrowserState('browser=1');
    const openPage = makeIndexedPage(openPageId);
    const context = {
        c: { newPage: jest.fn() },
        id: 'context=1',
        traceFile: '',
        pageStack: [openPage],
        options: {},
    } as any;
    browser.pushContext(context);
    state.browserStack.push(browser);
    return { state, browser, context, openPage };
}

const navigationTimeout = new Error('page.goto: Timeout 5000ms exceeded');

function newPageThatFailsNavigation(context: any) {
    const failedPage = makePlaywrightPage(jest.fn().mockRejectedValue(navigationTimeout));
    context.c.newPage.mockResolvedValueOnce(failedPage);
    return failedPage;
}

function newPageRequest(failedPageToken = 'token-1') {
    return { url: { url: 'http://slow', defaultTimeout: 5000 }, waitUntil: '', failedPageToken } as any;
}

async function failNewPage(state: PlaywrightState, context: any, failedPageToken = 'token-1') {
    const failedPage = newPageThatFailsNavigation(context);
    await newPage(newPageRequest(failedPageToken), state).catch(() => undefined);
    return failedPage;
}

describe('newPage', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('rethrows the navigation error', async () => {
        expect.assertions(1);
        const { state, browser } = stateWithOpenPage();
        newPageThatFailsNavigation(browser.context);

        await expect(newPage(newPageRequest(), state)).rejects.toBe(navigationTimeout);
    });

    it('keeps the failed page open and active when navigation fails', async () => {
        const { state, browser } = stateWithOpenPage();

        const failedPage = await failNewPage(state, browser.context);

        expect(browser.page?.p).toBe(failedPage);
        expect(failedPage.close).not.toHaveBeenCalled();
    });
});

describe('removeFailedPage', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('closes the failed page and reactivates the page below it', async () => {
        const { state, browser } = stateWithOpenPage();
        const failedPage = await failNewPage(state, browser.context);

        await removeFailedPage({ token: 'token-1' }, state);

        expect(failedPage.close).toHaveBeenCalledTimes(1);
        expect(browser.page?.id).toBe('page=open');
        expect(browser.context?.pageStack).toHaveLength(1);
    });

    it('leaves the active page alone when the failed page is not active', async () => {
        const { state, browser, openPage } = stateWithOpenPage();
        const failedPage = await failNewPage(state, browser.context);
        browser.pushPage(openPage);

        await removeFailedPage({ token: 'token-1' }, state);

        expect(failedPage.close).toHaveBeenCalledTimes(1);
        expect(browser.page?.id).toBe('page=open');
        expect(browser.context?.pageStack).toHaveLength(1);
    });

    it('removes only the page recorded under its token', async () => {
        const { state, browser } = stateWithOpenPage();
        const outer = await failNewPage(state, browser.context, 'outer');
        const inner = await failNewPage(state, browser.context, 'inner');

        await removeFailedPage({ token: 'outer' }, state);

        expect(outer.close).toHaveBeenCalledTimes(1);
        expect(inner.close).not.toHaveBeenCalled();
        expect(browser.page?.p).toBe(inner);
    });

    it('does not close a failed page that is already closed', async () => {
        const { state, browser } = stateWithOpenPage();
        const failedPage = await failNewPage(state, browser.context);
        failedPage.isClosed.mockReturnValue(true);

        await removeFailedPage({ token: 'token-1' }, state);

        expect(failedPage.close).not.toHaveBeenCalled();
        expect(browser.page?.id).toBe('page=open');
    });

    it('returns without waiting for the failed page to close', async () => {
        const { state, browser } = stateWithOpenPage();
        const failedPage = await failNewPage(state, browser.context);
        failedPage.close.mockReturnValue(new Promise(() => undefined));

        await removeFailedPage({ token: 'token-1' }, state);

        expect(failedPage.close).toHaveBeenCalledTimes(1);
        expect(browser.page?.id).toBe('page=open');
    });

    it('does not fail when closing the failed page fails, and forgets the page', async () => {
        const { state, browser } = stateWithOpenPage();
        const failedPage = await failNewPage(state, browser.context);
        failedPage.close.mockRejectedValue(new Error('Target closed'));

        await removeFailedPage({ token: 'token-1' }, state);
        await removeFailedPage({ token: 'token-1' }, state);

        expect(failedPage.close).toHaveBeenCalledTimes(1);
        expect(browser.page?.id).toBe('page=open');
    });

    it('does nothing for an unknown token', async () => {
        const { state, browser } = stateWithOpenPage();

        await removeFailedPage({ token: 'unknown' }, state);

        expect(browser.page?.id).toBe('page=open');
    });
});

function makeMockPage() {
    return { on: jest.fn() } as any;
}

function makeMockContext(pages: any[], close = jest.fn().mockResolvedValue(undefined)) {
    return { pages: () => pages, on: jest.fn(), close, setDefaultTimeout: jest.fn() } as any;
}

describe('adoptContext', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('adds the context as a new active browser without a browser object', async () => {
        const state = new PlaywrightState();
        state.browserStack.push(makeBrowserState('browser=existing'));

        const adopted = await state.adoptContext(makeMockContext([makeMockPage()]));

        expect(state.browserStack).toHaveLength(2);
        expect(state.activeBrowser?.id).toBe(adopted.browserId);
        expect(state.activeBrowser?.browser).toBeNull();
        expect(state.activeBrowser?.context?.id).toBe(adopted.contextId);
        expect(state.activeBrowser?.name).toBe('adopted');
        expect(state.activeBrowser?.headless).toBe(false);
    });

    it('takes the name and headless that the creator passes', async () => {
        const state = new PlaywrightState();

        await state.adoptContext(makeMockContext([makeMockPage()]), { name: 'electron', headless: true });

        expect(state.activeBrowser?.name).toBe('electron');
        expect(state.activeBrowser?.headless).toBe(true);
    });

    it('sets the library timeout as the default timeout of the context', async () => {
        const state = new PlaywrightState();
        const context = makeMockContext([makeMockPage()]);

        await state.adoptContext(context, {}, 5000);

        expect(context.setDefaultTimeout).toHaveBeenCalledWith(5000);
    });

    it('registers every existing page and makes the first one active', async () => {
        const state = new PlaywrightState();
        const first = makeMockPage();
        const second = makeMockPage();

        const adopted = await state.adoptContext(makeMockContext([first, second]));

        expect(state.activeBrowser?.context?.pageStack.map((page) => page.p)).toEqual([second, first]);
        expect(state.activeBrowser?.page?.p).toBe(first);
        expect(adopted.pageId).toBe(state.activeBrowser?.page?.id);
    });

    it('keeps an existing browser state with a null browser separate', async () => {
        const state = new PlaywrightState();

        const one = await state.adoptContext(makeMockContext([makeMockPage()]));
        const two = await state.adoptContext(makeMockContext([makeMockPage()]));

        expect(state.browserStack).toHaveLength(2);
        expect(state.browserStack.map((browser) => browser.id)).toEqual([one.browserId, two.browserId]);
    });

    it('runs onClose once after the adopted context is closed', async () => {
        const state = new PlaywrightState();
        const context = makeMockContext([makeMockPage()]);
        const onClose = jest.fn().mockResolvedValue(undefined);
        await state.adoptContext(context, { onClose });
        const adopted = state.getActiveBrowser();

        await closeBrowser(state);
        await adopted.close();

        expect(context.close).toHaveBeenCalled();
        expect(onClose).toHaveBeenCalledTimes(1);
    });

    it('runs onClose even if closing the context fails', async () => {
        expect.assertions(2);
        const state = new PlaywrightState();
        const context = makeMockContext([makeMockPage()], jest.fn().mockRejectedValue(new Error('gone')));
        const onClose = jest.fn().mockResolvedValue(undefined);
        await state.adoptContext(context, { onClose });

        await expect(state.getActiveBrowser().close()).rejects.toThrow('gone');
        expect(onClose).toHaveBeenCalledTimes(1);
    });

    it('closes the browser and waits for onClose when its context is closed', async () => {
        const state = new PlaywrightState();
        let released = false;
        await state.adoptContext(makeMockContext([makeMockPage()]), {
            onClose: async () => {
                await new Promise((resolve) => setTimeout(resolve, 0));
                released = true;
            },
        });

        await closeContext({ value: false }, state);

        expect(released).toBe(true);
        expect(state.browserStack).toHaveLength(0);
    });

    it('closes the browser and runs onClose even if closing its context fails', async () => {
        expect.assertions(3);
        const state = new PlaywrightState();
        const context = makeMockContext([makeMockPage()], jest.fn().mockRejectedValue(new Error('gone')));
        const onClose = jest.fn().mockResolvedValue(undefined);
        await state.adoptContext(context, { onClose });

        await expect(closeContext({ value: false }, state)).rejects.toThrow('gone');
        expect(onClose).toHaveBeenCalledTimes(1);
        expect(state.browserStack).toHaveLength(0);
    });
});

describe('extensionKeywordCall', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('lets an extension function adopt a context it created', async () => {
        const state = new PlaywrightState();
        const context = makeMockContext([makeMockPage()]);
        async function openOwnContext(adoptContext: (c: unknown, options?: unknown) => Promise<unknown>) {
            return adoptContext(context, { name: 'own' });
        }
        state.extensions.push({ openOwnContext } as any);
        const call = { write: jest.fn() } as any;

        const responses = await extensionKeywordCall(
            { name: 'openOwnContext', arguments: JSON.stringify({ arguments: [], defaultTimeout: 5000 }) },
            call,
            state,
        );

        const adopted = JSON.parse(responses.map((response) => response.bodyPart).join(''));
        expect(adopted.browserId).toBe(state.activeBrowser?.id);
        expect(state.activeBrowser?.context?.c).toBe(context);
        expect(state.activeBrowser?.name).toBe('own');
        expect(context.setDefaultTimeout).toHaveBeenCalledWith(5000);
    });
});
