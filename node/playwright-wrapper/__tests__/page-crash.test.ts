import { describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({ logger: { warn: jest.fn() } }));

import { logger } from '../browser_logger';
import { isCrashed, isGone, watchCrash } from '../page-crash';
import { crash } from './fake-crash';

function fakePage({ closed = false } = {}) {
    return {
        url: () => 'http://localhost/form.html',
        isClosed: () => closed,
        on: jest.fn(),
    };
}

describe('watchCrash', () => {
    it('marks a page as crashed once Playwright reports its crash, and warns', () => {
        const page = fakePage();
        watchCrash(page as any);
        expect(isCrashed(page as any)).toBe(false);
        crash(page);
        expect(isCrashed(page as any)).toBe(true);
        expect(logger.warn).toHaveBeenCalledWith(expect.stringContaining('http://localhost/form.html'));
    });

    it('knows nothing of a page it does not watch', () => {
        expect(isCrashed(fakePage() as any)).toBe(false);
    });
});

describe('isGone', () => {
    it('is true for a closed page and for a crashed one, false for a live one', () => {
        const crashed = fakePage();
        watchCrash(crashed as any);
        crash(crashed);
        expect(isGone(crashed as any)).toBe(true);
        expect(isGone(fakePage({ closed: true }) as any)).toBe(true);
        expect(isGone(fakePage() as any)).toBe(false);
    });
});
