import { describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({ logger: { info: jest.fn(), error: jest.fn() } }));

import { logger } from '../browser_logger';
import { hasSelectorHook, pickedSelector, recordedSelector, startRecordingHooks } from '../recorder-hooks';

beforeEach(() => jest.clearAllMocks());

describe('recordedSelector', () => {
    const context = {} as any;
    const page = {} as any;
    const action = { name: 'click', selector: '#a' };
    const rewrite = (...extensions: any[]) => recordedSelector('#a', action, page, context, extensions);

    it('keeps the selector without a hook', async () => {
        expect(await rewrite({}, { someKeyword: () => 'x' })).toBe('#a');
        expect(hasSelectorHook([{}, { someKeyword: () => 'x' }])).toBe(false);
    });

    it('takes a returned string, also from a promise, and keeps the selector for undefined or null', async () => {
        expect(await rewrite({ __recordedSelector: () => '#b' })).toBe('#b');
        expect(await rewrite({ __recordedSelector: async () => '#c' })).toBe('#c');
        expect(await rewrite({ __recordedSelector: () => undefined })).toBe('#a');
        expect(await rewrite({ __recordedSelector: async () => null })).toBe('#a');
    });

    it('chains the hooks in load order, each seeing the previous result', async () => {
        const second = jest.fn((args: any) => `${args.selector} >> nth=0`);
        expect(await rewrite({ __recordedSelector: async () => '#b' }, { __recordedSelector: second })).toBe(
            '#b >> nth=0',
        );
        expect(second).toHaveBeenCalledWith({
            selector: '#b',
            action: { name: 'click', selector: '#b' },
            page,
            context,
        });
    });

    it('passes a null action for a pick', async () => {
        const hook = jest.fn() as any;
        await recordedSelector('#a', null, page, context, [{ __recordedSelector: hook }]);
        expect(hook).toHaveBeenCalledWith({ selector: '#a', action: null, page, context });
    });

    it('never lets a hook change the action itself', async () => {
        await rewrite({
            __recordedSelector: (args: any) => {
                args.action.name = 'fill';
            },
        });
        expect(action).toEqual({ name: 'click', selector: '#a' });
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
        ['a number', () => 1, 'returned number'],
        ['an empty string', () => ' ', 'returned string'],
    ])('logs and ignores %s', async (_why, hook, message) => {
        expect(await rewrite({ __recordedSelector: hook })).toBe('#a');
        expect(logger.info).toHaveBeenCalledWith(expect.stringContaining(message));
    });
});

describe('pickedSelector', () => {
    const context = {} as any;
    const page = { context: () => context } as any;

    it('rewrites a pick with the page and its context', async () => {
        const hook = jest.fn(async () => '#b') as any;
        expect(await pickedSelector('#a', page, [{ __recordedSelector: hook }])).toBe('#b');
        expect(hook).toHaveBeenCalledWith({ selector: '#a', action: null, page, context });
    });

    it('keeps the selector without a hook', async () => {
        expect(await pickedSelector('#a', page, [])).toBe('#a');
    });

    it('keeps the selector when the hooks take too long', async () => {
        const slow = { __recordedSelector: () => new Promise<string>(() => undefined) };
        expect(await pickedSelector('#a', page, [slow], 10)).toBe('#a');
        expect(logger.info).toHaveBeenCalledWith(expect.stringContaining('took longer than 10 ms'));
    });
});

describe('startRecordingHooks', () => {
    it('runs each hook once per context, in load order', async () => {
        const calls: string[] = [];
        const started = (name: string) => jest.fn(async () => void calls.push(name)) as any;
        const first = { __recordingStarted: started('first') };
        const second = { __recordingStarted: started('second') };
        const context = {} as any;
        await startRecordingHooks(context, [first, {}, second]);
        await startRecordingHooks(context, [first, second]);
        expect(calls).toEqual(['first', 'second']);
        expect(first.__recordingStarted).toHaveBeenCalledWith({ context });
        await startRecordingHooks({} as any, [first]);
        expect(first.__recordingStarted).toHaveBeenCalledTimes(2);
    });

    it('fails the session when a hook fails, and runs it again next time', async () => {
        const hook = jest.fn(async () => {
            throw new Error('no binding');
        });
        const context = {} as any;
        const extension = { __recordingStarted: hook };
        await expect(startRecordingHooks(context, [extension])).rejects.toThrow(
            'The __recordingStarted hook of a JS extension failed: Error: no binding',
        );
        await expect(startRecordingHooks(context, [extension])).rejects.toThrow();
        expect(hook).toHaveBeenCalledTimes(2);
    });
});
