import { EventEmitter } from 'node:events';

import { beforeEach, describe, expect, it } from '@jest/globals';

jest.mock('../browser_logger', () => {
    const actual = jest.requireActual<typeof import('../browser_logger')>('../browser_logger');
    const logLines: Record<string, unknown>[] = [];
    const logger = actual.createLogger({ write: (msg: string) => logLines.push(JSON.parse(msg)) });
    logger.level = 'trace';
    return { ...actual, logger, logLines };
});
jest.mock('uuid', () => ({ v4: jest.fn().mockReturnValue('test-uuid') }));
jest.mock('monocart-coverage-reports', () => ({ CoverageReport: jest.fn() }));

import * as browserLogger from '../browser_logger';
import { ContextTracer } from '../context-tracer';
import { PlaywrightServer } from '../grpc-service';
import { BrowserState, PlaywrightState } from '../playwright-state';

const logLines = (browserLogger as unknown as { logLines: Record<string, unknown>[] }).logLines;

const peerA = 'ipv4:127.0.0.1:50001';
const peerB = 'ipv4:127.0.0.1:50002';

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

function rfContext(id: string) {
    return { suiteId: `suite-${id}`, suiteName: `Suite ${id}`, testId: `test-${id}`, testName: `Test ${id}` };
}

function makeTracing() {
    return {
        start: jest.fn().mockResolvedValue(undefined),
        stop: jest.fn().mockResolvedValue(undefined),
        group: jest.fn().mockResolvedValue(undefined),
        groupEnd: jest.fn().mockResolvedValue(undefined),
    };
}

async function openTracedContext(server: PlaywrightServer, peer: string, tracing: ReturnType<typeof makeTracing>) {
    const state: PlaywrightState = (server as any).getState(call(peer));
    const tracer = new ContextTracer('context=traced', tracing as any);
    await tracer.start({}, '/out/traced.zip');
    const browser = new BrowserState({ browser: null, name: 'chromium', headless: true });
    browser.pushContext({
        c: { close: jest.fn().mockResolvedValue(undefined) },
        id: 'context=traced',
        tracer,
        pageStack: [],
        options: {},
    } as any);
    state.browserStack.push(browser);
}

function traceGroup(name: string, depth: number) {
    return { name, file: 'test.robot', line: 1, column: 0, depth };
}

function linesOf(action: string) {
    return logLines.filter((line) => line.action === action);
}

describe('log lines carry the Robot Framework context of the peer they serve', () => {
    let server: PlaywrightServer;

    beforeEach(() => {
        logLines.length = 0;
        server = new PlaywrightServer();
    });

    it('stamps a call with its own peer suite and test, not the peer that set its context last', async () => {
        await rpc(server, 'setRfContext', peerA, rfContext('A'));
        await rpc(server, 'setRfContext', peerB, rfContext('B'));

        await rpc(server, 'getBrowserCatalog', peerA, { value: false });

        const lines = linesOf('getBrowserCatalog');
        expect(lines.length).toBeGreaterThan(0);
        for (const line of lines) {
            expect(line).toMatchObject({
                suite_id: 'suite-A',
                suite_name: 'Suite A',
                test_id: 'test-A',
                test_name: 'Test A',
            });
        }
    });

    it('stamps the end of a call with its own peer context when another peer changes context meanwhile', async () => {
        const tracing = makeTracing();
        let releaseGroup!: () => void;
        tracing.group.mockReturnValue(new Promise<void>((resolve) => (releaseGroup = resolve)));
        await openTracedContext(server, peerA, tracing);
        await rpc(server, 'setRfContext', peerA, rfContext('A'));

        const inFlight = rpc(server, 'openTraceGroup', peerA, traceGroup('Slow Keyword', 0));
        await rpc(server, 'setRfContext', peerB, rfContext('B'));
        releaseGroup();
        await inFlight;

        const finished = linesOf('openTraceGroup').filter((line) => line.status === 'succeeded');
        expect(finished).toHaveLength(1);
        expect(finished[0]).toMatchObject({ suite_id: 'suite-A', test_id: 'test-A' });
    });

    it('keeps each peer on its own keyword when their keywords open and close interleaved', async () => {
        await rpc(server, 'openTraceGroup', peerA, traceGroup('Keyword A', 0));
        await rpc(server, 'openTraceGroup', peerB, traceGroup('Keyword B', 0));
        logLines.length = 0;
        await rpc(server, 'getBrowserCatalog', peerA, { value: false });
        await rpc(server, 'closeTraceGroup', peerA, { depth: 0 });
        await rpc(server, 'getBrowserCatalog', peerB, { value: false });

        const [first, second] = [0, 1].map(
            (n) => linesOf('getBrowserCatalog').filter((line) => line.status === 'succeeded')[n],
        );
        expect(first).toMatchObject({ kw_name: 'Keyword A' });
        expect(second).toMatchObject({ kw_name: 'Keyword B' });
    });

    it('keeps no state for a peer that only checks health or looks up devices', async () => {
        await rpc(server, 'health', peerA);
        await rpc(server, 'getDevices', peerA);

        expect(server.peerMap).toEqual({});
    });

    it('reports no earlier peer id when a peer sets its id first', async () => {
        const response = (await rpc(server, 'setPeerId', peerA, { index: 'shared' })) as { body: string };

        expect(response.body).toBe('');
    });

    it('stamps the lines of a streamed upload with the peer that sent it', async () => {
        await rpc(server, 'setRfContext', peerA, rfContext('A'));
        const stream = Object.assign(new EventEmitter(), { getPeer: () => peerA });
        const finished = new Promise((resolve) => (server as any).uploadFileBySelector(stream, resolve));

        stream.emit('data', { selector: '#upload', buffer: '[]', strict: true });
        stream.emit('end');
        await finished;

        const lines = logLines.filter((line) => String(line.msg).includes('uploadFileBySelector'));
        expect(lines.length).toBeGreaterThan(0);
        for (const line of lines) {
            expect(line).toMatchObject({ suite_id: 'suite-A', test_id: 'test-A' });
        }
    });

    it('returns to the outer keyword after a missed close, as the trace groups do', async () => {
        await rpc(server, 'openTraceGroup', peerA, traceGroup('Outer', 0));
        await rpc(server, 'openTraceGroup', peerA, traceGroup('Inner Never Closed', 1));
        await rpc(server, 'openTraceGroup', peerA, traceGroup('Next Inner', 1));
        await rpc(server, 'closeTraceGroup', peerA, { depth: 1 });
        logLines.length = 0;

        await rpc(server, 'getBrowserCatalog', peerA, { value: false });

        expect(linesOf('getBrowserCatalog')[0]).toMatchObject({ kw_name: 'Outer' });
    });
});
