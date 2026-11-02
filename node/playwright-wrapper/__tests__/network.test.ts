import { afterEach, beforeEach, describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

jest.mock('uuid', () => ({
    v4: jest.fn().mockReturnValue('mock-uuid-1234'),
}));

import { _waitForDownload, waitForRequest, waitForResponse } from '../network';

function makeRequest(urlOrPredicate = '/.*/', timeout = 5000, excludeBody = false) {
    return { urlOrPredicate, timeout, excludeBody } as any;
}

function makeMockRequest(
    overrides: Partial<{
        url: jest.Mock;
        method: jest.Mock;
        headers: jest.Mock;
        allHeaders: jest.Mock;
        headersArray: jest.Mock;
        postData: jest.Mock;
        postDataBuffer: jest.Mock;
        redirectedFrom: jest.Mock;
        redirectedTo: jest.Mock;
        frame: jest.Mock;
    }> = {},
) {
    const postData = overrides.postData ?? jest.fn().mockReturnValue(null);
    return {
        url: jest.fn().mockReturnValue('https://example.com/api'),
        method: jest.fn().mockReturnValue('POST'),
        headers: jest.fn().mockReturnValue({ 'content-type': 'application/json' }),
        allHeaders: jest.fn().mockResolvedValue({ 'content-type': 'application/json', cookie: 'session=1' }),
        headersArray: jest.fn().mockResolvedValue([{ name: 'content-type', value: 'application/json' }]),
        postDataBuffer: jest.fn(() => {
            const text = postData();
            return text === null ? null : Buffer.from(text, 'utf8');
        }),
        resourceType: jest.fn().mockReturnValue('fetch'),
        isNavigationRequest: jest.fn().mockReturnValue(false),
        redirectedFrom: jest.fn().mockReturnValue(null),
        redirectedTo: jest.fn().mockReturnValue(null),
        frame: jest.fn().mockReturnValue({ url: () => 'https://example.com/', name: () => '' }),
        ...overrides,
        postData,
    } as any;
}

function makeMockPage(
    overrides: Partial<{ waitForRequest: jest.Mock; waitForResponse: jest.Mock; waitForEvent: jest.Mock }> = {},
) {
    const mockRequest = makeMockRequest();
    return {
        waitForRequest: jest.fn().mockResolvedValue(mockRequest),
        waitForEvent: jest.fn().mockResolvedValue(makeMockDownload()),
        ...overrides,
    } as any;
}

function pageWithRequest(request: any) {
    return makeMockPage({ waitForRequest: jest.fn().mockResolvedValue(request) });
}

async function capturedRequest(request: any = makeMockRequest()) {
    const [first] = await waitForRequest(makeRequest(), pageWithRequest(request));
    return JSON.parse(first.json);
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
        const parsed = await capturedRequest(
            makeMockRequest({ postData: jest.fn().mockReturnValue('{"key": "value"}') }),
        );

        expect(parsed.url).toBe('https://example.com/api');
        expect(parsed.method).toBe('POST');
        expect(parsed.postData).toEqual({ key: 'value' });
    });

    it('returns request data with raw postData when JSON parsing fails', async () => {
        const parsed = await capturedRequest(
            makeMockRequest({ postData: jest.fn().mockReturnValue('invalid json {') }),
        );

        expect(parsed.postData).toBe('invalid json {');
    });

    it('returns request data with binary data in postData', async () => {
        const binaryData = '\x00\x01\x02\x03\xFF\xFE';

        const parsed = await capturedRequest(makeMockRequest({ postData: jest.fn().mockReturnValue(binaryData) }));

        expect(parsed.postData).toBe(binaryData);
    });

    it('returns request data with null postData when postData is empty', async () => {
        const parsed = await capturedRequest();

        expect(parsed.postData).toBeNull();
    });

    it('parses JSON postData regardless of the request content type', async () => {
        const parsed = await capturedRequest(
            makeMockRequest({
                headers: jest.fn().mockReturnValue({ 'content-type': 'text/plain' }),
                postData: jest.fn().mockReturnValue('42'),
            }),
        );

        expect(parsed.postData).toBe(42);
    });

    it('handles headers without special characters', async () => {
        const headers = {
            'content-type': 'application/json',
            authorization: 'Bearer token123',
            'user-agent': 'Mozilla/5.0',
        };

        const parsed = await capturedRequest(makeMockRequest({ headers: jest.fn().mockReturnValue(headers) }));

        expect(parsed.headers).toEqual(headers);
    });

    it('returns the Playwright request details', async () => {
        const parsed = await capturedRequest(
            makeMockRequest({
                redirectedFrom: jest.fn().mockReturnValue({ url: () => 'https://example.com/old' }),
            }),
        );

        expect(parsed).toMatchObject({
            allHeaders: { 'content-type': 'application/json', cookie: 'session=1' },
            headersArray: [{ name: 'content-type', value: 'application/json' }],
            resourceType: 'fetch',
            isNavigationRequest: false,
            redirectedFrom: 'https://example.com/old',
            redirectedTo: null,
            frame: { url: 'https://example.com/', name: '' },
        });
    });

    it('returns no frame when Playwright cannot tell the frame', async () => {
        const parsed = await capturedRequest(
            makeMockRequest({
                frame: jest.fn(() => {
                    throw new Error('Service Worker requests do not have an associated frame');
                }),
            }),
        );

        expect(parsed.frame).toBeNull();
    });

    it('falls back to the plain headers when all headers cannot be read', async () => {
        const parsed = await capturedRequest(
            makeMockRequest({ allHeaders: jest.fn().mockRejectedValue(new Error('Target closed')) }),
        );

        expect(parsed.allHeaders).toEqual({ 'content-type': 'application/json' });
    });

    it('sends the raw post data in postDataBytes', async () => {
        const request = makeMockRequest({ postData: jest.fn().mockReturnValue('{"key": "value"}') });

        const messages = await waitForRequest(makeRequest(), pageWithRequest(request));

        expect(messages).toHaveLength(1);
        expect(messages[0].postDataBytes.toString('utf8')).toBe('{"key": "value"}');
        expect(JSON.parse(messages[0].json)).not.toHaveProperty('postDataBuffer');
    });

    it('marks postDataBuffer as null when the request has no post data', async () => {
        const parsed = await capturedRequest();

        expect(parsed.postDataBuffer).toBeNull();
    });

    it('splits post data over the chunk size and sends the metadata only once', async () => {
        const postData = 'x'.repeat(1_500_000);
        const request = makeMockRequest({ postData: jest.fn().mockReturnValue(postData) });

        const messages = await waitForRequest(makeRequest(), pageWithRequest(request));

        expect(messages).toHaveLength(2);
        expect(Buffer.concat(messages.map((message) => message.postDataBytes)).toString('utf8')).toBe(postData);
        expect(messages[1].json).toBe('');
    });

    it('throws when JSON.stringify fails due to circular references in headers', async () => {
        expect.assertions(1);
        const circularObject: any = { key: 'value' };
        circularObject.self = circularObject;
        const request = makeMockRequest({ headers: jest.fn().mockReturnValue(circularObject) });

        await expect(waitForRequest(makeRequest(), pageWithRequest(request))).rejects.toThrow(TypeError);
    });

    it('throws when JSON.stringify fails due to non-serializable toJSON method', async () => {
        expect.assertions(1);
        const badToJsonObject = {
            'content-type': 'application/json',
            toJSON() {
                throw new Error('Cannot serialize this header');
            },
        };
        const request = makeMockRequest({ headers: jest.fn().mockReturnValue(badToJsonObject) });

        await expect(waitForRequest(makeRequest(), pageWithRequest(request))).rejects.toThrow(
            'Cannot serialize this header',
        );
    });

    it('uses string matcher in response log message', async () => {
        const [first] = await waitForRequest(makeRequest('https://example.com/api'), makeMockPage());

        expect(first.log).toContain('matcher: https://example.com/api');
    });

    it('parses regex string matcher and includes it in response log', async () => {
        const mockWaitForRequest = jest.fn().mockResolvedValue(makeMockRequest());

        const [first] = await waitForRequest(makeRequest('/api/users/\\d+/'), {
            waitForRequest: mockWaitForRequest,
        } as any);

        const passedMatcher = mockWaitForRequest.mock.calls[0][0];
        expect(passedMatcher).toBeInstanceOf(RegExp);
        expect(first.log).toContain(`matcher: ${(passedMatcher as RegExp).toString()}`);
    });

    it('includes timeout in response message', async () => {
        const [first] = await waitForRequest(makeRequest('.*', 10000), makeMockPage());

        expect(first.log).toContain('10000ms');
    });
});

function makeMockResponse(
    overrides: Partial<{ body: jest.Mock; httpVersion: jest.Mock }> = {},
    request: any = makeMockRequest({ postData: jest.fn().mockReturnValue('{"name":"George"}') }),
) {
    return {
        status: jest.fn().mockReturnValue(200),
        headers: jest.fn().mockReturnValue({ 'content-type': 'application/json' }),
        allHeaders: jest.fn().mockResolvedValue({ 'content-type': 'application/json', 'set-cookie': 'session=1' }),
        headersArray: jest.fn().mockResolvedValue([{ name: 'set-cookie', value: 'session=1' }]),
        statusText: jest.fn().mockReturnValue('OK'),
        url: jest.fn().mockReturnValue('https://example.com/api'),
        ok: jest.fn().mockReturnValue(true),
        body: jest.fn().mockResolvedValue(Buffer.from('{"greeting":"HELLO"}', 'utf8')),
        httpVersion: jest.fn().mockResolvedValue('HTTP/1.1'),
        serverAddr: jest.fn().mockResolvedValue({ ipAddress: '127.0.0.1', port: 8080 }),
        securityDetails: jest.fn().mockResolvedValue(null),
        fromServiceWorker: jest.fn().mockReturnValue(false),
        request: jest.fn().mockReturnValue(request),
        ...overrides,
    } as any;
}

async function capturedResponse(response: any = makeMockResponse(), excludeBody = false) {
    return waitForResponse(
        makeRequest('/.*/', 5000, excludeBody),
        makeMockPage({ waitForResponse: jest.fn().mockResolvedValue(response) }),
    );
}

describe('waitForResponse', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('returns at least the legacy response metadata with headers serialized as JSON strings', async () => {
        const [first] = await capturedResponse();

        expect(JSON.parse(first.json)).toMatchObject({
            status: 200,
            headers: '{"content-type":"application/json"}',
            statusText: 'OK',
            url: 'https://example.com/api',
            ok: true,
            request: {
                headers: '{"content-type":"application/json"}',
                method: 'POST',
                postData: '{"name":"George"}',
            },
        });
    });

    it('returns the Playwright response details', async () => {
        const [first] = await capturedResponse();

        expect(JSON.parse(first.json)).toMatchObject({
            allHeaders: { 'content-type': 'application/json', 'set-cookie': 'session=1' },
            headersArray: [{ name: 'set-cookie', value: 'session=1' }],
            httpVersion: 'HTTP/1.1',
            serverAddr: { ipAddress: '127.0.0.1', port: 8080 },
            securityDetails: null,
            fromServiceWorker: false,
        });
    });

    it('nests the same request details that waitForRequest returns', async () => {
        const [first] = await capturedResponse();

        expect(JSON.parse(first.json).request).toMatchObject({
            url: 'https://example.com/api',
            resourceType: 'fetch',
            isNavigationRequest: false,
            redirectedFrom: null,
            frame: { url: 'https://example.com/', name: '' },
        });
    });

    it('sends the raw body in bodyBytes and the raw request post data in postDataBytes', async () => {
        const binary = Buffer.from('89504e470d0a1a0a', 'hex');

        const messages = await capturedResponse(makeMockResponse({ body: jest.fn().mockResolvedValue(binary) }));

        expect(messages).toHaveLength(1);
        expect(Buffer.compare(messages[0].bodyBytes, binary)).toBe(0);
        expect(messages[0].postDataBytes.toString('utf8')).toBe('{"name":"George"}');
    });

    it('sends an empty body as a single message without a body marker', async () => {
        const messages = await capturedResponse(
            makeMockResponse({ body: jest.fn().mockResolvedValue(Buffer.alloc(0)) }),
        );

        expect(messages).toHaveLength(1);
        expect(messages[0].bodyBytes).toHaveLength(0);
        expect(JSON.parse(messages[0].json)).not.toHaveProperty('body');
    });

    it('marks the body as null when it cannot be read', async () => {
        const messages = await capturedResponse(
            makeMockResponse({ body: jest.fn().mockRejectedValue(new Error('body unavailable')) }),
        );

        expect(messages).toHaveLength(1);
        expect(JSON.parse(messages[0].json).body).toBeNull();
    });

    it('does not read the body when it is excluded', async () => {
        const response = makeMockResponse();

        const messages = await capturedResponse(response, true);

        expect(response.body).not.toHaveBeenCalled();
        expect(messages[0].bodyBytes).toHaveLength(0);
        expect(JSON.parse(messages[0].json).body).toBeNull();
    });

    it('returns a null HTTP version when Playwright cannot read it', async () => {
        const [first] = await capturedResponse(
            makeMockResponse({ httpVersion: jest.fn().mockRejectedValue(new Error('Target closed')) }),
        );

        expect(JSON.parse(first.json).httpVersion).toBeNull();
    });

    it('splits a body over the chunk size and sends the metadata only once', async () => {
        const body = Buffer.alloc(1_500_000, 'x');

        const messages = await capturedResponse(makeMockResponse({ body: jest.fn().mockResolvedValue(body) }));

        expect(messages).toHaveLength(2);
        expect(Buffer.compare(Buffer.concat(messages.map((message) => message.bodyBytes)), body)).toBe(0);
        expect(JSON.parse(messages[0].json).status).toBe(200);
        expect(messages[1].json).toBe('');
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
