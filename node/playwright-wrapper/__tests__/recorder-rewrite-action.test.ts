import { describe, expect, it } from '@jest/globals';
import * as vm from 'vm';

jest.mock('../browser_logger', () => ({ logger: { info: jest.fn(), error: jest.fn() } }));
jest.mock('fs', () => ({ ...jest.requireActual('fs'), readFileSync: () => '/* page script */' }));

import { logger } from '../browser_logger';
import { installRewritingScript, rewritePickedSelector } from '../recorder-rewrite-action';
import { LOG_BINDING, REWRITE_PICKED_SELECTOR_FUNCTION, REWRITERS_PROPERTY } from '../recorder-rewrite-action-contract';

beforeEach(() => jest.clearAllMocks());

describe('installRewritingScript', () => {
    function fakeContext() {
        const frame = { evaluate: jest.fn(async () => undefined) };
        return {
            frame,
            _exposeConsoleApi: jest.fn(async () => undefined),
            addInitScript: jest.fn(async () => undefined),
            exposeBinding: jest.fn(async () => undefined),
            pages: () => [{ frames: () => [frame] }],
        } as any;
    }
    const added = (context: any): string[] => context.addInitScript.mock.calls.map((call: any) => call[0].content);
    // The names of the hooks a script gives the page.
    const hooksIn = (script: string) => {
        const page: Record<string, any> = {};
        vm.runInNewContext(script, { window: page });
        return page[REWRITERS_PROPERTY].map((hook: any) => hook.name);
    };
    function byName({ action }: any) {
        return { selector: action.name };
    }
    function another() {
        return undefined;
    }
    const extension = { __rewriteAction: byName };

    it('leaves the pages alone without a hook', async () => {
        const context = fakeContext();
        await installRewritingScript(context, [{ someKeyword: () => 'x' }, { __rewriteAction: 42 }]);
        expect(context._exposeConsoleApi).not.toHaveBeenCalled();
        expect(context.addInitScript).not.toHaveBeenCalled();
    });

    it('gives the page the hooks of the extensions that have one, by their names, in load order', async () => {
        const context = fakeContext();
        function bang({ action }: any) {
            return { selector: `${action.selector}!` };
        }
        await installRewritingScript(context, [extension, { someKeyword: () => 'x' }, { __rewriteAction: bang }]);
        const page: Record<string, any> = {};
        vm.runInNewContext(added(context)[0], { window: page });
        const [first, second] = page[REWRITERS_PROPERTY];
        expect([first.name, second.name]).toEqual(['byName', 'bang']);
        expect(first.rewriteAction({ action: { name: 'click' } })).toEqual({ selector: 'click' });
        expect(second.rewriteAction({ action: { selector: '#a' } })).toEqual({ selector: '#a!' });
    });

    const unnamed = 'recorder: __rewriteAction number 1 is not a named function, left out';
    it.each([
        ['a function without a name', [() => undefined][0], unnamed],
        ['a function named after the hook', { __rewriteAction: () => undefined }.__rewriteAction, unnamed],
        ['source instead of a function', '() => undefined', unnamed],
        ['a named method, whose source the page cannot run', Object.values({ myHook() {} })[0], unnamed],
        ['an arrow function with a name', Object.values({ myHook: () => undefined })[0], unnamed],
        ['an async function', async function myHook() {}, unnamed],
    ])('leaves out and logs %s, and gives the others', async (_what, hook, logged) => {
        const context = fakeContext();
        await installRewritingScript(context, [{ __rewriteAction: hook }, extension]);
        expect(logger.info).toHaveBeenCalledWith(logged);
        expect(hooksIn(added(context)[0])).toEqual(['byName']);
    });

    it('exposes the console API, and adds the hooks with the page script to every frame as one script, once', async () => {
        const context = fakeContext();
        await installRewritingScript(context, [extension]);
        await installRewritingScript(context, [extension]);
        expect(context._exposeConsoleApi).toHaveBeenCalledTimes(1);
        expect(added(context)).toHaveLength(1);
        expect(added(context)[0]).toContain('/* page script */');
        expect(hooksIn(added(context)[0])).toEqual(['byName']);
        expect(context.frame.evaluate).toHaveBeenCalledTimes(1);
    });
    it('exposes the binding through which the page logs to playwright-log.txt, once', async () => {
        const context = fakeContext();
        await installRewritingScript(context, [extension]);
        await installRewritingScript(context, [extension, { __rewriteAction: another }]);
        expect(context.exposeBinding).toHaveBeenCalledTimes(1);
        const [name, log] = context.exposeBinding.mock.calls[0];
        expect(name).toBe(LOG_BINDING);
        log({}, 'byName: tried 1');
        expect(logger.info).toHaveBeenCalledWith('recorder: __rewriteAction byName: tried 1');
    });

    it('serializes the hooks into one script that gives them to the page', async () => {
        const page: Record<string, any> = {};
        const context = fakeContext();
        await installRewritingScript(context, [extension]);
        vm.runInNewContext(added(context)[0], { window: page });
        expect(page[REWRITERS_PROPERTY][0].rewriteAction({ action: { name: 'click' } })).toEqual({ selector: 'click' });
    });

    it('gives the pages the new hooks when they change', async () => {
        const context = fakeContext();
        await installRewritingScript(context, [extension]);
        await installRewritingScript(context, [extension, { __rewriteAction: another }]);
        expect(added(context).map(hooksIn)).toEqual([['byName'], ['byName', 'another']]);
    });

    it('installs again after a failure, and logs it, but exposes the console API and the binding once', async () => {
        const context = fakeContext();
        context.addInitScript.mockImplementationOnce(async () => {
            throw new Error('context closing');
        });
        await installRewritingScript(context, [extension]);
        expect(logger.info).toHaveBeenCalledWith(expect.stringContaining('context closing'));
        await installRewritingScript(context, [extension]);
        expect(added(context).map(hooksIn)).toEqual([['byName'], ['byName']]);
        expect(context._exposeConsoleApi).toHaveBeenCalledTimes(1);
        expect(context.exposeBinding).toHaveBeenCalledTimes(1);
    });
    it('logs nothing without a hook, also when Playwright offers no console API', async () => {
        const context = fakeContext();
        delete context._exposeConsoleApi;
        await installRewritingScript(context, [{ someKeyword: () => 'x' }]);
        expect(logger.info).not.toHaveBeenCalled();
    });

    it('logs, and leaves the pages alone, when Playwright offers no console API', async () => {
        const context = fakeContext();
        delete context._exposeConsoleApi;
        await installRewritingScript(context, [extension]);
        expect(context.addInitScript).not.toHaveBeenCalled();
        expect(logger.info).toHaveBeenCalledWith(expect.stringContaining('BrowserContext._exposeConsoleApi'));
    });
});

describe('rewritePickedSelector', () => {
    const fakePage = (evaluate: jest.Mock) => ({ locator: jest.fn(() => ({ evaluate })) }) as any;
    const extensions = [{ __rewriteAction: another }];
    function another() {
        return undefined;
    }

    it('keeps the pick without a hook', async () => {
        const page = fakePage(jest.fn());
        expect(await rewritePickedSelector('#a', page, 1000, [])).toBe('#a');
        expect(page.locator).not.toHaveBeenCalled();
    });

    it('rewrites the pick in the frame of the picked element', async () => {
        const evaluate = jest.fn(async () => 'text="A"');
        const page = fakePage(evaluate);
        const selector = '#f >> internal:control=enter-frame >> #a';
        expect(await rewritePickedSelector(selector, page, 1000, extensions)).toBe(
            '#f >> internal:control=enter-frame >> text="A"',
        );
        expect(page.locator).toHaveBeenCalledWith(selector);
        expect((evaluate.mock.calls[0] as unknown[])[1]).toEqual([REWRITE_PICKED_SELECTOR_FUNCTION, '#a']);
    });

    it('keeps the pick when the page cannot rewrite it', async () => {
        const page = fakePage(
            jest.fn(async () => {
                throw new Error('detached');
            }),
        );
        expect(await rewritePickedSelector('#a', page, 1000, extensions)).toBe('#a');
        expect(logger.info).toHaveBeenCalledWith(expect.stringContaining('could not run on the pick'));
    });
});
