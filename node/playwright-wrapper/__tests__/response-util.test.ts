/// <reference types="jest" />

import { describe, expect, it } from '@jest/globals';

import { jsonResponse, jsResponse, stringResponse } from '../response-util';

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
