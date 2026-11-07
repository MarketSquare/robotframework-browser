import { beforeEach, describe, expect, it } from '@jest/globals';

jest.mock('uuid', () => ({
    v4: jest.fn().mockReturnValue('test-uuid'),
}));

import { adHocTraceFile, contextTraceFile, ContextTracer } from '../context-tracer';

describe('trace file names', () => {
    it('names a context trace after its context in the given directory', () => {
        expect(contextTraceFile('/out/traces', 'context=1')).toBe('/out/traces/trace_context=1.zip');
    });

    it('names an ad-hoc trace after its context and a uuid in the given directory', () => {
        expect(adHocTraceFile('/out/traces', 'context=1')).toBe('/out/traces/trace_context=1-test-uuid.zip');
    });

    it('keeps a zip path as it is', () => {
        expect(contextTraceFile('/out/Login.ZIP', 'context=1')).toBe('/out/Login.ZIP');
        expect(adHocTraceFile('/out/login.zip', 'context=1')).toBe('/out/login.zip');
    });

    it('puts the context id into a path that asks for it', () => {
        expect(contextTraceFile('/out/{contextid}.zip', 'context=1')).toBe('/out/context=1.zip');
        expect(adHocTraceFile('/out/{contextid}', 'context=1')).toBe('/out/context=1/trace_context=1-test-uuid.zip');
    });
});

function makeTracing() {
    return {
        start: jest.fn().mockResolvedValue(undefined),
        stop: jest.fn().mockResolvedValue(undefined),
        group: jest.fn().mockResolvedValue(undefined),
        groupEnd: jest.fn().mockResolvedValue(undefined),
    };
}

describe('ContextTracer', () => {
    let tracing: ReturnType<typeof makeTracing>;
    let tracer: ContextTracer;

    beforeEach(() => {
        tracing = makeTracing();
        tracer = new ContextTracer('context=1', tracing as any);
    });

    it('saves the running trace to its file when stopped', async () => {
        await tracer.start({ screenshots: true }, '/out/trace.zip');

        const saved = await tracer.stop();

        expect(tracing.start).toHaveBeenCalledWith({ screenshots: true });
        expect(tracing.stop).toHaveBeenCalledWith({ path: '/out/trace.zip' });
        expect(saved).toBe('/out/trace.zip');
    });

    it('fails to start while a trace is running', async () => {
        expect.assertions(2);
        await tracer.start({}, '/out/first.zip');

        await expect(tracer.start({}, '/out/second.zip')).rejects.toThrow(
            'Tracing is already running on context context=1, stop it before starting again',
        );
        expect(tracing.start).toHaveBeenCalledTimes(1);
    });

    it('fails to stop when no trace is running', async () => {
        expect.assertions(2);

        await expect(tracer.stop()).rejects.toThrow('No trace is running on context context=1');
        expect(tracing.stop).not.toHaveBeenCalled();
    });

    it('saves the trace to the given path instead of its file', async () => {
        await tracer.start({}, '/out/trace.zip');

        const saved = await tracer.stop('/out/login.zip');

        expect(tracing.stop).toHaveBeenCalledWith({ path: '/out/login.zip' });
        expect(saved).toBe('/out/login.zip');
    });

    it('discards the trace without saving it', async () => {
        await tracer.start({}, '/out/trace.zip');

        await tracer.discard();

        expect(tracing.stop).toHaveBeenCalledWith();
    });

    it('starts a new trace after the last one was discarded', async () => {
        await tracer.start({}, '/out/trace.zip');
        await tracer.discard();

        await tracer.start({}, '/out/next.zip');

        expect(tracer.file).toBe('/out/next.zip');
    });

    it('fails to discard when no trace is running', async () => {
        expect.assertions(2);

        await expect(tracer.discard()).rejects.toThrow('No trace is running on context context=1');
        expect(tracing.stop).not.toHaveBeenCalled();
    });

    it('is no longer running when discarding the trace fails', async () => {
        expect.assertions(2);
        tracing.stop.mockRejectedValueOnce(new Error('Target closed'));
        await tracer.start({}, '/out/trace.zip');

        await expect(tracer.discard()).rejects.toThrow('Target closed');
        expect(tracer.running).toBe(false);
    });

    it('is no longer running when stopping the trace fails', async () => {
        expect.assertions(2);
        tracing.stop.mockRejectedValueOnce(new Error('Target closed'));
        await tracer.start({}, '/out/trace.zip');

        await expect(tracer.stop()).rejects.toThrow('Target closed');
        expect(tracer.running).toBe(false);
    });

    it('tells the file and options of the running trace', async () => {
        const options = { screenshots: true, snapshots: { dom: true, aria: true } };
        await tracer.start(options, '/out/trace.zip');

        expect(tracer.file).toBe('/out/trace.zip');
        expect(tracer.options).toEqual(options);
    });

    it('tells no file and no options when no trace is running', async () => {
        await tracer.start({ screenshots: true }, '/out/trace.zip');
        await tracer.stop();

        expect(tracer.file).toBe('');
        expect(tracer.options).toBeUndefined();
    });

    describe('when its context closes', () => {
        it('saves the running trace to its file', async () => {
            await tracer.start({}, '/out/trace.zip');

            await tracer.endWithContext(true);

            expect(tracing.stop).toHaveBeenCalledWith({ path: '/out/trace.zip' });
        });

        it('discards the running trace when it is not saved', async () => {
            await tracer.start({}, '/out/trace.zip');

            await tracer.endWithContext(false);

            expect(tracing.stop).toHaveBeenCalledWith();
        });

        it('closes without failing when the discarded trace was already gone with its context', async () => {
            tracing.stop.mockRejectedValueOnce(
                Object.assign(new Error('Target closed'), { name: 'TargetClosedError' }),
            );
            await tracer.start({}, '/out/trace.zip');

            await tracer.endWithContext(false);

            expect(tracer.running).toBe(false);
        });

        it('fails when discarding the trace fails for another reason', async () => {
            expect.assertions(1);
            tracing.stop.mockRejectedValueOnce(new Error('ENOSPC'));
            await tracer.start({}, '/out/trace.zip');

            await expect(tracer.endWithContext(false)).rejects.toThrow('ENOSPC');
        });

        it('does nothing when no trace is running', async () => {
            await tracer.endWithContext(true);

            expect(tracing.stop).not.toHaveBeenCalled();
        });
    });

    describe('trace groups', () => {
        const location = { file: '/suite.robot', line: 3, column: 0 };

        it('opens and closes groups in the running trace', async () => {
            await tracer.start({}, '/out/trace.zip');

            await tracer.group('Click', location);
            await tracer.groupEnd();

            expect(tracing.group).toHaveBeenCalledWith('Click', { location });
            expect(tracing.groupEnd).toHaveBeenCalledTimes(1);
        });

        it('sends no groups when no trace is running', async () => {
            await tracer.group('Click', location);
            await tracer.groupEnd();

            expect(tracing.group).not.toHaveBeenCalled();
            expect(tracing.groupEnd).not.toHaveBeenCalled();
        });
    });
});
