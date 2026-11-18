import { describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({ logger: { info: jest.fn(), error: jest.fn() } }));

import { logger } from '../browser_logger';
import { hasRecordedActionHook, runRecordedActionHooks, runRecordingStartedHooks } from '../recorder-hooks';

beforeEach(() => jest.clearAllMocks());

describe('runRecordedActionHooks', () => {
    const context = {} as any;
    const page = {} as any;
    const click = { name: 'click', selector: '#a', modifiers: 0 };
    const record = (...extensions: any[]) => runRecordedActionHooks(click, page, context, extensions);

    it('keeps the Action without a hook', async () => {
        expect(await record({}, { someKeyword: () => 'x' })).toBe(click);
        expect(hasRecordedActionHook([{}, { someKeyword: () => 'x' }])).toBe(false);
    });

    it('takes a returned Action, also from a promise, and keeps the Action for undefined or null', async () => {
        expect(await record({ __recordedAction: () => ({ ...click, selector: '#b' }) })).toEqual({
            ...click,
            selector: '#b',
        });
        expect(await record({ __recordedAction: async () => ({ name: 'dblclick', selector: '#c' }) })).toEqual({
            name: 'dblclick',
            selector: '#c',
        });
        expect(await record({ __recordedAction: () => undefined })).toBe(click);
        expect(await record({ __recordedAction: async () => null })).toBe(click);
    });

    it('chains the hooks in load order, each on a copy of the previous result', async () => {
        const second = jest.fn(({ action }: any) => ({ ...action, selector: `${action.selector} >> nth=0` }));
        expect(
            await record(
                { __recordedAction: async ({ action }: any) => ({ ...action, selector: '#b' }) },
                {
                    __recordedAction: second,
                },
            ),
        ).toEqual({ ...click, selector: '#b >> nth=0' });
        expect(second).toHaveBeenCalledWith({ action: { ...click, selector: '#b' }, page, context });
    });

    it('keeps keys Browser does not know', async () => {
        const tagged = await record({ __recordedAction: ({ action }: any) => ({ ...action, mine: { why: 'x' } }) });
        expect(tagged).toEqual({ ...click, mine: { why: 'x' } });
    });

    it('never lets a hook change the Action it was given', async () => {
        const deep = { name: 'select', selector: '#s', options: ['1'] };
        await runRecordedActionHooks(deep, page, context, [
            {
                __recordedAction: ({ action }: any) => {
                    action.name = 'fill';
                    action.options.push('2');
                },
            },
        ]);
        expect(deep).toEqual({ name: 'select', selector: '#s', options: ['1'] });
    });

    it.each([
        ['labels', [{ label: 'AMELUNG' }, { label: 'AUDI' }]],
        ['values', [{ value: '14: 6792' }]],
        ['indexes', [{ index: 0 }]],
    ])('lets a select give its options as Playwright option descriptors, by %s', async (_by, options) => {
        const select = { name: 'select', selector: '#s', options: ['14: 6792'] };
        const recorded = await runRecordedActionHooks(select, page, context, [
            { __recordedAction: ({ action }: any) => ({ ...action, options }) },
        ]);
        expect(recorded).toEqual({ ...select, options });
    });

    it('keeps the Action when the hooks take too long', async () => {
        const slow = { __recordedAction: () => new Promise(() => undefined) };
        expect(await runRecordedActionHooks(click, page, context, [slow], 10)).toBe(click);
        expect(logger.info).toHaveBeenCalledWith(expect.stringContaining("took longer than 10 ms, the 'click'"));
    });

    it.each([
        [
            'a throw',
            () => {
                throw new Error('boom');
            },
            'boom',
        ],
        [
            'a rejection',
            async () => {
                throw new Error('gone');
            },
            'gone',
        ],
        ['a string', () => '#b', 'returned string, not an Action'],
        ['an Action of a class', () => new (class Click {})(), 'returned object, not an Action'],
        ['an Action without a name', () => ({ selector: '#b' }), 'without a name'],
        ['an empty selector', () => ({ ...click, selector: ' ' }), 'empty or non-string selector'],
        ['options that are numbers', () => ({ ...click, options: [1] }), 'neither values nor option descriptors'],
        ['an unknown descriptor key', () => ({ ...click, options: [{ title: 'A' }] }), 'neither values'],
        ['descriptors with two keys', () => ({ ...click, options: [{ label: 'A', value: '1' }] }), 'neither values'],
        ['mixed descriptor keys', () => ({ ...click, options: [{ label: 'A' }, { value: '1' }] }), 'neither values'],
        ['values mixed with descriptors', () => ({ ...click, options: ['1', { label: 'A' }] }), 'neither values'],
        ['a negative index', () => ({ ...click, options: [{ index: -1 }] }), 'neither values'],
        ['an Action that is not JSON', () => ({ ...click, size: BigInt(1) }), 'not JSON'],
    ])('logs and ignores %s', async (_why, hook, message) => {
        expect(await record({ __recordedAction: hook })).toBe(click);
        expect(logger.info).toHaveBeenCalledWith(expect.stringContaining(message));
    });
});

describe('runRecordedActionHooks on a pick', () => {
    const context = {} as any;
    const page = {} as any;
    const pick = { name: 'pick', selector: '#a' };

    it('gives the hooks the pick as an Action', async () => {
        const hook = jest.fn(async ({ action }: any) => ({ ...action, selector: '#b' })) as any;
        const recorded = await runRecordedActionHooks(pick, page, context, [{ __recordedAction: hook }]);
        expect(recorded.selector).toBe('#b');
        expect(hook).toHaveBeenCalledWith({ action: pick, page, context });
    });

    it('keeps the pick when a hook drops its selector', async () => {
        const dropped = { __recordedAction: () => ({ name: 'pick' }) };
        expect(await runRecordedActionHooks(pick, page, context, [dropped])).toBe(pick);
        expect(logger.info).toHaveBeenCalledWith(expect.stringContaining('a pick without a selector'));
    });
});

describe('runRecordingStartedHooks', () => {
    it('runs each hook once per context, in load order', async () => {
        const calls: string[] = [];
        const started = (name: string) => jest.fn(async () => void calls.push(name)) as any;
        const first = { __recordingStarted: started('first') };
        const second = { __recordingStarted: started('second') };
        const context = {} as any;
        await runRecordingStartedHooks(context, [first, {}, second]);
        await runRecordingStartedHooks(context, [first, second]);
        expect(calls).toEqual(['first', 'second']);
        expect(first.__recordingStarted).toHaveBeenCalledWith({ context });
        await runRecordingStartedHooks({} as any, [first]);
        expect(first.__recordingStarted).toHaveBeenCalledTimes(2);
    });

    it('fails the session when a hook fails, and runs it again next time', async () => {
        const hook = jest.fn(async () => {
            throw new Error('no binding');
        });
        const context = {} as any;
        const extension = { __recordingStarted: hook };
        await expect(runRecordingStartedHooks(context, [extension])).rejects.toThrow(
            'The __recordingStarted hook of a JS extension failed: Error: no binding',
        );
        await expect(runRecordingStartedHooks(context, [extension])).rejects.toThrow();
        expect(hook).toHaveBeenCalledTimes(2);
    });
});
