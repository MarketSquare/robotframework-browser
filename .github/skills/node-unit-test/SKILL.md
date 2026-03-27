---
name: write-node-unit-tests
description: 'Write Node.js/TypeScript unit tests for the playwright-wrapper layer. Use when: creating new Jest tests, mocking Playwright API calls, testing getters/interaction/browser-control functions in isolation, improving Node.js test coverage.'
applyTo: 'node/playwright-wrapper/__tests__/**'
---
# Write Node.js Unit Tests

Node.js unit tests live in `node/playwright-wrapper/__tests__/` and use **Jest + ts-jest**.

Tests must be readable and test one thing at a time. Use descriptive `it()` names that read as plain English sentences.

Run tests with invoke:

```bash
inv utest-node
inv utest-node --coverage   # generates HTML report at node/coverage/index.html
```

## File naming

Name test files after the source module they test: `getters.ts` → `getters.test.ts`.

## Mocking external module dependencies

Use `jest.mock()` at the top of the file (before imports) to replace modules with controlled fakes.

### Mocking `playwright-invoke`

`findLocator` is the primary dependency in most getter/interaction functions. Replace it with a `jest.fn()` and keep `exists` real:

```typescript
jest.mock('../playwright-invoke', () => ({
    findLocator: jest.fn(),
    exists: jest.requireActual('../playwright-invoke').exists,
}));

import { findLocator } from '../playwright-invoke';
const mockFindLocator = findLocator as jest.MockedFunction<typeof findLocator>;
```

### Mocking the logger

Suppress log output to keep test output clean:

```typescript
jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));
```

### Mocking Playwright errors

Use the real `errors` export from `playwright` — no mock needed. Throw `new errors.TimeoutError(...)` directly in test stubs.

## Creating mock locators

Build a helper that returns an object with all `Locator` methods stubbed. Pass `overrides` to change just one method per test:

```typescript
function makeMockLocator(overrides: Partial<{
    waitFor: jest.Mock;
    isVisible: jest.Mock;
    isEnabled: jest.Mock;
    getAttribute: jest.Mock;
    isEditable: jest.Mock;
    isChecked: jest.Mock;
    elementHandle: jest.Mock;
}> = {}) {
    return {
        waitFor: jest.fn().mockResolvedValue(undefined),
        isVisible: jest.fn().mockResolvedValue(true),
        isEnabled: jest.fn().mockResolvedValue(true),
        getAttribute: jest.fn().mockResolvedValue(null),
        isEditable: jest.fn().mockResolvedValue(true),
        isChecked: jest.fn().mockResolvedValue(false),
        elementHandle: jest.fn().mockResolvedValue(makeElementHandle()),
        ...overrides,
    } as any;
}
```

## Creating mock gRPC request objects

The generated protobuf `Request.*` classes have getter methods. Mock them with a plain object cast to `any`:

```typescript
function makeRequest(selector = '#el', strict = false) {
    return {
        getSelector: () => selector,
        getStrict: () => strict,
    } as any;
}
```

## Sequencing multiple `evaluate` calls

When a function calls `elementHandle.evaluate()` multiple times, use `mockResolvedValueOnce` chaining:

```typescript
const elementHandle = {
    evaluate: jest.fn()
        .mockResolvedValueOnce(false)   // first call: 'selected' in e
        .mockResolvedValueOnce(true),   // second call: document.activeElement === e
};
```

## Test structure

```typescript
describe('functionName', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('returns detached state when element times out', async () => {
        const locator = makeMockLocator({
            waitFor: jest.fn().mockRejectedValue(new errors.TimeoutError('Timeout')),
        });
        mockFindLocator.mockResolvedValue(locator);

        const result = await getElementStates(makeRequest(), {} as any);

        expect(JSON.parse(result.getJson())).toBe(2); // detached
    });
});
```

## Things to avoid

- Do not add comments or docstrings explaining what the test does — the test name and code should be self-explanatory.
- Do not mock modules that are not needed for the test being written.
- Do not assert on log messages — they are implementation details.
- Do not share mutable mock state between tests; always call `jest.clearAllMocks()` in `beforeEach`.
