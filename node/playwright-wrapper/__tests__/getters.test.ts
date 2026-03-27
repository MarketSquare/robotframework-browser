// Copyright 2020-     Robot Framework Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { getElementStates } from '../getters';

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
    return {
        getSelector: () => selector,
        getStrict: () => strict,
    } as any;
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
    return JSON.parse(response.getJson());
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
