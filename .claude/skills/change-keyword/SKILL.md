---
name: change-keyword
description: 'Add, change or remove a Browser library keyword across proto, Node and Python. Use when a task touches a keyword''s name, arguments, behaviour or docstring, or adds a new one.'
argument-hint: 'The keyword, and what should change'
---

# Change a keyword

A keyword spans three layers: a Python method in `Browser/keywords/`, an rpc in
`protobuf/playwright.proto`, and a Node handler in `node/playwright-wrapper/`. `Get Title` is a
small, complete example to copy: `Getters.get_title` → `rpc GetTitle` → `getTitle` in
`grpc-service.ts` → `getters.getTitle`.

## Steps

### 1. Is there a need for a keyword?

For a new keyword, name the need first. It is one of:

- Playwright functionality that can only be exposed to users as a keyword, or
- a user need that is generally useful, not one test's convenience.

Then look for a way that keeps the keyword count down: a new argument on an existing keyword, a
better assertion, or one higher-level keyword that combines several Playwright calls. State that
plugins, libraries built on Browser, or acceptance-test helpers need goes on an internal
`Browser` property, not a keyword (ADR 0009).

Every public keyword becomes an entry in each translation users maintain
(`rfbrowser translation`), so removing or renaming one is a breaking change for them too.

Done when the need is stated in one sentence and the maintainer agrees with the shape: new
keyword, new argument, or no keyword.

### 2. Proto

Add or change the rpc in `service Playwright` and its messages under `Request` or `Response`.
Reuse an existing message when one fits (`Request.Empty`, `Response.String`, `Response.Json`).
Run `inv node-build`; it regenerates the Python and TypeScript stubs.

Done when `inv node-build` succeeds.

### 3. Node

Write the implementation as a function in the feature module (`getters.ts`, `interaction.ts`,
...) that takes the request and the page, context or locator it acts on, and returns a
`pb.Response_*`. Register it in `grpc-service.ts` with a handler shaped like its neighbours:
resolve the active page or browser from `call`, call the function, and pass errors through
`errorResponse`. Element lookups go through `findLocator` in `playwright-invoke.ts`, so strict
mode and frame piercing behave like every other keyword.

Done when `inv node-build` and `inv lint-node` pass.

### 4. Python

Put the method on the keyword class for its feature area in `Browser/keywords/`, decorated with
`@keyword(tags=(...))`; a new class must also be added to the `libraries` list in
`Browser.__init__`. Call Node with `with self.playwright.grpc_channel() as stub:`.

- **Annotations stay narrow**: an Enum, not `Enum | str` (ADR 0006).
- **A getter asserts** with `@with_assertion_polling` and the `assertionengine` helpers
  (`verify_assertion` and friends), the way `get_title` does.
- **Timeouts and other settings** come from `LibraryComponent` properties (`self.timeout`), never
  from `scope_stack` directly (ADR 0009).

Done when `inv lint-python` passes.

### 5. Docstring

The docstring is the user documentation. It says what the keyword is for, what each argument
really does, and gives an example when usage is not obvious. When an argument's behaviour
changes, rewrite its row and check the example still holds. Code and tests stay free of
explanatory comments. `inv node-build` regenerates `browser.pyi` from the new signature.

Check the result the way users read it: `python -m robot.libdoc Browser show "<Keyword Name>"`
prints the signature and docstring, and `inv docs` renders the full page to `docs/Browser.html`
(gitignored) for checking links and formatting.

Done when every argument is described, the rendered page shows no broken links or formatting, and
`utest/test_docs.py` passes.

### 6. Tests

- **Jest** for Node logic worth testing in isolation (`node-unit-test` skill).
- **pytest** for Python logic that runs without a browser (`python-unit-test` skill).
- **Acceptance tests** for the keyword's behaviour against the Test App (`write-robot-tests`
  skill). A new page or element for them goes in `node/dynamic-test-app/`.

Done when `inv utest`, `inv utest-node` and the affected `inv atest --suite` runs pass, and
`inv lint` is clean.
