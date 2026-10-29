import { describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({ logger: { info: jest.fn(), error: jest.fn(), debug: jest.fn() } }));
jest.mock('../playwright-invoke', () => ({ findLocator: jest.fn() }));
jest.mock('../evaluation', () => ({ highlightAll: jest.fn() }));

import { findLocator } from '../playwright-invoke';
import { commandListeners, ensureRecorder, newBuffers } from '../recorder';
import { countOf, cssSelectorOf, PickerSession, startPick, stopPick } from '../selector-picker';

const flush = () => new Promise((resolve) => setTimeout(resolve, 0));

function fakeContext() {
    return {
        _startRecording: jest.fn(async () => undefined),
        exposeBinding: jest.fn(async () => undefined),
        pages: () => [],
    } as any;
}

describe('commandListeners', () => {
    it('exposes the command binding once and delivers to every active session', async () => {
        const context = fakeContext();
        const recorder = await ensureRecorder(context);
        const picker = newBuffers();
        (await commandListeners(context)).add(picker);
        recorder.active = true;
        picker.active = true;
        context.exposeBinding.mock.calls[0][1]({}, { cmd: 'use' });
        expect(context.exposeBinding).toHaveBeenCalledTimes(1);
        expect(recorder.entries).toEqual([{ command: { cmd: 'use' } }]);
        expect(picker.entries).toEqual([{ command: { cmd: 'use' } }]);
    });

    it('ignores commands for a session that is not running', async () => {
        const context = fakeContext();
        const picker = newBuffers();
        (await commandListeners(context)).add(picker);
        context.exposeBinding.mock.calls[0][1]({}, { cmd: 'use' });
        expect(picker.entries).toEqual([]);
    });
});

function session(pickLocator: () => Promise<unknown>): PickerSession {
    return {
        page: { pickLocator, cancelPickLocator: jest.fn(async () => undefined) } as any,
        buffers: newBuffers(),
        picking: false,
    };
}

function element(css: string, frame: any) {
    return { ownerFrame: async () => frame, evaluate: async () => css };
}

describe('startPick', () => {
    it("keeps Playwright's selector and the css selector of the picked element", async () => {
        const frame = { evaluate: jest.fn(async () => undefined), parentFrame: () => null };
        const s = session(async () => ({
            _selector: 'internal:role=button',
            elementHandle: async () => element('#b', frame),
        }));
        startPick(s);
        expect(s.picking).toBe(true);
        await flush();
        await flush();
        expect(s.picked).toEqual({ selector: 'internal:role=button', css: '#b' });
        expect(s.picking).toBe(false);
    });

    it('reports a failed pick', async () => {
        const s = session(async () => {
            throw new Error('boom');
        });
        startPick(s);
        await flush();
        expect(s.picked).toEqual({ error: 'Error: boom' });
    });

    it('does not report a cancelled pick', async () => {
        let reject: (e: Error) => void = () => undefined;
        const s = session(() => new Promise((_resolve, r) => (reject = r)));
        const cancel = jest.fn(async () => undefined);
        (s.page as any).cancelPickLocator = cancel;
        startPick(s);
        await stopPick(s);
        reject(new Error('Locator picking was cancelled'));
        await flush();
        expect(s.picked).toBeUndefined();
        expect(cancel).toHaveBeenCalled();
    });
});

describe('cssSelectorOf', () => {
    it('joins the selectors of the frames from the outside in', async () => {
        const main = { evaluate: jest.fn(async () => undefined), parentFrame: () => null };
        const inner = {
            evaluate: jest.fn(async () => undefined),
            parentFrame: () => main,
            frameElement: async () => element('iframe#f', main),
        };
        const locator = { elementHandle: async () => element('button.x', inner) } as any;
        expect(await cssSelectorOf(locator)).toBe('iframe#f >>> button.x');
    });
});

describe('countOf', () => {
    it('counts the elements a selector finds', async () => {
        (findLocator as jest.Mock).mockResolvedValueOnce({ count: async () => 3 });
        expect(await countOf({} as any, 'css=button')).toEqual({ count: 3 });
    });

    it('returns the first line of the error for a selector that does not parse', async () => {
        (findLocator as jest.Mock).mockResolvedValueOnce({
            count: async () => {
                throw new Error('Unexpected token\nCall log');
            },
        });
        expect(await countOf({} as any, 'css=[')).toEqual({ error: 'Unexpected token' });
    });
});
