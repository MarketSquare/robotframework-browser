import { describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({ logger: { info: jest.fn(), error: jest.fn() } }));
jest.mock('../playwright-invoke', () => ({ findLocator: jest.fn() }));

import {
    commandListeners,
    ensureRecorder,
    Entry,
    HELD_BACK_MS,
    isPicking,
    MAX_BUFFERED_COMMANDS,
    MAX_COMMAND_BYTES,
    MAX_ENTRIES_PER_POLL,
    MAX_EVENT_BYTES,
    MAX_REPLY_BYTES,
    newBuffers,
    RecorderBuffers,
    recorderPoll,
    recorderStop,
    resetSession,
    toAction,
    toolbarScript,
    writeMode,
} from '../recorder';

const commandsIn = (entries: Entry[]) => entries.flatMap((e) => ('command' in e ? [e.command] : []));
const eventsIn = (entries: Entry[]) => entries.filter((e) => !('command' in e)) as any[];
const freshBuffers = (armed = false): RecorderBuffers => ({
    entries: [],
    commandCount: 0,
    armed,
    active: false,
    rendered: new WeakMap(),
    ownPick: false,
});

beforeEach(() => jest.clearAllMocks());

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

describe('toolbarScript', () => {
    it('is a self-invoking script that hides the toolbar from the recorder in x-pw-glass', () => {
        const source = toolbarScript();
        expect(source).toContain("document.createElement('x-pw-glass')");
        // eslint-disable-next-line @typescript-eslint/no-implied-eval
        expect(() => new Function(source)).not.toThrow();
    });
});

describe('ensureRecorder', () => {
    function fakeContext(pages: unknown[] = []) {
        const sinks: any[] = [];
        return {
            sinks,
            _startRecording: jest.fn(async (_params: unknown, sink: unknown) => {
                sinks.push(sink);
            }),
            exposeBinding: jest.fn(async () => undefined),
            pages: () => pages,
            on: jest.fn(),
        } as any;
    }

    it('starts the recording once per context', async () => {
        const context = fakeContext();
        await ensureRecorder(context);
        await ensureRecorder(context);
        expect(context._startRecording).toHaveBeenCalledTimes(1);
        expect(context.exposeBinding).toHaveBeenCalledTimes(1);
    });

    it('fails clearly when Playwright offers no programmatic recorder', async () => {
        const context = { exposeBinding: jest.fn(), pages: () => [] } as any;
        await expect(ensureRecorder(context)).rejects.toThrow('BrowserContext._startRecording');
    });

    it('starts the recording once for concurrent calls', async () => {
        const context = fakeContext();
        await Promise.all([ensureRecorder(context), ensureRecorder(context)]);
        expect(context._startRecording).toHaveBeenCalledTimes(1);
    });

    it('buffers actions, updates, signals and commands in the order they happen', async () => {
        const context = fakeContext();
        const state = await ensureRecorder(context);
        await resetSession(context, state, async () => undefined);
        const sink = context.sinks[0];
        sink.actionAdded({}, { name: 'click', selector: '#a' });
        context.exposeBinding.mock.calls[0][1]({}, { cmd: 'undo' });
        sink.actionUpdated({}, { name: 'fill', selector: '#a', text: 'x' });
        sink.signalAdded({}, { name: 'popup', popupPageGuid: 'g' });
        expect(state.entries.map((e) => ('command' in e ? 'command' : e.event))).toEqual([
            'added',
            'command',
            'updated',
            'signal',
        ]);
    });

    it('names the page of every entry and reports a closed page itself', async () => {
        const closeHandlers: Array<() => void> = [];
        const first = {
            _guid: 'page@first',
            once: jest.fn((_event: string, fn: () => void) => closeHandlers.push(fn)),
        };
        const context = fakeContext([first]);
        const state = await ensureRecorder(context);
        await resetSession(context, state, async () => undefined);
        context.sinks[0].actionAdded(first, { name: 'click', selector: '#a' });
        const popup = { _guid: 'page@popup', once: jest.fn() };
        context.on.mock.calls[0][1](popup);
        closeHandlers[0]();
        expect(eventsIn(state.entries)).toEqual([
            { event: 'added', action: { name: 'click', selector: '#a' }, page: 'page@first' },
            { event: 'closed', action: { name: 'closePage' }, page: 'page@first' },
        ]);
        expect(context.on).toHaveBeenCalledWith('page', expect.any(Function));
        expect(popup.once).toHaveBeenCalledWith('close', expect.any(Function));
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
        const buffers = freshBuffers(true);
        const context = { pages: () => [] } as any;
        const wait = jest.fn(async (ms: number) => {
            expect(ms).toBe(HELD_BACK_MS);
            buffers.entries.push({ event: 'added', action: { name: 'navigate', url: 'http://before' } });
            buffers.entries.push({ command: { cmd: 'stop' } });
            buffers.commandCount = 1;
        });
        await resetSession(context, buffers, wait);
        expect(wait).toHaveBeenCalledTimes(1);
        expect(buffers.entries).toEqual([]);
        expect(buffers.commandCount).toBe(0);
        expect(buffers.armed).toBe(false);
    });

    it('waits and drains while still stopped, then starts recording', async () => {
        const order: string[] = [];
        const buffers = freshBuffers();
        const page = {
            evaluate: jest.fn(async (_fn: unknown, mode: string) => {
                order.push(`mode:${mode}:events=${buffers.entries.length}`);
                return true;
            }),
        };
        const context = { pages: () => [page] } as any;
        const wait = jest.fn(async () => {
            order.push('wait');
            buffers.entries.push({ event: 'added', action: { name: 'navigate', url: 'http://before' } });
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

function fakePage(mode: string | undefined = 'recording', { closed = false, failures = 0 } = {}) {
    const win: FakeWindow & { renders: number } = { mode, toolbar: undefined, removed: 0, renders: 0 };
    let failing = failures;
    if (mode !== undefined) {
        win.__pw_recorderState = () => ({ mode: win.mode });
        win.__pw_recorderSetMode = (m: string) => {
            win.mode = m;
        };
    }
    const evaluate = jest.fn(async (fn: unknown, arg?: unknown) => {
        if (closed) throw new Error('Target page, context or browser has been closed');
        if (failing > 0) {
            failing -= 1;
            throw new Error('Execution context was destroyed, most likely because of a navigation');
        }
        const global = globalThis as unknown as { window?: unknown };
        global.window = win;
        try {
            if (typeof fn === 'string') {
                win.__rfbToolbarRender = (state: unknown) => {
                    win.toolbar = state;
                    win.renders += 1;
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
    return { win, evaluate, once: jest.fn() };
}

function fakeRecorderContext(pages: ReturnType<typeof fakePage>[]) {
    const sinks: any[] = [];
    const bindings: Record<string, (source: unknown, arg: unknown) => void> = {};
    const context = {
        sinks,
        bindings,
        pages: () => pages,
        on: jest.fn(),
        _startRecording: jest.fn(async (_params: unknown, sink: unknown) => {
            sinks.push(sink);
        }),
        exposeBinding: jest.fn(async (name: string, fn: (source: unknown, arg: unknown) => void) => {
            bindings[name] = fn;
        }),
    };
    return context as any;
}

const stateFor = (context: unknown, headless = false, activePage: unknown = undefined) =>
    ({ getActiveContext: () => context, getActivePage: () => activePage, activeBrowser: { headless } }) as any;
const pollBody = (body: Record<string, unknown>) => ({ body: JSON.stringify(body) }) as any;
async function poll(context: unknown, body: Record<string, unknown> = {}) {
    const response = await recorderPoll(pollBody(body), stateFor(context));
    return JSON.parse(response.json);
}

describe('recorderPoll', () => {
    it('refuses to start a session in a headless browser', async () => {
        const context = fakeRecorderContext([fakePage()]);
        await expect(recorderPoll(pollBody({ reset: true }), stateFor(context, true))).rejects.toThrow(
            'Recording needs a visible browser',
        );
        expect(context.bindings.__rfbCommand).toBeUndefined();
    });

    it('starts a session in a headless browser when the test switch allows it', async () => {
        const context = fakeRecorderContext([fakePage()]);
        await recorderPoll(pollBody({ reset: true, allowHeadless: true }), stateFor(context, true));
        expect(typeof context.bindings.__rfbCommand).toBe('function');
    });

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

    it.each(['recording-inspecting', 'inspecting'])(
        'hands an inspecting mode (%s) over to the toolbar picker',
        async (mode) => {
            const page = fakePage(mode);
            const context = fakeRecorderContext([page]);
            const reply = await poll(context);
            expect(reply).toMatchObject({ picking: false, pickRequested: true, mode: 'recording' });
            expect(page.win.mode).toBe('recording');
        },
    );

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

    it('sends a page the state only when it changed or the page lost the toolbar', async () => {
        const page = fakePage();
        const context = fakeRecorderContext([page]);
        await poll(context, { state: { state: 'idle' } });
        await poll(context, { state: { state: 'idle' } });
        expect(page.win.renders).toBe(1);
        await poll(context, { state: { state: 'recording' } });
        expect(page.win.renders).toBe(2);
        delete page.win.__rfbToolbarRender;
        await poll(context, { state: { state: 'recording' } });
        expect(page.win.toolbar).toEqual({ state: 'recording' });
        expect(page.win.renders).toBe(3);
    });

    it('switches the recorder on with a later poll when the reset found no page to switch', async () => {
        const page = fakePage('none', { failures: 1 });
        const context = fakeRecorderContext([page]);
        const buffers = await ensureRecorder(context);
        await resetSession(context, buffers, async () => undefined);
        expect(page.win.mode).toBe('none');
        expect((await poll(context)).mode).toBe('recording');
        expect(page.win.mode).toBe('recording');
        await poll(context);
        expect(buffers.armed).toBe(true);
    });

    it('does not switch the recorder on again once it was seen recording', async () => {
        const page = fakePage('recording');
        const context = fakeRecorderContext([page]);
        await poll(context);
        page.win.mode = 'none';
        expect((await poll(context)).mode).toBe('stopped');
        expect(page.win.mode).toBe('none');
    });

    it('fails clearly without an active context at the start of a session', async () => {
        await expect(recorderPoll(pollBody({ reset: true }), stateFor(undefined))).rejects.toThrow(
            'No browser context',
        );
    });

    it('reports no pages once the context was closed during the session', async () => {
        const response = await recorderPoll(pollBody({}), stateFor(undefined));
        expect(JSON.parse(response.json)).toEqual({ mode: 'recording', picking: false, pages: 0, entries: [] });
    });

    it('renders again to a page that dropped the toolbar, even with an unchanged state', async () => {
        const page = fakePage();
        const context = fakeRecorderContext([page]);
        await poll(context, { state: { state: 'idle' } });
        expect(page.win.renders).toBe(1);
        (page.win as any).__rfbToolbarConnected = () => false;
        await poll(context, { state: { state: 'idle' } });
        expect(page.win.renders).toBe(2);
        (page.win as any).__rfbToolbarConnected = () => true;
        await poll(context, { state: { state: 'idle' } });
        expect(page.win.renders).toBe(2);
    });

    it('drains stale events and commands on reset, arms recording and accepts later ones', async () => {
        const page = fakePage('none');
        const context = fakeRecorderContext([page]);
        const buffers = await ensureRecorder(context);
        buffers.armed = true;
        buffers.entries.push({ event: 'added', action: { name: 'click', selector: '#stale' } });
        buffers.entries.push({ command: { cmd: 'stop' } });
        const reply = await poll(context, { reset: true });
        expect(reply).toMatchObject({ mode: 'recording', entries: [] });
        expect(page.win.mode).toBe('recording');
        context.bindings.__rfbCommand({}, { cmd: 'undo' });
        context.sinks[0].actionAdded({}, { name: 'click', selector: '#fresh' });
        const next = await poll(context);
        expect(next.entries).toEqual([
            { command: { cmd: 'undo' } },
            { event: 'added', action: { name: 'click', selector: '#fresh' } },
        ]);
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
        expect(commandsIn(buffers.entries)).toEqual([]);
    });

    it('drops commands after the session stopped', async () => {
        const { context, buffers, send } = await activeContext();
        await recorderStop({}, stateFor(context));
        send({ cmd: 'new', name: 'Late' });
        expect(commandsIn(buffers.entries)).toEqual([]);
    });

    it('drops an oversized command', async () => {
        const { buffers, send } = await activeContext();
        send({ cmd: 'new', name: 'x'.repeat(MAX_COMMAND_BYTES) });
        send('x'.repeat(5_000_000));
        expect(commandsIn(buffers.entries)).toEqual([]);
        send({ cmd: 'undo' });
        expect(commandsIn(buffers.entries)).toEqual([{ cmd: 'undo' }]);
    });

    it('accepts an argument command quoting a long value', async () => {
        const { buffers, send } = await activeContext();
        const command = { cmd: 'argument', call: 0, value: 1, start: 0, end: 1, name: 'a', raw: 'x'.repeat(64 * 1024) };
        send(command);
        expect(commandsIn(buffers.entries)).toEqual([command]);
    });

    it('measures a command in UTF-8 bytes', async () => {
        const { buffers, send } = await activeContext();
        send({ cmd: 'new', name: '\u6f22'.repeat(MAX_COMMAND_BYTES / 3 + 1) });
        expect(commandsIn(buffers.entries)).toEqual([]);
    });

    it('buffers at most MAX_BUFFERED_COMMANDS commands, counting only undelivered ones', async () => {
        const { context, buffers, send } = await activeContext();
        for (let i = 0; i < MAX_BUFFERED_COMMANDS + 10; i++) send({ cmd: 'undo' });
        expect(commandsIn(buffers.entries)).toHaveLength(MAX_BUFFERED_COMMANDS);
        await poll(context);
        send({ cmd: 'stop' });
        expect(commandsIn(buffers.entries)).toEqual([{ cmd: 'stop' }]);
    });
});

describe('event buffering', () => {
    it('drops Actions while no session is active', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        context.sinks[0].actionAdded({}, { name: 'click', selector: '#a' });
        expect(buffers.entries).toEqual([]);
    });

    it('drops an oversized Action', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        await resetSession(context, buffers, async () => undefined);
        context.sinks[0].actionAdded({}, { name: 'fill', selector: '#a', text: 'x'.repeat(MAX_EVENT_BYTES) });
        expect(buffers.entries).toEqual([]);
    });

    it('measures an Action in UTF-8 bytes', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        await resetSession(context, buffers, async () => undefined);
        context.sinks[0].actionAdded(
            {},
            { name: 'fill', selector: '#a', text: '\u6f22'.repeat(MAX_EVENT_BYTES / 3 + 1) },
        );
        expect(buffers.entries).toEqual([]);
    });

    it('delivers at most MAX_ENTRIES_PER_POLL entries per poll and keeps the rest', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        await resetSession(context, buffers, async () => undefined);
        for (let i = 0; i < MAX_ENTRIES_PER_POLL + 3; i++) {
            context.sinks[0].actionAdded({}, { name: 'click', selector: `#e${i}` });
        }
        expect((await poll(context)).entries).toHaveLength(MAX_ENTRIES_PER_POLL);
        const rest = eventsIn((await poll(context)).entries);
        expect(rest.map((e: any) => e.action.selector)).toEqual([
            `#e${MAX_ENTRIES_PER_POLL}`,
            `#e${MAX_ENTRIES_PER_POLL + 1}`,
            `#e${MAX_ENTRIES_PER_POLL + 2}`,
        ]);
    });

    it('keeps one poll reply within MAX_REPLY_BYTES, Actions and commands together', async () => {
        const context = fakeRecorderContext([fakePage()]);
        const buffers = await ensureRecorder(context);
        await resetSession(context, buffers, async () => undefined);
        const text = 'x'.repeat(MAX_EVENT_BYTES - 100);
        const raw = 'y'.repeat(MAX_COMMAND_BYTES - 1000);
        const count = Math.ceil(MAX_REPLY_BYTES / text.length) + 2;
        for (let i = 0; i < count; i++) {
            context.sinks[0].actionAdded({}, { name: 'fill', selector: '#a', text });
            context.bindings.__rfbCommand({}, { cmd: 'argument', raw });
        }
        const first = (await poll(context)).entries;
        expect(Buffer.byteLength(JSON.stringify(first))).toBeLessThanOrEqual(MAX_REPLY_BYTES);
        expect(first.length).toBeGreaterThan(0);
        expect(first.length).toBeLessThan(2 * count);
        let total = first.length;
        while (buffers.entries.length) total += (await poll(context)).entries.length;
        expect(total).toBe(2 * count);
        expect(buffers.commandCount).toBe(0);
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

describe('recorderPoll with the toolbar Pick button', () => {
    function pickPage() {
        let resolve: (locator: unknown) => void = () => undefined;
        const page = {
            pickLocator: jest.fn(() => new Promise((r) => (resolve = r))),
            cancelPickLocator: jest.fn(async () => undefined),
            isClosed: () => false,
            frames: () => [],
        };
        return { page, pick: (selector: string) => resolve({ _selector: selector, elementHandle: async () => null }) };
    }
    const flush = () => new Promise((resolve) => setTimeout(resolve, 0));
    async function pollWith(context: unknown, active: unknown, body: Record<string, unknown>) {
        const response = await recorderPoll(pollBody(body), stateFor(context, false, active));
        return JSON.parse(response.json);
    }

    it("turns Playwright's Pick locator back into recording and asks Python to pick", async () => {
        const page = fakePage('recording');
        const context = fakeRecorderContext([page]);
        await poll(context);
        page.win.mode = 'recording-inspecting';
        const reply = await poll(context);
        expect(reply.pickRequested).toBe(true);
        expect(reply.picking).toBe(false);
        expect(page.win.mode).toBe('recording');
    });

    it('does not end the session while its own pick holds the mode at none', async () => {
        const page = fakePage('recording');
        const context = fakeRecorderContext([page]);
        const picker = pickPage();
        await poll(context);
        await pollWith(context, picker.page, { pick: true });
        expect(picker.page.pickLocator).toHaveBeenCalledTimes(1);
        page.win.mode = 'inspecting';
        expect((await pollWith(context, picker.page, { pick: true })).mode).toBe('recording');
        page.win.mode = 'none';
        picker.pick('css=#a');
        await flush();
        const picked = await pollWith(context, picker.page, { pick: true });
        expect(picked.mode).toBe('recording');
        expect(picked.picked.selector).toBe('css=#a');
        expect(page.win.mode).toBe('recording');
        // Recording again: from now on a stop is a stop.
        expect((await pollWith(context, picker.page, { pick: false })).mode).toBe('recording');
        page.win.mode = 'none';
        expect((await pollWith(context, picker.page, {})).mode).toBe('stopped');
    });

    it('cancels its pick when Python closes the picker', async () => {
        const page = fakePage('recording');
        const context = fakeRecorderContext([page]);
        const picker = pickPage();
        await poll(context);
        await pollWith(context, picker.page, { pick: true });
        await pollWith(context, picker.page, {});
        expect(picker.page.cancelPickLocator).toHaveBeenCalled();
    });

    it('moves a pick from a closed page to the active one', async () => {
        const page = fakePage('recording');
        const context = fakeRecorderContext([page]);
        const first = pickPage();
        const second = pickPage();
        await poll(context);
        await pollWith(context, first.page, { pick: true });
        (first.page as any).isClosed = () => true;
        await pollWith(context, second.page, { pick: true });
        expect(second.page.pickLocator).toHaveBeenCalledTimes(1);
    });

    it('gives the page its own pointer back when Playwright leaves a hand-pointer mode', async () => {
        const page = fakePage('assertingText');
        const frameEvaluate = jest.fn(async () => undefined);
        (page as any).frames = () => [{ evaluate: frameEvaluate }];
        const context = fakeRecorderContext([page]);
        await poll(context);
        expect(frameEvaluate).not.toHaveBeenCalled();
        page.win.mode = 'recording';
        await poll(context);
        expect(frameEvaluate).toHaveBeenCalledTimes(1);
    });
});

describe('one recording session per context', () => {
    it('refuses a second session in the same context', async () => {
        const context = fakeRecorderContext([fakePage('recording')]);
        await recorderPoll(pollBody({ reset: true }), stateFor(context));
        await expect(recorderPoll(pollBody({ reset: true }), stateFor(context))).rejects.toThrow('already running');
    });

    it('refuses a session while Record Selector runs in the context', async () => {
        const context = fakeRecorderContext([fakePage('recording')]);
        const picker = newBuffers();
        picker.active = true;
        (await commandListeners(context)).add(picker);
        await expect(recorderPoll(pollBody({ reset: true }), stateFor(context))).rejects.toThrow('already running');
    });

    it('keeps polling the context it started in, and ends when that one closes', async () => {
        let close: () => void = () => undefined;
        const recorded = fakeRecorderContext([fakePage('recording')]);
        recorded.once = (_event: string, listener: () => void) => (close = listener);
        const other = fakeRecorderContext([fakePage('recording'), fakePage('recording')]);
        let active = recorded;
        const state = {
            getActiveContext: () => active,
            getActivePage: () => undefined,
            activeBrowser: { headless: false },
        } as any;
        await recorderPoll(pollBody({ reset: true }), state);
        active = other;
        expect(JSON.parse((await recorderPoll(pollBody({}), state)).json).pages).toBe(1);
        close();
        expect(JSON.parse((await recorderPoll(pollBody({}), state)).json).pages).toBe(0);
    });
});
