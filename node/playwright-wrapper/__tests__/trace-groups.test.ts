import { beforeEach, describe, expect, it } from '@jest/globals';

jest.mock('uuid', () => ({ v4: jest.fn() }));

import { ContextTracer } from '../context-tracer';
import { TraceGroups } from '../trace-groups';

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

const location = { file: 'test.robot', line: 1, column: 0 };

function group(name: string) {
    return { name, location };
}

describe('TraceGroups', () => {
    let tracingA: Tracing;
    let tracingB: Tracing;
    let a: ContextTracer;
    let b: ContextTracer;
    let active: ContextTracer | undefined;
    let groups: TraceGroups;

    beforeEach(async () => {
        tracingA = makeTracing();
        tracingB = makeTracing();
        a = new ContextTracer('context=a', tracingA as any);
        b = new ContextTracer('context=b', tracingB as any);
        await a.start({}, '/out/a.zip');
        await b.start({}, '/out/b.zip');
        active = a;
        groups = new TraceGroups(
            () => [a, b],
            () => active,
        );
    });

    it('sends a group only to the trace of the context it targets', async () => {
        await groups.open(group('Get Title'), 0);
        await groups.target(a);
        await groups.closeTo(0);

        expect(groupNames(tracingA)).toEqual(['Get Title']);
        expect(tracingA.groupEnd).toHaveBeenCalledTimes(1);
        expect(tracingB.group).not.toHaveBeenCalled();
        expect(tracingB.groupEnd).not.toHaveBeenCalled();
    });

    it('carries the callers into a trace with the first keyword that targets its context', async () => {
        await groups.open(group('My Flow'), 0);
        await groups.open(group('Get Title'), 1);
        await groups.target(a);
        await groups.closeTo(1);
        await groups.open(group('Click'), 1);
        await groups.target(b);
        await groups.closeTo(1);
        await groups.closeTo(0);

        expect(groupNames(tracingA)).toEqual(['My Flow', 'Get Title']);
        expect(groupNames(tracingB)).toEqual(['My Flow', 'Click']);
        expect(tracingA.groupEnd).toHaveBeenCalledTimes(2);
        expect(tracingB.groupEnd).toHaveBeenCalledTimes(2);
    });

    it('sends a keyword without a target context to the trace of the context active when it ends', async () => {
        await groups.open(group('My Flow'), 0);
        await groups.open(group('Switch Context'), 1);
        active = b;
        await groups.closeTo(1);
        await groups.closeTo(0);

        expect(groupNames(tracingA)).toEqual([]);
        expect(groupNames(tracingB)).toEqual(['My Flow', 'Switch Context']);
        expect(tracingB.groupEnd).toHaveBeenCalledTimes(2);
    });

    it('does not send a keyword to the active context when it reached a trace that has ended since', async () => {
        active = b;
        await groups.open(group('Stop Tracing'), 0);
        await groups.target(a);
        await a.stop();
        await groups.closeTo(0);

        expect(groupNames(tracingA)).toEqual(['Stop Tracing']);
        expect(tracingB.group).not.toHaveBeenCalled();
    });

    it('closes the groups a lost close left open when the next group opens at their depth', async () => {
        await groups.open(group('Timed Out'), 0);
        await groups.open(group('Click'), 1);
        await groups.target(a);
        await groups.open(group('Next Test'), 0);
        await groups.target(a);

        expect(groupNames(tracingA)).toEqual(['Timed Out', 'Click', 'Next Test']);
        expect(tracingA.groupEnd).toHaveBeenCalledTimes(2);
    });

    it('sends the open groups into a trace that starts while they are open', async () => {
        await groups.open(group('My Flow'), 0);
        await groups.target(a);
        await groups.open(group('Start Tracing'), 1);
        await b.stop();
        await b.start({}, '/out/b2.zip');
        await groups.started(b);

        expect(groupNames(tracingB)).toEqual(['My Flow', 'Start Tracing']);
    });

    it('sends the open groups again to a trace started after a stop', async () => {
        await groups.open(group('My Flow'), 0);
        await groups.target(a);
        await a.stop();
        await a.start({}, '/out/a2.zip');
        await groups.started(a);
        await groups.closeTo(0);

        expect(groupNames(tracingA)).toEqual(['My Flow', 'My Flow']);
        expect(tracingA.groupEnd).toHaveBeenCalledTimes(1);
    });

    it('forgets groups opened while no trace ran when the first trace starts', async () => {
        await a.stop();
        await b.stop();
        await groups.open(group('Long Gone'), 0);
        await a.start({}, '/out/a2.zip');
        await groups.started(a);

        expect(tracingA.group).not.toHaveBeenCalled();
    });
});
