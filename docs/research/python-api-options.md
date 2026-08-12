# Python-friendly keyword arguments — implementation options

> **Point-in-time record, 2026-08-11. Not maintained.**
>
> This is the investigation that led to a decision, kept for its evidence rather than as
> current documentation. The decision itself is
> [`docs/adr/0006-python-argument-conversion-via-attribute-table.md`](../adr/0006-python-argument-conversion-via-attribute-table.md),
> which is the file to read first and the one that is kept true.
>
> Measured against Browser 20.3.0, PythonLibCore 4.5.0, Python 3.14, RF 7.4.1. PythonLibCore
> has since moved to 4.6.0. These claims were re-verified on 2026-08-11 against 4.6.0 while
> Option B was implemented: the two-table split, the attribute/keyword entry counts, the
> conversion error text on RF 7.1.1 and 7.4.2, and that `rfbrowser translate` checksums are
> unchanged by wrapping. Everything else is as it was measured and has not been rechecked.
>
> Two things this document got wrong, corrected during implementation:
> **(1)** the `converting_proxy` in §3 binds arguments without guarding `signature.bind`, so a
> wrong-arity call reports bind's message instead of Python's — the shipped version falls back
> to calling through. **(2)** jsextension keywords are *not* covered: they are code-generated
> without type annotations, so there is nothing to convert against and they stay unwrapped.

Goal: make `browser.click("//button", "middle")` work from plain Python, without changing
anything about how the library behaves under Robot Framework.

Scope agreed with the maintainer: **Enum**, **timedelta**, **AssertionOperator**.
Priority order: **runtime behaviour first, IDE experience second, type checkers third.**
Cost on the RF execution path is not a constraint ("correctness first").

Further decisions, 2026-08-09:

- **Widening the runtime type hints is rejected** — it makes RF's automatic conversion
  harder and pushes a "str or Enum?" branch into every keyword body. Widening is allowed
  only in the *generated* `.pyi` (§9).
- **The Python-vs-RF behavioural difference stays.** Python callers not getting trace groups
  and failure screenshots is a known, accepted property; explaining it better in the docs is
  a separate task (§3.1).
- **RF floor raised.** RF 6.x is dropped; 7.2 was rejected as too recent for enterprise
  users. Evidence points to `>= 7.1.1`, the lowest version CI actually tests (§5).

Companion document: [`python-api-ergonomics.md`](python-api-ergonomics.md) — the primary-source
research this builds on. This file is the options comparison and recommendation.

Everything marked **[V]** was verified by running code against this repo at
`Browser` 20.3.0, PythonLibCore 4.5.0, Python 3.14. The default RF is 7.4.1; claims about
version behaviour were checked against RF 6.1.1, 7.0.1, 7.1.1, 7.2.2, 7.3 and 7.4.1 in
isolated environments. Reproduction scripts are listed in §11.

---

## 1. The two facts that decide the design

**Fact 1 — RF and Python reach a keyword through two independent dicts.** **[V]**

`HybridCore.add_library_components` stores each bound keyword method in *two* places
(`robotlibcore/core/hybrid.py:50,54`):

```python
self.keywords[kw_name] = kw                              # line 50 — used by run_keyword
self.attributes[name] = self.attributes[kw_name] = kw    # line 54 — used by __getattr__
```

- **Robot Framework** calls `DynamicCore.run_keyword`, which is one line —
  `return self.keywords[name](*args, **(kwargs or {}))` (`core/dynamic.py:24-25`).
  RF has already converted the arguments by then, using `get_keyword_types`.
- **Python** calls `browser.click(...)`, which misses on the class and falls through to
  `HybridCore.__getattr__` → `self.attributes[name]` (`core/hybrid.py:108-116`).
  No conversion happens anywhere.

`Browser` defines no `@keyword` methods on the class itself — all 151 come from the
component instances passed at `Browser/browser.py:972` — so **every** Python keyword call
goes through `__getattr__`. **[V]**

That means the two paths can be given different behaviour by touching only one dict.

**Fact 2 — the conversion machinery already ships in this repo.** **[V]**

`RobotTypeConverter` (`Browser/utils/data_types.py:25-37`) wraps `robot.api.TypeInfo` and
already guards RF < 7.0 with `try/except ImportError`. Two shipping call sites already do
exactly the `get_keyword_types` → `converter_for` → `convert` dance:
`Browser/keywords/promises.py:128-137` and `Browser/entry/__main__.py:463-482`.

So this feature is a *generalisation of code that already runs in production*, not new
machinery. The RF version floor is a separate question, treated in §5.

---

## 2. Option A — decorator on each keyword method

A `@converting_proxy` decorator applied to the keyword function, under `@keyword`.

```python
@keyword
@converting_proxy
def click(self, selector: str, button: MouseButton = MouseButton.left):
    ...
```

The wrapper binds the incoming arguments to the signature and converts each one whose
declared type has a converter.

**Verified working** for Enum, `timedelta` from `"1.5s"`, `AssertionOperator` from `"=="`,
`*varargs: KeyboardModifier`, `bool` from `"true"`, and RF's error message on a bad value.
`get_keyword_arguments` and `get_keyword_types` are unaffected because `KeywordBuilder`
calls `inspect.unwrap` (`robotlibcore/keywords/builder.py:45,124`). **[V]**

| | |
| --- | --- |
| ✅ | Explicit and greppable — you can see at each keyword that it opts in. |
| ✅ | Per-keyword opt-out is trivial: omit the decorator. |
| ❌ | **Touches all 151 keyword definitions** across 17 modules. |
| ❌ | **Sits on the RF path too.** Measured: `convert_args` ran **100 times for 100 `run_keyword` calls** — RF converts, then the decorator re-validates every argument. **[V]** |
| ❌ | Every new keyword must remember the decorator; nothing enforces it. |
| ❌ | Two decorators per keyword, order-sensitive. |

## 3. Option B — wrap the `attributes` dict (recommended)

Keyword bodies and signatures are untouched. After `DynamicCore.__init__`, rebuild
`self.attributes` with conversion-wrapping proxies and **leave `self.keywords` alone**:

```python
class Browser(DynamicCore):
    def __init__(self, ...):
        ...
        DynamicCore.__init__(self, libraries, translation_file)
        # RF reaches keywords via self.keywords; Python reaches them via self.attributes.
        # Wrapping only the latter gives Python callers argument conversion and leaves
        # the Robot Framework execution path byte-for-byte unchanged.
        #
        # Resolve types through self.keywords and cache by the bound method: keywords_spec
        # is keyed by ROBOT name only, while attributes is keyed by BOTH the method name
        # and the robot name (§1, `core/hybrid.py:54`). See the naming trap below.
        types_by_method = {
            kw: self.get_keyword_types(kw_name)
            for kw_name, kw in self.keywords.items()
        }
        wrapped: dict = {}
        for name, kw in list(self.attributes.items()):
            if kw not in wrapped:
                wrapped[kw] = converting_proxy(kw, types_by_method.get(kw, {}))
            self.attributes[name] = wrapped[kw]
```

with

```python
def converting_proxy(bound_method, types):
    """Return a proxy that converts plain Python values to the declared keyword types."""
    if not types:
        return bound_method
    sig = inspect.signature(bound_method)
    plan = {}
    for name, hint in types.items():
        if name in sig.parameters and (conv := RobotTypeConverter.converter_for(hint)):
            plan[name] = (conv, sig.parameters[name].kind)
    if not plan:
        return bound_method

    # @wraps is REQUIRED, not cosmetic: `rfbrowser translate`
    # (`Browser/entry/translation.py:40`) reads __name__ and __doc__ off these entries and
    # checksums the doc. Dropping it changes every translation checksum silently. **[V]**
    @wraps(bound_method)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, (conv, kind) in plan.items():
            if name not in bound.arguments:
                continue
            value = bound.arguments[name]
            # A Python caller who means "nothing" passes the None object. Never convert it:
            # on a `str` hint RF turns None into the string "None". See the None rule below.
            if value is None:
                continue
            if kind is inspect.Parameter.VAR_POSITIONAL:
                bound.arguments[name] = tuple(
                    v if v is None else conv.convert(name=name, value=v) for v in value
                )
            elif kind is inspect.Parameter.VAR_KEYWORD:
                bound.arguments[name] = {
                    k: (v if v is None else conv.convert(name=name, value=v))
                    for k, v in value.items()
                }
            else:
                bound.arguments[name] = conv.convert(name=name, value=value)
        return bound_method(*bound.args, **bound.kwargs)

    return wrapper
```

### The naming trap — why types are resolved through `self.keywords`

An earlier draft of this section looked types up as `self.get_keyword_types(kw.__name__)`.
That **cannot construct `Browser()`**: `keywords_spec` is keyed by the *robot* name only
(`core/hybrid.py:50`) and `get_keyword_types` raises `ValueError` on a miss
(`core/dynamic.py:46-50`), so all 10 `@keyword(name=...)` keywords blow up —
`Evaluate JavaScript`, `Get BoundingBox`, and the `LocalStorage`/`SessionStorage` families,
i.e. 20 of the 161 attribute entries. Every keyword misses when a translation file is in
use. Resolving through `self.keywords`, which is keyed the same way `keywords_spec` is,
fixes both. **[V]**

Caching by bound method matters for the same reason: `attributes` holds 161 entries for 151
distinct methods, so a per-entry comprehension builds two wrappers for each aliased keyword.

### The None rule

A Python `None` is never converted. Measured across every convertible parameter,
`convert(None)` gives **[V]**:

| result | parameters |
| --- | --- |
| `None` stays `None` | 328 |
| `None` becomes the string `'None'` | 126 |
| raises `ValueError` | 122 |

The 126 are hints containing `str` but not `None` (`close_browser_server(wsEndpoint: str)`);
the 122 are Enums and bare `timedelta`. Skipping `None` is never worse than today, because
the Python path converts nothing at all today. A *string* `"None"` is still converted per its
hint — on `str | None` it stays `"None"`, on `int | None` RF makes it `None` — which is RF's
documented behaviour and is left alone.

`str | None` needs no special handling: RF's union converter already returns `None` for a
real `None` and `"None"` for the string. **[V]**

Applied to the **real** Browser library, unmodified: **[V]**

```
attributes entries       : 161
distinct keyword methods : 151
wrapped (>=1 convertible): 139
convertible parameters   : 576
failures                 : 0
wrap cost                : 3.7 ms at construction

real click() type hints: {'selector': <class 'str'>, 'button': <enum 'MouseButton'>}
w("//button", "middle") -> received: {'selector': '//button', 'button': <MouseButton.middle: 2>}
bad value -> ValueError: Argument 'button' got value 'nope' that cannot be converted to
             MouseButton: MouseButton does not have member 'nope'.
             Available: 'left', 'middle' and 'right'
```

| | |
| --- | --- |
| ✅ | **One place.** ~25 lines in `browser.py` plus a helper. Zero keyword files edited. |
| ✅ | **RF path provably untouched:** `convert_args` ran **0 times for 100 `run_keyword` calls**. **[V]** |
| ✅ | Applies automatically to new keywords, including the ones generated at runtime (`Browser/browser.py:1116`) as long as wrapping happens after they are registered. |
| ✅ | Reuses `get_keyword_types`, so `@keyword(types=...)` overrides are respected for free. |
| ✅ | Same object — `browser.click(...)` keeps working; no new import or namespace for users to learn. |
| ⚠️ | Wrapping is implicit; a reader of `interaction.py` sees no sign of it. Mitigate with a comment at the wrap site and a section in the docs. |
| ⚠️ | `browser.attributes[...]` is PythonLibCore's internal structure. It is stable across PLC 4.x, but the project takes a dependency on it. See §6 for the upstream fix. |

### 3.1 B2 — also route through `run_keyword` (considered, out of scope)

> **Decision (maintainer, 2026-08-09): not doing this.** The behavioural difference between
> the Python and Robot Framework paths is a known, accepted property of the library. It
> should be explained better in the docs, but changing it is a separate concern from this
> feature. Recorded here because the option was evaluated and works; it is not part of the
> plan. **Option B ships without it.**

`Browser.run_keyword` (`Browser/browser.py:1335-1360`) is not a pass-through. It opens and
closes **Playwright trace groups**, takes a **failure screenshot** via `keyword_error()`,
rewrites error messages through `_alter_keyword_error`, and implements `pause_on_failure`.

Python callers reach the bound method through `__getattr__` and **never enter
`run_keyword`**, so they get none of that — today, and under plain Option A, B or C. **[V]**
This is a pre-existing gap, but it is worth closing in the same change: a Python user whose
`click` fails currently gets no failure screenshot and no trace group.

The fix is one line in the proxy — convert, then delegate to `run_keyword` instead of to the
bound method:

```python
    return lib.run_keyword(kw_name, list(bound.args), bound.kwargs)
```

**This cannot recurse**, and the two-dict split is exactly why: the proxy lives in
`self.attributes`, while `run_keyword` resolves through `self.keywords`, which is never
wrapped. Verified: **[V]**

```
python  lib.click("//b", "middle") -> ('click', '//b', MouseButton.middle)
  trace: [open_trace_group, close_trace_group]
python  failing call raised: element not found
  trace: [open_trace_group, failure_screenshot, close_trace_group]
RF      run_keyword("click", ["//b", MouseButton.right]) -> ok
  trace: [open_trace_group, close_trace_group]
```

Note `bound.args` includes `self` only if the signature is unbound — the proxy wraps the
*bound* method, so it does not. Trace-group code is additionally guarded by
`self.keyword_call_stack`, which is empty outside an RF run, so it degrades quietly rather
than misbehaving.

B2 costs one line over B and would give Python callers parity with RF. Not pursued — see
the decision note above. If the accepted difference is ever revisited, this is the
mechanism, and it is already verified.

### Overhead

Measured on a keyword call with no I/O, 100k iterations: **[V]**

| | µs/call |
| --- | --- |
| undecorated method | 0.04 |
| wrapper, already-typed value passed | 1.60 |
| wrapper, string passed (real conversion) | 20.96 |

Both numbers are irrelevant next to a gRPC round-trip to the Playwright node process
(milliseconds). Caching `inspect.signature` and the converter at wrap time — as the code
above does — is what keeps the already-typed case at 1.6 µs; resolving them per call costs
**47 µs**. **[V]**

## 4. Option C — the separate facade

A second namespace, e.g. `browser.py.click("//button", "middle")` or a `PyBrowser` class,
generated from the keyword list.

| | |
| --- | --- |
| ✅ | Zero ambiguity: the RF surface and the Python surface are different objects. |
| ✅ | Free rein to diverge — rename to snake_case, drop RF-only arguments, return plain types. |
| ❌ | **Two public APIs to document, version, and deprecate.** For 151 keywords that is a real ongoing cost. |
| ❌ | Users must learn which one to use; every Stack Overflow answer becomes ambiguous. |
| ❌ | Delivers nothing Option B doesn't, for the agreed scope. The facade only pays off if you also want a *different* API shape, which is not the stated goal. |

Worth keeping in reserve if the goal later expands to "a genuinely Pythonic API"
(snake_case, no `AssertionOperator`, native return types). It is not the cheaper path to
`browser.click("//button", "middle")`.

## 5. Robot Framework version floor

`pyproject.toml:12` currently allows `robotframework >= 6.1.1`. The maintainer has confirmed
RF 6.x can be dropped, and ruled out 7.2 as too recent. That leaves 7.0.1 or 7.1.1 — this
section works out which, and what the choice actually buys.

Verified across every relevant release: **[V]**

| | 6.1.1 | 7.0 | 7.1 | 7.2 | 7.3+ |
| --- | --- | --- | --- | --- | --- |
| `robot.api.TypeInfo` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `TypeInfo.from_type_hint` / `.convert` | ❌ | ✅ | ✅ | ✅ | ✅ |
| **`TypeInfo.get_converter`** | ❌ | ❌ | ❌ | ✅ | ✅ |
| `typeconverters.TypeConverter.converter_for` (internal) | ✅ | ✅ | ✅ | ✅ | ✅ |

### Why `get_converter` is the one that matters

Option B builds a **conversion plan once per keyword at wrap time**: for each parameter,
decide whether a converter exists and, if not, leave that parameter alone. That check is
what needs a public API.

- `TypeConverter.converter_for(hint)` returns `None` for unconvertible types — clean, but
  it lives in `robot.running.arguments.typeconverters`, i.e. **RF internals**.
- `TypeInfo.get_converter()` is the public equivalent — but it arrives in **7.2**, not 7.0.

On 7.0/7.1 there is no public way to ask "is this convertible?" ahead of time. `convert()`
raises rather than reporting, and the exception *type* is the only stable signal — the
message changed across releases: **[V]**

```
RF 7.0    TypeError: No converter found for 'Weird'.
RF 7.2    TypeError: Cannot convert type 'W'.
RF 7.3+   TypeError: Unrecognized type 'W'.
```

(`ValueError` means "value is wrong"; `TypeError` means "type has no converter" — but that
contract is not documented as public API.)

### What the library actually requires today **[V]**

`pyproject.toml:12` declares `>= 6.1.1`. Measured rather than assumed:

- **RF 6.1.1 is not known to be broken.** `import Browser` + `Browser()` succeeds
  (151 keywords), and the non-browser unit suite passes: 72 passed / 2 skipped on both
  6.1.1 and 7.0.1, 74 passed on 7.4.1. (One `test_secrets` failure is environmental and
  identical on all three.) **Weigh this lightly** — the maintainer notes unit coverage is
  thin and the acceptance suite carries the real coverage, and the acceptance suite has
  never run on anything below 7.1.1. Every RF 7 API the code touches is deliberately
  guarded:
  `TypeInfo` (`data_types.py:30-37`), `LOGLEVEL` (`logger.py:20-23`), `Secret`
  (`types.py:15-20`), each with a working fallback.
- **But CI tests only `7.1.1` and `7.4.2`** — 6 matrix entries each, across all workflows
  (`.github/workflows/on-push.yml`). Nothing below 7.1.1 is exercised anywhere, including
  the acceptance tests.

So the declared floor is not demonstrably false about *functionality*, but it is false about
*verification*: 6.1.1 and 7.0.x are supported only in the sense that nobody has broken them
yet by accident — and the tests that would notice are the ones that never run there.

Release dates, from PyPI: **[V]**

| 6.1.1 | 7.0 | 7.0.1 | 7.1.1 | 7.2.2 | 7.3 | 7.4 | 7.4.2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-07-28 | 2024-01-11 | 2024-06-10 | **2024-10-19** | 2025-02-07 | 2025-05-30 | 2025-12-12 | 2026-03-03 |

### Decision: floor should be `robotframework >= 7.1.1`

**7.1.1 is the lowest version CI actually verifies**, and at 2024-10-19 it is *older* than
the 7.2.2 that was rejected as too recent for enterprise users. Declaring 7.1.1 costs
nothing that 7.0.1 doesn't already cost, and makes the declared floor an honest statement
about what is tested.

For this feature specifically, **7.0.1 and 7.1.1 are technically identical** — `get_converter`
still arrives in 7.2, so either way the implementation uses `RobotTypeConverter`. The choice
between them is about honesty of the dependency declaration, not capability.

Consequences of any 7.x floor:

- `TypeInfo.get_converter` is unavailable below 7.2, so the plan-time "is this convertible?"
  check keeps using `RobotTypeConverter` → `TypeConverter.converter_for`, i.e. **RF
  internals**. This is not new debt: two shipping call sites already do exactly this
  (§1, Fact 2).
- Two guards become dead code and should be deleted:
  - `Browser/utils/data_types.py:30-37` — the `TypeInfo` `try/except ImportError`. Deleting
    it removes the `UnboundLocalError` rather than fixing it.
  - `Browser/utils/logger.py:20-23` — the `LOGLEVEL` guard, which already carries the
    comment `TODO: Remove when Robot Framework 7 is minimum version`.
- Two things must **stay**, because they guard against RF < **7.4**, not RF < 7:
  - `Browser/utils/types.py:15-20` — the `Secret` fallback class.
  - The two `test_data_types.py` tests that skip on RF older than 7.4.0.
- No change to the architecture. Option B is unaffected.

### Internal API stability across 7.0.1 – 7.4.1 **[V]**

Since the implementation depends on internals, this was verified on every release in range:

- `TypeConverter.convert` signature is **identical** on 7.0.1, 7.1.1, 7.2.2, 7.3 and 7.4.1:
  `(self, value, name=None, kind='Argument')`. Calling it as `convert(name=..., value=...)`
  — as the existing call sites do — is safe throughout.
- Enum, `timedelta` and `Optional[Enum]` convert identically on all five.

One behaviour change to be aware of: for an **unconvertible** type, `converter_for` returns
`None` on 7.0.1–7.2.2 but an `UnknownConverter` instance on 7.3+. `UnknownConverter.convert`
is a pass-through (`'hello' -> 'hello'`, `42 -> 42`, `None -> None`), so correctness is
unaffected — but the conversion plan will contain a few extra no-op entries on 7.3+.
**Tests must not assert on plan size or on `converter_for(...) is None`.** **[V]**

> **Note on 7.4.** `from_type_hint` changed its sequence handling in 7.4. Enums, `timedelta`
> and `AssertionOperator` — the agreed scope — are unaffected, but the acceptance tests
> should run against both the floor and the latest RF. **[V]**

> **Pre-existing bug.** `Browser/utils/data_types.py:33-37`: when `arg_type` is already a
> `TypeInfo`, `type_hint` is never assigned and the function raises `UnboundLocalError`.
> Unreachable today because `get_keyword_types` returns raw hints. If the floor moves to
> 7.0+, the surrounding `try/except ImportError` is dead and the whole branch should go,
> taking the bug with it. **[V]**

## 6. Where this should eventually live

Option B works by reaching into `self.attributes`, a PythonLibCore internal. The clean
long-term home is **PythonLibCore itself** — `HybridCore` owns both dicts and is the only
place that knows the split is intentional. An opt-in flag would let every RF library get
this:

```python
class Browser(DynamicCore):
    ROBOT_PYTHON_FRIENDLY_ARGS = True
```

Recommended sequencing: **ship Option B in Browser first**, prove it over a release, then
propose it upstream with a working implementation and real usage behind it. Blocking on an
upstream release would stall the feature, and PLC has no conversion hooks today
(`python-api-ergonomics.md` §3.3).

## 7. Interaction with the repo's own Python-calling code **[V]**

Two places inside this repo already call keywords from Python. Option B affects exactly one
of them, and the difference is which dict they use:

| Call site | How it dispatches | Wrapped by Option B? |
| --- | --- | --- |
| `Browser/keywords/promises.py:68` (`promise_to`) | `self.library.keywords[known_keyword](...)` | **No** — uses the RF dict |
| `Browser/entry/__main__.py:444` (`rfbrowser launch-browser-server`) | `browser_lib.launch_browser_server(browser=..., **params)` | **Yes** — attribute access |

`promise_to` already converts its own arguments (`convert_keyword_arg`, line 128) and then
calls the unwrapped method, so it is unaffected in both behaviour and cost.

The entry point is different: `convert_options_types` converts at line 443, then line 444
calls through `__getattr__` — so under Option B those arguments would be converted **twice**.

**This matters because the `rfbrowser` entry point is the least-tested code in the project**
— acceptance coverage was dropped as too flaky on GitHub runners, and it is validated by
manual testing on each change. CI will not catch a regression here.

### Double conversion is safe — conversion is idempotent **[V]**

Verified on the entry point's own parameter list — every one converts to itself, including
the `Proxy` TypedDict and both `timedelta` fields:

```
browser    ok  SupportedBrowsers.chromium -> SupportedBrowsers.chromium
proxy      ok  {'server': 'http://p:8080'} -> {'server': 'http://p:8080'}
timeout    ok  timedelta(seconds=10)      -> timedelta(seconds=10)
non-idempotent: none
```

And library-wide, by converting **every parameter default of every keyword** — defaults are
already-typed values by construction, so this models a Python caller passing
`AssertionOperator["=="]` or `SupportedBrowsers.chromium`, as `utest/test_python_usage.py`
does today:

```
params with defaults + a converter : 416
converted cleanly to themselves    : 415
no converter (skipped)             : 0
problems                           : 1
   save_page_as_pdf.scale  hint=float  default=1  -> 1.0
```

The single exception is `int 1` → `float 1.0` on a `float`-hinted parameter: same value,
widened type, harmless.

**Consequences for the plan:**

- Option B is safe for the entry point, but `rfbrowser launch-browser-server` must go on the
  manual test checklist for this change.
- Deleting the `TypeInfo` guard in `RobotTypeConverter` touches code the entry point depends
  on. **Land it as a separate commit from the Option B feature**, so a manual-test failure
  has an unambiguous cause.

## 8. Conversion is necessary but not sufficient — AssertionOperator

Converting `"=="` to `AssertionOperator.equal` works fine outside an RF run. *Executing*
some operators does not. AssertionEngine's `validate` and `then` call `BuiltIn().evaluate`,
which needs an execution context: **[V]**

```
==         -> 'abc'
contains   -> 'abc'
validate   !! RobotNotRunningError: Cannot access execution context
then       !! RobotNotRunningError: Cannot access execution context
```

So of the 31 keywords taking an `AssertionOperator`, all convert, and the ordinary
comparison operators work from Python — but `validate` and `then` cannot, for reasons
outside this library's control. This is pre-existing and unrelated to which option is
chosen. Worth a documented note, and ideally a clearer error than
`RobotNotRunningError` when a Python caller reaches for them.

## 9. IDE and type-checker tiers

Runtime (tier 1) is what Options A–C address. The other two tiers are **independent work**
that rides on the existing stub pipeline, and can land later without revisiting the runtime
choice.

`Browser/browser.pyi` is generated at build time by `Browser/gen_stub.py` from
`mypy_stub/Browser/keywords/*.pyi`, and is not checked in. That generated file is what IDEs
and mypy actually read for the public class. **[V]** So the annotations that Python users
*see* can be widened without touching the runtime annotations that RF reads:

```python
# mypy_stub source (runtime, RF sees this):
def click(self, selector: str, button: MouseButton = ...): ...

# generated Browser/browser.pyi (IDE and mypy see this):
def click(self, selector: str,
          button: MouseButton | Literal["left", "middle", "right"] = ...): ...
```

This gives autocomplete of the valid strings and mypy/ruff understanding of them, with no
effect on libdoc, on RF's conversion, or on the keyword bodies — which is precisely the
objection that ruled out widening the real type hints. `Literal` appears in **zero** keyword
signatures today, so there is no precedent to conflict with. **[V]**

Note this only works cleanly for Enums whose members map to strings. `timedelta` would
widen to `timedelta | str | int | float` and `AssertionOperator` to a 30-odd member
`Literal`, which is accurate but noisy in tooltips. Worth deciding per type.

## 10. Recommendation

1. Raise the RF floor in `pyproject.toml:12` to **`>= 7.1.1`** (§5) — the lowest version CI
   verifies, and older than the rejected 7.2.2. Dropping RF 6 is a breaking change for
   users, so it belongs in a major release.
2. Delete the two now-dead RF < 7 guards: the `TypeInfo` branch in `RobotTypeConverter`
   (`Browser/utils/data_types.py:30-37`), which removes the `UnboundLocalError`, and the
   `LOGLEVEL` guard (`Browser/utils/logger.py:20-23`). Keep the `Secret` guard — it is a
   7.4 guard, not a 7.0 one (§5).
3. Implement **Option B** — wrap `self.attributes` after `DynamicCore.__init__` with cached
   signatures and converters resolved once per keyword. One place, RF path provably
   untouched, works on all 150 wrappable keywords today. Do **not** route through
   `run_keyword` (§3.1).
4. Add acceptance tests calling keywords from Python with plain values, plus a test
   asserting the RF path does not enter the conversion wrapper. Run them against both the
   RF floor and the latest RF (§5).
5. Document that `validate` and `then` assertion operators are unavailable outside an RF
   run (§8).
6. Later, independently: widen Enum annotations in generated `.pyi` for tiers 2 and 3.
7. Later still: propose the mechanism upstream to PythonLibCore.

Option A is the same feature at 151× the diff and with the RF path dragged in.
Option C is a bigger product decision that this goal does not require.

## 11. Reproduction

The scripts below were written in the session scratchpad and **were never committed** — they
do not exist anywhere in this repo, so do not go looking for them. They are listed to record
what was run for each claim; the code that matters is quoted inline above, and the shipped
implementation is `Browser/python_arguments.py` with its tests in
`utest/test_python_arguments.py`.

- `proto.py` — Options A and B side by side on a synthetic PLC library; the
  `convert_args` call-counting that proves the RF-path bypass; the naive-overhead numbers.
- `proto2.py` — the cached-signature variant and its timings.
- `real.py` — Option B applied to the real `Browser()` instance; the 150/161 and 609
  parameter counts, and the intercepted `click` call.
- `b2.py` — the `run_keyword`-routing variant, showing trace-group and failure-screenshot
  parity for Python callers and the absence of recursion.

RF version matrix reproduced with
`uv run --isolated --no-project --with "robotframework==<v>" python -c ...`.

Note: `robot.api.TypeInfo` has **no** `is_valid` method in RF 7.4.1 — the fast path must
use `isinstance` against `info.type` (guarding `info.is_union`), or the converter's own
result. An `is_valid` call inside a `try/except` silently disables the fast path. **[V]**
