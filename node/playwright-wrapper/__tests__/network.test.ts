import { beforeEach, describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

jest.mock('uuid', () => ({
    v4: jest.fn().mockReturnValue('mock-uuid-1234'),
}));

import { logger } from '../browser_logger';
import { waitForRequest } from '../network';

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

function makeMockPage(overrides: Partial<{ waitForRequest: jest.Mock }> = {}) {
    const mockRequest = makeMockRequest();
    return {
        waitForRequest: jest.fn().mockResolvedValue(mockRequest),
        ...overrides,
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
