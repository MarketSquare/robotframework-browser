---
name: write-robot-tests
description: 'Write or review Robot Framework acceptance tests for the Browser library. Use when: creating new .robot test files, adding test cases, checking what a keyword logs, writing user keywords, writing library keywords in atest/library/, or reviewing existing tests for rule compliance.'
argument-hint: 'Describe what to test or point to the file to create/review'
---

# Write Robot Framework Tests

These rules apply to acceptance tests in the `atest/` folder.

## Rules

### Tests and user keywords must be self-explanatory

Test case names and keyword calls must read like plain English. No reader should need to look at an implementation to understand the intent. Choose names that describe *what* is being verified, not *how*.

**Good**
```robotframework
*** Test Cases ***
Login Fails With Wrong Password
    Go To    ${LOGIN_URL}
    Fill Text    input#username_field    wrong_user
    Fill Secret    input#password_field    $wrong_password
    Click    css=input#login_button
    Get Text    css=.error-message    ==    Login failed. Invalid user name and/or password.
```

**Bad** — name says nothing specific, comment compensates for a weak name
```robotframework
*** Test Cases ***
Test Login
    # Verify that login with incorrect credentials shows an error
    Go To    ${LOGIN_URL}
    Fill Text    input#username_field    wrong_user
    Fill Secret    input#password_field    $wrong_password
    Click    css=input#login_button
    Get Text    css=.error-message    ==    Login failed. Invalid user name and/or password.
```

### One feature per test, as many assertions as it needs

A test checks one feature, and it asserts every data point that feature shows after its setup.
Split a test when it covers a second feature, not to give each assertion its own test that
reruns the same setup. When reviewing, judge a test by the features it covers, not by its
assertion count.

### No `[Documentation]` in test cases or user keywords

Test cases and user keywords defined in `.robot` files must **not** use `[Documentation]`. The name and structure must be sufficient. Inline comments (`#`) are acceptable sparingly for genuinely non-obvious details — they are the exception, not the rule. The one exception is robotstatuschecker expectations, see [Checking what a keyword logs or how a test ends](#checking-what-a-keyword-logs-or-how-a-test-ends).

The one exception: a test that checks what a keyword logs puts its robotstatuschecker expectations in `[Documentation]`, because that is the only place `inv atest` reads them from, for example `...    LOG 5:*    INFO    REGEXP: Removed route rule \\S+\\. It ran 2 times\\.` in `route_rules.robot`. The documentation then holds only those `LOG` lines.

**Good**
```robotframework
*** Keywords ***
Login User
    Fill Text    input#username_field    demo
    Fill Secret    input#password_field    $mode
    Click    css=input#login_button
```

**Bad**
```robotframework
*** Keywords ***
Login User
    [Documentation]    Fills in credentials and submits the login form.
    Fill Text    input#username_field    demo
    Fill Secret    input#password_field    $mode
    Click    css=input#login_button
```

### Library keywords may have documentation

Python keywords in `atest/library/` and `Browser/keywords/` can and should have docstrings. These are discoverable via libdoc and IDE tooling.

```python
def child_test_status_should_be(
    result: Result, name: str, status: str, message_pattern: str | None = None
) -> None:
    """Verify status, and optionally the failure message, of a child run test."""
    ...
```

### Complex logic belongs in library keywords

If a keyword requires nested branching, or loops, those belong to Python library. Complex data transformation, or non-trivial orchestration, should be also implemented as a Python keyword in `atest/library/` — not as a user keyword in a `.robot` file. Robot Framework syntax is not suited for complex logic.

**Good** — complex assertion delegated to Python
```robotframework
*** Test Cases ***
Scope Settings Are Restored After Test
    Log All Scopes    exp_timeout=10    exp_strict_mode=True
```

```python
# atest/test/08_Scope_Tests/scope_logger.py
def log_all_scopes(exp_timeout: float, exp_strict_mode: bool) -> None:
    b: Browser = BuiltIn().get_library_instance("Browser")
    timeout = b.timeout
    assert timeout == exp_timeout, f"timeout {timeout} != {exp_timeout}"
```

A helper reads library state through a `Browser` property, as `b.timeout` does here (ADR 0009).
State a helper needs that has no property gets a new internal property on `Browser`.

**Bad** — logic squeezed into user keyword
```robotframework
*** Keywords ***
Verify Scope Timeout
    [Arguments]    ${expected}
    ${actual}=    Evaluate    ...complex expression...
    Run Keyword If    '${actual}' != '${expected}'    Fail    ...
```

### Library keywords must have type hints

All Python keyword functions in `atest/library/` must have type annotations on parameters and return values.

**Good**
```python
def start_test_server() -> str: ...


def child_test_status_should_be(
    result: Result, name: str, status: str, message_pattern: str | None = None
) -> None: ...
```

**Bad**
```python
def start_test_server(): ...


def child_test_status_should_be(result, name, status, message_pattern=None): ...
```

### Do not assert elapsed wall-clock time

CI runners stall, so a test that measures how long something took is flaky, and an upper bound
like `< 5000` proves little about the value it means to check. To check a timeout, read the
value Playwright reports in its error, `Timeout 1000ms exceeded`. Where nothing reports the
value, assert only a lower bound: a loaded runner makes a wait longer, never shorter.

**Good** — exact value from Playwright's error (`atest/test/08_Scope_Tests/scope_keywords.resource`)
```robotframework
*** Keywords ***
Timeout Should Be
    [Arguments]    ${expected_ms}
    Run Keyword And Expect Error
    ...    *Timeout ${expected_ms}ms exceeded*
    ...    Click    id=not_here
```

**Bad** — elapsed time with a range
```robotframework
*** Test Cases ***
Timeout Is Set
    Set Browser Timeout    1s
    ${elapsed} =    Milliseconds Until A Wait Fails
    Should Be True    500 < ${elapsed} < 1700
```

### Avoid deeply nested user keywords

The Browser library already provides rich, high-level keywords. Avoid building deep stacks of user keywords that wrap other user keywords. Test-suite-level keywords (in a `*** Keywords ***` section of a `.robot` file) are fine for encapsulating setup/teardown or repeated actions *within that suite*.

**Good** — one thin suite-level keyword delegates directly to Browser keywords
```robotframework
*** Keywords ***
Open Browser To Login Page
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page    ${LOGIN_URL}
```

**Bad** — unnecessary nesting: suite keyword → user keyword → user keyword
```robotframework
*** Keywords ***
Open Browser To Login Page
    Open Browser With Settings
    Navigate To Login

Open Browser With Settings
    New Browser    ${BROWSER}    headless=${HEADLESS}

Navigate To Login
    Go To Login Page

Go To Login Page
    New Page    ${LOGIN_URL}
```

### Checking what a keyword logs or how a test ends

`inv atest` runs robotstatuschecker on the output, which reads expectations from the test's
`[Documentation]`. That is the one use of `[Documentation]` in a test, and it then holds only
these lines. `atest/test/02_Content_Keywords/route_rules.robot` and
`atest/test/01_Browser_Management/load_report.robot` are worked examples.

```robotframework
*** Test Cases ***
Removing A Rule Logs How Many Times It Ran
    [Documentation]
    ...    LOG 5:*    INFO    REGEXP: Removed route rule \\S+\\. It ran 2 times\\.
    ${path} =    Open HTTP Page Without Sending    /api/echo/runs
    ${rule} =    Abort Requests    **${path}
    Send Request    expected_state=error
    Send Request    expected_state=error
    Remove Route Rule    ${rule}
```

- `LOG <keyword>:<message>    <LEVEL>    <message>`. The keyword index counts the test body's
  keywords from 1; Test Setup is not counted. `5.1` is the first keyword inside keyword 5, so
  a keyword run through `Run Keyword And Expect Error` in step 1 is `1.1`. `:*` matches any
  message of that keyword.
- The message is exact unless it starts with `REGEXP:` or `GLOB:`. A regex backslash is
  doubled in Robot Framework data: `\\S+`, `\\.`, `\\n` for a line break inside one message.
- `FAIL <message>` as the first line expects the test to fail with that message, and the test
  then counts as passed.
- A failing expectation names the keyword it looked at (`locator '5'`); a wrong index shows up
  there.

### Network tests drive the HTTP test page

A test that sends, waits for, mocks or changes HTTP traffic uses `${HTTP_URL}`
(`node/dynamic-test-app/static/http.html`) and the generic endpoints `/api/echo/**`,
`/api/respond/**` and `/api/basic-auth/:user/:password`. When a test needs more, extend them.
Their parameters and the page's ids are in `node/dynamic-test-app/README.md`, section "HTTP
test page and endpoints". `atest/test/05_JS_Tests/http_test_page.robot` is the worked example;
for **route rules** it is `atest/test/02_Content_Keywords/route_rules.robot`.

- Build a scenario with `HTTP Page Url` (`atest/library/http_test_page.py`) and one `Go To`.
  `send=1` fires the request on load, so register routes and start `Promise To` waits first.
- Wait with `Get Text    id=state    ==    done` (or `error`), then assert on the panel.
- Compare bytes by sha256: `HTTP Fixture Sha256` against `#response-sha256` or the echo's `sha256`.
- To see whether a request reached the server, give it a path from `Unique HTTP Path` and read
  `HTTP Journal` for that path. `#served-by` tells a real answer (`test-app #<n>`) from a
  **mock response** (`not test-app`).
- The `HTTP` keyword runs `fetch` in the current page, so routes, Wait For keywords and context
  headers see it as page traffic.
- Assert status, size or headers on a `fetch` or `xhr` request; an `<img>` load or a form submit
  shows only the image size or the form result.
- `fixture=` loads its file with one extra request to `/http-fixtures/<name>`; keep matchers
  narrower than `**`.
- A second origin is `${OTHER_ORIGIN_ROOT_URL}` (`127.0.0.1`).
- In the backend, endpoints that read the body raw are registered in `registerHttpTestRoutes`
  (`src/http-test.ts`), before `express.json()`. For a credentialed cross-origin request,
  `Access-Control-Expose-Headers: *` is a literal, so a new response header is listed by name.
- Run the tests with `--browser firefox` and `--browser webkit` too.

## File locations

| Content | Location |
|---|---|
| Acceptance test files | `atest/test/<suite>/`; a new `.robot` file imports `Resource    imports.resource` from its folder |
| Shared library keywords (Python) | `atest/library/` |
| Library keywords for one suite (Python) | next to the suite, as `atest/test/08_Scope_Tests/scope_logger.py` |
| Shared resource files | `atest/test/keywords.resource`, `atest/test/variables.resource`, reached through each folder's `imports.resource` |

## Tags that keep a test out of a run

`inv atest` excludes tests by tag. Tag a new test that cannot run everywhere:

| Tag | Excluded when |
|---|---|
| `no-windows-support`, `no-mac-support` | running on that OS (`--include-mac` keeps macOS ones) |
| `no-iframe` | running with `--framed` |
| `slow` | running with `--smoke` |
| `known-bug-<browser>` | running with `--browser <browser>`; a comment names the issue, or says `Playwright limitation: ...` when Playwright does not support it in that browser. The tag goes once the issue is fixed or Playwright supports it |
| `chromium-only`, `firefox-only`, `webkit-only` | running with `--browser` set to another browser: the feature exists only in that one |
| `require-rf-7.4+` | Robot Framework is older than 7.4 |
| `no-coverage-support` | running `inv atest-coverage` |
| `no-docker-pr` | running in the CI Docker job |
| `tidy-transformer` | always: the file is input data for the `rfbrowser transform` tests |
| `not-implemented` | always |

## Running acceptance tests

The commands are in `AGENTS.md`, section "Build and test". What catches people out:

- `inv atest` tests the last wrapper build: run `inv node-build` after a change to the
  TypeScript wrapper, the proto or a keyword.
- `--test` takes one test name per run; for several, use `--suite` or a tag with `--include`.
- `inv atest-failed` reruns the failures of the last run; pass it the same `--browser`.
- `inv lint-robot` formats the `.robot` files locally; CI only checks them.
