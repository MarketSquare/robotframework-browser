import { beforeEach, describe, expect, it } from '@jest/globals';
import { EventEmitter } from 'events';
import { _electron } from 'playwright';

jest.mock('playwright', () => ({
    ...jest.requireActual('playwright'),
    _electron: { launch: jest.fn() },
}));
jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn(), warn: jest.fn() },
}));
jest.mock('uuid', () => {
    let id = 0;
    return { v4: () => String(++id) };
});

import {
    BrowserState,
    closeAllBrowsers,
    closeBrowser,
    closeElectron,
    launchElectron,
    PlaywrightState,
} from '../playwright-state';

const mockLaunch = jest.spyOn(_electron, 'launch');

function makeApp() {
    const context = Object.assign(new EventEmitter(), {
        setDefaultTimeout: jest.fn(),
        close: jest.fn().mockResolvedValue(undefined),
    });
    const page = Object.assign(new EventEmitter(), {
        context: () => context,
        waitForLoadState: jest.fn().mockResolvedValue(undefined),
        video: () => null,
        isClosed: () => false,
    });
    const app = Object.assign(new EventEmitter(), {
        context: () => context,
        firstWindow: jest.fn().mockResolvedValue(page),
        windows: () => [page],
        close: jest.fn().mockImplementation(async () => {
            app.emit('close');
        }),
    });
    return { app, context, page };
}

function request(timeout = 30000) {
    return { rawOptions: JSON.stringify({ executablePath: '/electron', timeout }), defaultTimeout: timeout };
}

describe('Electron lifecycle', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('preserves zero for window, DOM and context timeouts', async () => {
        const { app, context, page } = makeApp();
        mockLaunch.mockResolvedValue(app as any);
        await launchElectron(request(0), new PlaywrightState());
        expect(app.firstWindow).toHaveBeenCalledWith({ timeout: 0 });
        expect(page.waitForLoadState).toHaveBeenCalledWith('domcontentloaded', { timeout: 0 });
        expect(context.setDefaultTimeout).toHaveBeenCalledWith(0);
    });

    it('keeps a persistent context separate and removes only Electron when another browser is active', async () => {
        const { app } = makeApp();
        mockLaunch.mockResolvedValue(app as any);
        const state = new PlaywrightState();
        const persistent = new BrowserState({ browser: null, browserType: 'chromium', headless: true });
        state.browserStack.push(persistent);
        const response = await launchElectron(request(), state);
        expect(response.browserId).not.toBe(persistent.id);
        const other = new BrowserState({ browser: null, browserType: 'firefox', headless: true });
        state.browserStack.push(other);
        await closeElectron(state);
        expect(state.browserStack).toEqual([persistent, other]);
        expect(state.electronBrowserState).toBeNull();
    });

    it('closes the previous app before launching again', async () => {
        const first = makeApp();
        const second = makeApp();
        mockLaunch.mockResolvedValueOnce(first.app as any).mockResolvedValueOnce(second.app as any);
        const state = new PlaywrightState();
        await launchElectron(request(), state);
        await launchElectron(request(), state);
        expect(first.app.close).toHaveBeenCalledTimes(1);
        expect(state.browserStack).toHaveLength(1);
        expect(state.electronBrowserState?.electronApplication).toBe(second.app);
    });

    it('does not reuse Electron state when a persistent context is opened afterwards', async () => {
        const { app } = makeApp();
        mockLaunch.mockResolvedValue(app as any);
        const state = new PlaywrightState();
        await launchElectron(request(), state);
        const electronState = state.electronBrowserState;
        const persistent = state.addBrowser({ browser: null, browserType: 'chromium', headless: true });
        expect(persistent).not.toBe(electronState);
        await closeElectron(state);
        expect(state.browserStack).toEqual([persistent]);
    });

    it('closes the app when waiting for its first window fails', async () => {
        expect.assertions(3);
        const { app } = makeApp();
        app.firstWindow.mockRejectedValue(new Error('window timeout'));
        mockLaunch.mockResolvedValue(app as any);
        const state = new PlaywrightState();
        await expect(launchElectron(request(), state)).rejects.toThrow('window timeout');
        expect(app.close).toHaveBeenCalledTimes(1);
        expect(state.browserStack).toHaveLength(0);
    });

    it('returns recording metadata with its context id', async () => {
        const { app, page } = makeApp();
        page.video = () => ({ path: async () => '/videos/first.webm' }) as any;
        mockLaunch.mockResolvedValue(app as any);
        const response = await launchElectron(request(), new PlaywrightState());
        expect(JSON.parse(response.video)).toEqual({ video_path: '/videos/first.webm', contextUuid: response.id });
    });

    it.each([closeBrowser, closeAllBrowsers])('closes Electron through standard browser teardown %p', async (close) => {
        const { app } = makeApp();
        mockLaunch.mockResolvedValue(app as any);
        const state = new PlaywrightState();
        await launchElectron(request(), state);
        await close(state);
        expect(app.close).toHaveBeenCalledTimes(1);
        expect(state.electronBrowserState).toBeNull();
        expect(state.browserStack).toHaveLength(0);
    });

    it('removes state when the app exits externally', async () => {
        const { app } = makeApp();
        mockLaunch.mockResolvedValue(app as any);
        const state = new PlaywrightState();
        await launchElectron(request(), state);
        app.emit('close');
        expect(state.electronBrowserState).toBeNull();
        expect(state.browserStack).toHaveLength(0);
    });

    it('preserves app state when closing fails so cleanup can be retried', async () => {
        expect.assertions(3);
        const { app } = makeApp();
        mockLaunch.mockResolvedValue(app as any);
        const state = new PlaywrightState();
        await launchElectron(request(), state);
        app.close.mockRejectedValueOnce(new Error('close failed'));
        await expect(closeElectron(state)).rejects.toThrow('close failed');
        expect(state.electronBrowserState?.electronApplication).toBe(app);
        await closeElectron(state);
        expect(state.electronBrowserState).toBeNull();
    });
});
