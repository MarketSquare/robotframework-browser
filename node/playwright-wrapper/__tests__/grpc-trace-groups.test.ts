import { beforeEach, describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => ({
    ...jest.requireActual<object>('../browser_logger'),
    logger: { info: jest.fn(), error: jest.fn(), debug: jest.fn(), warn: jest.fn() },
}));
jest.mock('uuid', () => ({ v4: jest.fn().mockReturnValue('test-uuid') }));
jest.mock('monocart-coverage-reports', () => ({ CoverageReport: jest.fn() }));

import { ContextTracer } from '../context-tracer';
import { PlaywrightServer } from '../grpc-service';
import { BrowserState, PlaywrightState } from '../playwright-state';

function makeTracing() {
    return {
        start: jest.fn().mockResolvedValue(undefined),
        stop: jest.fn().mockResolvedValue(undefined),
        group: jest.fn().mockResolvedValue(undefined),
        groupEnd: jest.fn().mockResolvedValue(undefined),
    };
}

type Tracing = ReturnType<typeof makeTracing>;

function groupNames(tracing: Tracing): string[] {
    return tracing.group.mock.calls.map((call) => call[0] as string);
}

function call(peer: string, request: unknown = {}) {
    return { getPeer: () => peer, request } as any;
}

function rpc(server: PlaywrightServer, name: string, peer: string, request: unknown = {}) {
    return new Promise<unknown>((resolve, reject) => {
        (server as any)[name](call(peer, request), (error: { details?: string } | null, response: unknown) =>
            error ? reject(new Error(error.details)) : resolve(response),
        );
    });
}

async function tracedContext(id: string, tracing: Tracing) {
    const tracer = new ContextTracer(id, tracing as any);
    await tracer.start({}, `/out/${id}.zip`);
    return {
        c: { close: jest.fn().mockResolvedValue(undefined), cookies: jest.fn().mockResolvedValue([]) },
        id,
        tracer,
        pageStack: [],
        options: {},
    } as any;
}

function traceGroup(name: string, depth: number) {
    return { name, file: 'test.robot', line: 1, column: 0, depth };
}

describe('trace groups through the gRPC service', () => {
    const peer = 'ipv4:127.0.0.1:50000';
    let server: PlaywrightServer;
    let state: PlaywrightState;
    let tracingA: Tracing;
    let tracingB: Tracing;

    beforeEach(async () => {
        server = new PlaywrightServer();
        state = (server as any).getState(call(peer));
        const browser = new BrowserState({ browser: null, name: 'chromium', headless: true });
        tracingA = makeTracing();
        tracingB = makeTracing();
        browser.pushContext(await tracedContext('context=a', tracingA));
        browser.pushContext(await tracedContext('context=b', tracingB));
        state.browserStack.push(browser);
    });

    it('sends a keyword to the trace of every context it acts on, and no other', async () => {
        await rpc(server, 'openTraceGroup', peer, traceGroup('Compare Cookies', 0));
        await rpc(server, 'getCookies', peer, {});
        await rpc(server, 'switchContext', peer, { index: 'context=a' });
        await rpc(server, 'getCookies', peer, {});
        await rpc(server, 'closeTraceGroup', peer, { depth: 0 });

        expect(groupNames(tracingA)).toEqual(['Compare Cookies']);
        expect(groupNames(tracingB)).toEqual(['Compare Cookies']);
        expect(tracingA.groupEnd).toHaveBeenCalledTimes(1);
        expect(tracingB.groupEnd).toHaveBeenCalledTimes(1);
    });

    it('sends Switch Context only to the trace of the context it switches to', async () => {
        await rpc(server, 'openTraceGroup', peer, traceGroup('Switch Context    context=a', 0));
        await rpc(server, 'getBrowserCatalog', peer, { value: false });
        await rpc(server, 'switchContext', peer, { index: 'context=a' });
        await rpc(server, 'closeTraceGroup', peer, { depth: 0 });

        expect(groupNames(tracingA)).toEqual(['Switch Context    context=a']);
        expect(tracingB.group).not.toHaveBeenCalled();
    });

    it('opens the Switch Context group before the page it switches to comes to front', async () => {
        const events: string[] = [];
        tracingA.group.mockImplementation(async (name: string) => {
            events.push(`group ${name}`);
        });
        const contextA = state.activeBrowser!.contextStack[0];
        contextA.pageStack.push({
            id: 'page=a',
            p: {
                bringToFront: async () => {
                    events.push('bringToFront');
                },
            },
        } as any);
        await rpc(server, 'openTraceGroup', peer, traceGroup('Switch Context    context=a', 0));
        await rpc(server, 'switchContext', peer, { index: 'context=a' });

        expect(events).toEqual(['group Switch Context    context=a', 'bringToFront']);
    });

    it('sends Close Context only to the trace of the context it closes', async () => {
        await rpc(server, 'switchContext', peer, { index: 'context=a' });
        await rpc(server, 'openTraceGroup', peer, traceGroup('Close Context    context=b', 0));
        await rpc(server, 'getBrowserCatalog', peer, { value: false });
        await rpc(server, 'switchContext', peer, { index: 'context=b' });
        await rpc(server, 'closeContext', peer, { value: true });
        await rpc(server, 'closeTraceGroup', peer, { depth: 0 });

        expect(groupNames(tracingB)).toEqual(['Close Context    context=b']);
        expect(tracingB.stop).toHaveBeenCalledTimes(1);
        expect(tracingA.group).not.toHaveBeenCalled();
    });

    it('sends the open groups into a trace that Start Tracing starts', async () => {
        await rpc(server, 'switchContext', peer, { index: 'context=a' });
        await rpc(server, 'stopTracing', peer, { save: false });
        await rpc(server, 'openTraceGroup', peer, traceGroup('My Flow', 0));
        await rpc(server, 'openTraceGroup', peer, traceGroup('Start Tracing', 1));
        await rpc(server, 'startTracing', peer, { traceFile: '/out' });
        await rpc(server, 'closeTraceGroup', peer, { depth: 1 });
        await rpc(server, 'closeTraceGroup', peer, { depth: 0 });

        expect(groupNames(tracingA)).toEqual(['My Flow', 'Start Tracing']);
        expect(tracingA.groupEnd).toHaveBeenCalledTimes(2);
        expect(tracingB.group).not.toHaveBeenCalled();
    });

    it('keeps the keyword running when its trace group can not be sent', async () => {
        tracingB.group.mockRejectedValue(new Error('Target page, context or browser has been closed'));
        await rpc(server, 'openTraceGroup', peer, traceGroup('Get Cookies', 0));

        await expect(rpc(server, 'getCookies', peer, {})).resolves.toBeDefined();
        expect(tracingB.group).toHaveBeenCalled();
    });

    it('keeps the trace groups of each client of a shared Node process apart', async () => {
        const otherPeer = 'ipv4:127.0.0.1:50001';
        const tracingOther = makeTracing();
        const otherBrowser = new BrowserState({ browser: null, name: 'chromium', headless: true });
        otherBrowser.pushContext(await tracedContext('context=other', tracingOther));
        ((server as any).getState(call(otherPeer)) as PlaywrightState).browserStack.push(otherBrowser);

        await rpc(server, 'openTraceGroup', peer, traceGroup('Worker 1 Keyword', 0));
        await rpc(server, 'openTraceGroup', otherPeer, traceGroup('Worker 2 Keyword', 0));
        await rpc(server, 'getCookies', peer, {});
        await rpc(server, 'closeTraceGroup', otherPeer, { depth: 0 });
        await rpc(server, 'getCookies', peer, {});
        await rpc(server, 'closeTraceGroup', peer, { depth: 0 });

        expect(groupNames(tracingB)).toEqual(['Worker 1 Keyword']);
        expect(tracingB.groupEnd).toHaveBeenCalledTimes(1);
        expect(groupNames(tracingOther)).toEqual(['Worker 2 Keyword']);
    });
});
