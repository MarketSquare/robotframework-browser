/// <reference types="jest" />

import { beforeEach, describe, expect, it } from '@jest/globals';

jest.mock('../playwright-invoke', () => ({
    findLocator: jest.fn(),
    exists: jest.requireActual('../playwright-invoke').exists,
}));

jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

jest.mock('../network', () => ({
    _waitForDownload: jest.fn(),
}));

import { highlightAll, HighlightDisposableCache, highlightDisposableCache } from '../evaluation';
import { findLocator } from '../playwright-invoke';

const mockFindLocator = jest.mocked(findLocator);

function makeMockState() {
    return {} as any;
}

function makeHighlight() {
    return { dispose: jest.fn().mockResolvedValue(undefined) };
}

function makeMockLocator(
    overrides: Partial<{
        count: jest.Mock;
        highlight: jest.Mock;
        evaluateAll: jest.Mock;
    }> = {},
) {
    return {
        count: jest.fn().mockResolvedValue(3),
        highlight: jest.fn().mockResolvedValue(makeHighlight()),
        evaluateAll: jest.fn().mockResolvedValue(undefined),
        ...overrides,
    } as any;
}

describe('HighlightDisposableCache', () => {
    describe('disposeAll', () => {
        it('calls dispose on every added disposable', async () => {
            const cache = new HighlightDisposableCache();
            const dispose1 = jest.fn().mockResolvedValue(undefined);
            const dispose2 = jest.fn().mockResolvedValue(undefined);
            cache.add({ dispose: dispose1 });
            cache.add({ dispose: dispose2 });

            await cache.disposeAll();

            expect(dispose1).toHaveBeenCalledTimes(1);
            expect(dispose2).toHaveBeenCalledTimes(1);
        });

        it('clears the cache so a second disposeAll does not call dispose again', async () => {
            const cache = new HighlightDisposableCache();
            const dispose = jest.fn().mockResolvedValue(undefined);
            cache.add({ dispose });

            await cache.disposeAll();
            await cache.disposeAll();

            expect(dispose).toHaveBeenCalledTimes(1);
        });

        it('resolves without error when cache is empty', async () => {
            const cache = new HighlightDisposableCache();
            await expect(cache.disposeAll()).resolves.toBeUndefined();
        });
    });
});

describe('highlightAll', () => {
    beforeEach(async () => {
        jest.clearAllMocks();
        await highlightDisposableCache.disposeAll();
    });

    describe('error handling', () => {
        it('returns 0 when locator.count throws', async () => {
            const locator = makeMockLocator({
                count: jest.fn().mockRejectedValue(new Error('Page closed')),
            });
            mockFindLocator.mockResolvedValue(locator);

            const result = await highlightAll('#el', 1000, '1px', 'dotted', 'blue', false, makeMockState());

            expect(result).toBe(0);
        });
    });

    describe('ROBOT_FRAMEWORK_BROWSER_NO_ELEMENT selector', () => {
        it('disposes all cached highlights and returns 0', async () => {
            const dispose = jest.fn().mockResolvedValue(undefined);
            highlightDisposableCache.add({ dispose });
            const locator = makeMockLocator({ count: jest.fn().mockResolvedValue(0) });
            mockFindLocator.mockResolvedValue(locator);

            const result = await highlightAll(
                'ROBOT_FRAMEWORK_BROWSER_NO_ELEMENT',
                0,
                '1px',
                'dotted',
                'blue',
                false,
                makeMockState(),
            );

            expect(result).toBe(0);
            expect(dispose).toHaveBeenCalledTimes(1);
        });
    });

    describe('border mode (default)', () => {
        it('calls evaluateAll and does not call locator.highlight', async () => {
            const locator = makeMockLocator();
            mockFindLocator.mockResolvedValue(locator);

            await highlightAll('#el', 1000, '3px', 'dotted', 'blue', false, makeMockState());

            expect(locator.evaluateAll).toHaveBeenCalledTimes(1);
            expect(locator.highlight).not.toHaveBeenCalled();
        });

        it('passes duration, width, style, and color as evaluation options', async () => {
            const locator = makeMockLocator();
            mockFindLocator.mockResolvedValue(locator);

            await highlightAll('#el', 2000, '5px', 'solid', 'red', false, makeMockState(), 'border');

            expect(locator.evaluateAll).toHaveBeenCalledWith(expect.any(Function), {
                dur: 2000,
                wdt: '5px',
                stl: 'solid',
                clr: 'red',
            });
        });

        it('returns the locator element count', async () => {
            const locator = makeMockLocator({ count: jest.fn().mockResolvedValue(7) });
            mockFindLocator.mockResolvedValue(locator);

            const result = await highlightAll('#el', 0, '1px', 'dotted', 'blue', false, makeMockState());

            expect(result).toBe(7);
        });
    });

    describe('playwright mode', () => {
        it('calls locator.highlight and does not call evaluateAll', async () => {
            const locator = makeMockLocator();
            mockFindLocator.mockResolvedValue(locator);

            await highlightAll('#el', 0, '3px', 'dotted', 'blue', false, makeMockState(), 'playwright');

            expect(locator.highlight).toHaveBeenCalledTimes(1);
            expect(locator.evaluateAll).not.toHaveBeenCalled();
        });

        it('adds the returned highlight object to the disposable cache', async () => {
            const highlight = makeHighlight();
            const locator = makeMockLocator({ highlight: jest.fn().mockResolvedValue(highlight) });
            mockFindLocator.mockResolvedValue(locator);

            await highlightAll('#el', 0, '1px', 'dotted', 'blue', false, makeMockState(), 'playwright');
            await highlightDisposableCache.disposeAll();

            expect(highlight.dispose).toHaveBeenCalledTimes(1);
        });

        it('returns the locator element count', async () => {
            const locator = makeMockLocator({ count: jest.fn().mockResolvedValue(4) });
            mockFindLocator.mockResolvedValue(locator);

            const result = await highlightAll('#el', 0, '1px', 'dotted', 'blue', false, makeMockState(), 'playwright');

            expect(result).toBe(4);
        });
    });

    describe('both mode', () => {
        it('calls both locator.highlight and evaluateAll', async () => {
            const locator = makeMockLocator();
            mockFindLocator.mockResolvedValue(locator);

            await highlightAll('#el', 0, '3px', 'dotted', 'blue', false, makeMockState(), 'both');

            expect(locator.highlight).toHaveBeenCalledTimes(1);
            expect(locator.evaluateAll).toHaveBeenCalledTimes(1);
        });

        it('returns the locator element count', async () => {
            const locator = makeMockLocator({ count: jest.fn().mockResolvedValue(2) });
            mockFindLocator.mockResolvedValue(locator);

            const result = await highlightAll('#el', 0, '1px', 'dotted', 'blue', false, makeMockState(), 'both');

            expect(result).toBe(2);
        });
    });
});
