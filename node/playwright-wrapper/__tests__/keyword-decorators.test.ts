import { beforeEach, describe, expect, it } from '@jest/globals';

const mockInfo = jest.fn();
jest.mock('../browser_logger', () => ({
    logger: { info: mockInfo },
}));

import { async_logger } from '../keyword-decorators';

function capturedCalls(): Array<{ mergingObject: Record<string, unknown>; msg: string }> {
    return mockInfo.mock.calls.map((call) => ({
        mergingObject: call[0] as Record<string, unknown>,
        msg: call[1] as string,
    }));
}

describe('async_logger', () => {
    beforeEach(() => {
        mockInfo.mockClear();
    });

    it('emits event_kind grpc on start', async () => {
        const descriptor = { value: async () => 'result' };
        const wrapped = async_logger('myMethod', descriptor);
        await wrapped.value();
        expect(capturedCalls()[0].mergingObject.event_kind).toBe('grpc');
    });

    it('emits action equal to the property key on start', async () => {
        const descriptor = { value: async () => 'result' };
        const wrapped = async_logger('doSomething', descriptor);
        await wrapped.value();
        expect(capturedCalls()[0].mergingObject.action).toBe('doSomething');
    });

    it('emits status started before calling the method', async () => {
        let statusAtCallTime: unknown;
        const descriptor = {
            value: async () => {
                statusAtCallTime = capturedCalls()[0]?.mergingObject.status;
                return 'result';
            },
        };
        const wrapped = async_logger('myMethod', descriptor);
        await wrapped.value();
        expect(statusAtCallTime).toBe('started');
    });

    it('emits status succeeded after the method resolves', async () => {
        const descriptor = { value: async () => 'result' };
        const wrapped = async_logger('myMethod', descriptor);
        await wrapped.value();
        expect(capturedCalls()[1].mergingObject.status).toBe('succeeded');
    });

    it('emits status failed when the method throws', async () => {
        expect.assertions(1);
        const descriptor = {
            value: async () => {
                throw new Error('boom');
            },
        };
        const wrapped = async_logger('myMethod', descriptor);
        try {
            await wrapped.value();
        } catch {
            // expected
        }
        expect(capturedCalls()[1].mergingObject.status).toBe('failed');
    });

    it('re-throws the error after emitting the failed log line', async () => {
        expect.assertions(1);
        const descriptor = {
            value: async () => {
                throw new Error('original error');
            },
        };
        const wrapped = async_logger('myMethod', descriptor);
        await expect(wrapped.value()).rejects.toThrow('original error');
    });

    it('emits exactly two log lines on success', async () => {
        const descriptor = { value: async () => 'result' };
        const wrapped = async_logger('myMethod', descriptor);
        await wrapped.value();
        expect(mockInfo).toHaveBeenCalledTimes(2);
    });

    it('emits exactly two log lines on failure', async () => {
        const descriptor = {
            value: async () => {
                throw new Error('fail');
            },
        };
        const wrapped = async_logger('myMethod', descriptor);
        try {
            await wrapped.value();
        } catch {
            // expected
        }
        expect(mockInfo).toHaveBeenCalledTimes(2);
    });
});
