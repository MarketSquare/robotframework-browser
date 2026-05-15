/// <reference types="jest" />

import { beforeEach, describe, expect, it } from '@jest/globals';

import { getElementStates, getText } from '../getters';

// Mock playwright-invoke so findLocator returns our controlled mock locator
jest.mock('../playwright-invoke', () => ({
    findLocator: jest.fn(),
    exists: jest.requireActual('../playwright-invoke').exists,
}));

// Mock the logger to suppress output in tests
jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

import { errors, Locator } from 'playwright';

import { findLocator } from '../playwright-invoke';

const mockFindLocator = jest.mocked(findLocator);

// Bitmask values defined in getters.ts (mirrored here for readable assertions)
const state = {
    attached: 1,
    detached: 2,
    visible: 4,
    hidden: 8,
    enabled: 16,
    disabled: 32,
    editable: 64,
    readonly: 128,
    selected: 256,
    deselected: 512,
    focused: 1024,
    defocused: 2048,
    checked: 4096,
    unchecked: 8192,
};

function makeRequest(selector = '#el', strict = false) {
    return { selector, strict } as any;
}

function makeMockState() {
    return {} as any;
}

function makeElementHandle(overrides: Partial<{ evaluate: jest.Mock }> = {}) {
    return {
        evaluate: jest.fn().mockImplementation(async (fn: (el: unknown) => unknown) => {
            const fakeEl = { selected: undefined };
            return fn(fakeEl);
        }),
        ...overrides,
    };
}

function makeNonOptionElementHandle(focused = false) {
    return makeElementHandle({
        evaluate: jest.fn().mockResolvedValueOnce(false).mockResolvedValueOnce(focused),
    });
}

function makeOptionElementHandle(selected: boolean) {
    return makeElementHandle({
        evaluate: jest.fn().mockResolvedValueOnce(true).mockResolvedValueOnce(selected).mockResolvedValueOnce(false),
    });
}

function makeMockLocator(
    overrides: Partial<{
        waitFor: jest.Mock;
        isVisible: jest.Mock;
        isEnabled: jest.Mock;
        getAttribute: jest.Mock;
        isEditable: jest.Mock;
        isChecked: jest.Mock;
        elementHandle: jest.Mock;
    }> = {},
) {
    return {
        waitFor: jest.fn().mockResolvedValue(undefined),
        isVisible: jest.fn().mockResolvedValue(true),
        isEnabled: jest.fn().mockResolvedValue(true),
        getAttribute: jest.fn().mockResolvedValue(null),
        isEditable: jest.fn().mockResolvedValue(true),
        isChecked: jest.fn().mockResolvedValue(false),
        elementHandle: jest.fn().mockResolvedValue(makeElementHandle()),
        ...overrides,
    } as unknown as Locator;
}

function parsedStates(response: any): number {
    return JSON.parse(response.json);
}

describe('getElementStates', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('returns detached state when element is not attached to DOM', async () => {
        const locator = makeMockLocator({
            waitFor: jest.fn().mockRejectedValue(new errors.TimeoutError('Timeout')),
        });
        mockFindLocator.mockResolvedValue(locator);

        const result = await getElementStates(makeRequest(), makeMockState());

        expect(parsedStates(result)).toBe(state.detached);
    });

    it('returns attached + visible + enabled + editable + unchecked + defocused for a standard interactive element', async () => {
        const locator = makeMockLocator({
            elementHandle: jest.fn().mockResolvedValue(makeNonOptionElementHandle()),
        });
        mockFindLocator.mockResolvedValue(locator);

        const result = await getElementStates(makeRequest(), makeMockState());
        const bits = parsedStates(result);

        expect(bits & state.attached).toBeTruthy();
        expect(bits & state.visible).toBeTruthy();
        expect(bits & state.enabled).toBeTruthy();
        expect(bits & state.editable).toBeTruthy();
        expect(bits & state.unchecked).toBeTruthy();
        expect(bits & state.defocused).toBeTruthy();
        expect(bits & state.detached).toBeFalsy();
        expect(bits & state.hidden).toBeFalsy();
        expect(bits & state.disabled).toBeFalsy();
        expect(bits & state.checked).toBeFalsy();
        expect(bits & state.focused).toBeFalsy();
    });

    it('returns hidden state when element is not visible', async () => {
        const locator = makeMockLocator({
            isVisible: jest.fn().mockResolvedValue(false),
        });
        mockFindLocator.mockResolvedValue(locator);

        const result = await getElementStates(makeRequest(), makeMockState());
        const bits = parsedStates(result);

        expect(bits & state.hidden).toBeTruthy();
        expect(bits & state.visible).toBeFalsy();
    });

    describe('enabled and editable states', () => {
        it('returns disabled + readonly state when element has disabled attribute', async () => {
            const locator = makeMockLocator({
                isEnabled: jest.fn().mockResolvedValue(false),
                getAttribute: jest.fn().mockResolvedValue(''),
                isEditable: jest.fn().mockResolvedValue(false),
            });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getElementStates(makeRequest(), makeMockState());
            const bits = parsedStates(result);

            expect(bits & state.disabled).toBeTruthy();
            expect(bits & state.readonly).toBeTruthy();
            expect(bits & state.enabled).toBeFalsy();
            expect(bits & state.editable).toBeFalsy();
        });

        it('returns readonly state when element is not editable without disabled attribute', async () => {
            const locator = makeMockLocator({
                isEnabled: jest.fn().mockResolvedValue(true),
                getAttribute: jest.fn().mockResolvedValue(null),
                isEditable: jest.fn().mockResolvedValue(false),
            });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getElementStates(makeRequest(), makeMockState());
            const bits = parsedStates(result);

            expect(bits & state.readonly).toBeTruthy();
            expect(bits & state.editable).toBeFalsy();
        });
    });

    it('returns checked state for a checked checkbox', async () => {
        const locator = makeMockLocator({
            isChecked: jest.fn().mockResolvedValue(true),
        });
        mockFindLocator.mockResolvedValue(locator);

        const result = await getElementStates(makeRequest(), makeMockState());
        const bits = parsedStates(result);

        expect(bits & state.checked).toBeTruthy();
        expect(bits & state.unchecked).toBeFalsy();
    });

    it('returns focused state when element is the active element', async () => {
        const locator = makeMockLocator({
            elementHandle: jest.fn().mockResolvedValue(makeNonOptionElementHandle(true)),
        });
        mockFindLocator.mockResolvedValue(locator);

        const result = await getElementStates(makeRequest(), makeMockState());
        const bits = parsedStates(result);

        expect(bits & state.focused).toBeTruthy();
        expect(bits & state.defocused).toBeFalsy();
    });

    describe('option element selected state', () => {
        it('returns selected state for a selected <option> element', async () => {
            const locator = makeMockLocator({
                elementHandle: jest.fn().mockResolvedValue(makeOptionElementHandle(true)),
            });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getElementStates(makeRequest(), makeMockState());
            const bits = parsedStates(result);

            expect(bits & state.selected).toBeTruthy();
            expect(bits & state.deselected).toBeFalsy();
        });

        it('returns deselected state for an unselected <option> element', async () => {
            const locator = makeMockLocator({
                elementHandle: jest.fn().mockResolvedValue(makeOptionElementHandle(false)),
            });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getElementStates(makeRequest(), makeMockState());
            const bits = parsedStates(result);

            expect(bits & state.deselected).toBeTruthy();
            expect(bits & state.selected).toBeFalsy();
        });
    });

    describe('error handling', () => {
        it('silently skips select/focus states when elementHandle throws', async () => {
            const locator = makeMockLocator({
                elementHandle: jest.fn().mockRejectedValue(new Error('not an element')),
            });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getElementStates(makeRequest(), makeMockState());
            const bits = parsedStates(result);

            expect(bits & state.attached).toBeTruthy();
            expect(bits & state.visible).toBeTruthy();
            expect(bits & state.selected).toBeFalsy();
            expect(bits & state.deselected).toBeFalsy();
            expect(bits & state.focused).toBeFalsy();
            expect(bits & state.defocused).toBeFalsy();
        });

        it('re-throws non-timeout errors from waitFor', async () => {
            expect.assertions(1);
            const locator = makeMockLocator({
                waitFor: jest.fn().mockRejectedValue(new Error('unexpected network error')),
            });
            mockFindLocator.mockResolvedValue(locator);

            await expect(getElementStates(makeRequest(), makeMockState())).rejects.toThrow('unexpected network error');
        });
    });
});

describe('getText', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    function makeTextRequest(selector = '#el', strict = false, textType = 'ROBOT_FRAMEWORK_BROWSER_NO_SET') {
        return { selector, strict, textType } as any;
    }

    function makeTextLocator(
        overrides: Partial<{
            evaluate: jest.Mock;
            inputValue: jest.Mock;
            innerText: jest.Mock;
            allInnerTexts: jest.Mock;
            allTextContents: jest.Mock;
            innerHTML: jest.Mock;
        }> = {},
    ) {
        return {
            evaluate: jest.fn().mockResolvedValue('DIV'),
            inputValue: jest.fn().mockResolvedValue('input text'),
            innerText: jest.fn().mockResolvedValue('inner text'),
            allInnerTexts: jest.fn().mockResolvedValue(['text1', 'text2']),
            allTextContents: jest.fn().mockResolvedValue(['content1', 'content2']),
            innerHTML: jest.fn().mockResolvedValue('<span>html</span>'),
            ...overrides,
        } as unknown as Locator;
    }

    describe('when textType is ROBOT_FRAMEWORK_BROWSER_NO_SET', () => {
        it('returns inputValue for a SELECT element', async () => {
            const locator = makeTextLocator({ evaluate: jest.fn().mockResolvedValue('SELECT') });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getText(makeTextRequest(), {} as any);

            expect(result.items).toEqual(['input text']);
        });

        it('returns inputValue for an INPUT element', async () => {
            const locator = makeTextLocator({ evaluate: jest.fn().mockResolvedValue('INPUT') });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getText(makeTextRequest(), {} as any);

            expect(result.items).toEqual(['input text']);
        });

        it('returns inputValue for a TEXTAREA element', async () => {
            const locator = makeTextLocator({ evaluate: jest.fn().mockResolvedValue('TEXTAREA') });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getText(makeTextRequest(), {} as any);

            expect(result.items).toEqual(['input text']);
        });

        it('falls back to innerText for a non-input element', async () => {
            const locator = makeTextLocator({ evaluate: jest.fn().mockResolvedValue('DIV') });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getText(makeTextRequest(), {} as any);

            expect(result.items).toEqual(['inner text']);
        });
    });

    it('returns allInnerTexts for textType allInnerTexts', async () => {
        const locator = makeTextLocator();
        mockFindLocator.mockResolvedValue(locator);

        const result = await getText(makeTextRequest('#el', false, 'allInnerTexts'), {} as any);

        expect(result.items).toEqual(['text1', 'text2']);
    });

    it('returns allTextContents for textType allTextContents', async () => {
        const locator = makeTextLocator();
        mockFindLocator.mockResolvedValue(locator);

        const result = await getText(makeTextRequest('#el', false, 'allTextContents'), {} as any);

        expect(result.items).toEqual(['content1', 'content2']);
    });

    it('returns innerHTML for textType innerHTML', async () => {
        const locator = makeTextLocator();
        mockFindLocator.mockResolvedValue(locator);

        const result = await getText(makeTextRequest('#el', false, 'innerHTML'), {} as any);

        expect(result.items).toEqual(['<span>html</span>']);
    });

    it('returns inputValue for textType inputValue', async () => {
        const locator = makeTextLocator();
        mockFindLocator.mockResolvedValue(locator);

        const result = await getText(makeTextRequest('#el', false, 'inputValue'), {} as any);

        expect(result.items).toEqual(['input text']);
    });

    it('returns innerText for textType innerText', async () => {
        const locator = makeTextLocator();
        mockFindLocator.mockResolvedValue(locator);

        const result = await getText(makeTextRequest('#el', false, 'innerText'), {} as any);

        expect(result.items).toEqual(['inner text']);
    });

    describe('response log message', () => {
        it('includes text type in log when textType is explicit', async () => {
            const locator = makeTextLocator();
            mockFindLocator.mockResolvedValue(locator);

            const result = await getText(makeTextRequest('#el', false, 'innerText'), {} as any);

            expect(result.log).toContain('with text type innerText');
        });

        it('omits text type in log when textType is ROBOT_FRAMEWORK_BROWSER_NO_SET', async () => {
            const locator = makeTextLocator({ evaluate: jest.fn().mockResolvedValue('DIV') });
            mockFindLocator.mockResolvedValue(locator);

            const result = await getText(makeTextRequest(), {} as any);

            expect(result.log).not.toContain('with text type');
            expect(result.log).toMatch(/successfully\.$/);
        });
    });

    describe('error handling', () => {
        it('re-throws errors from locator methods', async () => {
            expect.assertions(1);
            const locator = makeTextLocator({
                innerText: jest.fn().mockRejectedValue(new Error('element detached')),
            });
            mockFindLocator.mockResolvedValue(locator);

            await expect(getText(makeTextRequest('#el', false, 'innerText'), {} as any)).rejects.toThrow(
                'element detached',
            );
        });
    });
});
