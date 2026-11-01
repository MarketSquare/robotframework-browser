/// <reference types="jest" />

import { beforeEach, describe, expect, it } from '@jest/globals';

// Mock playwright-invoke so findLocator returns our controlled mock locator
jest.mock('../playwright-invoke', () => ({
    findLocator: jest.fn(),
    exists: jest.requireActual('../playwright-invoke').exists,
}));

// Mock the logger to suppress output in tests
jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

import { executePlaywright, takeScreenshot } from '../browser-control';
import { findLocator } from '../playwright-invoke';

const mockFindLocator = jest.mocked(findLocator);

function makeMockLocator(overrides: Partial<{ screenshot: jest.Mock }> = {}) {
    return {
        screenshot: jest.fn().mockResolvedValue(undefined),
        ...overrides,
    } as any;
}

function makeMockPage(overrides: Partial<{ screenshot: jest.Mock }> = {}) {
    return {
        screenshot: jest.fn().mockResolvedValue(undefined),
        ...overrides,
    } as any;
}

function makeRequest(selector?: string, options: Record<string, any> = {}, mask: string[] = [], strict = false) {
    return {
        selector: selector || '',
        options: JSON.stringify(options),
        mask: JSON.stringify(mask),
        strict,
    } as any;
}

function makeMockState(page?: any) {
    return {
        getActivePage: jest.fn().mockReturnValue(page),
    } as any;
}

describe('takeScreenshot', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('takes full page screenshot when no selector provided', async () => {
        const mockPage = makeMockPage();
        const state = makeMockState(mockPage);
        const opts = { path: 'full.png' };
        const req = makeRequest('', opts, []);

        const res = await takeScreenshot(req, state);

        expect(mockPage.screenshot).toHaveBeenCalledWith(expect.objectContaining(opts));
        expect(res.body).toBe('full.png');
        expect(res.log).toMatch(/Screenshot successfully captured/);
    });

    it('uses locator.screenshot when selector provided', async () => {
        const locator = makeMockLocator();
        mockFindLocator.mockResolvedValue(locator);
        const state = makeMockState(makeMockPage());
        const opts = { path: 'sel.png' };
        const req = makeRequest('#el', opts, []);

        const res = await takeScreenshot(req, state);

        expect(locator.screenshot).toHaveBeenCalledWith(expect.objectContaining(opts));
        expect(res.body).toBe('sel.png');
    });

    it('applies mask locators when mask provided', async () => {
        const locatorA = makeMockLocator();
        const locatorB = makeMockLocator();
        // first two calls for mask locators
        mockFindLocator.mockResolvedValueOnce(locatorA).mockResolvedValueOnce(locatorB);
        const mockPage = makeMockPage();
        const state = makeMockState(mockPage);
        const opts = { path: 'masked.png' };
        const req = makeRequest('', opts, ['#a', '#b']);

        const res = await takeScreenshot(req, state);

        expect(mockFindLocator).toHaveBeenCalledWith(state, '#a', false, false);
        expect(mockFindLocator).toHaveBeenCalledWith(state, '#b', false, false);
        expect(mockPage.screenshot).toHaveBeenCalledWith(
            expect.objectContaining({ path: 'masked.png', mask: [locatorA, locatorB] }),
        );
        expect(res.body).toBe('masked.png');
    });

    it('throws when no page open', async () => {
        expect.assertions(1);
        const state = makeMockState(undefined);
        const req = makeRequest('', { path: 'no.png' }, []);
        await expect(takeScreenshot(req, state)).rejects.toThrow('Tried to take screenshot, but no page was open.');
    });
});

describe('executePlaywright', () => {
    function makeJsonRequest(args: string[]) {
        return { body: JSON.stringify(args) } as any;
    }

    let consoleLog: jest.SpyInstance;

    beforeEach(() => {
        consoleLog = jest.spyOn(console, 'log').mockImplementation(() => undefined);
    });

    afterEach(() => {
        consoleLog.mockRestore();
    });

    it('runs a Playwright CLI command', async () => {
        const res = await executePlaywright(makeJsonRequest(['install', '--dry-run', 'chromium']));

        expect(res.log).toBe('Executed Playwright command: install --dry-run chromium');
    });

    it('runs a second command after the first one', async () => {
        await executePlaywright(makeJsonRequest(['install', '--dry-run', 'chromium']));

        const res = await executePlaywright(makeJsonRequest(['install', '--dry-run', 'firefox']));

        expect(res.log).toBe('Executed Playwright command: install --dry-run firefox');
    });

    it('rejects an unknown command instead of exiting the process', async () => {
        expect.assertions(1);
        const stderrWrite = jest.spyOn(process.stderr, 'write').mockImplementation(() => true);
        try {
            await expect(executePlaywright(makeJsonRequest(['no-such-command']))).rejects.toMatchObject({
                code: 'commander.unknownCommand',
            });
        } finally {
            stderrWrite.mockRestore();
        }
    });
});
