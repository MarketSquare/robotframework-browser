// Copyright 2020-     Robot Framework Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { status } from '@grpc/grpc-js';
import { errors } from 'playwright';

import { IndexedPage } from '../playwright-state';
import {
    boolResponse,
    emptyWithLog,
    errorResponse,
    getConsoleLogResponse,
    getErrorMessagesResponse,
    intResponse,
    jsonResponse,
    jsResponse,
    keywordsResponse,
    pageReportResponse,
    parseRegExpOrKeepString,
    stringResponse,
} from '../response-util';

function makePage(overrides: Partial<IndexedPage> = {}): IndexedPage {
    return {
        p: {} as any,
        id: 'page-1',
        timestamp: 0,
        pageErrors: [],
        errorIndex: 0,
        consoleMessages: [],
        consoleIndex: 0,
        activeDownloads: new Map(),
        coverage: undefined,
        ...overrides,
    } as IndexedPage;
}

describe('emptyWithLog', () => {
    it('sets the log on the response', () => {
        const response = emptyWithLog('hello log');
        expect(response.getLog()).toBe('hello log');
    });

    it('returns an empty log when given an empty string', () => {
        const response = emptyWithLog('');
        expect(response.getLog()).toBe('');
    });
});

describe('stringResponse', () => {
    it('sets body and log on the response', () => {
        const response = stringResponse('hello body', 'hello log');
        expect(response.getBody()).toBe('hello body');
        expect(response.getLog()).toBe('hello log');
    });
});

describe('jsonResponse', () => {
    it('sets json body and log', () => {
        const response = jsonResponse('{"key":"value"}', 'log message');
        expect(response.getJson()).toBe('{"key":"value"}');
        expect(response.getLog()).toBe('log message');
    });

    it('sets bodyPart to empty string by default', () => {
        const response = jsonResponse('{}', 'log');
        expect(response.getBodypart()).toBe('');
    });

    it('sets bodyPart when provided', () => {
        const response = jsonResponse('{}', 'log', 'part1');
        expect(response.getBodypart()).toBe('part1');
    });
});

describe('intResponse', () => {
    it('sets body and log', () => {
        const response = intResponse(42, 'int log');
        expect(response.getBody()).toBe(42);
        expect(response.getLog()).toBe('int log');
    });

    it('handles zero', () => {
        const response = intResponse(0, 'zero');
        expect(response.getBody()).toBe(0);
    });

    it('handles negative numbers', () => {
        const response = intResponse(-5, 'negative');
        expect(response.getBody()).toBe(-5);
    });
});

describe('boolResponse', () => {
    it('sets body to true and log', () => {
        const response = boolResponse(true, 'bool log');
        expect(response.getBody()).toBe(true);
        expect(response.getLog()).toBe('bool log');
    });

    it('sets body to false', () => {
        const response = boolResponse(false, 'bool log');
        expect(response.getBody()).toBe(false);
    });
});

describe('jsResponse', () => {
    it('JSON-stringifies the result and sets the log', () => {
        const response = jsResponse('script result', 'js log');
        expect(response.getResult()).toBe(JSON.stringify('script result'));
        expect(response.getLog()).toBe('js log');
    });
});

describe('keywordsResponse', () => {
    it('sets keywords, arguments, docs and log', () => {
        const response = keywordsResponse(['kw1', 'kw2'], ['arg1', 'arg2'], ['doc1', 'doc2'], 'kw log');
        expect(response.getKeywordsList()).toEqual(['kw1', 'kw2']);
        expect(response.getKeywordargumentsList()).toEqual(['arg1', 'arg2']);
        expect(response.getKeyworddocumentationsList()).toEqual(['doc1', 'doc2']);
        expect(response.getLog()).toBe('kw log');
    });

    it('handles empty lists', () => {
        const response = keywordsResponse([], [], [], '');
        expect(response.getKeywordsList()).toEqual([]);
        expect(response.getKeywordargumentsList()).toEqual([]);
        expect(response.getKeyworddocumentationsList()).toEqual([]);
    });
});

describe('errorResponse', () => {
    it('returns null for a non-Error value', () => {
        expect(errorResponse('some string')).toBeNull();
        expect(errorResponse(42)).toBeNull();
        expect(errorResponse(null)).toBeNull();
        expect(errorResponse(undefined)).toBeNull();
        expect(errorResponse({ message: 'plain object' })).toBeNull();
    });

    it('returns RESOURCE_EXHAUSTED code for a generic Error', () => {
        const result = errorResponse(new Error('generic error'));
        expect(result).not.toBeNull();
        expect(result!.code).toBe(status.RESOURCE_EXHAUSTED);
    });

    it('includes the error message in the response', () => {
        const result = errorResponse(new Error('the message'));
        expect(result!.message).toContain('the message');
    });

    it('returns DEADLINE_EXCEEDED code for a TimeoutError', () => {
        const result = errorResponse(new errors.TimeoutError('timed out'));
        expect(result).not.toBeNull();
        expect(result!.code).toBe(status.DEADLINE_EXCEEDED);
    });

    it('truncates very long error messages to 5000 characters', () => {
        const longMessage = 'x'.repeat(10000);
        const result = errorResponse(new Error(longMessage));
        expect(result!.message.length).toBeLessThanOrEqual(5000);
    });
});

describe('pageReportResponse', () => {
    it('sets log and page id', () => {
        const page = makePage({ id: 'page-42' });
        const response = pageReportResponse('page log', page);
        expect(response.getLog()).toBe('page log');
        expect(response.getPageid()).toBe('page-42');
    });

    it('serialises console messages to JSON', () => {
        const page = makePage({
            consoleMessages: [
                { time: 1000, type: 'log', text: 'hello', location: { url: 'x', lineNumber: 1, columnNumber: 0 } },
            ] as any,
        });
        const response = pageReportResponse('log', page);
        const parsed = JSON.parse(response.getConsole());
        expect(parsed).toHaveLength(1);
        expect(parsed[0].text).toBe('hello');
        expect(parsed[0].type).toBe('log');
    });

    it('serialises page errors to JSON', () => {
        const err = Object.assign(new Error('boom'), { name: 'Error' });
        const page = makePage({ pageErrors: [err] as any });
        const response = pageReportResponse('log', page);
        const parsed = JSON.parse(response.getErrors());
        expect(parsed).toHaveLength(1);
        expect(parsed[0]).toContain('Error: boom');
    });

    it('handles null page errors gracefully', () => {
        const page = makePage({ pageErrors: [null] as any });
        const response = pageReportResponse('log', page);
        const parsed = JSON.parse(response.getErrors());
        expect(parsed[0]).toBe('unknown error');
    });

    it('returns empty arrays when no messages or errors exist', () => {
        const page = makePage();
        const response = pageReportResponse('log', page);
        expect(JSON.parse(response.getConsole())).toEqual([]);
        expect(JSON.parse(response.getErrors())).toEqual([]);
    });
});

describe('getConsoleLogResponse', () => {
    const messages = [
        { time: 1, type: 'log', text: 'msg1', location: {} },
        { time: 2, type: 'log', text: 'msg2', location: {} },
        { time: 3, type: 'log', text: 'msg3', location: {} },
    ] as any;

    it('returns all messages when fullLog is true', () => {
        const page = makePage({ consoleMessages: messages, consoleIndex: 2 });
        const response = getConsoleLogResponse(page, true, 'log msg');
        expect(JSON.parse(response.getJson())).toHaveLength(3);
    });

    it('returns only new messages since last call when fullLog is false', () => {
        const page = makePage({ consoleMessages: messages, consoleIndex: 1 });
        const response = getConsoleLogResponse(page, false, 'log msg');
        const parsed = JSON.parse(response.getJson());
        expect(parsed).toHaveLength(2);
        expect(parsed[0].text).toBe('msg2');
    });

    it('advances the consoleIndex to the end of the messages', () => {
        const page = makePage({ consoleMessages: messages, consoleIndex: 0 });
        getConsoleLogResponse(page, false, 'log msg');
        expect(page.consoleIndex).toBe(3);
    });

    it('sets the log message', () => {
        const page = makePage();
        const response = getConsoleLogResponse(page, true, 'the log');
        expect(response.getLog()).toBe('the log');
    });
});

describe('getErrorMessagesResponse', () => {
    const errs = [new Error('err1'), new Error('err2'), new Error('err3')] as any;

    it('returns all errors when fullLog is true', () => {
        const page = makePage({ pageErrors: errs, errorIndex: 2 });
        const response = getErrorMessagesResponse(page, true, 'err log');
        expect(JSON.parse(response.getJson())).toHaveLength(3);
    });

    it('returns only new errors since last call when fullLog is false', () => {
        const page = makePage({ pageErrors: errs, errorIndex: 1 });
        const response = getErrorMessagesResponse(page, false, 'err log');
        expect(JSON.parse(response.getJson())).toHaveLength(2);
    });

    it('advances the errorIndex to the end', () => {
        const page = makePage({ pageErrors: errs, errorIndex: 0 });
        getErrorMessagesResponse(page, false, 'log');
        expect(page.errorIndex).toBe(3);
    });

    it('sets the log message', () => {
        const page = makePage();
        const response = getErrorMessagesResponse(page, true, 'the log');
        expect(response.getLog()).toBe('the log');
    });
});

describe('parseRegExpOrKeepString', () => {
    it('returns a plain string when input has no regex delimiters', () => {
        const result = parseRegExpOrKeepString('hello');
        expect(result).toBe('hello');
    });

    it('returns a RegExp for a valid regex pattern', () => {
        const result = parseRegExpOrKeepString('/foo/');
        expect(result).toBeInstanceOf(RegExp);
        expect((result as RegExp).source).toBe('foo');
    });

    it('parses regex flags correctly', () => {
        const result = parseRegExpOrKeepString('/abc/gi') as RegExp;
        expect(result.flags).toContain('g');
        expect(result.flags).toContain('i');
    });

    it('returns the original string when the regex is invalid', () => {
        const result = parseRegExpOrKeepString('/[invalid/');
        expect(typeof result).toBe('string');
        expect(result).toBe('/[invalid/');
    });

    it('returns an empty string as-is', () => {
        const result = parseRegExpOrKeepString('');
        expect(result).toBe('');
    });

    it('handles a pattern with no flags', () => {
        const result = parseRegExpOrKeepString('/\\d+/') as RegExp;
        expect(result).toBeInstanceOf(RegExp);
        expect(result.test('123')).toBe(true);
    });
});
