/// <reference types="jest" />

import { afterEach, describe, expect, it } from '@jest/globals';

import {
    clearRFKeywordContext,
    createLogger,
    errorType,
    getRFKeywordContext,
    setRFKeywordContext,
} from '../browser_logger';

function makeStream() {
    const lines: Record<string, unknown>[] = [];
    const stream = {
        write(msg: string) {
            lines.push(JSON.parse(msg));
        },
    };
    return { lines, stream };
}

// Build a logger using the real production factory so tests exercise the same config.
function makeCapture() {
    const { lines, stream } = makeStream();
    const log = createLogger(stream);
    log.level = 'trace';
    return { log, lines };
}

// Same as makeCapture but the logger's mixin picks up the real module-level RF context.
function makeRFCapture() {
    const { lines, stream } = makeStream();
    const log = createLogger(stream);
    log.level = 'trace';
    return { log, lines };
}

describe('browser_logger configuration', () => {
    describe('level field', () => {
        it('emits level as a string not a number', () => {
            const { log, lines } = makeCapture();
            log.info('test message');
            expect(typeof lines[0].level).toBe('string');
        });

        it('emits "info" for info calls', () => {
            const { log, lines } = makeCapture();
            log.info('test');
            expect(lines[0].level).toBe('info');
        });

        it('emits "warn" for warn calls', () => {
            const { log, lines } = makeCapture();
            log.warn('warning');
            expect(lines[0].level).toBe('warn');
        });

        it('emits "error" for error calls', () => {
            const { log, lines } = makeCapture();
            log.error('error message');
            expect(lines[0].level).toBe('error');
        });

        it('emits "debug" for debug calls', () => {
            const { log, lines } = makeCapture();
            log.debug('debug message');
            expect(lines[0].level).toBe('debug');
        });
    });

    describe('base fields', () => {
        it('does not emit hostname', () => {
            const { log, lines } = makeCapture();
            log.info('test');
            expect(lines[0]).not.toHaveProperty('hostname');
        });

        it('does not emit pid', () => {
            const { log, lines } = makeCapture();
            log.info('test');
            expect(lines[0]).not.toHaveProperty('pid');
        });
    });

    describe('mixin fields', () => {
        it('emits component as browser-library', () => {
            const { log, lines } = makeCapture();
            log.info('test');
            expect(lines[0].component).toBe('browser-library');
        });

        it('emits seq as a number', () => {
            const { log, lines } = makeCapture();
            log.info('test');
            expect(typeof lines[0].seq).toBe('number');
        });

        it('seq is monotonically increasing across calls', () => {
            const { log, lines } = makeCapture();
            log.info('first');
            log.info('second');
            log.info('third');
            expect(lines[0].seq as number).toBeLessThan(lines[1].seq as number);
            expect(lines[1].seq as number).toBeLessThan(lines[2].seq as number);
        });

        it('seq increments by 1 for each call', () => {
            const { log, lines } = makeCapture();
            log.info('first');
            log.info('second');
            expect((lines[1].seq as number) - (lines[0].seq as number)).toBe(1);
        });
    });

    describe('standard fields', () => {
        it('emits a time field', () => {
            const { log, lines } = makeCapture();
            log.info('test');
            expect(lines[0]).toHaveProperty('time');
        });

        it('emits msg field with the log message', () => {
            const { log, lines } = makeCapture();
            log.info('hello from test');
            expect(lines[0].msg).toBe('hello from test');
        });
    });
});

describe('RF keyword context', () => {
    afterEach(() => {
        clearRFKeywordContext();
    });

    it('setRFKeywordContext sets kw_name, kw_file, kw_line', () => {
        setRFKeywordContext({ kw_name: 'Click Button', kw_file: 'test.robot', kw_line: 10 });
        const ctx = getRFKeywordContext();
        expect(ctx.kw_name).toBe('Click Button');
        expect(ctx.kw_file).toBe('test.robot');
        expect(ctx.kw_line).toBe(10);
    });

    it('clearRFKeywordContext removes all keyword fields', () => {
        setRFKeywordContext({ kw_name: 'Click Button', kw_file: 'test.robot', kw_line: 10 });
        clearRFKeywordContext();
        const ctx = getRFKeywordContext();
        expect(ctx).not.toHaveProperty('kw_name');
        expect(ctx).not.toHaveProperty('kw_file');
        expect(ctx).not.toHaveProperty('kw_line');
    });

    it('setRFKeywordContext replaces current context and saves previous to stack', () => {
        setRFKeywordContext({ kw_name: 'First Keyword', kw_file: 'suite.robot', kw_line: 5 });
        setRFKeywordContext({ kw_name: 'Second Keyword' });
        const ctx = getRFKeywordContext();
        expect(ctx.kw_name).toBe('Second Keyword');
        expect(ctx).not.toHaveProperty('kw_file');
        expect(ctx).not.toHaveProperty('kw_line');
        clearRFKeywordContext();
        const restored = getRFKeywordContext();
        expect(restored.kw_name).toBe('First Keyword');
        expect(restored.kw_file).toBe('suite.robot');
        expect(restored.kw_line).toBe(5);
    });

    it('keyword fields appear in log lines after setRFKeywordContext', () => {
        const { log, lines } = makeRFCapture();
        setRFKeywordContext({ kw_name: 'Open Browser', kw_file: 'browser.robot', kw_line: 3 });
        log.info('inside keyword');
        expect(lines[0].kw_name).toBe('Open Browser');
        expect(lines[0].kw_file).toBe('browser.robot');
        expect(lines[0].kw_line).toBe(3);
    });

    it('keyword fields are absent from log lines after clearRFKeywordContext', () => {
        const { log, lines } = makeRFCapture();
        setRFKeywordContext({ kw_name: 'Open Browser', kw_file: 'browser.robot', kw_line: 3 });
        clearRFKeywordContext();
        log.info('after keyword');
        expect(lines[0]).not.toHaveProperty('kw_name');
        expect(lines[0]).not.toHaveProperty('kw_file');
        expect(lines[0]).not.toHaveProperty('kw_line');
    });
});

describe('errorType', () => {
    it('returns the constructor name for a standard Error', () => {
        expect(errorType(new Error('boom'))).toBe('Error');
    });

    it('returns the subclass name for Error subclasses', () => {
        expect(errorType(new TypeError('type error'))).toBe('TypeError');
        expect(errorType(new RangeError('range error'))).toBe('RangeError');
    });

    it('returns UnknownError for a thrown string', () => {
        expect(errorType('some string')).toBe('UnknownError');
    });

    it('returns UnknownError for null', () => {
        expect(errorType(null)).toBe('UnknownError');
    });

    it('returns UnknownError for a plain object', () => {
        expect(errorType({ code: 42 })).toBe('UnknownError');
    });
});

describe('setRFKeywordContext – field normalization', () => {
    afterEach(() => {
        clearRFKeywordContext();
    });

    it('omits kw_file from log when normalized to undefined before setting', () => {
        const { log, lines } = makeRFCapture();
        const file = '';
        setRFKeywordContext({ kw_name: 'Click', kw_file: file || undefined });
        log.info('msg');
        expect(lines[0]).not.toHaveProperty('kw_file');
    });

    it('omits kw_line from log when normalized to undefined before setting', () => {
        const { log, lines } = makeRFCapture();
        const line = 0;
        setRFKeywordContext({ kw_name: 'Click', kw_line: line || undefined });
        log.info('msg');
        expect(lines[0]).not.toHaveProperty('kw_line');
    });

    it('emits kw_file when set to a non-empty string', () => {
        const { log, lines } = makeRFCapture();
        setRFKeywordContext({ kw_name: 'Click', kw_file: 'suite.robot' });
        log.info('msg');
        expect(lines[0].kw_file).toBe('suite.robot');
    });

    it('emits kw_line when set to a non-zero number', () => {
        const { log, lines } = makeRFCapture();
        setRFKeywordContext({ kw_name: 'Click', kw_line: 42 });
        log.info('msg');
        expect(lines[0].kw_line).toBe(42);
    });
});

describe('setRFKeywordContext – nested keyword context stack', () => {
    afterEach(() => {
        clearRFKeywordContext();
    });

    it('restores outer keyword context when inner keyword closes', () => {
        const { log, lines } = makeRFCapture();
        setRFKeywordContext({ kw_name: 'Outer Keyword', kw_file: 'outer.robot', kw_line: 10 });
        setRFKeywordContext({ kw_name: 'Inner Keyword', kw_file: 'inner.robot', kw_line: 20 });
        clearRFKeywordContext();
        log.info('after inner closes');
        expect(lines[0].kw_name).toBe('Outer Keyword');
        expect(lines[0].kw_file).toBe('outer.robot');
        expect(lines[0].kw_line).toBe(10);
    });

    it('clears all kw fields after the outermost keyword closes', () => {
        const { log, lines } = makeRFCapture();
        setRFKeywordContext({ kw_name: 'Only Keyword', kw_file: 'test.robot', kw_line: 5 });
        clearRFKeywordContext();
        log.info('after all keywords closed');
        expect(lines[0]).not.toHaveProperty('kw_name');
        expect(lines[0]).not.toHaveProperty('kw_file');
        expect(lines[0]).not.toHaveProperty('kw_line');
    });

    it('handles three levels of nesting correctly', () => {
        const { log, lines } = makeRFCapture();
        setRFKeywordContext({ kw_name: 'Level 1', kw_line: 1 });
        setRFKeywordContext({ kw_name: 'Level 2', kw_line: 2 });
        setRFKeywordContext({ kw_name: 'Level 3', kw_line: 3 });
        clearRFKeywordContext();
        log.info('back at level 2');
        expect(lines[0].kw_name).toBe('Level 2');
        clearRFKeywordContext();
        log.info('back at level 1');
        expect(lines[1].kw_name).toBe('Level 1');
        clearRFKeywordContext();
        log.info('all closed');
        expect(lines[2]).not.toHaveProperty('kw_name');
    });
});
