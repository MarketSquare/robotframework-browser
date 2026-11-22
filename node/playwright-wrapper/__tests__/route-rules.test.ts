import { describe, expect, it, jest } from '@jest/globals';
import type { Page, Route } from 'playwright';

jest.mock('uuid', () => ({ v4: jest.fn().mockReturnValue('test-uuid') }));
jest.mock('../browser_logger', () => ({ logger: { info: jest.fn() } }));

import type { PlaywrightState } from '../playwright-state';
import { addContextRoute, addPageRoute, removeAllRouteRules, removeRouteRule, RouteRules } from '../route-rules';

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

function fakeRoute(abort: (errorCode?: string) => Promise<void> = async () => {}): Route {
    const request = { method: () => 'GET', url: () => 'http://x/api' };
    return { abort, request: () => request } as unknown as Route;
}

describe('route rules', () => {
    it('aborts with the error code', async () => {
        const { state, context } = fakeState();
        await addContextRoute({ url: '**/api', abort: { errorCode: 'timedout' } }, state);
        const abort = jest.fn<(errorCode?: string) => Promise<void>>(async () => {});
        await context.handlers[0](fakeRoute(abort));
        expect(abort).toHaveBeenCalledWith('timedout');
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

    it('rejects an invalid regular expression', async () => {
        const { state } = fakeState();
        await expect(addContextRoute({ url: '/[/', abort: {} }, state)).rejects.toThrow('Invalid regular expression');
    });
});
