jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

import { beforeEach, describe, expect, it } from '@jest/globals';
import { EventEmitter } from 'events';
import { errors, Page, Request } from 'playwright';

import { loadReportOf, trackRequests, withLoadReport } from '../load-report';

type FakePage = EventEmitter & { mainFrame: () => object; url: () => string; evaluate: jest.Mock };

function makePage(url = 'about:blank'): FakePage {
    const frame = {};
    const page = new EventEmitter() as FakePage;
    page.mainFrame = () => frame;
    page.url = () => url;
    page.evaluate = jest.fn();
    return page;
}

function makePlaywrightRequest(
    page: FakePage,
    url: string,
    { resourceType = 'image', navigation = false, method = 'GET' } = {},
): Request {
    return {
        url: () => url,
        method: () => method,
        resourceType: () => resourceType,
        isNavigationRequest: () => navigation,
        frame: () => page.mainFrame(),
    } as unknown as Request;
}

function documentRequest(page: FakePage, url: string): Request {
    return makePlaywrightRequest(page, url, { resourceType: 'document', navigation: true });
}

async function reportOfTimeout(page: FakePage): Promise<string | undefined> {
    const timeout = new errors.TimeoutError('page.goto: Timeout 1000ms exceeded.');
    await expect(withLoadReport(page as unknown as Page, () => Promise.reject(timeout))).rejects.toBe(timeout);
    return loadReportOf(timeout);
}

describe('withLoadReport', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('returns what the wait returns', async () => {
        const page = makePage();
        trackRequests(page as unknown as Page);

        expect(await withLoadReport(page as unknown as Page, () => Promise.resolve('done'))).toBe('done');
    });

    it('reports nothing for an error that is not a timeout', async () => {
        expect.assertions(2);
        const page = makePage();
        trackRequests(page as unknown as Page);
        const refused = new Error('net::ERR_CONNECTION_REFUSED');

        await expect(withLoadReport(page as unknown as Page, () => Promise.reject(refused))).rejects.toBe(refused);
        expect(loadReportOf(refused)).toBeUndefined();
    });

    it('raises the timeout without a report when the report cannot be built', async () => {
        expect.assertions(2);
        const untrackedPage = makePage();

        const report = await reportOfTimeout(untrackedPage);

        expect(report).toBeUndefined();
    });
});

describe('load report', () => {
    let page: FakePage;

    beforeEach(() => {
        jest.clearAllMocks();
        page = makePage();
        trackRequests(page as unknown as Page);
    });

    describe('when the navigation has not committed', () => {
        it('names the document request that never got a response', async () => {
            page.emit('request', documentRequest(page, 'http://localhost/slowpage.html'));

            const report = await reportOfTimeout(page);

            expect(report).toContain('URL: about:blank');
            expect(report).toContain('Navigation committed: no (waiting for http://localhost/slowpage.html)');
            expect(report).toMatch(/GET http:\/\/localhost\/slowpage\.html \[document\] open for \d+ ms/);
        });

        it('does not ask the page anything', async () => {
            page.emit('request', documentRequest(page, 'http://localhost/slowpage.html'));

            await reportOfTimeout(page);

            expect(page.evaluate).not.toHaveBeenCalled();
        });
    });

    describe('when the navigation has committed', () => {
        beforeEach(() => {
            const document = documentRequest(page, 'http://localhost/stalledpage.html');
            page.emit('request', document);
            page.emit('response', { request: () => document });
            page.emit('requestfinished', document);
        });

        it('tells how far the document got', async () => {
            page.evaluate.mockResolvedValue({ readyState: 'interactive', domContentLoaded: 12.4, load: 0 });

            const report = await reportOfTimeout(page);

            expect(report).toContain('Navigation committed: yes');
            expect(report).toContain('readyState: interactive');
            expect(report).toContain('DOMContentLoaded: 12 ms');
            expect(report).toContain('load: never fired');
        });

        it('names only the requests that are still open', async () => {
            const finished = makePlaywrightRequest(page, 'http://localhost/ok.png');
            const failed = makePlaywrightRequest(page, 'http://localhost/broken.png');
            page.emit('request', finished);
            page.emit('request', failed);
            page.emit('request', makePlaywrightRequest(page, 'http://localhost/api/stalled-image'));
            page.emit('requestfinished', finished);
            page.emit('requestfailed', failed);
            page.evaluate.mockResolvedValue({ readyState: 'interactive', domContentLoaded: 12, load: 0 });

            const report = await reportOfTimeout(page);

            expect(report).toContain('Outstanding requests: 1');
            expect(report).toMatch(/GET http:\/\/localhost\/api\/stalled-image \[image\] open for \d+ ms/);
            expect(report).not.toContain('stalledpage.html [document]');
            expect(report).not.toContain('ok.png');
            expect(report).not.toContain('broken.png');
        });

        it('is no longer committed once the page navigates again', async () => {
            page.emit('request', documentRequest(page, 'http://localhost/slowpage.html'));

            const report = await reportOfTimeout(page);

            expect(report).toContain('Navigation committed: no');
            expect(page.evaluate).not.toHaveBeenCalled();
        });

        it('is not committed when the next document request failed', async () => {
            const failedDocument = documentRequest(page, 'http://localhost/unreachable.html');
            page.emit('request', failedDocument);
            page.emit('requestfailed', failedDocument);
            page.evaluate.mockResolvedValue({ readyState: 'complete', domContentLoaded: 5, load: 9 });

            const report = await reportOfTimeout(page);

            expect(report).toContain('Navigation committed: no (document request failed)');
            expect(report).toContain('readyState: complete');
        });

        it('keeps the requests of the current document while the next one is loading', async () => {
            page.emit('request', makePlaywrightRequest(page, 'http://localhost/api/stalled-image'));
            page.emit('request', documentRequest(page, 'http://localhost/slowpage.html'));
            page.emit('framenavigated', page.mainFrame());

            const report = await reportOfTimeout(page);

            expect(report).toContain('stalled-image');
        });

        it('stays committed when only an iframe navigates', async () => {
            const iframeDocument = {
                ...documentRequest(page, 'http://localhost/frame.html'),
                frame: () => ({}),
            } as unknown as Request;
            page.emit('request', iframeDocument);
            page.evaluate.mockResolvedValue({ readyState: 'complete', domContentLoaded: 5, load: 9 });

            const report = await reportOfTimeout(page);

            expect(report).toContain('Navigation committed: yes');
        });
    });

    describe('when the old document keeps loading while the next one is requested', () => {
        it('forgets what the old document started before the next one answered', async () => {
            const document = documentRequest(page, 'http://localhost/slow-b.html');
            page.emit('request', document);
            page.emit('request', makePlaywrightRequest(page, 'http://localhost/api/poll'));
            page.emit('response', { request: () => document });
            page.emit('framenavigated', page.mainFrame());
            page.emit('request', makePlaywrightRequest(page, 'http://localhost/api/stalled-image'));
            page.evaluate.mockResolvedValue({ readyState: 'loading', domContentLoaded: 0, load: 0 });

            const report = await reportOfTimeout(page);

            expect(report).not.toContain('api/poll');
            expect(report).toContain('slow-b.html [document]');
            expect(report).toContain('stalled-image');
        });
    });

    describe('when the navigation ends in a download', () => {
        beforeEach(() => {
            page.emit('request', makePlaywrightRequest(page, 'http://localhost/api/stalled-image'));
            const download = documentRequest(page, 'http://localhost/file.zip');
            page.emit('request', download);
            page.emit('response', { request: () => download });
            page.emit('requestfailed', download);
            page.evaluate.mockResolvedValue({ readyState: 'complete', domContentLoaded: 3, load: 5 });
        });

        it('reports that no document came of it', async () => {
            const report = await reportOfTimeout(page);

            expect(report).toContain('Navigation committed: no (document request failed)');
            expect(report).toContain('readyState: complete');
        });

        it('keeps the requests of the page it stayed on when that page navigates within itself', async () => {
            page.emit('framenavigated', page.mainFrame());

            const report = await reportOfTimeout(page);

            expect(report).toContain('stalled-image');
        });
    });

    describe('when Playwright cannot tell the frame of a request', () => {
        it('lists the request but does not take it for the page document', async () => {
            const frameless = {
                ...documentRequest(page, 'http://localhost/popup.html'),
                frame: () => {
                    throw new Error('Frame for this navigation request is not available');
                },
            } as unknown as Request;
            page.evaluate.mockResolvedValue({ readyState: 'complete', domContentLoaded: 3, load: 5 });
            page.emit('request', frameless);

            const report = await reportOfTimeout(page);

            expect(report).toContain('Navigation committed: yes');
            expect(report).toContain('popup.html [document]');
        });
    });

    describe('when reading a request fails', () => {
        it('does not let the failure escape the page event', () => {
            const broken = {
                ...makePlaywrightRequest(page, 'http://localhost/broken'),
                isNavigationRequest: () => {
                    throw new Error('Target page, context or browser has been closed');
                },
            } as unknown as Request;

            expect(() => page.emit('request', broken)).not.toThrow();
        });
    });

    describe('when the page navigates away', () => {
        let document: Request;

        beforeEach(() => {
            page.emit('request', makePlaywrightRequest(page, 'http://localhost/old-image.png'));
            document = documentRequest(page, 'http://localhost/stalledpage.html');
            page.emit('request', document);
            page.emit('response', { request: () => document });
            page.evaluate.mockResolvedValue({ readyState: 'interactive', domContentLoaded: 3, load: 0 });
        });

        it('forgets the requests of the document it left', async () => {
            page.emit('framenavigated', page.mainFrame());
            page.emit('request', makePlaywrightRequest(page, 'http://localhost/api/stalled-image'));

            const report = await reportOfTimeout(page);

            expect(report).not.toContain('old-image.png');
            expect(report).toContain('stalled-image');
        });

        it('keeps the requests of the page when it navigates within the same document', async () => {
            page.emit('framenavigated', page.mainFrame());
            page.emit('request', makePlaywrightRequest(page, 'http://localhost/api/stalled-image'));
            page.emit('requestfinished', document);
            page.emit('framenavigated', page.mainFrame());

            const report = await reportOfTimeout(page);

            expect(report).toContain('stalled-image');
        });

        it('keeps the requests of the page when only an iframe navigates', async () => {
            page.emit('framenavigated', {});

            const report = await reportOfTimeout(page);

            expect(report).toContain('old-image.png');
        });
    });

    describe('when asking the page fails', () => {
        beforeEach(() => {
            page.emit('request', makePlaywrightRequest(page, 'http://localhost/api/stalled-image'));
        });

        it('gives up on the page after 500 ms and still names the open requests', async () => {
            jest.useFakeTimers();
            try {
                page.evaluate.mockReturnValue(new Promise(() => undefined));
                const report = reportOfTimeout(page);
                await jest.advanceTimersByTimeAsync(500);

                expect(await report).toContain('readyState: unknown (probe failed: no answer in 500 ms)');
                expect(await report).toContain('http://localhost/api/stalled-image');
            } finally {
                jest.useRealTimers();
            }
        });

        it('tells why the page could not answer', async () => {
            page.evaluate.mockRejectedValue(new Error('Execution context was destroyed'));

            const report = await reportOfTimeout(page);

            expect(report).toContain('readyState: unknown (probe failed: Execution context was destroyed)');
        });
    });

    describe('when the page changes while it is being asked', () => {
        it('does not list a request that started after the timeout', async () => {
            page.evaluate.mockImplementation(async () => {
                page.emit('request', documentRequest(page, 'http://localhost/slowpage.html'));
                throw new Error('Execution context was destroyed');
            });

            const report = await reportOfTimeout(page);

            expect(report).toContain('Navigation committed: yes');
            expect(report).toContain('Outstanding requests: 0');
            expect(report).not.toContain('slowpage.html');
        });

        it('lists a request that was open at the timeout and finished after it', async () => {
            const stalled = makePlaywrightRequest(page, 'http://localhost/api/stalled-image');
            page.emit('request', stalled);
            page.evaluate.mockImplementation(async () => {
                page.emit('requestfinished', stalled);
                return { readyState: 'interactive', domContentLoaded: 12, load: 0 };
            });

            const report = await reportOfTimeout(page);

            expect(report).toContain('Outstanding requests: 1');
            expect(report).toMatch(/GET http:\/\/localhost\/api\/stalled-image \[image\] open for \d+ ms/);
        });
    });

    describe('when there is a lot to report', () => {
        it('names the first 20 open requests and counts the rest', async () => {
            for (let i = 0; i < 23; i++) {
                page.emit('request', makePlaywrightRequest(page, `http://localhost/image-${i}.png`));
            }
            page.evaluate.mockResolvedValue({ readyState: 'interactive', domContentLoaded: 12, load: 0 });

            const report = await reportOfTimeout(page);

            expect(report).toContain('Outstanding requests: 23');
            expect(report).toContain('image-19.png');
            expect(report).not.toContain('image-20.png');
            expect(report).toContain('... and 3 more');
        });

        it('cuts a long URL to 150 characters', async () => {
            const longUrl = `http://localhost/${'a'.repeat(300)}`;
            page.emit('request', makePlaywrightRequest(page, longUrl));
            page.evaluate.mockResolvedValue({ readyState: 'interactive', domContentLoaded: 12, load: 0 });

            const report = await reportOfTimeout(page);

            expect(report).toContain(`GET ${longUrl.slice(0, 149)}… [image]`);
        });

        it('stays within 4 KB of UTF-8', async () => {
            for (let i = 0; i < 20; i++) {
                page.emit('request', makePlaywrightRequest(page, `http://localhost/${i}/${'ä'.repeat(200)}`));
            }
            page.evaluate.mockResolvedValue({ readyState: 'interactive', domContentLoaded: 12, load: 0 });

            const report = (await reportOfTimeout(page)) as string;

            expect(Buffer.byteLength(report, 'utf8')).toBeLessThanOrEqual(4096);
            expect(report.endsWith('... load report truncated')).toBe(true);
        });
    });

    describe('when the document redirects', () => {
        it('waits for the document the redirect points to', async () => {
            const original = documentRequest(page, 'http://localhost/redirect');
            page.emit('request', original);
            page.emit('response', { request: () => original });
            page.emit('requestfinished', original);
            page.emit('request', documentRequest(page, 'http://localhost/slowpage.html'));

            const report = await reportOfTimeout(page);

            expect(report).toContain('Navigation committed: no');
            expect(report).toContain('Outstanding requests: 1');
            expect(report).toContain('http://localhost/slowpage.html');
        });
    });
});
