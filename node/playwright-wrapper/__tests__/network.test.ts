import { afterEach, beforeEach, describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

jest.mock('uuid', () => ({
    v4: jest.fn().mockReturnValue('mock-uuid-1234'),
}));

import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';

import { _waitForDownload, httpRequest, waitForRequest, waitForResponse } from '../network';

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

async function capturedRequest(request: any = makeMockRequest(), waitForAllFields = false) {
    const [first] = await waitForRequest({ ...makeRequest(), waitForAllFields }, pageWithRequest(request));
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

    it('fails when asked to wait for all fields and the headers cannot be read', async () => {
        expect.assertions(1);
        const request = makeMockRequest({ allHeaders: jest.fn().mockRejectedValue(new Error('Target closed')) });

        await expect(capturedRequest(request, true)).rejects.toThrow('Target closed');
    });

    it('returns at once without the headers that are known only later', async () => {
        const request = makeMockRequest();

        const parsed = await capturedRequest(request);

        expect(request.allHeaders).not.toHaveBeenCalled();
        expect(parsed.allHeaders).toBeNull();
        expect(parsed.headersArray).toBeNull();
    });

    it('returns all headers when asked to wait for all fields', async () => {
        const parsed = await capturedRequest(makeMockRequest(), true);

        expect(parsed.allHeaders).toEqual({ 'content-type': 'application/json', cookie: 'session=1' });
        expect(parsed.headersArray).toEqual([{ name: 'content-type', value: 'application/json' }]);
    });

    it('fails when all fields do not arrive within the timeout', async () => {
        expect.assertions(1);
        const request = makeMockRequest({ allHeaders: jest.fn(() => new Promise(() => {})) });

        await expect(
            waitForRequest({ ...makeRequest('/.*/', 20), waitForAllFields: true }, pageWithRequest(request)),
        ).rejects.toThrow('Timeout 20ms exceeded while waiting for all fields of the request.');
    });

    it('sends the raw post data in postDataBytes', async () => {
        const request = makeMockRequest({ postData: jest.fn().mockReturnValue('{"key": "value"}') });

        const messages = await waitForRequest(makeRequest(), pageWithRequest(request));

        expect(messages).toHaveLength(1);
        expect(messages[0].postDataBytes.toString('utf8')).toBe('{"key": "value"}');
        expect(JSON.parse(messages[0].json).hasPostData).toBe(true);
    });

    it('sends the post data only as bytes, so a large body fits one gRPC message', async () => {
        const request = makeMockRequest({ postData: jest.fn().mockReturnValue('{"key": "value"}') });

        const [first] = await waitForRequest(makeRequest(), pageWithRequest(request));

        expect(JSON.parse(first.json)).not.toHaveProperty('postData');
    });

    it('flags a request without post data', async () => {
        const parsed = await capturedRequest();

        expect(parsed.hasPostData).toBe(false);
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
    overrides: Partial<{
        body: jest.Mock;
        httpVersion: jest.Mock;
        status: jest.Mock;
        headers: jest.Mock;
        allHeaders: jest.Mock;
    }> = {},
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
            },
        });
        expect(JSON.parse(first.json).request).not.toHaveProperty('postData');
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

    it('sends an empty body as a single message that has a body', async () => {
        const messages = await capturedResponse(
            makeMockResponse({ body: jest.fn().mockResolvedValue(Buffer.alloc(0)) }),
        );

        expect(messages).toHaveLength(1);
        expect(messages[0].bodyBytes).toHaveLength(0);
        expect(JSON.parse(messages[0].json).hasBody).toBe(true);
    });

    it('flags the body as missing when it cannot be read', async () => {
        const messages = await capturedResponse(
            makeMockResponse({ body: jest.fn().mockRejectedValue(new Error('body unavailable')) }),
        );

        expect(messages).toHaveLength(1);
        expect(JSON.parse(messages[0].json).hasBody).toBe(false);
    });

    it('does not read the body when it is excluded', async () => {
        const response = makeMockResponse();

        const messages = await capturedResponse(response, true);

        expect(response.body).not.toHaveBeenCalled();
        expect(messages[0].bodyBytes).toHaveLength(0);
        expect(JSON.parse(messages[0].json).hasBody).toBe(false);
    });

    it('does not wait for the fields that some browsers report only after the body when it is excluded', async () => {
        const response = makeMockResponse();

        const [first] = await capturedResponse(response, true);

        expect(response.httpVersion).not.toHaveBeenCalled();
        expect(response.serverAddr).not.toHaveBeenCalled();
        expect(response.securityDetails).not.toHaveBeenCalled();
        expect(JSON.parse(first.json)).toMatchObject({ httpVersion: null, serverAddr: null, securityDetails: null });
    });

    it('fails when the response fields do not arrive within the timeout', async () => {
        expect.assertions(1);
        const response = makeMockResponse({ body: jest.fn(() => new Promise(() => {})) });

        await expect(
            waitForResponse(
                makeRequest('/.*/', 20),
                makeMockPage({ waitForResponse: jest.fn().mockResolvedValue(response) }),
            ),
        ).rejects.toThrow('Timeout 20ms exceeded while waiting for all fields of the response.');
    });

    it.each([
        ['a 204 response', { status: jest.fn().mockReturnValue(204) }],
        ['a 304 response', { status: jest.fn().mockReturnValue(304) }],
        ['a response with content-length 0', { headers: jest.fn().mockReturnValue({ 'content-length': '0' }) }],
    ])('returns an empty body for %s whose body the browser did not keep', async (_, overrides) => {
        const missing = jest.fn().mockRejectedValue(new Error('Missing content of resource for given requestId'));

        const [first] = await capturedResponse(makeMockResponse({ body: missing, ...overrides }));

        expect(first.bodyBytes).toHaveLength(0);
        expect(JSON.parse(first.json).hasBody).toBe(true);
    });

    it('returns no body for a redirect with content-length 0 whose body cannot be read', async () => {
        const unavailable = jest
            .fn()
            .mockRejectedValue(new Error('Response body is unavailable for redirect responses'));

        const [first] = await capturedResponse(
            makeMockResponse({
                body: unavailable,
                status: jest.fn().mockReturnValue(302),
                headers: jest.fn().mockReturnValue({ 'content-length': '0' }),
            }),
        );

        expect(first.bodyBytes).toHaveLength(0);
        expect(JSON.parse(first.json).hasBody).toBe(false);
    });

    it('returns no headers instead of partial ones when all headers cannot be read', async () => {
        const [first] = await capturedResponse(
            makeMockResponse({ allHeaders: jest.fn().mockRejectedValue(new Error('Target closed')) }),
        );

        const meta = JSON.parse(first.json);
        expect(meta.allHeaders).toBeNull();
        expect(meta.headersArray).toBeNull();
    });

    it('returns no body when a response with content cannot be read', async () => {
        const missing = jest.fn().mockRejectedValue(new Error('Target closed'));

        const [first] = await capturedResponse(makeMockResponse({ body: missing }));

        expect(JSON.parse(first.json).hasBody).toBe(false);
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

    it('logs a chunked body once, in the first message', async () => {
        const body = Buffer.alloc(1_500_000, 'x');

        const messages = await capturedResponse(makeMockResponse({ body: jest.fn().mockResolvedValue(body) }));

        expect(messages[0].log).toBe('Response received, sent in 2 chunks');
        expect(messages[1].log).toBe('');
    });

    it('logs a body that fits in one message without a chunk count', async () => {
        const [only] = await capturedResponse(makeMockResponse());

        expect(only.log).toBe('Response received');
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
            createReadStream: jest.fn(() => new Promise((resolve) => setTimeout(() => resolve({}), 300))),
        });
        const startsAfter900ms = jest.fn().mockImplementation(async () => {
            jest.advanceTimersByTime(900);
            return download;
        });
        const mockPage = makeMockPage({ waitForEvent: startsAfter900ms });

        const result = _waitForDownload(mockPage, makeMockDownloadState(), '', 1000, true);
        const assertion = expect(result).rejects.toThrow('Download failed, Timeout exceeded.');
        await jest.advanceTimersByTimeAsync(300);

        await assertion;
        expect(download.cancel).toHaveBeenCalledTimes(1);
    });

    it('keeps the download timeout when the wall clock jumps forward', async () => {
        jest.useFakeTimers();
        const download = makeMockDownload({
            createReadStream: jest.fn(() => new Promise((resolve) => setTimeout(() => resolve({}), 300))),
        });
        const wallClockJumpsAnHour = jest.fn().mockImplementation(async () => {
            jest.setSystemTime(Date.now() + 3_600_000);
            return download;
        });
        const mockPage = makeMockPage({ waitForEvent: wallClockJumpsAnHour });

        const result = _waitForDownload(mockPage, makeMockDownloadState(), '', 1000, true);
        await jest.advanceTimersByTimeAsync(300);

        expect(JSON.parse((await result).json).state).toBe('finished');
        expect(download.cancel).not.toHaveBeenCalled();
    });
});

function makeHttpRequest(overrides: Record<string, unknown> = {}) {
    return {
        url: '/api/echo',
        method: 'POST',
        headers: '{}',
        form: [],
        multipart: [],
        timeout: 0,
        ...overrides,
    } as any;
}

function makeFetchResult(overrides: Record<string, unknown> = {}) {
    return {
        timedOut: false,
        status: 200,
        statusText: 'OK',
        url: 'http://localhost/api/echo',
        ok: true,
        redirected: false,
        type: 'basic',
        headers: { 'content-type': 'text/plain' },
        body: new Uint8Array([104, 105]),
        ...overrides,
    };
}

function makeFetchPage(result = makeFetchResult()) {
    return { evaluate: jest.fn().mockResolvedValue(result) } as any;
}

function fetchArguments(page: any) {
    return page.evaluate.mock.calls[0][1];
}

describe('httpRequest', () => {
    it('passes only the given fetch options to RequestInit, falsy ones included', async () => {
        const page = makeFetchPage();
        await httpRequest(makeHttpRequest({ keepalive: false, referrer: '', mode: 'no-cors' }), page);
        expect(fetchArguments(page).init).toEqual({
            method: 'POST',
            headers: {},
            keepalive: false,
            referrer: '',
            mode: 'no-cors',
        });
    });

    it('sends form fields as name and value pairs in the given order', async () => {
        const page = makeFetchPage();
        const form = [
            { name: 'q', value: 'a&b' },
            { name: 'lang', value: 'en' },
        ];
        await httpRequest(makeHttpRequest({ form }), page);
        expect(fetchArguments(page).form).toEqual([
            ['q', 'a&b'],
            ['lang', 'en'],
        ]);
    });

    it('sends no form when no field is given', async () => {
        const page = makeFetchPage();
        await httpRequest(makeHttpRequest(), page);
        expect(fetchArguments(page).form).toBeUndefined();
    });

    it('reads a multipart file from its path', async () => {
        const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'http-')), 'notes.txt');
        fs.writeFileSync(file, 'hello');
        const page = makeFetchPage();
        await httpRequest(
            makeHttpRequest({
                multipart: [{ name: 'file', path: file, fileName: 'notes.txt', mimeType: 'text/plain' }],
            }),
            page,
        );
        const [field] = fetchArguments(page).multipart;
        expect(field).toEqual({
            name: 'file',
            fileName: 'notes.txt',
            mimeType: 'text/plain',
            buffer: new Uint8Array(Buffer.from('hello')),
        });
    });

    it('sends a multipart value as text', async () => {
        const page = makeFetchPage();
        await httpRequest(makeHttpRequest({ multipart: [{ name: 'count', value: '3' }] }), page);
        expect(fetchArguments(page).multipart).toEqual([{ name: 'count', value: '3' }]);
    });

    it('fails with the timeout in milliseconds when the fetch timed out', async () => {
        const page = makeFetchPage({ timedOut: true } as any);
        await expect(httpRequest(makeHttpRequest({ timeout: 500 }), page)).rejects.toThrow(
            'Timeout 500ms exceeded while waiting for the response of /api/echo.',
        );
    });

    it('returns the response metadata and the raw body bytes', async () => {
        const [message] = await httpRequest(makeHttpRequest(), makeFetchPage());
        expect(JSON.parse(message.json)).toEqual({
            status: 200,
            statusText: 'OK',
            ok: true,
            url: 'http://localhost/api/echo',
            headers: JSON.stringify({ 'content-type': 'text/plain' }),
            redirected: false,
            type: 'basic',
        });
        expect(Buffer.from(message.bodyBytes)).toEqual(Buffer.from('hi'));
    });
});
