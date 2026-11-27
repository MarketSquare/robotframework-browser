import { describe, expect, it } from '@jest/globals';

import {
    defineRewritePickedSelector,
    patchReportAction,
    PW_RECORD_ACTION_BINDING,
} from '../page/recorder-rewrite-action';
import {
    LOG_BINDING,
    REWRITE_PICKED_SELECTOR_FUNCTION,
    Rewriter,
    REWRITERS_PROPERTY,
} from '../recorder-rewrite-action-contract';

// What the page script does when it runs.
function runPageScript(win: Record<string, unknown>): void {
    patchReportAction(win);
    defineRewritePickedSelector(win);
}

const save = { id: 'save' } as unknown as Element;
const other = { id: 'other' } as unknown as Element;

// A page with two buttons: `#save` and `#other`, both found by `button`.
const query = (selector: string): Element[] => {
    if (selector === 'button') return [save, other];
    if (selector.startsWith('#save') || selector === 'text="Save"') return [save];
    if (selector === '#other') return [other];
    if (selector === 'bad=') throw new Error('Unknown engine "bad"\nmore');
    return [];
};
const click = { name: 'click', selector: '#save', clickCount: 1 };
const rewriter = (rewriteAction: Rewriter['rewriteAction'], name = 'extension 1'): Rewriter => ({
    name,
    rewriteAction,
});

// What the patched binding reports for `action`, and what is logged, on a page
// with `rewriters`.
function record(action: { name: string; selector: string }, ...rewriters: Rewriter[]) {
    const logged: string[] = [];
    const recorded: unknown[] = [];
    const win: Record<string, unknown> = {
        playwright: { $$: query },
        [REWRITERS_PROPERTY]: rewriters,
        [LOG_BINDING]: (line: string) => logged.push(line),
        [PW_RECORD_ACTION_BINDING]: (reported: unknown) => recorded.push(reported),
    };
    runPageScript(win);
    (win[PW_RECORD_ACTION_BINDING] as (reported: unknown) => void)(action);
    return { rewritten: recorded[0], logged };
}

const rewrite = (...rewriters: Rewriter[]) => record(click, ...rewriters);

describe('the hooks on a recorded Action', () => {
    it('gives the hook a copy of the Action and the element, and takes the parts it changes', () => {
        const hook: jest.Mock = jest.fn(({ action }: any) => {
            action.clickCount = 5;
            return { selector: 'text="Save"', button: 'right' };
        });
        expect(rewrite(rewriter(hook))).toEqual({
            rewritten: { ...click, selector: 'text="Save"', button: 'right' },
            logged: [],
        });
        expect(hook).toHaveBeenCalledWith(
            expect.objectContaining({ action: { ...click, clickCount: 5 }, element: save }),
        );
        expect(click.clickCount).toBe(1);
    });

    it('chains the rewriters in load order, each on the Action the one before gave, with its name', () => {
        const second: jest.Mock = jest.fn(({ action }: any) => ({ selector: `${action.selector} >> nth=0` }));
        const { rewritten } = rewrite(
            rewriter(() => ({ selector: '#save-id', name: 'fill' })),
            rewriter(second, 'extension 2'),
        );
        expect(rewritten).toEqual({ ...click, selector: '#save-id >> nth=0' });
        expect(second).toHaveBeenCalledWith(expect.objectContaining({ action: { ...click, selector: '#save-id' } }));
    });

    it.each([
        ['finds no element', '#nothing', 'finds no element'],
        ['finds several', 'button', 'finds 2 elements'],
        ['finds another element', '#other', 'finds another element'],
        ['cannot be checked', 'bad=', 'cannot be checked: Error: Unknown engine "bad"'],
        ['is not a selector', 3, 'is not a selector'],
    ])('records none of the changes when the selector given %s', (_why, selector, reason) => {
        expect(rewrite(rewriter(() => ({ selector, button: 'right' })))).toEqual({
            rewritten: click,
            logged: [`extension 1: Error: ${JSON.stringify(selector)} ${reason}, its changes are not recorded`],
        });
    });

    it('logs what a rewriter logs, and what it does wrong, and goes on', () => {
        const rewritten = rewrite(
            rewriter(({ log }) => {
                log('tried 2 selectors');
            }),
            rewriter(() => {
                throw new Error('boom');
            }, 'extension 2'),
            rewriter(() => 'text="Save"', 'extension 3'),
            rewriter(() => ({ selector: 'text="Save"' }), 'extension 4'),
        );
        expect(rewritten).toEqual({
            rewritten: { ...click, selector: 'text="Save"' },
            logged: [
                'extension 1: tried 2 selectors',
                'extension 2: Error: boom, its changes are not recorded',
                'extension 3: Error: expected an object, received a string, its changes are not recorded',
            ],
        });
    });

    it('takes what a hook gives as data, as Playwright passes it to Node', () => {
        expect(rewrite(rewriter(() => ({ text: 'a', at: () => 1 }))).rewritten).toEqual({ ...click, text: 'a' });
    });

    it("keeps the Action when Playwright's own selector does not find exactly one element", () => {
        const hook = jest.fn();
        const button = { name: 'click', selector: 'button' };
        expect(record(button, rewriter(hook))).toEqual({
            rewritten: button,
            logged: ['button finds 2 elements here, the Action is kept'],
        });
        expect(hook).not.toHaveBeenCalled();
    });
});

describe('the page script', () => {
    function fakeWindow(rewriters: Rewriter[], binding?: (action: unknown) => void) {
        const logged: unknown[] = [];
        const win: Record<string, any> = {
            playwright: { $$: query },
            [REWRITERS_PROPERTY]: rewriters,
            [LOG_BINDING]: (line: unknown) => logged.push(line),
        };
        if (binding) win[PW_RECORD_ACTION_BINDING] = binding;
        runPageScript(win);
        return { win, logged };
    }
    const toSave = rewriter(() => ({ selector: 'text="Save"' }));

    it('reports the Action with what the rewriters changed, and its name', () => {
        const recorded: unknown[] = [];
        const renaming = rewriter(() => ({ selector: 'text="Save"', name: 'fill' }));
        const { win } = fakeWindow([renaming], (action) => recorded.push(action));
        win[PW_RECORD_ACTION_BINDING](click);
        expect(recorded).toEqual([{ ...click, selector: 'text="Save"' }]);
    });

    it('sends what the rewriters log to Node', () => {
        const logging = rewriter(({ log }) => {
            log('tried 1');
        });
        const { win, logged } = fakeWindow([logging], () => undefined);
        win[PW_RECORD_ACTION_BINDING](click);
        expect(logged).toEqual(['extension 1: tried 1']);
    });

    it('patches a binding Playwright sets after it, and every one it sets later', () => {
        const recorded: unknown[] = [];
        const { win } = fakeWindow([toSave]);
        expect(win[PW_RECORD_ACTION_BINDING]).toBeUndefined();
        win[PW_RECORD_ACTION_BINDING] = (action: any) => recorded.push(['first', action.selector]);
        win[PW_RECORD_ACTION_BINDING](click);
        win[PW_RECORD_ACTION_BINDING] = (action: any) => recorded.push(['second', action.selector]);
        win[PW_RECORD_ACTION_BINDING]({ name: 'fill', selector: '#save' });
        expect(recorded).toEqual([
            ['first', 'text="Save"'],
            ['second', 'text="Save"'],
        ]);
    });

    it('patches the binding once, however often it runs', () => {
        const recorded: any[] = [];
        const nth = rewriter(({ action }) => ({ selector: `${String(action.selector)} >> nth=0` }));
        const { win } = fakeWindow([nth], (action) => recorded.push(action));
        runPageScript(win);
        win[PW_RECORD_ACTION_BINDING](click);
        expect(recorded[0].selector).toBe('#save >> nth=0');
    });

    it('reports the Action unchanged without rewriters, and without a selector', () => {
        const recorded: unknown[] = [];
        fakeWindow([], (action) => recorded.push(action)).win[PW_RECORD_ACTION_BINDING](click);
        fakeWindow([toSave], (action) => recorded.push(action)).win[PW_RECORD_ACTION_BINDING]({ name: 'navigate' });
        expect(recorded).toEqual([click, { name: 'navigate' }]);
    });

    it('reports the Action, and logs why, when the hooks cannot run', () => {
        const recorded: unknown[] = [];
        const { win, logged } = fakeWindow([toSave], (action) => recorded.push(action));
        delete win.playwright;
        win[PW_RECORD_ACTION_BINDING](click);
        expect(recorded).toEqual([click]);
        expect(String(logged[0])).toMatch(/^the Action is kept: TypeError/);
    });

    it('gives the later clicks of a double click what the hooks gave for the first', () => {
        const hook: jest.Mock = jest.fn(() => ({ selector: 'text="Save"' }));
        const recorded: any[] = [];
        const { win } = fakeWindow([rewriter(hook)], (action) => recorded.push(action));
        win[PW_RECORD_ACTION_BINDING](click);
        win[PW_RECORD_ACTION_BINDING]({ ...click, clickCount: 2 });
        win[PW_RECORD_ACTION_BINDING]({ ...click, clickCount: 3 });
        expect(hook).toHaveBeenCalledTimes(1);
        expect(recorded.map((action) => action.selector)).toEqual(Array(3).fill('text="Save"'));
        win[PW_RECORD_ACTION_BINDING]({ name: 'fill', selector: '#save' });
        win[PW_RECORD_ACTION_BINDING]({ ...click, clickCount: 2 });
        expect(hook).toHaveBeenCalledTimes(3);
    });

    it('rewrites a later click on another selector than the click before', () => {
        const hook: jest.Mock = jest.fn(() => undefined);
        const recorded: any[] = [];
        const { win } = fakeWindow([rewriter(hook)], (action) => recorded.push(action));
        win[PW_RECORD_ACTION_BINDING](click);
        win[PW_RECORD_ACTION_BINDING]({ ...click, selector: '#other', clickCount: 2 });
        expect(hook).toHaveBeenCalledTimes(2);
        expect(recorded[1].selector).toBe('#other');
    });

    it('rewrites a pick through its function', () => {
        const { win } = fakeWindow([toSave]);
        expect(win[REWRITE_PICKED_SELECTOR_FUNCTION]('#save')).toBe('text="Save"');
        expect(fakeWindow([]).win[REWRITE_PICKED_SELECTOR_FUNCTION]('#save')).toBe('#save');
    });
});
