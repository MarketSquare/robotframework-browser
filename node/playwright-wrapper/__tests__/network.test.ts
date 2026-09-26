import { afterEach, beforeEach, describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

jest.mock('uuid', () => ({
    v4: jest.fn().mockReturnValue('mock-uuid-1234'),
}));

import { logger } from '../browser_logger';
import { _waitForDownload, waitForRequest } from '../network';

const mockLogger = jest.mocked(logger);

function makeRequest(urlOrPredicate = '/.*/', timeout = 5000) {
    return { urlOrPredicate, timeout } as any;
}

function makeMockRequest(
    overrides: Partial<{
        url: jest.Mock;
        method: jest.Mock;
        headers: jest.Mock;
        postData: jest.Mock;
    }> = {},
) {
    return {
        url: jest.fn().mockReturnValue('https://example.com/api'),
        method: jest.fn().mockReturnValue('POST'),
        headers: jest.fn().mockReturnValue({ 'content-type': 'application/json' }),
        postData: jest.fn().mockReturnValue(null),
        ...overrides,
    } as any;
}

function makeMockPage(overrides: Partial<{ waitForRequest: jest.Mock; waitForEvent: jest.Mock }> = {}) {
    const mockRequest = makeMockRequest();
    return {
        waitForRequest: jest.fn().mockResolvedValue(mockRequest),
        waitForEvent: jest.fn().mockResolvedValue(makeMockDownload()),
        ...overrides,
    } as any;
}

function makeMockDownload(overrides: Partial<{ createReadStream: jest.Mock; cancel: jest.Mock }> = {}) {
    return {
        suggestedFilename: jest.fn().mockReturnValue('report.bin'),
        createReadStream: jest.fn().mockResolvedValue({}),
        cancel: jest.fn().mockResolvedValue(undefined),
        saveAs: jest.fn().mockResolvedValue(undefined),
        path: jest.fn().mockResolvedValue('/tmp/report.bin'),
        ...overrides,
    } as any;
}

function makeMockDownloadState() {
    return {
        activeBrowser: {
            browser: { _options: {} },
            page: { activeDownloads: new Map() },
        },
    } as any;
}

describe('waitForRequest', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('returns request data with parsed JSON postData', async () => {
        const mockPage = makeMockPage({
            waitForRequest: jest.fn().mockResolvedValue(
                makeMockRequest({
                    postData: jest.fn().mockReturnValue('{"key": "value"}'),
                }),
            ),
        });

        const result = await waitForRequest(makeRequest(), mockPage);

        expect(result.json).toBeDefined();
        const parsed = JSON.parse(result.json);
        expect(parsed.url).toBe('https://example.com/api');
        expect(parsed.method).toBe('POST');
        expect(parsed.postData).toEqual({ key: 'value' });
    });

    it('returns request data with raw postData when JSON parsing fails', async () => {
        const mockPage = makeMockPage({
            waitForRequest: jest.fn().mockResolvedValue(
                makeMockRequest({
                    postData: jest.fn().mockReturnValue('invalid json {'),
                }),
            ),
        });

        const result = await waitForRequest(makeRequest(), mockPage);

        expect(result.json).toBeDefined();
        const parsed = JSON.parse(result.json);
        expect(parsed.postData).toBe('invalid json {');
        expect(mockLogger.info).toHaveBeenCalledWith(expect.stringContaining('Failed to parse postData as JSON'));
    });

    it('returns request data with binary data in postData', async () => {
        const binaryData = '\x00\x01\x02\x03\xFF\xFE';
        const mockPage = makeMockPage({
            waitForRequest: jest.fn().mockResolvedValue(
                makeMockRequest({
                    postData: jest.fn().mockReturnValue(binaryData),
                }),
            ),
        });

        const result = await waitForRequest(makeRequest(), mockPage);

        expect(result.json).toBeDefined();
        const parsed = JSON.parse(result.json);
        expect(parsed.postData).toBe(binaryData);
        expect(mockLogger.info).toHaveBeenCalledWith(expect.stringContaining('Failed to parse postData as JSON'));
    });

    it('returns request data with null postData when postData is empty', async () => {
        const mockPage = makeMockPage();

        const result = await waitForRequest(makeRequest(), mockPage);

        expect(result.json).toBeDefined();
        const parsed = JSON.parse(result.json);
        expect(parsed.postData).toBeNull();
    });

    it('handles headers without special characters', async () => {
        const mockPage = makeMockPage({
            waitForRequest: jest.fn().mockResolvedValue(
                makeMockRequest({
                    headers: jest.fn().mockReturnValue({
                        'content-type': 'application/json',
                        authorization: 'Bearer token123',
                        'user-agent': 'Mozilla/5.0',
                    }),
                }),
            ),
        });

        const result = await waitForRequest(makeRequest(), mockPage);

        expect(result.json).toBeDefined();
        const parsed = JSON.parse(result.json);
        expect(parsed.headers).toEqual({
            'content-type': 'application/json',
            authorization: 'Bearer token123',
            'user-agent': 'Mozilla/5.0',
        });
    });

    it('throws when JSON.stringify fails due to circular references in headers', async () => {
        expect.assertions(1);

        // Create a circular reference object
        const circularObject: any = { key: 'value' };
        circularObject.self = circularObject;

        const mockPage = makeMockPage({
            waitForRequest: jest.fn().mockResolvedValue(
                makeMockRequest({
                    headers: jest.fn().mockReturnValue(circularObject),
                }),
            ),
        });

        await expect(waitForRequest(makeRequest(), mockPage)).rejects.toThrow(TypeError);
    });

    it('throws when JSON.stringify fails due to non-serializable toJSON method', async () => {
        expect.assertions(1);

        // Create an object with a toJSON method that throws
        const badToJsonObject = {
            'content-type': 'application/json',
            toJSON() {
                throw new Error('Cannot serialize this header');
            },
        };

        const mockPage = makeMockPage({
            waitForRequest: jest.fn().mockResolvedValue(
                makeMockRequest({
                    headers: jest.fn().mockReturnValue(badToJsonObject),
                }),
            ),
        });

        await expect(waitForRequest(makeRequest(), mockPage)).rejects.toThrow('Cannot serialize this header');
    });

    it('logs request information', async () => {
        const mockPage = makeMockPage({
            waitForRequest: jest.fn().mockResolvedValue(
                makeMockRequest({
                    url: jest.fn().mockReturnValue('https://api.example.com/data'),
                    method: jest.fn().mockReturnValue('GET'),
                }),
            ),
        });

        await waitForRequest(makeRequest('https://api.example.com/.*'), mockPage);

        expect(mockLogger.info).toHaveBeenCalledWith(
            expect.stringContaining('waitForRequest received: https://api.example.com/data method: GET'),
        );
    });

    it('uses string matcher in response log message', async () => {
        const mockPage = makeMockPage();

        const result = await waitForRequest(makeRequest('https://example.com/api'), mockPage);

        expect(result.log).toContain('matcher: https://example.com/api');
    });

    it('parses regex string matcher and includes it in response log', async () => {
        const mockWaitForRequest = jest.fn().mockResolvedValue(makeMockRequest());
        const mockPage = { waitForRequest: mockWaitForRequest } as any;

        const result = await waitForRequest(makeRequest('/api/users/\\d+/'), mockPage);

        // Verify regex parsing worked
        const passedMatcher = mockWaitForRequest.mock.calls[0][0];
        expect(passedMatcher).toBeInstanceOf(RegExp);

        // Verify the regex representation is in the log
        const regexString = passedMatcher.toString();
        expect(result.log).toContain(`matcher: ${regexString}`);
    });

    it('includes timeout in response message', async () => {
        const mockPage = makeMockPage();

        const result = await waitForRequest(makeRequest('.*', 10000), mockPage);

        expect(result.log).toContain('10000ms');
    });
});

describe('_waitForDownload', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    it('waits for the download to start at most the download timeout', async () => {
        const mockPage = makeMockPage();

        await _waitForDownload(mockPage, makeMockDownloadState(), '', 30000, true);

        expect(mockPage.waitForEvent).toHaveBeenCalledWith('download', { timeout: 30000 });
    });

    it('waits for the download to start at most the browser timeout when no download timeout is set', async () => {
        const mockPage = makeMockPage();

        await _waitForDownload(mockPage, makeMockDownloadState(), '', 0, true);

        expect(mockPage.waitForEvent).toHaveBeenCalledWith('download', { timeout: undefined });
    });

    it('applies the download timeout also when not waiting for the download to finish', async () => {
        const mockPage = makeMockPage();

        const result = await _waitForDownload(mockPage, makeMockDownloadState(), '', 30000, false);

        expect(mockPage.waitForEvent).toHaveBeenCalledWith('download', { timeout: 30000 });
        expect(JSON.parse(result.json).state).toBe('in_progress');
    });

    it('leaves no download timeout timer running after the download finishes', async () => {
        jest.useFakeTimers();
        const mockPage = makeMockPage();

        await _waitForDownload(mockPage, makeMockDownloadState(), '', 30000, true);

        expect(jest.getTimerCount()).toBe(0);
    });

    it('cancels the download and fails when it does not finish within the download timeout', async () => {
        expect.assertions(2);
        const download = makeMockDownload({ createReadStream: jest.fn().mockReturnValue(new Promise(() => {})) });
        const mockPage = makeMockPage({ waitForEvent: jest.fn().mockResolvedValue(download) });

        await expect(_waitForDownload(mockPage, makeMockDownloadState(), '', 1, true)).rejects.toThrow(
            'Download failed, Timeout exceeded.',
        );
        expect(download.cancel).toHaveBeenCalledTimes(1);
    });

    it('gives the download only the time left of the download timeout to finish after a slow start', async () => {
        expect.assertions(2);
        jest.useFakeTimers();
        const download = makeMockDownload({
            createReadStream: jest.fn().mockReturnValue(new Promise((resolve) => setTimeout(() => resolve({}), 300))),
        });
        const startsAfter900ms = jest.fn().mockImplementation(async () => {
            jest.setSystemTime(Date.now() + 900);
            return download;
        });
        const mockPage = makeMockPage({ waitForEvent: startsAfter900ms });

        const result = _waitForDownload(mockPage, makeMockDownloadState(), '', 1000, true);
        const assertion = expect(result).rejects.toThrow('Download failed, Timeout exceeded.');
        await jest.advanceTimersByTimeAsync(300);

        await assertion;
        expect(download.cancel).toHaveBeenCalledTimes(1);
    });
});
