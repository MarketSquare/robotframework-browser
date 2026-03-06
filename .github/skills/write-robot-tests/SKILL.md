---
name: write-robot-tests
description: 'Write or review Robot Framework acceptance tests for the Browser library. Use when: creating new .robot test files, adding test cases, writing user keywords, writing library keywords in atest/library/, or reviewing existing tests for rule compliance.'
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

### No `[Documentation]` in test cases or user keywords

Test cases and user keywords defined in `.robot` files must **not** use `[Documentation]`. The name and structure must be sufficient. Inline comments (`#`) are acceptable sparingly for genuinely non-obvious details — they are the exception, not the rule.

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
def assert_passed_duration(start_time: datetime, max_duration_ms: int, delta_ms: int = 300) -> None:
    """Assert that the time elapsed since start_time does not exceed max_duration_ms + delta_ms."""
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
# atest/library/scope_logger.py
def log_all_scopes(exp_timeout: float, exp_strict_mode: bool) -> None:
    b: Browser = BuiltIn().get_library_instance("Browser")
    timeout = b.scope_stack["timeout"].get()
    assert timeout == exp_timeout, f"timeout {timeout} != {exp_timeout}"
```

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
def start_test_server() -> str:
    ...

def assert_passed_duration(start_time: datetime, max_duration_ms: int, delta_ms: int = 300) -> None:
    ...
```

**Bad**
```python
def start_test_server():
    ...

def assert_passed_duration(start_time, max_duration_ms, delta_ms=300):
    ...
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

## File locations

| Content | Location |
|---|---|
| Acceptance test files | `atest/test/<suite>/` |
| Shared library keywords (Python) | `atest/library/` |
| Shared resource files | `atest/test/keywords.resource`, `atest/test/variables.resource` |

## Running acceptance tests

```bash
inv atest
```

Lint after changes:

```bash
inv lint-robot
```
