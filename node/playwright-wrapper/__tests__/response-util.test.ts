jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
    errorType: jest.requireActual('../browser_logger').errorType,
}));

import { describe, expect, it } from '@jest/globals';
import { EventEmitter } from 'events';
import { errors, Page } from 'playwright';

import { trackRequests, withLoadReport } from '../load-report';
import { errorResponse, jsonResponse, jsResponse, stringResponse } from '../response-util';

describe('responses built from JSON.stringify output', () => {
    it('keeps a stringified value as it is', () => {
        expect(stringResponse(JSON.stringify('text'), 'log').body).toBe('"text"');
        expect(jsonResponse(JSON.stringify({ a: 1 }), 'log').json).toBe('{"a":1}');
    });

    it('turns a stringified null into the JSON null literal', () => {
        expect(stringResponse(JSON.stringify(null), 'log').body).toBe('null');
        expect(jsonResponse(JSON.stringify(null), 'log').json).toBe('null');
    });

    it('turns a stringified undefined into an empty string', () => {
        expect(stringResponse(JSON.stringify(undefined), 'log').body).toBe('');
        expect(jsonResponse(JSON.stringify(undefined), 'log').json).toBe('');
    });

    it('keeps the log message and body part untouched', () => {
        const response = jsonResponse(JSON.stringify(undefined), 'my log', 'part');
        expect(response.log).toBe('my log');
        expect(response.bodyPart).toBe('part');
    });
});

describe('jsResponse', () => {
    it('stringifies the evaluation result', () => {
        expect(jsResponse('text', 'log').result).toBe('"text"');
        expect(jsResponse(2 as unknown as string, 'log').result).toBe('2');
        expect(jsResponse(null as unknown as string, 'log').result).toBe('null');
    });

    it('returns an empty result when the JavaScript returned undefined', () => {
        expect(jsResponse(undefined as unknown as string, 'log').result).toBe('');
    });
});

describe('errorResponse', () => {
    it('sends the load report of a timed-out wait as UTF-8 metadata', async () => {
        const page = Object.assign(new EventEmitter(), {
            mainFrame: () => undefined,
            url: () => 'http://localhost/ä.html',
        });
        trackRequests(page as unknown as Page);
        page.emit('request', {
            url: () => 'http://localhost/slowpage.html',
            method: () => 'GET',
            resourceType: () => 'document',
            isNavigationRequest: () => true,
            frame: () => undefined,
        });
        const timeout = new errors.TimeoutError('page.goto: Timeout 1000ms exceeded.');
        await withLoadReport(page as unknown as Page, () => Promise.reject(timeout)).catch(() => undefined);

        const response = errorResponse(timeout);

        const [report] = response?.metadata?.get('load-report-bin') ?? [];
        expect((report as Buffer).toString('utf8')).toContain('URL: http://localhost/ä.html');
        expect(response?.message).toBe('TimeoutError: page.goto: Timeout 1000ms exceeded.');
    });

    it('sends no metadata for an error without a load report', () => {
        expect(errorResponse(new Error('boom'))?.metadata).toBeUndefined();
    });
});
