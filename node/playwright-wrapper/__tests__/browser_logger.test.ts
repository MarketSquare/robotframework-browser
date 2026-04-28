/// <reference types="jest" />

import { afterEach, describe, expect, it } from '@jest/globals';
import pino, { stdTimeFunctions } from 'pino';

import { clearRFKeywordContext, errorType, getRFKeywordContext, setRFKeywordContext } from '../browser_logger';

// Build a fresh pino instance with the same configuration as browser_logger.ts
// but writing to a captured in-memory stream so tests are isolated and synchronous.
function makeCapture() {
    let seq = 0;
    const lines: Record<string, unknown>[] = [];
    const stream = {
        write(msg: string) {
            lines.push(JSON.parse(msg));
        },
    };
    const log = pino(
        {
            timestamp: stdTimeFunctions.isoTime,
            level: 'trace',
            base: null,
            formatters: {
                level(label: string) {
                    return { level: label };
                },
            },
            mixin() {
                return {
                    seq: ++seq,
                    component: 'browser-library',
                };
            },
        },
        stream,
    );
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

// Build a pino instance whose mixin reads from the real module-level RF context so
// we can verify that setRFKeywordContext / clearRFKeywordContext are reflected in log lines.
function makeRFCapture() {
    const lines: Record<string, unknown>[] = [];
    const stream = {
        write(msg: string) {
            lines.push(JSON.parse(msg));
        },
    };
    let seq = 0;
    const log = pino(
        {
            timestamp: stdTimeFunctions.isoTime,
            level: 'trace',
            base: null,
            formatters: {
                level(label: string) {
                    return { level: label };
                },
            },
            mixin() {
                return {
                    seq: ++seq,
                    component: 'browser-library',
                    ...getRFKeywordContext(),
                };
            },
        },
        stream,
    );
    return { log, lines };
}

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

    it('setRFKeywordContext only updates provided fields', () => {
        setRFKeywordContext({ kw_name: 'First Keyword', kw_file: 'suite.robot', kw_line: 5 });
        setRFKeywordContext({ kw_name: 'Second Keyword' });
        const ctx = getRFKeywordContext();
        expect(ctx.kw_name).toBe('Second Keyword');
        expect(ctx.kw_file).toBe('suite.robot');
        expect(ctx.kw_line).toBe(5);
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
