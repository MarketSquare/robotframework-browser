/// <reference types="jest" />

import { describe, expect, it } from '@jest/globals';
import { runInNewContext } from 'vm';

import { initScriptSource } from '../init-script';

describe('initScriptSource', () => {
    it('keeps the source as it is without an argument', () => {
        const source = 'window.a = 1;\nwindow.b = 2;';
        expect(initScriptSource(source)).toBe(source);
    });

    it('calls a function with the argument', () => {
        const window: Record<string, unknown> = {};
        const source = initScriptSource('(value) => { window.seed = value }', '{"n": 1, "flags": ["a"]}');
        runInNewContext(source, { window });
        expect(window.seed).toEqual({ n: 1, flags: ['a'] });
    });

    it('rejects statements with an argument', () => {
        expect(() => initScriptSource('window.a = 1; window.b = 2;', '5')).toThrow(
            'With arg, the init script must be one expression',
        );
    });

    it('calls a function from a file that ends with a line comment', () => {
        const window: Record<string, unknown> = {};
        const source = initScriptSource('function (value) {\n    window.seed = value;\n}\n// preload.js', '7');
        runInNewContext(source, { window });
        expect(window.seed).toBe(7);
    });
});
