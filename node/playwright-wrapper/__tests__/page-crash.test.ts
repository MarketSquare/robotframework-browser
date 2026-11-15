import { describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({ logger: { warn: jest.fn() } }));

import { logger } from '../browser_logger';
import { isCrashed, watchCrash } from '../page-crash';

function fakePage() {
    const listeners: Record<string, () => void> = {};
    return {
        listeners,
        url: () => 'http://localhost/form.html',
        on: jest.fn((event: string, listener: () => void) => {
            listeners[event] = listener;
        }),
    };
}

describe('watchCrash', () => {
    it('marks a page as crashed once Playwright reports its crash, and warns', () => {
        const page = fakePage();
        watchCrash(page as any);
        expect(isCrashed(page as any)).toBe(false);
        page.listeners.crash();
        expect(isCrashed(page as any)).toBe(true);
        expect(logger.warn).toHaveBeenCalledWith(expect.stringContaining('http://localhost/form.html'));
    });

    it('knows nothing of a page it does not watch', () => {
        expect(isCrashed(fakePage() as any)).toBe(false);
    });
});
