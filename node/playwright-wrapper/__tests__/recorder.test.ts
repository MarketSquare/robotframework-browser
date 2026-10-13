import { describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({ logger: { info: jest.fn(), error: jest.fn() } }));

import { drain, ensureRecorder, isToolbarAction, toAction, TOOLBAR_TAG, toolbarScript } from '../recorder';

describe('toAction', () => {
    it('unwraps the 1.62 ActionInContext shape', () => {
        expect(toAction({ action: { name: 'click', selector: '#a' }, pageGuid: 'p' })).toEqual({
            name: 'click',
            selector: '#a',
        });
    });
    it('accepts the bare 1.63 Action and drops ariaSnapshot', () => {
        expect(toAction({ name: 'fill', text: 'x', ariaSnapshot: 'big' })).toEqual({ name: 'fill', text: 'x' });
    });
    it('rejects garbage', () => {
        expect(toAction(null)).toBeNull();
        expect(toAction({ action: { selector: '#a' } })).toBeNull();
    });
});

describe('isToolbarAction', () => {
    it('matches actions on the toolbar host', () => {
        expect(isToolbarAction({ name: 'click', selector: `internal:role=button >> ${TOOLBAR_TAG}` })).toBe(true);
        expect(isToolbarAction({ name: 'click', selector: '#other' })).toBe(false);
    });
});

describe('drain', () => {
    it('empties in place', () => {
        const list = [1, 2];
        expect(drain(list)).toEqual([1, 2]);
        expect(list).toEqual([]);
    });
});

describe('toolbarScript', () => {
    it('is a self-invoking script that defines the toolbar tag', () => {
        const source = toolbarScript();
        expect(source).toContain(TOOLBAR_TAG);
        // eslint-disable-next-line @typescript-eslint/no-implied-eval
        expect(() => new Function(source)).not.toThrow();
    });
});

describe('ensureRecorder', () => {
    function fakeContext() {
        const sinks: any[] = [];
        return {
            sinks,
            _enableRecorder: jest.fn(async (_params: unknown, sink: unknown) => {
                sinks.push(sink);
            }),
            exposeBinding: jest.fn(async () => undefined),
        } as any;
    }

    it('enables the recorder once per context', async () => {
        const context = fakeContext();
        await ensureRecorder(context);
        await ensureRecorder(context);
        expect(context._enableRecorder).toHaveBeenCalledTimes(1);
        expect(context.exposeBinding).toHaveBeenCalledTimes(1);
    });

    it('buffers actions, updates and signals, but not toolbar actions', async () => {
        const context = fakeContext();
        const state = await ensureRecorder(context);
        const sink = context.sinks[0];
        sink.actionAdded({}, { name: 'click', selector: '#a' });
        sink.actionUpdated({}, { name: 'fill', selector: '#a', text: 'x' });
        sink.signalAdded({}, { name: 'popup', popupPageGuid: 'g' });
        sink.actionAdded({}, { name: 'click', selector: TOOLBAR_TAG });
        expect(state.events.map((e) => e.event)).toEqual(['added', 'updated', 'signal']);
    });

    it('fails clearly without the programmatic recorder', async () => {
        await expect(ensureRecorder({ exposeBinding: jest.fn() } as any)).rejects.toThrow('programmatic recorder');
    });
});
