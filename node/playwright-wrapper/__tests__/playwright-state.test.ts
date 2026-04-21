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
    locatorCache,
    PlaywrightState,
} from '../playwright-state';

function makeBrowserState(id: string): BrowserState {
    const state = new BrowserState({
        browser: null,
        browserType: 'chromium',
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

        expect(() => state.getActiveBrowser()).toThrow('Browser has been closed.');
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
            browserType: 'chromium',
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
