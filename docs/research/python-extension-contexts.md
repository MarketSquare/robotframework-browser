# Extending Browser from your own Python library — what each context gets

> **An evidence record, not documentation. Documentation lives on robotframework-browser.org.**
>
> User-facing prose about extending Browser from Python is on the site, at
> [`/docs/extending/python-libraries`](https://robotframework-browser.org/docs/extending/python-libraries)
> and [`/docs/extending/browser-as-a-base`](https://robotframework-browser.org/docs/extending/browser-as-a-base).
> This repository generates the keyword documentation and the release notes; everything else
> belongs there. This file is kept here anyway, because it is not documentation — it is the
> record of what the acceptance tests in `atest/test/13_Python_Extension/` actually prove, and
> those tests live here.
>
> A snapshot of this file is vendored into the site repository, as
> `docs/research/python-extension-contexts.md`, so those two pages can be checked without a
> checkout of this repository. **That copy is not maintained there — this is the original.** If
> you change anything under `atest/test/13_Python_Extension/`, update this file and re-copy it,
> along with any changed example sources, to the site's `examples/python-extension/`. Nothing
> automates the copy, and the site's build only catches drift in the example files it quotes.

> **Point-in-time record, 2026-08-18. The handoff artifact to robotframework-browser.org.**
>
> This document states what a user's own Python library gets from Browser, in each of the two
> contexts in which Robot Framework is running. It exists because the site repository owns the
> prose and this repository owns the facts, and the site's `CONTRIBUTING.md` promises its
> contributors need neither Python nor a checkout of this library. Every behavioural claim here
> therefore cites a test that proves it, so a site page can be written — and later checked —
> without reading this library's source.
>
> Measured against Browser 20.3.0, Robot Framework 7.4.1, PythonLibCore 4.6.0, Python 3.14,
> macOS. Verification run and environment: §9.
>
> **Two markers are used throughout and they mean different things.**
>
> - **[M] measured** — proven by a named test in `atest/test/13_Python_Extension/`, in a suite
>   run green on the date above.
> - **[R] read** — verified against the source of Browser or Robot Framework at a named line,
>   but never executed. Treat as intent, not as behaviour.
>
> The distinction is not decoration. An earlier draft of ticket 0010 asserted two behaviours
> that had been read from source and never run, and got their scope wrong both times; §3 is
> written the way it is to stop that recurring. Anything not carrying a marker is a definition
> or a pointer, not a claim.
>
> Related, and deliberately **not** restated here:
> [`python-api-options.md`](python-api-options.md) — §3.1 is the Python-vs-Robot-Framework
> behavioural gap and the decision to keep it, §8 is why `validate` and `then` need an
> execution context. Argument conversion is decided by
> [`../adr/0006-python-argument-conversion-via-attribute-table.md`](../adr/0006-python-argument-conversion-via-attribute-table.md),
> which wins over anything below if they ever disagree.

---

## 1. The two contexts, named by who imports Browser

There is exactly one question that decides what your library gets, and it is not how advanced
your library is. It is **who imports Browser**.

| | Context A | Context B |
| --- | --- | --- |
| Robot Framework imports | Browser **and** your library | only your library |
| Who constructs `Browser()` | Robot Framework | your library |
| How your library reaches it | `BuiltIn().get_library_instance("Browser")` | it holds the instance it made |
| Browser's listener is registered | yes, automatically | only if you register it (§4) |
| The motivating user | has outgrown a plugin and wants business logic — logging, `IF`/`ELSE`, `TRY`/`EXCEPT`, data parsing — in Python, with Browser behaving exactly as it does today | is replacing Browser imports and resource-file keywords with their own library, using Browser as a base |
| Worked example | `atest/test/13_Python_Extension/_child/MyLibraryA.py` | `atest/test/13_Python_Extension/_child/MyLibraryB.py` |
| Suite that exercises it | `_child/context_a.robot` | `_child/context_b.robot`, and `_child/context_b_no_listener.robot` for the same library without the registration |

Context A, the lookup, quoted verbatim from
`atest/test/13_Python_Extension/_child/MyLibraryA.py`:

```python
    @property
    def browser(self) -> Browser:
        """The Browser instance that Robot Framework imported.

        Looked up on first use rather than in ``__init__``, because Robot
        Framework may not have imported Browser yet when this library is
        constructed.
        """
        if self._browser is None:
            self._browser = BuiltIn().get_library_instance("Browser")
        return self._browser
```

The lazy lookup is not a style choice. Robot Framework may not have imported Browser yet when
your library is constructed, so `get_library_instance` in `__init__` is a race you lose
depending on the order of the `*** Settings ***` table.

Context B, the ownership, quoted verbatim from
`atest/test/13_Python_Extension/_child/MyLibraryB.py`:

```python
class MyLibraryB:
    """Browser used as a base, with this library owning the instance."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    # Robot Framework resolves the listener API version of every listener
    # separately. Browser declares version 2, but this library would default to
    # version 3, which has different method signatures.
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self._browser = Browser(enable_playwright_debug=True)
        # Robot Framework accepts a list of listeners and calls Browser's
        # listener methods itself. Without this line Browser gets no suite and
        # test events, so automatic closing and scope settings do not work.
        self.ROBOT_LIBRARY_LISTENER = [self, self._browser]
```

**In context B, importing Browser anywhere in the suite — including from a resource file —
turns the run into context A** and quietly makes every context-B property untestable. The
suites guard it rather than trusting review: `Child Should Not Use Library` in
`python_extension.robot` fails the run if any keyword owned by `Browser` appears in the child
`output.xml`. **[M]**

A third context — **no Robot Framework running at all** — is out of scope here and already
measured elsewhere. See §8 before measuring anything about it.

---

## 2. The three-tier matrix

Every row cites the test that proves it. Test names are `robot` test cases; file paths are
relative to the repository root and abbreviated below as `_child/…` for
`atest/test/13_Python_Extension/_child/…`.

### Tier 1 — free, because Robot Framework is running

Present in **both** contexts, and in context B whether or not you register the listener. These
hang off "an execution context exists", not off Browser being imported by Robot Framework
(§3.2).

| What you get | Proven by |
| --- | --- |
| Argument conversion: `browser.click("id=x", "middle")`, `"2 seconds"` → `timedelta`, `"validate"` → `AssertionOperator` **[M]** | `Call Browser From Python` — `_child/context_a.robot`, `_child/context_b.robot`, `_child/context_b_no_listener.robot` |
| A Python `None` stays `None` and never becomes the string `"None"` **[M]** | `Call Browser From Python` (the `evaluate_javascript(None, …)` call in each of the three `MyLibrary*.py`) |
| `browser.outputdir` is Robot Framework's `${OUTPUTDIR}`, so screenshots, videos, traces and the Playwright log land in the run's output directory **[M]** | `Outputdir And Validate Work` — all three child suites |
| The `validate` and `then` assertion operators execute **[M]** | `Outputdir And Validate Work` — all three child suites |

### Tier 2 — recovered by one line of listener registration

Absent in context B until you add `ROBOT_LIBRARY_LISTENER = [self, browser]` (§4); automatic in
context A because Browser registers itself when Robot Framework imports it (§3.1).

| What you get | Proven by |
| --- | --- |
| Automatic closing — pages and contexts opened in a test are closed at its end **[M]** | present: `Open Page Without Closing It` + `Previous Page Was Auto Closed` — `_child/context_a.robot`, `_child/context_b.robot`; absent: `Open Page Without Closing It` + `Previous Page Is Still Open` — `_child/context_b_no_listener.robot` (three pages still open, not one) |
| Scope settings — `set_browser_timeout(…, "Test")` reverts when the test ends **[M]** | present: `Set Test Scoped Timeout` + `Test Scoped Timeout Is Reverted` — `_child/context_a.robot`, `_child/context_b.robot`; absent: `Test Scoped Timeout Leaks To Next Test` — `_child/context_b_no_listener.robot` |
| The Robot Framework suite and test names reaching the node side, so Playwright's own log and trace carry them **[M]** | present: `Playwright Log Should Have Rf Context` in `python_extension.robot`, for the context A and context B runs; absent: `Playwright Log Should Not Have Rf Context` for the no-listener run |
| Playwright **trace groups** in the default `TracingGroupMode.Full` — one group per Robot Framework keyword **[R]** | not measured; source mechanism in §3.4. This row was previously published as "never in context B", which is wrong |

### Tier 3 — yours to build

Not recovered by the listener, in either context, because it lives in the dynamic library API
that Robot Framework only calls on the library **it** imported (§3.3).

| What you do **not** get | Proven by |
| --- | --- |
| `run_on_failure` for a Browser keyword your library calls **from Python** — in context A too, for exactly the calls you moved into Python **[M]** | `Python Call Failure Takes No Screenshot` — `_child/context_a.robot`; contrast `Run On Failure Takes Screenshot` in the same file, where Robot Framework calls the keyword and a screenshot is written |
| `run_on_failure` anywhere in context B, listener or not **[M]** | `Run On Failure Does Not Take Screenshot` — `_child/context_b.robot` and `_child/context_b_no_listener.robot`; the parent asserts zero `fail-screenshot-*` files in both output directories |
| Trace groups in the non-default `TracingGroupMode.Browser`, Browser's error-message rewriting, and `pause_on_failure` **[R]** | not measured; all four live in `Browser.run_keyword` (§3.3) |

Recipes for building the missing failure handling yourself are §6; the first one is tested.

### One more thing the log looks like

A Browser keyword called from Python is **not** a keyword in `output.xml` — Robot Framework
never saw a keyword call. Everything it logs lands inside the keyword of *your* library that
called it. **[M]** — `Child Keyword Should Log` in `python_extension.robot` finds Browser's
`Clicks the element` message inside a `MyLibraryA` / `MyLibraryB` /
`MyLibraryB_no_listener` keyword in each child run.

That is worth saying on the site: a user moving logic into Python is trading a detailed Robot
Framework log for their own keyword's log, in both contexts.

---

## 3. Why the tiers exist — three conditions, routinely conflated

Three *different* conditions decide the three tiers. Nearly every wrong claim about this
feature comes from treating them as one.

| Condition | True when | Drives | Source |
| --- | --- | --- | --- |
| `ROBOT_LIBRARY_LISTENER` is registered | Robot Framework imported Browser, **or** you registered it (§4) | auto-closing, scope settings, node-side Robot Framework context, trace groups in `Full` mode | `Browser/browser.py:510` |
| `EXECUTION_CONTEXTS.current` is non-empty | a Robot Framework run exists at all | `outputdir`, `validate` / `then` | `Browser/browser.py:829-832` |
| `run_keyword` is entered | Robot Framework itself calls a **Browser** keyword | `run_on_failure`, `TracingGroupMode.Browser` groups, error rewriting, `pause_on_failure` | `Browser/browser.py:976-1001` |

### 3.1 Listener registration — tier 2

`Browser.__init__` registers itself (`Browser/browser.py:510`): **[R]**

```python
        self.ROBOT_LIBRARY_LISTENER = self
```

Robot Framework then calls Browser's listener methods — `_start_suite` (`browser.py:866`),
`_start_test` (`893`), `_start_keyword` (`921`), `_end_keyword` (`1027`), `_end_test` (`1035`)
and `_end_suite` (`1050`) — and everything in tier 2 is implemented inside them. `_end_test`
and `_end_suite` call `execute_auto_closing`; `_start_suite` and `_start_test` push scope
frames and push the current suite and test name to the node side. **[R]**

The registration happens in `__init__`, so it exists on every `Browser` instance, including one
your own library constructs. What is missing in context B is not the attribute — it is Robot
Framework *knowing to look at it*, because Robot Framework only reads `ROBOT_LIBRARY_LISTENER`
from libraries it imported. §4 is how you hand it over.

### 3.2 An execution context exists — tier 1

`outputdir` asks a different question entirely (`Browser/browser.py:829-832`): **[R]**

```python
    @property
    def outputdir(self) -> str:
        if EXECUTION_CONTEXTS.current:
            return BuiltIn().get_variable_value("${OUTPUTDIR}")
        return self._output_dir
```

`EXECUTION_CONTEXTS.current` is true whenever a Robot Framework run is in progress, no matter
which library it imported. That is why `outputdir` and the `validate` / `then` operators are
tier 1 and not tier 2 — they were previously published as properties of *calling from Python*,
which is the scope error this document exists to prevent. Measured green in all three child
suites, including the one with no listener at all. **[M]**

### 3.3 `run_keyword` is entered — tier 3

`Browser.run_keyword` (`Browser/browser.py:976-1001`) is the dynamic library API method Robot
Framework calls to execute a Browser keyword. It is not a pass-through: it opens and closes
`TracingGroupMode.Browser` trace groups, and on `AssertionError` / `AttributeError` it calls
`self.keyword_error(selector)` (`browser.py:986`), which is what runs the `run_on_failure`
keyword (`browser.py:1203`). **[R]**

Robot Framework calls `run_keyword` **only on the library it imported itself**. Two
consequences, and the second is the one everybody gets wrong:

1. In context B, Robot Framework calls `run_keyword` on *your* library, never on Browser. No
   registration changes that, because registering a listener is not importing a library. **[M]**
2. In context A, Robot Framework does call Browser's `run_keyword` — but only for keywords
   written in the suite. A Browser keyword that *your Python code* calls goes through
   `__getattr__` and the attribute table, never through `run_keyword`, so it gets no
   screenshot. **[M]** A context-A user who moves logic into Python loses failure screenshots
   for exactly the calls they moved, and nothing warns them.

Both are pinned by a pair of tests in `_child/context_a.robot` that differ only in who calls
the failing keyword, and are told apart by distinct screenshot filename patterns rather than by
an empty directory:

```robotframework
Run On Failure Takes Screenshot
    [Documentation]    Expected to fail. The keyword is called by Robot Framework, so Browser
    ...    runs its `run_on_failure` keyword and leaves a screenshot on disk.
    Open Login Page    ${LOGIN_URL}
    Click    id=this_element_does_not_exist

Python Call Failure Takes No Screenshot
    [Documentation]    Expected to fail. The very same Browser keyword, called from Python by
    ...    MyLibraryA, never enters Browser's `run_on_failure` and leaves no screenshot.
    Open Login Page    ${LOGIN_URL}
    Click Missing Element
```

That this gap is a deliberate, accepted property of the library — and the one-line mechanism
that would close it, which is not being implemented — is §3.1 of
[`python-api-options.md`](python-api-options.md). Do not re-derive it.

### 3.4 Trace groups are tier 2, not tier 3 — **[R] read, not measured**

Trace groups look like they belong with `run_on_failure`, and they do not. In the default
`TracingGroupMode.Full`, the group is opened by the **listener** method `_start_keyword`
(`browser.py:921-932`) and closed by `_end_keyword` (`browser.py:1027-1031`): **[R]**

```python
        if self.tracing_group_mode == TracingGroupMode.Full:
            self._playwright_state.open_trace_group(**kw_call_stack_entry)
```

Library listeners receive events for *every* keyword, not only their own library's
(§6, second recipe), so a context-B library that registers the listener **does** get a trace
group per Robot Framework keyword. Only `TracingGroupMode.Browser` groups come from
`run_keyword` and are therefore genuinely tier 3.

**This row is deliberately untested.** The only observable is Playwright's trace file format,
which is internal and not a public API, and asserting on it would pin a format this project
does not own. It is carried here as a source-cited mechanism claim so that the previously
published "trace groups: never in context B" is not repeated — but it is **read, not
measured**, and a site page should not imply otherwise.

### 3.5 `scope=Test` fails silently without the listener

Worth calling out because there is no error to search for. `SettingsStack.set`
(`Browser/utils/settings_stack.py:64-66`) begins: **[R]**

```python
    def set(self, setting: Any, scope: Scope | None = Scope.Global):
        if not self.library.suite_ids:
            scope = Scope.Global
```

`suite_ids` is only ever populated in `_start_suite`, a listener method. So an unregistered
context-B library asking for a test-scoped setting silently gets a **global** one: no
exception, no warning, and the setting leaks into every later test. Measured by
`Test Scoped Timeout Leaks To Next Test` in `_child/context_b_no_listener.robot`, which asserts
the leaked value rather than the reverted one. **[M]**

### 3.6 Nothing leaks a node process

Browser registers `atexit.register(self.close)` when it starts the node process
(`Browser/playwright.py:167`, inside the `_playwright_process` cached property), so the process
tree goes down at interpreter exit whether or not a listener is registered. **[R]** Verified
after the full run: no `Browser/wrapper/index.js` process survives. **[M]**

A suite teardown closing the browser is therefore not required for cleanliness. The one in
`_child/context_b_no_listener.robot` is kept only for the case where a parent process
terminates the run with a signal, where `atexit` does not run.

---

## 4. The listener-registration recipe — a supported public contract

**Registering Browser as a listener from your own library is a supported, public contract of
Browser.** It is not a workaround, and it is not reaching into a private API. The tests in
`atest/test/13_Python_Extension/` exist partly to keep it supported.

The recipe, verbatim from `atest/test/13_Python_Extension/_child/MyLibraryB.py`:

```python
class MyLibraryB:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self._browser = Browser(enable_playwright_debug=True)
        self.ROBOT_LIBRARY_LISTENER = [self, self._browser]
```

Two Robot Framework primary sources make it legitimate, both verified in Robot Framework
7.4.1: **[R]**

1. **A list is accepted.** `robot/running/testlibraries.py:95`:

   ```python
        return list(listener) if is_list_like(listener) else [listener]
   ```

2. **Underscore-prefixed names are resolved for library listeners.**
   `robot/output/listeners.py:152-155`:

   ```python
       def _get_method_names(self, name):
           names = [name, self._to_camelCase(name)] if "_" in name else [name]
           if self.library is not None:
               names += ["_" + name for name in names]
           return names
   ```

   The leading underscore on `Browser._start_suite` is therefore **not** "private". It is the
   convention that keeps a listener method from also becoming a keyword: Robot Framework's
   static library API skips names starting with `_` (`robot/running/testlibraries.py:517`,
   `name[:1] != "_"`), and the library-listener path adds the underscore back when looking the
   method up.

If you drop the list and write `ROBOT_LIBRARY_LISTENER = self._browser`, this still works —
Browser gets its events. You lose only your own library's listener hooks. The list form exists
so you can have both.

### The `ROBOT_LISTENER_API_VERSION = 2` trap

Robot Framework resolves the listener API version **per listener**, not per registration.
`Listeners._import_listener` (`robot/output/listeners.py:65`) is applied to each element of the
list, and asks each element for its own version at line 78, via `_get_version`
(`robot/output/listeners.py:82`). **[R]**

So in `[self, self._browser]`, Browser gets version 2 from its own class attribute
(`Browser/browser.py:456`) and your library defaults to version 3 — which has different method
signatures. A user who copies Browser's `_end_keyword(self, name, attrs)` signature into their
own library without declaring `ROBOT_LISTENER_API_VERSION = 2` gets a confusing `TypeError` at
run time. `MyLibraryB` declares it explicitly, with a comment, for exactly that reason.

### What you get for the line, and what happens without it

`_child/context_b.robot` and `_child/context_b_no_listener.robot` import libraries that differ
**only** in whether `ROBOT_LIBRARY_LISTENER` is assigned; the bodies are duplicated so either
file can be read on its own. The difference between the two runs *is* tier 2 of the matrix, and
it is measured, not argued: **[M]**

| | with the line | without it |
| --- | --- | --- |
| pages open after three tests that each opened one | 1 | 3 |
| `scope=Test` browser timeout at the start of the next test | reverted to `10 seconds` | still `3 seconds` |
| node-side log records carrying a Robot Framework test name | present — 73 records in the verification run | none — 0 records |

### One practical note **[R]**

`Browser` is `ROBOT_LIBRARY_SCOPE = "GLOBAL"` (`Browser/browser.py:458`) and keeps class-level
state shared by every instance in the process — `_context_cache`, `_suite_cleanup_done` and
`_output_dir` (`Browser/browser.py:460-462`). Give your own library `GLOBAL` scope too, as
`MyLibraryB` does, or Robot Framework will construct several of them and each new `Browser()`
will join state the previous one left behind.

---

## 5. Argument conversion, as it appears to a Python caller

Decided in
[`../adr/0006-python-argument-conversion-via-attribute-table.md`](../adr/0006-python-argument-conversion-via-attribute-table.md),
which is the authority. What a site page needs to say:

- **Plain values convert exactly as Robot Framework converts them.** `"middle"` becomes
  `MouseButton.middle`, `"2 seconds"` becomes a `timedelta`, `"validate"` becomes an
  `AssertionOperator`, `"true"` becomes `True`. This is not a curated subset: conversion reuses
  Robot Framework's own converters, so every type Robot Framework can convert for a keyword
  argument converts on the Python path too, and `@keyword(types=...)` overrides are respected.
- **A Python `None` is passed through unchanged.** It is never converted, so it never becomes
  the string `"None"`. From Python, a caller who means *nothing* passes the `None` object.
- **A string `"None"` is still converted per its hint** — `"None"` is not `None`. On `str | None`
  it stays the string; on `int | None` Robot Framework turns it into `None`. That is Robot
  Framework's documented behaviour and is left alone.
- **Passing an already-typed value is the opt-out.** Conversion is idempotent, so
  `browser.click("//button", MouseButton.middle)` keeps working unchanged.
- **This needs no Robot Framework at all.** Conversion is a property of how a Python call
  reaches the keyword, so it holds in both contexts and outside a run entirely.

Measured in all three child suites by `Call Browser From Python`, whose library method is
identical in the three `MyLibrary*.py` files — quoted verbatim from
`atest/test/13_Python_Extension/_child/MyLibraryA.py`: **[M]**

```python
    def click_heading_with_middle_mouse_button(self):
        """Call Browser with plain Python values.

        ``"middle"`` becomes a ``MouseButton``, ``"2 seconds"`` becomes a
        ``timedelta``, and the ``None`` stays ``None`` instead of turning into
        the string ``"None"``.
        """
        self.browser.wait_for_elements_state("id=heading1", "visible", "2 seconds")
        self.browser.click("id=heading1", "middle")
        return self.browser.evaluate_javascript(None, "() => 'evaluated'")
```

The `None` is load-bearing: `evaluate_javascript(selector: str | None, …)` is a `str` hint, the
exact shape that would be corrupted into the string `"None"` if `None` were converted.

The mechanism — the two dicts, why the Robot Framework path is untouched, the measured cost —
is in the ADR and in [`python-api-options.md`](python-api-options.md) §3. Do not restate it in a
user-facing page; a user needs the four bullets above.

---

## 6. Recovering `run_on_failure` yourself — three recipes

Tier 3 leaves a real problem, so here are the three shapes that solve it. There is no single
correct one; pick by the size of the library. **Only the first is tested.**

### A decorator — best for a small library **[M]**

Quoted verbatim from `atest/test/13_Python_Extension/_child/MyLibraryA.py`:

```python
def screenshot_on_failure(keyword):
    """Take a screenshot when the wrapped keyword fails, then re-raise.

    Browser runs its own ``run_on_failure`` from the Robot Framework dynamic
    library API, which is not entered when a keyword is called from Python.
    A small library can get equivalent behaviour with a decorator like this.
    Larger libraries usually intercept in one place instead, either by being a
    dynamic library themselves or by using PythonLibCore.
    """

    @functools.wraps(keyword)
    def wrapper(self, *args, **kwargs):
        try:
            return keyword(self, *args, **kwargs)
        except Exception:
            self.browser.take_screenshot("my-library-failure-{index}")
            raise

    return wrapper
```

Applied as `@screenshot_on_failure` on `click_missing_element_with_screenshot`, and
demonstrated by `Decorated Python Call Takes Screenshot` in `_child/context_a.robot`. The
parent asserts the screenshot by its own filename pattern, so it cannot be confused with the
one Browser's own `run_on_failure` writes: after the context A run there is exactly one
`fail-screenshot-*` (Browser's, from the Robot-Framework-called failure) and exactly one
`my-library-failure-*` (the decorator's). **[M]**

Works in both contexts. Costs one decorator per keyword you care about, and nothing enforces
that you remember it.

### A library listener `_end_keyword` — nearly free in context B **[R]**

If your library is already a listener — which in context B it is, because that is how you
registered Browser (§4) — you can implement `_end_keyword` and take a screenshot when
`attrs["status"] == "FAIL"`.

Two things to know, both read from Robot Framework source:

- **Library listeners receive events for all keywords, not only their own library's.** Robot
  Framework merges CLI listeners and library listeners into one list
  (`robot/output/logger.py:75-79`) and broadcasts `start_keyword` / `end_keyword` to all of them
  with no filtering by owning library (`robot/output/logger.py:239-246`;
  `robot/output/listeners.py:99-107` keeps the per-suite-scope list). This is why Browser's own
  `_start_keyword` has to test `attrs["libname"] != "Browser"` (`Browser/browser.py:936`) to
  tell its keywords from everybody else's — and why yours will have to do something similar.
- **It carries the version-2 trap** from §4: `_end_keyword(self, name, attrs)` is a listener
  API v2 signature and needs `ROBOT_LISTENER_API_VERSION = 2` on your class.

Note the scope: a listener sees the *Robot Framework keyword* fail — your library's keyword —
not the individual Browser call inside it. That is usually what you want, and it is a different
granularity from the decorator.

### A dynamic library, optionally via PythonLibCore — best for a large library **[R]**

Implement `run_keyword` yourself and put the failure handling in it, so every keyword is covered
by construction and nothing has to be remembered per keyword. Browser's own
`Browser.run_keyword` (`Browser/browser.py:976-1001`) is the worked reference implementation:
try, delegate, and on `AssertionError` / `AttributeError` call the failure keyword before
re-raising.

---

## 7. Corrections to earlier published claims

If a site page or an older ticket says any of the following, it is wrong. Recorded here so the
corrections travel with the facts.

| Previously said | Correct | Where proven |
| --- | --- | --- |
| `outputdir` and `validate` / `then` are properties of calling from Python | They are properties of a Robot Framework run existing at all, and work in both contexts including context B with no listener | §3.2 **[M]** |
| `run_on_failure` is automatic in context A | Automatic only for keywords Robot Framework calls. A Browser keyword called from Python in context A gets no screenshot | §3.3 **[M]** |
| Trace groups: never in context B | In the default `TracingGroupMode.Full` they come from a listener method, so registering the listener is enough. Only `TracingGroupMode.Browser` groups are tier 3 | §3.4 **[R]**, deliberately untested |
| A context-B library without a listener leaks a node process | Nothing leaks; `atexit` closes the process tree at interpreter exit | §3.6 **[M]** |

---

## 8. Deliberately out of scope — no Robot Framework at all

The pure-Python case, where Browser is used from a script with no Robot Framework run anywhere,
is **supported and deliberately not covered here**. It is parked in ticket 0010
(`0010_document_python_usage.md`, section "Parked: using Browser with no Robot Framework at
all"), which is also where its two already-measured facts are recorded:

- `browser.outputdir` is `.` — the current working directory — so screenshots, videos, traces
  and the Playwright log land wherever the script was started from.
- `validate` and `then` raise `RobotNotRunningError: Cannot access execution context`. All 31
  keywords taking an `AssertionOperator` still accept and convert the operator; only these two
  operators' *execution* needs a run. Pre-existing and outside this library's control — see
  [`python-api-options.md`](python-api-options.md) §8 and
  [MarketSquare/robotframework-browser#5164](https://github.com/MarketSquare/robotframework-browser/issues/5164).

**Both are true only in that context.** Under Robot Framework — including when a user library
owns the Browser instance and registers nothing — `${OUTPUTDIR}` resolves and `validate` /
`then` work, which is tier 1 above.

Nobody needs to measure these two again. Argument conversion (§5) applies there as well, since
it needs no execution context.

---

## 9. How this was verified

Run on 2026-08-18, macOS, against Browser 20.3.0, Robot Framework 7.4.1, PythonLibCore 4.6.0,
Python 3.14.

```
node node/dynamic-test-app/dist/server.js &          # the acceptance suites need the test app
uv run inv atest-robot --suite "Python Extension"
```

Result: **3 tests, 3 passed, 0 failed**, process exit code 0. Every **[M]** claim above is a
claim about that run.

Structure worth knowing when reading the suite:

- `atest/test/13_Python_Extension/python_extension.robot` is the **parent** and is pure
  orchestration. It is the suite that must pass.
- The demonstrations are in `_child/`, run as child `robot` processes. Robot Framework skips
  directories whose name starts with `_` when walking a directory but runs them when named
  explicitly, which is what keeps them out of the normal acceptance run. They must be separate
  processes because `Browser` keeps class-level state shared by every instance in a process
  (`Browser/browser.py:460-462`).
- **The child runs are expected to fail.** Robot Framework returns the number of failed tests;
  the failing tests *are* the demonstration. Context A expects exit code **3**, each context B
  suite expects **1**. The parent asserts those codes and then inspects each child's
  `output.xml`, screenshot directory and `playwright-log.txt`.
- Assertion helpers live in `atest/library/child_result.py`, kept out of `13_Python_Extension/`
  on purpose: the files under it are quoted by path on the site and must stay free of test
  scaffolding.

Source line numbers cited above were re-checked against the working tree on 2026-08-18. Line
numbers drift; the quoted code is the durable part of each citation.
