import { describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({ logger: { info: jest.fn(), error: jest.fn() } }));

import { logger } from '../browser_logger';
import {
    drain,
    ensureRecorder,
    HELD_BACK_MS,
    isPicking,
    isToolbarAction,
    MAX_BUFFERED_COMMANDS,
    MAX_COMMAND_LENGTH,
    MAX_EVENT_LENGTH,
    MAX_EVENTS_PER_POLL,
    MAX_REPLY_EVENT_CHARS,
    recorderPoll,
    recorderStop,
    resetSession,
    toAction,
    TOOLBAR_TAG,
    toolbarScript,
    writeMode,
} from '../recorder';

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
    it('keeps ariaSnapshot only for assertSnapshot', () => {
        expect(toAction({ name: 'assertSnapshot', selector: '#a', ariaSnapshot: '- button "x"\n- link' })).toEqual({
            name: 'assertSnapshot',
            selector: '#a',
            ariaSnapshot: '- button "x"\n- link',
        });
        expect(toAction({ action: { name: 'assertSnapshot', ariaSnapshot: 'y' } })).toEqual({
            name: 'assertSnapshot',
            ariaSnapshot: 'y',
        });
        expect(toAction({ name: 'assertText', text: 't', ariaSnapshot: 'big' })).toEqual({
            name: 'assertText',
            text: 't',
        });
    });
    it('rejects garbage', () => {
        expect(toAction(null)).toBeNull();
        expect(toAction({ action: { selector: '#a' } })).toBeNull();
    });
});

describe('isPicking', () => {
    it('is true only in the inspecting modes', () => {
        expect(isPicking('recording-inspecting')).toBe(true);
        expect(isPicking('inspecting')).toBe(true);
        for (const mode of ['recording', 'standby', 'none', 'assertingText', undefined]) {
            expect(isPicking(mode)).toBe(false);
        }
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
            pages: () => [],
        } as any;
    }

    it('enables the recorder once per context', async () => {
        const context = fakeContext();
        await ensureRecorder(context);
        await ensureRecorder(context);
        expect(context._enableRecorder).toHaveBeenCalledTimes(1);
        expect(context.exposeBinding).toHaveBeenCalledTimes(1);
    });

    it('enables the recorder once for concurrent calls', async () => {
        const context = fakeContext();
        await Promise.all([ensureRecorder(context), ensureRecorder(context)]);
        expect(context._enableRecorder).toHaveBeenCalledTimes(1);
    });

    it('buffers actions, updates and signals, but not toolbar actions', async () => {
        const context = fakeContext();
        const state = await ensureRecorder(context);
        await resetSession(context, state, async () => undefined);
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

describe('writeMode', () => {
    const page = (result: boolean | Error) => ({
        evaluate: jest.fn(async () => {
            if (result instanceof Error) throw result;
            return result;
        }),
    });

    it('continues to the next page when the binding is missing', async () => {
        const first = page(false);
        const second = page(true);
        const context = { pages: () => [first, second] } as any;
        await expect(writeMode(context, 'recording')).resolves.toBe(true);
        expect(second.evaluate).toHaveBeenCalledTimes(1);
    });

    it('skips a failing page and reports false when no page has the binding', async () => {
        const context = { pages: () => [page(new Error('closed')), page(false)] } as any;
        await expect(writeMode(context, 'recording')).resolves.toBe(false);
    });
});

describe('resetSession', () => {
    it('drops an Action Playwright held back from before the session', async () => {
        const buffers = { events: [] as any[], commands: [] as unknown[], armed: true, active: false };
        const context = { pages: () => [] } as any;
        const wait = jest.fn(async (ms: number) => {
            expect(ms).toBe(HELD_BACK_MS);
            buffers.events.push({ event: 'added', action: { name: 'navigate', url: 'http://before' } });
        });
        await resetSession(context, buffers, wait);
        expect(wait).toHaveBeenCalledTimes(1);
        expect(buffers.events).toEqual([]);
        expect(buffers.armed).toBe(false);
    });

    it('waits and drains while still stopped, then starts recording', async () => {
        const order: string[] = [];
        const buffers = { events: [] as any[], commands: [] as unknown[], armed: false, active: false };
        const page = {
            evaluate: jest.fn(async (_fn: unknown, mode: string) => {
                order.push(`mode:${mode}:events=${buffers.events.length}`);
                return true;
            }),
        };
        const context = { pages: () => [page] } as any;
        const wait = jest.fn(async () => {
            order.push('wait');
            buffers.events.push({ event: 'added', action: { name: 'navigate', url: 'http://before' } });
        });
        await resetSession(context, buffers, wait);
        expect(order).toEqual(['wait', 'mode:recording:events=0']);
    });
});

interface FakeWindow {
    mode: string | undefined;
    toolbar: unknown;
    removed: number;
    __pw_recorderState?: () => { mode?: string };
    __pw_recorderSetMode?: (mode: string) => void;
    __rfbToolbarRender?: (state: unknown) => void;
    __rfbToolbarRemove?: () => void;
}

// A page whose `evaluate` runs the recorder's page functions against its own fake `window`.
function fakePage(mode: string | undefined = 'recording', { closed = false } = {}) {
    const win: FakeWindow = { mode, toolbar: undefined, removed: 0 };
    if (mode !== undefined) {
        win.__pw_recorderState = () => ({ mode: win.mode });
        win.__pw_recorderSetMode = (m: string) => {
            win.mode = m;
        };
    }
    const evaluate = jest.fn(async (fn: unknown, arg?: unknown) => {
        if (closed) throw new Error('Target page, context or browser has been closed');
        const global = globalThis as unknown as { window?: unknown };
        global.window = win;
        try {
            if (typeof fn === 'string') {
                win.__rfbToolbarRender = (state: unknown) => {
                    win.toolbar = state;
                };
                win.__rfbToolbarRemove = () => {
                    win.removed += 1;
                    win.toolbar = undefined;
                };
                return undefined;
            }
            return (fn as (a: unknown) => unknown)(arg);
        } finally {
            delete global.window;
        }
    });
    return { win, evaluate };
}

function fakeRecorderContext(pages: ReturnType<typeof fakePage>[]) {
    const sinks: any[] = [];
    const bindings: Record<string, (source: unknown, arg: unknown) => void> = {};
    const context = {
        sinks,
        bindings,
        pages: () => pages,
        _enableRecorder: jest.fn(async (_params: unknown, sink: unknown) => {
            sinks.push(sink);
        }),
        exposeBinding: jest.fn(async (name: string, fn: (source: unknown, arg: unknown) => void) => {
            bindings[name] = fn;
        }),
    };
    return context as any;
}

const stateFor = (context: unknown) => ({ getActiveContext: () => context }) as any;
const pollBody = (body: Record<string, unknown>) => ({ body: JSON.stringify(body) }) as any;
async function poll(context: unknown, body: Record<string, unknown> = {}) {
    const response = await recorderPoll(pollBody(body), stateFor(context));
    return JSON.parse(response.json);
}

describe('recorderPoll', () => {
    it('does not treat standby before the recorder was seen recording as a stop', async () => {
        const context = fakeRecorderContext([fakePage('standby')]);
        await ensureRecorder(context);
        expect((await poll(context)).mode).toBe('recording');
    });

    it('reports a stop once recording was seen and the mode turns to standby or none', async () => {
        for (const stopMode of ['standby', 'none']) {
            const page = fakePage('recording');
            const context = fakeRecorderContext([page]);
            expect((await poll(context)).mode).toBe('recording');
            page.win.mode = stopMode;
            expect((await poll(context)).mode).toBe('stopped');
        }
    });

    it('reports picking while an inspecting mode is on', async () => {
        const page = fakePage('recording-inspecting');
        const context = fakeRecorderContext([page]);
        const reply = await poll(context);
        expect(reply.picking).toBe(true);
        expect(reply.mode).toBe('recording');
        page.win.mode = 'recording';
        expect((await poll(context)).picking).toBe(false);
    });

    it('reports how many pages the context has', async () => {
        const context = fakeRecorderContext([fakePage(), fakePage()]);
        expect((await poll(context)).pages).toBe(2);
        expect((await poll(fakeRecorderContext([]))).pages).toBe(0);
    });

    it('renders the toolbar state on every page', async () => {
        const first = fakePage();
        const second = fakePage();
        const context = fakeRecorderContext([first, second]);
        await poll(context, { state: { state: 'idle' } });
        expect(first.win.toolbar).toEqual({ state: 'idle' });
        expect(second.win.toolbar).toEqual({ state: 'idle' });
    });

    it('fails clearly without an active context', async () => {
        await expect(recorderPoll(pollBody({}), stateFor(undefined))).rejects.toThrow('No browser context');
    });

    it('drains stale events and commands on reset, arms recording and accepts later ones', async () => {
        const page = fakePage('none');
        const context = fakeRecorderContext([page]);
        const buffers = await ensureRecorder(context);
        buffers.armed = true;
        buffers.events.push({ event: 'added', action: { name: 'click', selector: '#stale' } });
        buffers.commands.push({ cmd: 'stop' });
        const reply = await poll(context, { reset: true });
        expect(reply).toMatchObject({ mode: 'recording', events: [], commands: [] });
        expect(page.win.mode).toBe('recording');
        context.sinks[0].actionAdded({}, { name: 'click', selector: '#fresh' });
        context.bindings.__rfbCommand({}, { cmd: 'undo' });
        const next = await poll(context);
        expect(next.events).toEqual([{ event: 'added', action: { name: 'click', selector: '#fresh' } }]);
        expect(next.commands).toEqual([{ cmd: 'undo' }]);
    });
});

describe('the command channel', () => {
    async function activeContext() {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        await resetSession(context, buffers, async () => undefined);
        return { context, buffers, send: (command: unknown) => context.bindings.__rfbCommand({}, command) };
    }

    it('drops commands while no session is active', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        context.bindings.__rfbCommand({}, { cmd: 'stop' });
        expect(buffers.commands).toEqual([]);
    });

    it('drops commands after the session stopped', async () => {
        const { context, buffers, send } = await activeContext();
        await recorderStop({}, stateFor(context));
        send({ cmd: 'new', name: 'Late' });
        expect(buffers.commands).toEqual([]);
    });

    it('drops an oversized command', async () => {
        const { buffers, send } = await activeContext();
        send({ cmd: 'new', name: 'x'.repeat(MAX_COMMAND_LENGTH) });
        send('x'.repeat(5_000_000));
        expect(buffers.commands).toEqual([]);
        expect(logger.info).toHaveBeenCalledWith('recorder: ignoring an oversized toolbar command');
        send({ cmd: 'undo' });
        expect(buffers.commands).toEqual([{ cmd: 'undo' }]);
    });

    it('buffers at most MAX_BUFFERED_COMMANDS commands', async () => {
        const { buffers, send } = await activeContext();
        for (let i = 0; i < MAX_BUFFERED_COMMANDS + 10; i++) send({ cmd: 'undo' });
        expect(buffers.commands).toHaveLength(MAX_BUFFERED_COMMANDS);
    });
});

describe('event buffering', () => {
    it('drops Actions while no session is active', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        context.sinks[0].actionAdded({}, { name: 'click', selector: '#a' });
        expect(buffers.events).toEqual([]);
    });

    it('drops an oversized Action', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        await resetSession(context, buffers, async () => undefined);
        context.sinks[0].actionAdded({}, { name: 'fill', selector: '#a', text: 'x'.repeat(MAX_EVENT_LENGTH) });
        expect(buffers.events).toEqual([]);
        expect(logger.info).toHaveBeenCalledWith("recorder: ignoring an oversized 'fill' event");
    });

    it('delivers at most MAX_EVENTS_PER_POLL events per poll and keeps the rest', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        await resetSession(context, buffers, async () => undefined);
        for (let i = 0; i < MAX_EVENTS_PER_POLL + 3; i++) {
            context.sinks[0].actionAdded({}, { name: 'click', selector: `#e${i}` });
        }
        expect((await poll(context)).events).toHaveLength(MAX_EVENTS_PER_POLL);
        const rest = (await poll(context)).events;
        expect(rest.map((e: any) => e.action.selector)).toEqual([
            `#e${MAX_EVENTS_PER_POLL}`,
            `#e${MAX_EVENTS_PER_POLL + 1}`,
            `#e${MAX_EVENTS_PER_POLL + 2}`,
        ]);
    });

    it('keeps one poll reply within MAX_REPLY_EVENT_CHARS', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        await resetSession(context, buffers, async () => undefined);
        const text = 'x'.repeat(MAX_EVENT_LENGTH - 100);
        const count = Math.ceil(MAX_REPLY_EVENT_CHARS / text.length) + 2;
        for (let i = 0; i < count; i++) context.sinks[0].actionAdded({}, { name: 'fill', selector: '#a', text });
        const first = (await poll(context)).events;
        expect(JSON.stringify(first).length).toBeLessThanOrEqual(MAX_REPLY_EVENT_CHARS + MAX_EVENT_LENGTH);
        expect(first.length).toBeGreaterThan(0);
        expect(first.length).toBeLessThan(count);
        let total = first.length;
        while (buffers.events.length) total += (await poll(context)).events.length;
        expect(total).toBe(count);
    });
});

describe('recorderStop', () => {
    it('writes mode none, which hides Playwright overlay, and removes the toolbar on every page', async () => {
        const first = fakePage('recording');
        const closed = fakePage('recording', { closed: true });
        const second = fakePage('recording');
        const context = fakeRecorderContext([first, closed, second]);
        await poll(context, { state: { state: 'recording' } });
        const response = await recorderStop({}, stateFor(context));
        expect(first.win.mode).toBe('none');
        expect(first.win.removed).toBe(1);
        expect(second.win.removed).toBe(1);
        expect(response.log).toBe('Recording stopped.');
    });

    it('tolerates a context without the recorder or without pages', async () => {
        await expect(recorderStop({} as any, stateFor(fakeRecorderContext([])))).resolves.toEqual({
            log: 'Recording stopped.',
        });
        await expect(recorderStop({} as any, stateFor(undefined))).resolves.toEqual({
            log: 'No context to stop recording in.',
        });
    });
});
