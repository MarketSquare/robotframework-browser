/// <reference types="jest" />

import { describe, expect, it } from '@jest/globals';
import pino, { stdTimeFunctions } from 'pino';

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
