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

// Suppress log output from the module under test
jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

import { extractArgumentsStringFromJavascript } from '../playwright-state';

describe('extractArgumentsStringFromJavascript', () => {
    it('extracts a single argument', () => {
        const fn = function (page: unknown) {
            return page;
        };
        expect(extractArgumentsStringFromJavascript(fn.toString())).toBe('page');
    });

    it('extracts multiple arguments', () => {
        const fn = function (page: unknown, context: unknown, browser: unknown) {
            return [page, context, browser];
        };
        expect(extractArgumentsStringFromJavascript(fn.toString())).toBe('page, context, browser');
    });

    it('returns an empty string for a function with no arguments', () => {
        const fn = function () {
            return 42;
        };
        expect(extractArgumentsStringFromJavascript(fn.toString())).toBe('');
    });

    it('handles arrow functions with a single argument', () => {
        const fn = (page: unknown) => page;
        expect(extractArgumentsStringFromJavascript(fn.toString())).toBe('page');
    });

    it('handles arrow functions with multiple arguments', () => {
        const fn = (page: unknown, logger: unknown) => [page, logger];
        expect(extractArgumentsStringFromJavascript(fn.toString())).toBe('page, logger');
    });

    it('handles arrow functions with no arguments', () => {
        const fn = () => 42;
        expect(extractArgumentsStringFromJavascript(fn.toString())).toBe('');
    });

    it('strips single-line comments before extracting arguments', () => {
        const javascript = `// my keyword\nfunction myKeyword(page, context) { return page; }`;
        expect(extractArgumentsStringFromJavascript(javascript)).toBe('page, context');
    });

    it('strips block comments before extracting arguments', () => {
        const javascript = `/* @param page */\nfunction myKeyword(page) { return page; }`;
        expect(extractArgumentsStringFromJavascript(javascript)).toBe('page');
    });

    it('collapses newlines so multi-line signatures are parsed correctly', () => {
        const javascript = `function myKeyword(\n  page,\n  context\n) { return page; }`;
        expect(extractArgumentsStringFromJavascript(javascript)).toBe('page, context');
    });

    it('returns *args when the input contains no parentheses', () => {
        expect(extractArgumentsStringFromJavascript('not a function at all')).toBe('*args');
    });

    it('uses the first parenthesised group when multiple exist', () => {
        // The regex is non-greedy and matches the first `(...)`, which is the argument list.
        const fn = function myFn(page: unknown) {
            return String(page).replace(/foo/, 'bar');
        };
        expect(extractArgumentsStringFromJavascript(fn.toString())).toBe('page');
    });
});
