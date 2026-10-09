import { describe, expect, it } from '@jest/globals';

import { HighlightDisposableCache } from '../highlight-cache';

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
