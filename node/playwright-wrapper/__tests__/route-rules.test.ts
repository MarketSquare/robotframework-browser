import { beforeEach, describe, expect, it, jest } from '@jest/globals';
import type { Page, Route } from 'playwright';

jest.mock('uuid', () => ({ v4: jest.fn().mockReturnValue('test-uuid') }));
jest.mock('../browser_logger', () => ({ logger: { info: jest.fn() } }));

import { logger } from '../browser_logger';
import type * as pb from '../generated/playwright';
import type { PlaywrightState } from '../playwright-state';
import {
    addContextRoute,
    addPageRoute,
    jsonMergePatch,
    removeAllRouteRules,
    removeRouteRule,
    RouteRules,
} from '../route-rules';

type Handler = (route: Route) => Promise<void>;

function fakeTarget() {
    const handlers: Handler[] = [];
    const dispose = jest.fn(async () => {});
    const route = jest.fn(async (_url: unknown, handler: Handler) => {
        handlers.push(handler);
        return { dispose };
    });
    return { route, handlers, dispose };
}

function fakeState() {
    const context = fakeTarget();
    const page = fakeTarget();
    const indexedContext = { id: 'context=1', c: context, routeRules: new RouteRules() };
    const indexedPage = { id: 'page=1', p: page };
    const state = {
        activeBrowser: { context: indexedContext, page: indexedPage },
        browserStack: [{ contextStack: [indexedContext] }],
    } as unknown as PlaywrightState;
    return { state, context, page, indexedContext };
}

function fakeRoute(abort: (errorCode?: string) => Promise<void> = async () => {}, fulfill = jest.fn()): Route {
    const request = { method: () => 'GET', url: () => 'http://x/api' };
    return { abort, fulfill, request: () => request } as unknown as Route;
}

describe('route rules', () => {
    it('aborts with the error code', async () => {
        const { state, context } = fakeState();
        await addContextRoute({ url: '**/api', abort: { errorCode: 'timedout' } }, state);
        const abort = jest.fn<(errorCode?: string) => Promise<void>>(async () => {});
        await context.handlers[0](fakeRoute(abort));
        expect(abort).toHaveBeenCalledWith('timedout');
    });

    it('fulfills with the status, headers and body bytes', async () => {
        const { state, page } = fakeState();
        const body = Buffer.from([0x89, 0x50, 0x00, 0xff]);
        await addPageRoute(
            { url: '**/api', fulfill: { status: 418, headers: { 'Content-Type': 'image/png' }, body } },
            state,
        );
        const fulfill = jest.fn<(options: unknown) => Promise<void>>(async () => {});
        await page.handlers[0](fakeRoute(undefined, fulfill));
        expect(fulfill).toHaveBeenCalledWith({ status: 418, headers: { 'Content-Type': 'image/png' }, body });
    });

    it('waits for running handler calls before a removal returns', async () => {
        const { state, context } = fakeState();
        const { id } = await addContextRoute({ url: '**/api', abort: {} }, state);
        let finishAbort: () => void = () => {};
        const running = context.handlers[0](fakeRoute(() => new Promise<void>((resolve) => (finishAbort = resolve))));
        let removed = false;
        const removal = removeRouteRule({ id }, state).then(() => (removed = true));
        await new Promise((resolve) => setImmediate(resolve));
        expect(context.dispose).toHaveBeenCalled();
        expect(removed).toBe(false);
        finishAbort();
        await Promise.all([running, removal]);
        expect(removed).toBe(true);
    });

    it('logs that a removed rule never ran', async () => {
        const { state } = fakeState();
        const { id } = await addContextRoute({ url: '**/api', abort: {} }, state);
        const response = await removeRouteRule({ id }, state);
        expect(response.log).toBe(`Removed route rule ${id}. It ran 0 times.`);
    });

    it('logs that a removed rule ran once', async () => {
        const { state, context } = fakeState();
        const { id } = await addContextRoute({ url: '**/api', abort: {} }, state);
        await context.handlers[0](fakeRoute());
        const response = await removeRouteRule({ id }, state);
        expect(response.log).toBe(`Removed route rule ${id}. It ran 1 time.`);
    });

    it('logs how many times a removed rule ran', async () => {
        const { state, page } = fakeState();
        const { id } = await addPageRoute({ url: '**/api', abort: {} }, state);
        await page.handlers[0](fakeRoute());
        await page.handlers[0](fakeRoute());
        const response = await removeRouteRule({ id }, state);
        expect(response.log).toBe(`Removed route rule ${id}. It ran 2 times.`);
    });

    it('forgets a rule that used up its times', async () => {
        const { state, context } = fakeState();
        const { id } = await addContextRoute({ url: '**/api', times: 1, abort: {} }, state);
        await context.handlers[0](fakeRoute());
        const response = await removeRouteRule({ id }, state);
        expect(response.log).toContain(`No route rule ${id}`);
        expect(context.dispose).not.toHaveBeenCalled();
    });

    it('forgets the page rules of a closed page', async () => {
        const { state, page, indexedContext } = fakeState();
        const { id } = await addPageRoute({ url: '**/api', abort: {} }, state);
        indexedContext.routeRules.dropPage(page as unknown as Page);
        const response = await removeRouteRule({ id }, state);
        expect(response.log).toContain(`No route rule ${id}`);
    });

    it('removes all Context and Page rules of the active context', async () => {
        const { state, context, page } = fakeState();
        await addContextRoute({ url: '**/a', abort: {} }, state);
        await addPageRoute({ url: '**/b', abort: {} }, state);
        await addPageRoute({ url: '**/c', abort: {} }, state);
        const response = await removeAllRouteRules({}, state);
        expect(response.log).toContain('Removed 1 Context and 2 Page route rules');
        expect(context.dispose).toHaveBeenCalledTimes(1);
        expect(page.dispose).toHaveBeenCalledTimes(2);
        expect((await removeAllRouteRules({}, state)).log).toContain('Removed 0 Context and 0 Page');
    });

    it('waits for every running handler call even when one removal fails', async () => {
        expect.assertions(2);
        const { state, context, page } = fakeState();
        await addContextRoute({ url: '**/a', abort: {} }, state);
        await addPageRoute({ url: '**/b', abort: {} }, state);
        context.dispose.mockRejectedValueOnce(new Error('dispose failed'));
        let finishAbort: () => void = () => {};
        void page.handlers[0](fakeRoute(() => new Promise<void>((resolve) => (finishAbort = resolve))));
        let settled = false;
        const removal = removeAllRouteRules({}, state).finally(() => (settled = true));
        await new Promise((resolve) => setImmediate(resolve));
        expect(settled).toBe(false);
        finishAbort();
        await expect(removal).rejects.toThrow('dispose failed');
    });

    it('rejects an invalid regular expression', async () => {
        expect.assertions(1);
        const { state } = fakeState();
        await expect(addContextRoute({ url: '/[/', abort: {} }, state)).rejects.toThrow('Invalid regular expression');
    });
});

type FetchOptions = {
    url?: string;
    method?: string;
    headers?: Record<string, string>;
    postData?: Buffer;
    timeout?: number;
};
type FulfillOptions = { response?: unknown; status?: number; headers?: Record<string, string>; body?: Buffer };

function fakeModifyRoute(
    realHeaders: Record<string, string> = {},
    realBody = '',
    requestHeaders: Record<string, string> = {},
    fetch: (options: FetchOptions) => Promise<unknown> = async () => ({
        headers: () => realHeaders,
        body: async () => Buffer.from(realBody),
    }),
) {
    const request = {
        method: () => 'GET',
        url: () => 'http://localhost/api/orders?x=1',
        headers: () => requestHeaders,
    };
    const route = {
        fetch: jest.fn(fetch),
        fulfill: jest.fn<(options: FulfillOptions) => Promise<void>>(async () => {}),
        abort: jest.fn<(errorCode?: string) => Promise<void>>(async () => {}),
        request: () => request,
    };
    return route;
}

async function runModify(modify: Partial<pb.Request_RouteModify>, route: ReturnType<typeof fakeModifyRoute>) {
    const { state, context } = fakeState();
    await addContextRoute(
        {
            url: '**/api',
            modify: {
                requestHeaders: {},
                headers: {},
                removedRequestHeaders: [],
                removedHeaders: [],
                timeout: 5000,
                ...modify,
            },
        },
        state,
    );
    await context.handlers[0](route as unknown as Route);
}

describe('modify route rules', () => {
    beforeEach(() => {
        jest.mocked(logger.info).mockClear();
    });

    it('fulfills with the real response, the new status and merged headers', async () => {
        const route = fakeModifyRoute({
            'content-type': 'application/json',
            'x-real': 'kept',
            'X-Drop': 'gone',
            'x-over': 'old',
        });
        await runModify(
            { status: 500, headers: { 'X-New': 'added', 'X-Over': 'new', 'X-Empty': '' }, removedHeaders: ['x-drop'] },
            route,
        );
        const options = route.fulfill.mock.calls[0][0];
        expect(options.status).toBe(500);
        expect(options.headers).toEqual({
            'content-type': 'application/json',
            'x-real': 'kept',
            'X-New': 'added',
            'X-Over': 'new',
            'X-Empty': '',
        });
        expect(options.body).toBeUndefined();
        expect(options.response).toBe(await route.fetch.mock.results[0].value);
    });

    it('applies the JSON merge patch and drops the stale encoding headers', async () => {
        const route = fakeModifyRoute(
            { 'content-type': 'application/json', 'content-encoding': 'gzip', 'Content-Length': '99' },
            '{"order": {"id": 1, "note": "x"}, "items": [1, 2]}',
        );
        await runModify({ jsonPatch: '{"order": {"note": null, "state": "open"}, "items": [3]}' }, route);
        const options = route.fulfill.mock.calls[0][0];
        expect(options.headers).toEqual({ 'content-type': 'application/json' });
        expect(JSON.parse(String(options.body))).toEqual({ order: { id: 1, state: 'open' }, items: [3] });
    });

    it('replaces the body and keeps the content type that Python resolved', async () => {
        const route = fakeModifyRoute({ 'content-type': 'application/json', 'content-length': '2' }, '{}');
        const body = Buffer.from('replaced');
        await runModify({ body, headers: { 'Content-Type': 'text/plain; charset=utf-8' } }, route);
        const options = route.fulfill.mock.calls[0][0];
        expect(options.headers).toEqual({ 'Content-Type': 'text/plain; charset=utf-8' });
        expect(options.body).toBe(body);
    });

    it('fetches the original request when only the response changes', async () => {
        const route = fakeModifyRoute();
        await runModify({ status: 201 }, route);
        expect(route.fetch).toHaveBeenCalledWith({ timeout: 5000 });
    });

    it('merges the request headers onto the real ones', async () => {
        const route = fakeModifyRoute({}, '', { accept: '*/*', 'x-remove': 'a', Cookie: 'kept=1' });
        await runModify(
            { requestHeaders: { Authorization: 'Bearer abc' }, removedRequestHeaders: ['X-Remove'] },
            route,
        );
        expect(route.fetch.mock.calls[0][0].headers).toEqual({
            accept: '*/*',
            Cookie: 'kept=1',
            Authorization: 'Bearer abc',
        });
    });

    it('resolves a relative URL and drops the original host and cookie', async () => {
        const route = fakeModifyRoute({}, '', { host: 'localhost', Cookie: 'a=1', accept: '*/*' });
        await runModify({ url: '/api/v2/orders' }, route);
        const options = route.fetch.mock.calls[0][0];
        expect(options.url).toBe('http://localhost/api/v2/orders');
        expect(options.headers).toEqual({ accept: '*/*' });
    });

    it('sends the new method and body', async () => {
        const route = fakeModifyRoute();
        const postData = Buffer.from('{"a": 1}');
        await runModify({ method: 'POST', postData }, route);
        const options = route.fetch.mock.calls[0][0];
        expect(options.method).toBe('POST');
        expect(options.postData).toBe(postData);
    });

    it.each(['GET', 'HEAD'])('sends no body when the method changes to %s without one', async (method) => {
        const route = fakeModifyRoute();
        await runModify({ method }, route);
        expect(route.fetch.mock.calls[0][0].postData).toEqual(Buffer.alloc(0));
    });

    it('aborts the request and logs the error without the call log when the fetch fails', async () => {
        const error = new Error(
            'apiRequestContext.fetch: connect ECONNREFUSED 127.0.0.1:1\nCall log:\n  - → GET http://127.0.0.1:1/\n    - authorization: Bearer abc',
        );
        const route = fakeModifyRoute({}, '', {}, async () => {
            throw error;
        });
        await runModify({ url: 'http://127.0.0.1:1/' }, route);
        expect(route.abort).toHaveBeenCalledWith('failed');
        const logged = jest.mocked(logger.info).mock.calls.map(([message]) => String(message));
        expect(logged.some((message) => message.includes('connect ECONNREFUSED 127.0.0.1:1'))).toBe(true);
        expect(logged.some((message) => message.includes('Bearer abc') || message.includes('Call log'))).toBe(false);
    });

    it('aborts the request and logs the error without the call log when the fulfill fails', async () => {
        const route = fakeModifyRoute();
        route.fulfill.mockRejectedValueOnce(
            new Error('route.fulfill: Cannot fulfill with redirect status: 302\nCall log:\n  - x-token: abc'),
        );
        await runModify({ status: 302 }, route);
        expect(route.abort).toHaveBeenCalledWith('failed');
        const logged = jest.mocked(logger.info).mock.calls.map(([message]) => String(message));
        expect(logged.some((message) => message.includes('Cannot fulfill with redirect status: 302'))).toBe(true);
        expect(logged.some((message) => message.includes('x-token: abc'))).toBe(false);
    });

    it('logs the sanitized error when the abort fails too', async () => {
        const route = fakeModifyRoute({}, '', {}, async () => {
            throw new Error('connect ECONNREFUSED\nCall log:\n  - authorization: Bearer abc');
        });
        route.abort.mockRejectedValueOnce(new Error('route.abort: Target page has been closed'));
        await runModify({ url: 'http://127.0.0.1:1/' }, route);
        const logged = jest.mocked(logger.info).mock.calls.map(([message]) => String(message));
        expect(logged.some((message) => message.includes('connect ECONNREFUSED'))).toBe(true);
        expect(logged.some((message) => message.includes('Bearer abc'))).toBe(false);
    });

    it('aborts the request when the real body is not JSON', async () => {
        const route = fakeModifyRoute({}, 'not json');
        await runModify({ jsonPatch: '{"a": 1}' }, route);
        expect(route.abort).toHaveBeenCalledWith('failed');
        expect(route.fulfill).not.toHaveBeenCalled();
    });
});

describe('jsonMergePatch', () => {
    it.each([
        [{ a: 'b' }, { a: 'c' }, { a: 'c' }],
        [{ a: 'b' }, { b: 'c' }, { a: 'b', b: 'c' }],
        [{ a: 'b' }, { a: null }, {}],
        [{ a: 'b', b: 'c' }, { a: null }, { b: 'c' }],
        [{ a: ['b'] }, { a: 'c' }, { a: 'c' }],
        [{ a: 'c' }, { a: ['b'] }, { a: ['b'] }],
        [{ a: { b: 'c' } }, { a: { b: 'd', c: null } }, { a: { b: 'd' } }],
        [{ a: [{ b: 'c' }] }, { a: [1] }, { a: [1] }],
        [
            ['a', 'b'],
            ['c', 'd'],
            ['c', 'd'],
        ],
        [{ a: 'b' }, ['c'], ['c']],
        [{ a: 'foo' }, null, null],
        [{ a: 'foo' }, 'bar', 'bar'],
        [{ e: null }, { a: 1 }, { e: null, a: 1 }],
        [[1, 2], { a: 'b', c: null }, { a: 'b' }],
        [{}, { a: { bb: { ccc: null } } }, { a: { bb: {} } }],
    ])('patches %j with %j into %j (RFC 7386 Appendix A)', (target, patch, expected) => {
        expect(jsonMergePatch(target, patch)).toEqual(expected);
    });
});
