# Browser Library

The keyword library itself. This context is about **how a keyword call reaches a keyword
body** — there are two routes into the same keyword, and they behave differently on purpose.

## Language

**Robot Framework path**:
A keyword call arriving through `run_keyword`, with arguments already converted by Robot
Framework before the library sees them.
_Avoid_: RF path, dynamic API path

**Python path**:
A keyword call arriving by attribute access on the library instance, from a plain Python
script with no Robot Framework run.
_Avoid_: direct call, native call

**Keyword table**:
The mapping the **Robot Framework path** reads (`self.keywords`), keyed by Robot name.
_Avoid_: keyword dict, keyword registry

**Attribute table**:
The mapping the **Python path** reads (`self.attributes`), keyed by both the method name and
the Robot name, so one keyword may appear twice.
_Avoid_: attribute dict

**Argument conversion**:
Turning a plain value into the keyword's declared type using Robot Framework's own
converters — `"middle"` into `MouseButton.middle`, `"1.5s"` into a `timedelta`.
_Avoid_: coercion, casting, parsing

**Translation**:
A language package that replaces keywords' Robot names and documentation. A keyword keeps
its method name under a translation; only the name a test calls it by changes.
_Avoid_: localisation, language file

**Run-on-failure keyword**:
The keyword the library runs when a Browser keyword fails on the **Robot Framework path**,
by default `Take Screenshot`. It may be a Browser keyword or any other keyword.
_Avoid_: failure handler, on-failure hook

**Failed page**:
A page that a keyword opened and that the library will remove because that keyword failed.
It still exists while the keyword's failure is being handled, so the failure screenshot shows
it; it is gone by the time the failure reaches the test.
_Avoid_: broken page, dead page

**Load report**:
What a page had and had not loaded at the moment a keyword's wait for it to load timed out:
whether its navigation committed, how far the document got, and which requests were still
outstanding. It answers "did the page never load, or did the wait miss it?"
_Avoid_: load state (that is the `waitUntil` value a keyword waits for), load diagnostics

**JavaScript extension keyword**:
A keyword whose body is a function in a `jsextension` module. It is called like any other
keyword, over the **Robot Framework path** or the **Python path**, and a Python library built
on Browser can also call the function by name with `call_js_keyword`.
_Avoid_: JS keyword, extension function (that is the JavaScript side only)

**Adopted context**:
A browser context that a **JavaScript extension keyword** created itself, such as the context of
an Electron app, and handed over with `adoptContext`. From then on Browser owns its lifecycle and
registers it like a context of `New Context`.
_Avoid_: external context, foreign context

**Injected argument**:
An argument of a **JavaScript extension keyword**'s function that the library supplies by
name instead of taking it from the caller: `page`, `context`, `browser`, `logger`,
`playwright`, `adoptContext` and `defaultTimeout`.
_Avoid_: reserved argument, API argument

**Context trace**:
A trace that runs from the moment a context is created, because the test asked for tracing when
it created the context or turned tracing on for the whole run. It is saved when the context
closes, unless it is stopped earlier.
_Avoid_: full trace, context tracing

**Ad-hoc trace**:
A trace that a test starts on purpose on an already open context, to record only part of what
that context does. A test may record several ad-hoc traces one after another on the same
context.
_Avoid_: trace chunk (Playwright's chunks are a different thing), partial trace

**Trace group**:
A keyword's entry in a trace, under which the trace viewer nests what the keyword did on that
trace's context.
_Avoid_: keyword group, trace step

**Target context**:
The context a keyword is about: the one an argument names, or the active one when no argument
does. A keyword can have several, like `Close Context    ALL`.
_Avoid_: touched context, current context

**Init script**:
JavaScript that a context or page runs in every document it loads, before the document's own
scripts. It lives as long as the context or page it was added to; a context's init script also
runs in the context's popups, a page's does not.
_Avoid_: preload script, startup script

## Relationships

- A context runs at most one trace at a time, a **context trace** or an **ad-hoc trace**.
  Starting a trace while one is running is a mistake in the test and fails. Stopping works the
  same for both kinds; stopping when nothing is running fails.
- An **ad-hoc trace** has a scope, like the library settings: it is saved when that test or
  suite ends, or when its context closes, whichever comes first. A `Global` one lasts until it
  is stopped or its context closes. On the **Python path** every scope is `Global`.
- A trace that the library ends on its own, when a test or suite ends, is not saved if that test
  or suite passed and the library is set to drop traces of passed tests. A trace the test stops
  or closes itself is always saved. Both kinds of trace follow this rule.
- A **trace group** appears only in the traces of the keyword's **target contexts**, nested
  in the groups of the keywords that called it. A keyword with no **target context**, like
  `Log`, goes to the trace of the context active when it ends. Reading other contexts on the
  way, as `Get Browser Catalog` does, does not make them **target contexts**.
- Both tables hold the *same* keyword methods, stored twice by PythonLibCore. They are
  independent: changing one does not change the other.
- **Argument conversion** happens before the **Robot Framework path** reaches the keyword
  table, and inside the **attribute table** for the **Python path**.
- Trace groups and failure screenshots exist only on the **Robot Framework path**. This is a
  known, accepted difference, not a defect.
- A **failed page** outlives its keyword only on the **Robot Framework path**, where failure
  handling runs; on the **Python path** it is removed as soon as the keyword fails.
- A **load report** belongs to a page, not to a keyword: every keyword that waits for a page to
  load gives one when that wait times out. When `New Page` times out, it is the report of the
  **failed page**.
- **Injected arguments** are filled however a **JavaScript extension keyword** is called.
  Only `defaultTimeout` yields to a caller, and only to a library calling the function by name
  with `call_js_keyword`. Called as a keyword, it always gets the library timeout, which a test
  changes with `Set Browser Timeout`.
- An **init script** has no scope of its own. It ends when its context or page closes, so when
  that happens is decided by the automatic closing level, not by the library's `Scope`. On the
  **Python path** it behaves the same.
- An **adopted context** is registered by `call_js_keyword`, from what Node reports when
  `adoptContext` resolves, however the **JavaScript extension keyword** was called.

## Example dialogue

> **Dev:** "I added conversion for Python callers — won't that convert twice under Robot
> Framework?"
> **Domain expert:** "No. Robot Framework reads the keyword table and never touches the
> attribute table, so the Robot Framework path never enters the wrapper at all."
