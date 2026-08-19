# Pure-Python ergonomics for the Browser library

Research notes: how to make `Browser` pleasant to call from plain Python
(`browser.click("//button", "middle")`) without degrading Robot Framework usage.

> **Point-in-time record, 2026-08-11. Not maintained.**
>
> Primary-source research into Robot Framework's conversion API and PythonLibCore's
> internals, kept because re-deriving it is the expensive part. It is evidence, not current
> documentation, and nothing here is updated as those libraries move. Measured against the
> versions in the table below.
>
> The decision this fed into is
> [`docs/adr/0006-python-argument-conversion-via-attribute-table.md`](../adr/0006-python-argument-conversion-via-attribute-table.md);
> the options comparison is [`python-api-options.md`](python-api-options.md); the shipped
> implementation is `Browser/python_arguments.py`.

**Status:** research only. No library code was changed *by this document* — the feature it
led to has since been implemented.

## Where this file lives and why

The repo has no existing `notes/` or `docs/research/` convention. `docs/` currently
holds `adr/`, `examples/`, `plugins/`, `releasenotes/`, `versions/`. The closest
existing convention is `docs/adr/` (architecture decision records, e.g.
`docs/adr/0004-rf-listener-as-library-not-standalone.md`), but this document is
investigation, not a decision, so it is **not** an ADR. Per the task instruction it is
filed at `docs/research/python-api-ergonomics.md`, creating that directory.
The decision that followed became
[`docs/adr/0006-python-argument-conversion-via-attribute-table.md`](../adr/0006-python-argument-conversion-via-attribute-table.md)
(0005 was taken in the meantime).

## Legend

- **[V]** VERIFIED — I read the source and/or executed it and observed the result.
- **[I]** INFERRED — reasoning on top of verified facts; not directly observed.

## Versions this was verified against

| Component | Version | Path |
| --- | --- | --- |
| Robot Framework | 7.4.2 | `.venv/lib/python3.14/site-packages/robot/` |
| PythonLibCore | 4.6.0 | `.venv/lib/python3.14/site-packages/robotlibcore/` |
| Browser (this repo) | branch `python_usage` | `Browser/` |

Cross-checked against `robotframework/robotframework` git tags `v6.1.1`, `v7.0`,
`v7.1`, `v7.2`, `v7.3`, `v7.4` and `master` via the GitHub contents API. **[V]**

Repo-local source line numbers refer to the working tree at the time of writing.

---

## 1. Executive summary

1. **RF's argument conversion is fully reachable outside a Robot Framework run.** The
   entire `robot.running.arguments` package has exactly one reference to the execution
   context, and it is an optional fallback for *language* configuration only
   (`typeinfo.py:422-423`). With no context, conversion works and degrades to the
   default English language config. **[V]** — see §4.
2. **`robot.api.TypeInfo` exists and is explicitly public API**, documented as such in
   RF's own source and its readthedocs API reference, since **RF 7.0**. **[V]** — §2.
3. **PythonLibCore performs no conversion whatsoever.** `DynamicCore.run_keyword` is a
   one-line direct call of the bound method. All conversion happens on the *Robot
   Framework* side, before `run_keyword` is invoked, driven by `get_keyword_types`.
   A Python caller therefore bypasses 100% of it. **[V]** — §3.
4. **The pattern is already in this repo, twice.** `Browser/keywords/promises.py:133`
   and `Browser/entry/__main__.py:463` both do
   `get_keyword_types(kw)` → `RobotTypeConverter.converter_for(type)` → `.convert(value)`.
   `RobotTypeConverter` (`Browser/utils/data_types.py:26`) is a thin wrapper over
   `robot.api.TypeInfo.from_type_hint`. A python-friendly API is a generalisation of
   code that already ships. **[V]** — §6.4.
5. **Scale of the problem: 123 Enum-typed parameters across 84 of 151 keywords (55.6%)**,
   plus 35 `timedelta` parameters across 30 keywords, plus 4 Enum / 2 `timedelta` /
   1 TypedDict arguments on `Browser.__init__` itself. **[V]** — §6.
6. **Blocker on the current dependency floor:** `pyproject.toml:12` allows
   `robotframework >= 6.1.1`, but `TypeInfo` does not exist before RF 7.0. **[V]** — §2.3.
7. **Nothing coerces strings today.** No Browser enum is a `str` mixin, none defines
   `_missing_`, and the library registers no `ROBOT_LIBRARY_CONVERTERS`. So
   `MouseButton("right")` raises `ValueError` (values are `auto()` ints). **[V]** — §6.3.
8. **No RF library anywhere offers a documented string-accepting Python API.** Browser is
   already the furthest along (documented Python example in `README.md:143-159`,
   generated `.pyi` stubs, and the converter in §6.4). SeleniumLibrary is Python-callable
   only because it never adopted Enums. **[V]** — §7.
9. **Two things conversion alone will not fix:** the `run_keyword` bypass costs
   run-on-failure / tracing / pause-on-failure (three closed Browser issues about exactly
   this), and AssertionEngine's `validate` / `then` operators call `BuiltIn().evaluate`
   and raise `RobotNotRunningError` outside a run. **[V]** — §7.

---

## 2. Robot Framework's public conversion API

### 2.1 `robot.api.TypeInfo` — it exists

`robot/api/__init__.py` re-exports it. **[V]**

```python
from robot.running import (
    TestSuite as TestSuite,
    TestSuiteBuilder as TestSuiteBuilder,
    TypeInfo as TypeInfo,
)
```

- Local: `.venv/lib/python3.14/site-packages/robot/api/__init__.py:104-108`
- Master: <https://github.com/robotframework/robotframework/blob/master/src/robot/api/__init__.py> — identical lines, fetched and confirmed. **[V]**

The module docstring lists it as public API (`robot/api/__init__.py:67-68`): **[V]**

> `TypeInfo` class for parsing type hints and converting values based on them.
> New in Robot Framework 7.0.

The class docstring states its status directly (`robot/running/arguments/typeinfo.py:107-108`): **[V]**

> Part of the public API starting from Robot Framework 7.0. In such usage
> should be imported via the `robot.api` package.

The readthedocs API reference documents `TypeInfo`, `ArgumentSpec`, `TypeConverter`,
`CustomArgumentConverters`, `ArgumentConverter` and `ArgumentResolver`, and repeats the
public-API sentence for `TypeInfo` only:
<https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.arguments.html> **[V]**

**Public-ness ranking [I], based on the above:**

| Symbol | Import path | Status |
| --- | --- | --- |
| `TypeInfo` | `from robot.api import TypeInfo` | **Public, stability-guaranteed** since 7.0 **[V]** |
| `TypeInfo` | `from robot.running.arguments import TypeInfo` | Works, but docstring says prefer `robot.api` **[V]** |
| `ArgumentSpec`, `TypeConverter`, `CustomArgumentConverters`, `PythonArgumentParser`, `DynamicArgumentParser` | `from robot.running.arguments import ...` | Exported in `__init__.py` and autodoc'd, but **not** in `robot.api` and **not** declared public — treat as semi-internal **[I]** |
| `ArgumentConverter`, `ArgumentResolver` | `from robot.running.arguments.argumentconverter import ArgumentConverter` | Not re-exported from the package `__init__.py` at all — internal **[V]** |

`robot/running/arguments/__init__.py` exports exactly: `DefaultValue`,
`DynamicArgumentParser`, `PythonArgumentParser`, `UserKeywordArgumentParser`, `ArgInfo`,
`ArgumentSpec`, `CustomArgumentConverters`, `EmbeddedArguments`, `TypeConverter`,
`TypeInfo`. Note `ArgumentConverter` and `ArgumentResolver` are **absent**. **[V]**

### 2.2 Signatures

`TypeInfo.convert` — `robot/running/arguments/typeinfo.py:367-394` **[V]**

```python
def convert(
    self,
    value: Any,
    name: "str|None" = None,
    custom_converters: "CustomArgumentConverters|dict|None" = None,
    languages: "LanguagesLike" = None,
    kind: str = "Argument",
    allow_unknown: bool = False,
) -> object:
```

Raises `ValueError` if conversion fails, `TypeError` if there is no converter for the
type and `allow_unknown` is false.

Constructors — all classmethods on `TypeInfo`: **[V]**

| Method | Line | Accepts |
| --- | --- | --- |
| `from_type_hint(hint, sequence_is_union=False)` | `typeinfo.py:202` | anything: a type, `list[int]`, `int \| float`, the string `'int'`, a TypedDict |
| `from_type(hint: type)` | `typeinfo.py:268` | an actual concrete type only |
| `from_string(hint: str)` | `typeinfo.py:277` | `'int'`, `'list[int]'`, `'int \| float'` |
| `from_sequence(sequence)` | `typeinfo.py:296` | `[int, float]` → a union |
| `from_variable(variable, ...)` | `typeinfo.py:320` | `${x: int}` syntax; new in RF 7.3 |
| `get_converter(...)` | `typeinfo.py:396` | returns the `TypeConverter` for reuse; new in RF 7.2 |

So the idiom named in the question is correct and supported: **[V]**

```python
from robot.api import TypeInfo
TypeInfo.from_type(MouseButton).convert("middle")   # -> MouseButton.middle
```

### 2.3 Version availability — verified per git tag

Checked by fetching `src/robot/api/__init__.py` and
`src/robot/running/arguments/typeinfo.py` at each tag. **[V]**

| RF version | `typeinfo.py` | `TypeInfo` in `robot.api` | `.convert` | `.get_converter` | `allow_unknown` |
| --- | --- | --- | --- | --- | --- |
| 6.1.1 | **absent** | no | — | — | — |
| 7.0 | yes | **yes** | yes (`typeinfo.py:259`) | no | no |
| 7.1 | yes | yes | yes | no | no |
| 7.2 | yes | yes | yes | **yes** (`:288`, doc "New in Robot Framework 7.2") | no |
| 7.3 | yes | yes | yes | yes | **yes** |
| 7.4 | yes | yes | yes | yes | yes |

The RF 7.0 `convert` signature is the 7.4 one minus `allow_unknown`. **[V]**

**Behaviour change in 7.4** — the only `TypeInfo` mention in any RF 7.x release note
(`doc/releasenotes/rf-7.4.rst:298-301`, and identically in `rf-7.4rc1/rc2`): **[V]**

> `robot.api.TypeInfo.from_type_hint` does not anymore consider a sequence of types
> [a union]. […] use the `robot.api.TypeInfo.from_sequence` method instead.

I grepped **all** `doc/releasenotes/rf-7*.rst` files: `TypeInfo` is mentioned only in
`rf-7.4.rst`, `rf-7.4rc1.rst`, `rf-7.4rc2.rst`. The 7.0 "public API" claim is sourced
from the class docstring and `robot/api/__init__.py`, not from the 7.0 release notes. **[V]**

**Consequence for this repo:** `pyproject.toml:12` declares
`"robotframework >= 6.1.1, < 9.0.0"`. Any `TypeInfo`-based feature must either raise the
floor to `>= 7.0` or guard the import — which is exactly what
`Browser/utils/data_types.py:30-36` already does with a `try/except ImportError`. **[V]**

### 2.4 What RF converts, observed empirically with **no execution context**

Script: `scratchpad/verify_rf.py`. `EXECUTION_CONTEXTS.current` printed as `None`
throughout. **[V]**

| Type hint | Input | Result |
| --- | --- | --- |
| `MouseButton` (Enum) | `"middle"` | `MouseButton.middle` |
| `MouseButton` | `"MIDDLE"` | `MouseButton.middle` (case/`_-` insensitive) |
| `MouseButton` | `MouseButton.left` | passthrough, unchanged |
| `SelectAttribute` (`auto()` values) | `"label"` / `"LABEL"` | `SelectAttribute.label` |
| `SelectAttribute` | `"bogus"` | `ValueError: … does not have member 'bogus'. Available: 'index', 'label', 'text' and 'value'` |
| `timedelta` | `"3s"`, `"1 min 5 s"`, `5`, `1.5` | `0:00:03`, `0:01:05`, `0:00:05`, `0:00:01.5` |
| `Path` | `"foo/bar"` | `PosixPath('foo/bar')` |
| `Optional[MouseButton]` | `None` / `"right"` | `None` / `MouseButton.right` |
| `Union[int, MouseButton]` | `"left"` | `MouseButton.left` |
| `Literal["a","b"]` | `"a"` / `"c"` | `'a'` / `ValueError: … cannot be converted to 'a' or 'b'` |
| `List[MouseButton]` | `"['left','right']"` (string!) | `[MouseButton.left, MouseButton.right]` |
| `list[MouseButton]` | `["left","right"]` | `[MouseButton.left, MouseButton.right]` |
| TypedDict `Coord` | `"{'x': '1', 'y': '2'}"` or `{"x":"1","y":"2"}` | `{'x': 1, 'y': 2}` — **nested values converted too** |
| `bool` | `"true"` | `True` |
| `int` | `"1_000"` | `1000` (separators stripped) |
| unregistered class `Custom` | `"x"` | `TypeError: Unrecognized type 'Custom'`; with `allow_unknown=True` → `"x"` passthrough |
| `Custom` + `custom_converters={Custom: to_custom}` | `"abc"` | `Custom` instance, `.v == "ABC"` |

Error messages carry the argument name when `name=` is passed: **[V]**

```
Argument 'button' got value 'nope' that cannot be converted to MouseButton:
MouseButton does not have member 'nope'. Available: 'left', 'middle' and 'right'
```

**Enum matching rules** (`typeconverters.py:204-250`) **[V]**: exact member-name lookup
`enum[value]` first; then normalized comparison ignoring case, `_` and `-`
(`eq(m, value, ignore="_-")`); ambiguity across multiple members is an error; for
`int`-subclass enums, lookup by integer value is also tried. Matching is by **member
name**, not by value — important for `AssertionOperator`, whose member names are
`"=="`, `"equal"`, `"should be"` etc.

**Custom converters** (`customconverters.py`) **[V]**: `ROBOT_LIBRARY_CONVERTERS` is a
`{type: callable}` mapping; the callable may take `(value)` or `(value, library)`;
the value type it accepts is read from the converter's own annotation
(`ConverterInfo.for_converter`, `customconverters.py:68-100`). `TypeInfo.convert` accepts
the same mapping directly via `custom_converters=` — it calls
`CustomArgumentConverters.from_dict` internally (`typeinfo.py:420-421`). **[V]**

---

## 3. PythonLibCore

### 3.1 `run_keyword` bypasses everything — confirmed

`robotlibcore/core/dynamic.py:24-25`, in full: **[V]**

```python
class DynamicCore(HybridCore):
    def run_keyword(self, name, args, kwargs=None):
        return self.keywords[name](*args, **(kwargs or {}))
```

That is the entire implementation. There is **no conversion, no validation, no
coercion** anywhere in PythonLibCore. `self.keywords[name]` is the bound method captured
in `HybridCore.add_library_components` (`hybrid.py:48-50`). **[V]**

Conversion in a real RF run happens *before* RF ever calls `run_keyword`: RF asks the
library for `get_keyword_types(name)`, builds an `ArgumentSpec`, and runs
`ArgumentResolver` + `ArgumentConverter` on the test-data strings. So:

- **RF call path:** test data → RF resolves/converts using `get_keyword_types` → `run_keyword` → bound method with real objects. **[V]**
- **Python call path:** `browser.click(...)` → `HybridCore.__getattr__` (`hybrid.py:108-116`) → the bound method directly. **RF is not in the loop at all.** **[V]**

Note the Python path does not even go through `run_keyword`; attribute access resolves
straight to the component's bound method via `self.attributes`. That means Browser's own
`run_keyword` override (`Browser/browser.py:976-1001`, which adds trace groups, failure
screenshots and pause-on-failure) is *also* bypassed from Python. The library's own
`__init__` docstring already documents this consequence, for `run_on_failure`
(`Browser/browser.py:501`): **[V]**

> Run on failure is not applied when library methods are executed directly from Python.

### 3.2 How the dynamic API is built

| Method | File:line | Source of truth |
| --- | --- | --- |
| `get_keyword_names` | `hybrid.py:122-123` | `sorted(self.keywords)` |
| `run_keyword` | `dynamic.py:24-25` | direct bound-method call |
| `get_keyword_arguments` | `dynamic.py:27-32` | `KeywordSpecification.argument_specification` |
| `get_keyword_types` | `dynamic.py:46-50` | `KeywordSpecification.argument_types` |
| `get_keyword_tags` | `dynamic.py:34-35` | `func.robot_tags` |
| `get_keyword_documentation` | `dynamic.py:37-44` | `inspect.getdoc` |

`get_keyword_types` returns **raw type hints**, not `TypeInfo` objects
(`KeywordBuilder._get_types`, `builder.py:113-132`): it returns `func.robot_types` if the
`@keyword(types=...)` option was used, otherwise `typing.get_type_hints(func)` with
non-argument entries stripped. **[V]** This is precisely what
`Browser/keywords/promises.py:129` and `Browser/entry/__main__.py:466` consume.

Keyword discovery is `callable(func) and hasattr(func, "robot_name")`
(`hybrid.py:47`). **Note:** bare `@keyword` sets `robot_name = None`, so detection must
use `hasattr`, never truthiness. **[V]**

### 3.3 Conversion hooks in PythonLibCore: none

Grepping the whole 650-line package for `convert`, `TypeInfo`, `TypeConverter` finds
nothing. There is no pre-call hook, no argument filter, no `types=` post-processing.
The only extension points are `add_library_components`, the plugin system
(`robotlibcore/plugin/parser.py`) and the translation mechanism
(`robotlibcore/utils/translations.py`). **[V]**

`robotlibcore.__init__` re-exports RF's decorator verbatim: `from robot.api.deco import
keyword` (`robotlibcore/__init__.py:16`). **[V]**

### 3.4 `@keyword` decorator options

`robot/api/deco.py:68-125` — signature `keyword(name=None, tags=(), types=())`, setting
`func.robot_name`, `func.robot_tags`, `func.robot_types`. **[V]** From its docstring: **[V]**

> Types [may be given] either as a dictionary mapping argument names to types or as a
> list of types mapped to arguments based on position. It is OK to specify types only to
> some arguments, and **setting `types` to `None` disables type conversion altogether**.

This is the one existing lever that decouples the *declared RF type* from the *Python
annotation*: `types=` overrides annotations for RF only. **[I]** A design that annotates
parameters permissively for Python (e.g. `str | MouseButton`) while declaring the strict
RF type via `@keyword(types={...})` is mechanically possible, but it would degrade IDE
completion and Libdoc-from-annotations, and would have to be applied 151 times.

### 3.5 Precedent inside PythonLibCore for a python-friendly wrapper

None found. **[V]**

---

## 4. Is RF conversion usable outside a run? Yes.

This is the load-bearing question, so it was checked two ways.

**By source.** Grepping the entire `robot/running/arguments/` package for
`EXECUTION_CONTEXTS`, `robot.running.context`, `LOGGER`, `BuiltIn()`: **[V]**

```
embedded.py:24    from ..context import EXECUTION_CONTEXTS
embedded.py:114                   context = EXECUTION_CONTEXTS.current
typeinfo.py:55    from ..context import EXECUTION_CONTEXTS
typeinfo.py:422       if not languages and EXECUTION_CONTEXTS.current:
typeinfo.py:423           languages = EXECUTION_CONTEXTS.current.languages
```

`embedded.py` is embedded-argument parsing and is not on the conversion path.
The only conversion-path reference is `typeinfo.py:422-423`: **[V]**

```python
if not languages and EXECUTION_CONTEXTS.current:
    languages = EXECUTION_CONTEXTS.current.languages
elif not isinstance(languages, Languages):
    languages = Languages(languages)
```

With no context this falls to `Languages(None)` — the default English configuration.
**`typeconverters.py` (938 lines, every converter) contains zero context references.** **[V]**

Language config only affects `BooleanConverter` (`typeconverters.py:313-315`, matching
localized true/false words) and `NoneConverter`. Enum, timedelta, Path, Union, Literal,
TypedDict and custom-converter conversion are entirely language-independent. **[I]**

**By execution.** Every table row in §2.4 and §5 was produced in a bare Python process
with `EXECUTION_CONTEXTS.current is None`. **[V]**

**Counter-example for contrast:** `robot.libraries.BuiltIn` is the RF library that *is*
context-dependent — most of its keywords call `self._get_context()` and raise
`RobotNotRunningError` outside a run. Conversion machinery is deliberately not like
this. **[I]**

---

## 5. Full round-trip on a real Browser keyword

Because `Browser/generated/` (protobuf gencode) is not built in a source checkout,
`import Browser` fails at `Browser/base/librarycomponent.py:29`. Stubbing
`Browser.generated.playwright_pb2` + `grpc` in `sys.modules` makes real introspection
work (`scratchpad/stubgen.py`). **[V]**

Using only `robot.running.arguments` APIs, outside any RF run, on
`Browser/keywords/interaction.py:358` `click_with_options`: **[V]**

```python
from robot.running.arguments import PythonArgumentParser
spec = PythonArgumentParser().parse(Interaction.click_with_options, name="Click With Options")
spec.convert([None, "//b", "middle", "Shift"],
             [("delay", "200ms"), ("trial", "true"), ("position_x", "10")])
```

Observed output: **[V]**

```
converted positional: [None, '//b', <MouseButton.middle: 2>, <KeyboardModifier.Shift: 5>]
converted named:      [('delay', datetime.timedelta(microseconds=200000)),
                       ('trial', True), ('position_x', 10.0)]
```

Notes: **[V]**

- `*modifiers` varargs are converted element-wise.
- Already-correct values pass through untouched: passing `MouseButton.middle` and
  `timedelta(seconds=2)` returns them unchanged.
- A bad value produces the RF error message verbatim:
  `Argument 'button' got value 'nope' that cannot be converted to MouseButton: …`
- `spec` is derived from the *live annotations*, so it stays correct automatically as
  signatures change — no parallel type table to maintain. **[I]**

**Two API choices at this level [V]:**

- `ArgumentSpec.convert(positional, named, converters=None, dry_run=False, languages=None)`
  (`argumentspec.py:142-153`) — conversion only. **This is the right one for a Python wrapper.**
- `ArgumentSpec.resolve(args, named_args=None, variables=None, ...)`
  (`argumentspec.py:116-140`) — adds RF named-arg splitting on `=`, `${var}` replacement
  and arity validation, then calls `convert`. It passes `dry_run=not variables`, and
  `ArgumentConverter._convert` (`argumentconverter.py:67-72`) **skips conversion for any
  value containing an RF variable** when `dry_run` is true. Verified: with
  `resolve(..., variables=None)`, the value `"${sel}"` is left unconverted while
  `"middle"` still converts. Harmless for `str` parameters, but a silent no-op if a
  typed argument's value happened to look like `${...}`. Prefer `convert`.

`ArgumentConverter` also carries RF's subtle default-value fallback rules
(`argumentconverter.py:76-121`): `None` is preserved when the default is `None`; a `str`
default suppresses conversion; an `int` default also permits `float`. Reusing
`ArgumentSpec.convert` inherits all of this for free; a hand-rolled converter would not. **[I]**

---

## 6. Grounding in this repo

Counts produced by runtime introspection with `typing.get_type_hints` over every class in
`Browser/keywords/*.py`, detecting keywords via `hasattr(fn, "robot_name")` and flattening
nested generics (`Optional[...]`, `X | None`, `list[...]`, `dict[...]`).
Independently reproduced by two separate scripts with identical results. **[V]**
Scripts: `scratchpad/recount.py`, `scratchpad/analyze_kw_types.py`.

### 6.1 Headline numbers **[V]**

| Metric | Value |
| --- | --- |
| Total keywords | **151** |
| Keywords with ≥1 Enum parameter | **84 (55.6%)** |
| Enum-typed parameters | **123** |
| Distinct Enum classes used in signatures | **43** |
| Keywords with a `timedelta` parameter | **30** |
| `timedelta` parameters | **35** |
| Keywords with an `AssertionOperator` parameter | **31** |
| Keywords with a `SelectAttribute` parameter | **2** |
| Total parameters (excl. `self`) | 585 (577 annotated, 8 unannotated) |

Keywords per module (top 5): `interaction.py` 32, `getters.py` 28,
`playwright_state.py` 23, `browser_control.py` 16, `webapp_state.py` 8. **[V]**

Only 10 keywords pass an explicit name to `@keyword`; the other 141 use bare `@keyword`
(`robot_name is None`). **[V]**

### 6.2 Non-Enum RF-friendly types in signatures **[V]**

| Type | Keywords | Parameters |
| --- | --- | --- |
| Union / `X \| None` | 93 | ~280 (248 include `None`, i.e. Optional) |
| TypedDict | 12 | 23 |
| `list` / `List` / `Sequence` | 9 | 16 |
| `dict` / `Dict` / `Mapping` | 8 | 13 |
| `Path` | 4 | 6 |
| `timedelta` | 30 | 35 |
| `Literal` | **0** | **0** |

`Literal` is never used in a keyword signature — only internally at
`Browser/browser.py:1063` and `Browser/utils/logger.py:23`. **[V]**

TypedDict parameters: `Proxy` ×4; `DownloadInfo`, `NewPageDetails`, `GeoLocation`,
`HttpCredentials`, `RecordHar`, `RecordVideo`, `ViewportDimensions` ×2 each;
`BoundingBox`, `HighLightElement`, `FileUploadBuffer`, `PdfMarging`, `ClientCertificate`
×1 each. **[V]**

Enum classes by parameter count (top 15): `AssertionOperator` 31, `SelectionType` 16,
`Scope` 8, `SupportedBrowsers` 7, `PageLoadStates` 5, then `Permission`, `SizeFields`,
`MouseButton`, `KeyboardModifier`, `DialogAction`, `ColorScheme`, `ForcedColors` at 3
each, and `CookieType`, `ElementState`, `SelectAttribute` at 2. 42 of the 43 Enum classes
come from `Browser/utils/data_types.py`; `AssertionOperator` comes from
`assertionengine`. **[V]**

Return annotations: 1 keyword returns an Enum (`get_element_states` → `ElementState`,
`Browser/keywords/getters.py:1456`); 14 return a `data_types` class. **[V]**

### 6.3 `Browser/utils/data_types.py` **[V]**

- 71 top-level `class` statements; 79 classes at runtime, because 8 enums are built with
  the **functional** `Enum(...)` API: `FormatterKeywords`, `FormatingRules`,
  `CookieSameSite`, `ColorScheme`, `Permission`, `ScrollBehavior`, `InstallableBrowser`,
  `InstallationOptions`.
- **47 Enum subclasses**: 46 plain `Enum`, 1 `IntFlag` (`ElementState`, line 1118).
  **0 `str`-mixin enums, 0 `IntEnum`, 0 `Flag`.** Roughly 28 use `auto()`.
- **27 TypedDicts**, **0 dataclasses**, 5 plain classes (`RobotTypeConverter` :25,
  `Deprecated` :151, `RegExp` :265 (a `str` subclass), `DelayedKeyword` :388,
  `LambdaFunction` :701).
- Largest enum: `ElementRole` (line 293, 82 members).

**`_missing_` is defined nowhere** — `grep -rn "def _missing_" Browser/ atest/ utest/`
returns zero hits, as does the installed `assertionengine`. (A naive `grep _missing_`
returns 3 hits in `Browser/mypy.ini`, but those are `ignore_missing_imports` — false
positives.) **[V]** Combined with 0 `str`-mixin enums and `auto()`
integer values, this means plain-Python `browser.click(button="right")` cannot work
today: `MouseButton("right")` raises `ValueError`. Name-based, case-insensitive lookup
exists **only** inside RF's `EnumConverter`. **[V]**

`AssertionOperator` (`assertionengine/assertion_engine.py:27-56`, assertionengine 5.0.1)
is a functional `Enum` whose *member names* are the human aliases (`"equal"`, `"equals"`,
`"=="`, `"should be"`, …) and whose *values* are the operator symbols (`"=="`). It has
26 members but only 13 canonical ones — the rest are Python enum aliases. It defines no
`_missing_`. **[V]** The practical consequence, all observed: **[V]**

| Call | Result |
| --- | --- |
| `AssertionOperator("==")` (by value) | works → `AssertionOperator.equal` |
| `AssertionOperator("equal")` (by value) | `ValueError: 'equal' is not a valid AssertionOperator` |
| `AssertionOperator["should be"]` (by name) | works → `AssertionOperator.equal` |
| `TypeInfo.from_type(AssertionOperator).convert(x)` for `x` in `"=="`, `"equal"`, `"should be"`, `"SHOULD BE"`, `"should_be"`, `"contains"` | **all work** |

This is the sharpest single illustration of the gap: the plain-Python constructor accepts
one arbitrary subset of the spellings, while RF's converter accepts all of them
case- and separator-insensitively. It also explains why
`utest/test_python_usage.py:131` has to write `AssertionOperator["=="]` with
`__getitem__` rather than the more natural call syntax. **[V]**

### 6.4 Existing string→typed conversion in this repo — the precedent

Two shipping call sites already do exactly what a python-friendly API needs. **[V]**

`Browser/keywords/promises.py:128-137`:

```python
def convert_keyword_arg(self, kw: str, arg_name: str, arg_value: Any) -> Any:
    argument_type = self.library.get_keyword_types(kw).get(arg_name)
    if argument_type is not None:
        converter = TypeConverter.converter_for(argument_type)
        return (
            converter.convert(name=arg_name, value=arg_value)
            if converter
            else arg_value
        )
    return arg_value
```

`Browser/entry/__main__.py:463-482` `convert_options_types` does the same for the
`launch_browser_server` CLI, via `browser_lib.get_keyword_types("launch_browser_server")`.

Both route through `RobotTypeConverter` (`Browser/utils/data_types.py:25-37`):

```python
class RobotTypeConverter(TypeConverter):
    @classmethod
    def converter_for(cls, arg_type):
        if arg_type is None:
            return None
        try:
            from robot.api import TypeInfo
            if not isinstance(arg_type, TypeInfo):
                type_hint = TypeInfo.from_type_hint(arg_type)
        except ImportError:
            type_hint = arg_type
        return TypeConverter.converter_for(type_hint)
```

So **the library already depends on `robot.api.TypeInfo`**, already guards it for
RF < 7.0 with `try/except ImportError`, and already imports
`robot.running.arguments.typeconverters.TypeConverter` directly
(`Browser/utils/data_types.py:20`). Verified working outside an RF run: **[V]**

```
RobotTypeConverter.converter_for(MouseButton).convert('middle')        -> MouseButton.middle
RobotTypeConverter.converter_for(timedelta).convert('3s')              -> 0:00:03
RobotTypeConverter.converter_for(Optional[MouseButton]).convert('right') -> MouseButton.right
```

> **Latent bug found while verifying (not fixed — research only).**
> `Browser/utils/data_types.py:33-37`: when `arg_type` *is* already a `TypeInfo`, the
> `if not isinstance(...)` branch is skipped and `type_hint` is never assigned, so the
> `return` raises `UnboundLocalError: cannot access local variable 'type_hint'`.
> Reproduced: `RobotTypeConverter.converter_for(TypeInfo.from_type(MouseButton))`.
> It is unreachable today because `get_keyword_types` returns raw hints, never
> `TypeInfo` — but it would fire immediately if anything started passing `TypeInfo`
> objects around. **[V]**

Also note `Browser/utils/data_types.py:44-148` contains a hand-rolled TypedDict/Union
coercion layer (`convert_typed_dict` and helpers) that predates / duplicates what
`TypedDictConverter` in RF does (`typeconverters.py:607-674`), including nested
conversion. **[V]** (Whether it can be retired is out of scope here. **[I]**)

Other conversion-ish helpers: `Browser/keywords/getters.py:1537` local `convert_str`;
`Browser/utils/misc.py` `type_converter` (display-only, tested in
`utest/test_type_converter.py`); `Browser/browser.py:1278` and
`Browser/base/librarycomponent.py:230` `convert_timeout`. **[V]**

### 6.5 `Browser/browser.py` **[V]**

| What | Line |
| --- | --- |
| `from robotlibcore import DynamicCore, PluginParser` | 36 |
| `class Browser(DynamicCore)` | 156 |
| `ROBOT_LIBRARY_VERSION` / `ROBOT_LIBRARY_LISTENER` / `ROBOT_LIBRARY_SCOPE = "GLOBAL"` | 842-845 |
| `__init__` (keyword-only; `*_` rejects positionals at :896) | 851-871 |
| component list handed to `DynamicCore` (20 components) | 905-925 |
| `DynamicCore.__init__(self, libraries, translation_file)` | 972 |
| `run_keyword` **overridden** (trace groups, failure screenshot, pause-on-failure) | 1335-1359 |
| `get_keyword_tags` overridden (adds `Plugin` tag) | 1380-1384 |
| `get_keyword_documentation` overridden | 1647-1648 |
| `get_keyword_types` — **not** overridden, inherited from PLC | — |

`ROBOT_LIBRARY_CONVERTERS` appears **exactly once in the whole repo's Python sources**,
and it is test-only: `atest/library/os_wrapper.py:191` (`{datetime: _parse_fi_date}`).
(Other matches are only in `atest/output/**/syslog.txt` execution logs.)
The Browser library itself registers **no** custom converters. **[V]**

`Browser.__init__` itself has the same ergonomics problem: `auto_closing_level:
AutoClosingLevel`, `enable_playwright_debug: PlaywrightLogTypes | bool`,
`enable_presenter_mode: HighLightElement | bool` (TypedDict),
`external_browser_executable: dict[SupportedBrowsers, str] | None`,
`tracing_group_mode: TracingGroupMode`, `retry_assertions_for: timedelta = 1s`,
`timeout: timedelta = 10s` — i.e. 4 Enum + 2 `timedelta` + 1 TypedDict arguments. **[V]**

### 6.6 How the library is used from Python today **[V]**

`utest/test_python_usage.py` is the canonical example: `Browser.Browser()` at lines 52,
60, 70, 85, 193, 203, 261. It **mixes styles**, which is itself evidence of the problem:

- line 131 `browser.get_text("h1", AssertionOperator["=="], "Login Page")` — Enum object,
  via `__getitem__` because `AssertionOperator("==")` would not work
- line 183 `browser.new_browser(browser=SupportedBrowsers.chromium, headless=True, timeout="0")`
  — Enum object, but a *string* timeout
- lines 54/62/72/87/184 `browser.close_browser("ALL")` — plain string, works only because
  that keyword handles it
- lines 222/231/240/249 `browser.promise_to("Wait For Response", "matcher=", "timeout=1s")`
  — all strings, and they work **because** `promises.py` routes them through the RF converter

Other direct instantiations: `utest/test_shared_playwright_port.py`,
`test_screenshot.py:22`, `test_browser_folder_cleanup.py:13`, `test_docs.py:5`,
`test_output_dir.py:5`, `test_run_on_failure.py:8`, `test_secrets.py:38`,
`test_get_time.py:10,15`, `test_translation.py:12,57`, `test_waiters.py`.

The untracked scratch file `test.py` in the repo root does **not** use Browser at all;
it sketches three throwaway functions (`foo_1`, `foo_2`, `get_text`) with fully
`str`-annotated, python-friendly signatures — apparently an exploration of "what would a
string-typed `Get Text` look like". **[V]** (It is untracked and unreferenced. **[I]**)

---

## 7. Prior art

**Headline: no Robot Framework library offers a first-class, documented
"call me from Python with strings" API.** That is a genuine negative result across
SeleniumLibrary, RequestsLibrary, `BuiltIn` and PythonLibCore. Browser is already the
furthest along of any of them.

| Project | Prior art? | Why |
| --- | --- | --- |
| SeleniumLibrary | **No** | Python-callable only incidentally — it never adopted Enums |
| RequestsLibrary | **No** | Static library, no Enums; problem never arose |
| `robot.libraries.BuiltIn` | **Counter-example** | Deliberately context-*dependent*; raises outside a run |
| PythonLibCore | **No** | No conversion hook exists (§3.3); no issue/PR proposes one |
| AssertionEngine | **No** | Enum with no `_missing_`; `verify_assertion` rejects strings |
| **Browser (this repo)** | **Partial — the most of any** | Documented Python example, generated `.pyi` stubs, and a shipped context-free converter (§6.4) |
| `manykarim/rf-mcp` | **Yes — the one real external instance** | Uses `TypeInfo.convert` outside a run |

**SeleniumLibrary** (<https://github.com/robotframework/SeleniumLibrary>) — `SeleniumLibrary(DynamicCore)`
at `src/SeleniumLibrary/__init__.py:62`. It *does* override `run_keyword`
(`src/SeleniumLibrary/__init__.py:676-681`) but **only** to call `failure_occurred()`;
no argument conversion. Its only conversion is for *library import* arguments
(`_convert_timeout` / `_convert_delay`, `src/SeleniumLibrary/__init__.py:633-636`) —
notably the same `__init__`-arguments gap Browser has (§6.5).
Its keyword signatures use plain `str` for choice arguments
(`switch_window(locator=..., browser: str = "CURRENT")`, `src/SeleniumLibrary/keywords/window.py:31-35`);
`keywords/element.py` imports no `Enum` at all. Its README documents no Python API.
**This is the key comparison: SeleniumLibrary "just works" from Python because it never
demanded Enums — which argues the Enum design, not the dynamic API, is the thing needing
a Python-side answer.**

**RequestsLibrary** (<https://github.com/MarketSquare/robotframework-requests>) — does not
use PythonLibCore at all; a plain static library using `@keyword` from `robot.api.deco`
(`class RequestsLibrary(RequestsOnSessionKeywords)`, `src/RequestsLibrary/__init__.py:17`).
No `run_keyword` override, no conversion, no Enums. It is Python-callable only
incidentally, and it holds an RF-context dependency at construction
(`self.builtin = BuiltIn()`, `src/RequestsLibrary/RequestsKeywords.py:19`).

**`robot.libraries.BuiltIn`** — the instructive counter-example. `_get_context`
(`src/robot/libraries/BuiltIn.py:155-159`) raises
`RobotNotRunningError("Cannot access execution context")` when
`EXECUTION_CONTEXTS.current is None`; `RobotNotRunningError(AttributeError)` at line 5540.
Constructing `BuiltIn()` is free, but anything touching variables, the namespace or the RF
log raises. Its `robot_running` property (line 116, new in RF 6.1) is the **sanctioned
idiom for "am I inside a run?"** — directly useful to any Python-friendly design.
So "BuiltIn is usable from Python" is only half true, and RF's *conversion* machinery
(§4) is deliberately unlike it.

**PythonLibCore issue tracker** — all issues and PRs enumerated; **nothing** proposes
python-friendly calling or argument conversion. The closest is
issue #2 (closed, 2017), a complaint that a `@keyword`-renamed method could not be called
programmatically by its Python name — fixed by `core/hybrid.py:54`
(`self.attributes[name] = self.attributes[kw_name] = kw`), which is exactly the line that
makes `browser.click(...)` resolve at all. Note the double keying: `attributes` carries both
names while `keywords` and `keywords_spec` carry only the robot name, so anything looking up
a keyword spec by `kw.__name__` fails for every `@keyword(name=...)` keyword. See options doc
§3, "The naming trap".

**Browser's own issue tracker** — no open request for a Python-friendly API or
string-instead-of-enum, but the demand shows up as recurring *bug reports* about the
`run_keyword` bypass:

- <https://github.com/MarketSquare/robotframework-browser/issues/4741> (closed) — run-on-failure
  screenshots missing when driving Browser from Python. Maintainer: "Because this is by
  design, we are not going to change the functionality. That being said, you are not the
  first one that stumbled into this feature and raises an issue about it." Referenced in
  `docs/releasenotes/Browser-20.0.0.md:117`.
- <https://github.com/MarketSquare/robotframework-browser/issues/1685> (closed) — `Promise To` fails from Python.
- <https://github.com/MarketSquare/robotframework-browser/issues/4224> (closed) — `Take Screenshot` fails from Python.

**Browser already documents Python usage** — `README.md:143-159`, verified verbatim: **[V]**

```python
import Browser
browser = Browser.Browser()
browser.new_page("https://playwright.dev")
assert 'Playwright' in browser.get_text("h1")
browser.close_browser()
```

> But please note that not all features all available from Python. Example automatic
> closing, run on failure and some others features depends with the library interacting
> with Robot Framework. […] Python code must mimic the the required Robot Framework
> interfaces that the library requires.

Note the example carefully uses `get_text("h1")` with **no** assertion operator — it
sidesteps the Enum problem rather than solving it. **[I]**
The project also already generates `.pyi` stubs for Python users
(`Browser/gen_stub.py`, `tasks.py:298-302`, producing `Browser/browser.pyi`), so
investment in Python-side typing already exists. **[V]**

**`manykarim/rf-mcp`** (<https://github.com/manykarim/rf-mcp>) — the one genuine external
precedent for the technique. `src/robotmcp/utils/rf_native_type_converter.py` caches
`TypeInfo` per keyword argument and calls
`type_info.convert(value, name=name, kind="argument")` after `signature.bind_partial`,
to execute arbitrary RF keywords from Python with string arguments, outside a run. It is
LLM tooling rather than a library-authoring pattern, but it validates the approach. **[I]**

**Related RF issue, filed by the Browser team**:
<https://github.com/robotframework/robotframework/issues/3611> (closed) — "Argument
conversion with enums should work with normalized names", opened with "We are using a lot
of enums in Browser Library…". That change is what makes `"should not be"` →
`AssertionOperator.inequal` work — **but only through RF's conversion layer, which Python
callers skip.** The ergonomics gap is the direct consequence of a fix this project itself
requested. **[I]**

### AssertionEngine — no string coercion, and a context landmine

`verify_assertion` (`assertionengine/assertion_engine.py:188-219`) is typed
`operator: AssertionOperator | None` and dispatches via `handlers.get(operator)`
(line 206), raising if the lookup misses. Verified by execution: **[V]**

```
verify_assertion('abc', '==', 'abc')                     -> RuntimeError: `==` is not a valid assertion operator
verify_assertion('abc', AssertionOperator['=='], 'abc')  -> 'abc'
verify_assertion('abc', AssertionOperator['validate'], …) -> RobotNotRunningError: Cannot access execution context
```

So (a) it does **not** coerce strings, and (b) the `validate` and `then`/`evaluate`
operators call `BuiltIn().evaluate(...)` (`assertion_engine.py:152, 205, 272, 390`) and
therefore **cannot work outside an RF run at all**, no matter how good the argument
conversion is. **[V]** Any Python-friendly design must treat those two operators as a
separate problem.

Note also that AssertionEngine's `type_converter.py` is **not** a coercion helper despite
the name — 29 lines containing only `type_converter()` (returns a type name for error
messages) and `is_truthy()`. **[V]**

---

## 8. Implications

Purely derived from the above; no recommendation is being made here. **[I]**

1. A wrapper that converts arguments using RF's own machinery is **feasible, cheap and
   context-free**. `ArgumentSpec.convert` (or `TypeInfo.convert` per argument) reproduces
   RF semantics exactly, including error messages, and is derived from live annotations
   so it cannot drift from the signatures.
2. It is **strictly additive**: RF's own path never calls it, `get_keyword_types` is
   untouched, annotations stay as they are, so Libdoc, IDE completion and RF conversion
   are all unaffected.
3. The **dependency floor is the real constraint**: `robotframework >= 6.1.1` in
   `pyproject.toml:12` vs. `TypeInfo` requiring 7.0. The existing
   `try/except ImportError` in `RobotTypeConverter` shows the established mitigation.
   `allow_unknown=` needs 7.3, `get_converter()` needs 7.2 — avoid both if the floor stays low.
4. Alternatives considered and their costs:
   - **`_missing_` on every enum** — 47 classes to touch, only fixes Enums (not the 35
     `timedelta` params, TypedDicts or Unions), and diverges from RF's normalization
     rules (`ignore="_-"`, ambiguity detection). Cheap per-class, incomplete overall.
   - **`str`-mixin enums** — same partial coverage, and changes wire/serialization values.
   - **`@keyword(types=...)` with loosened annotations** — 151 sites, and it degrades
     exactly the IDE/Libdoc benefits the current design exists for.
   - **Wrapping via RF conversion** — one implementation, covers Enums, `timedelta`,
     `Path`, Unions, TypedDicts and nested generics uniformly.
5. Three behaviours differ between the RF path and any direct-Python path **regardless of
   conversion**, and each needs its own decision:
   - `Browser.run_keyword`'s failure-screenshot / trace-group / pause-on-failure layer is
     skipped entirely on attribute access (§3.1) — the subject of Browser issues 4741,
     1685 and 4224, and already acknowledged in `README.md` and the `run_on_failure`
     docstring.
   - AssertionEngine's `validate` and `then`/`evaluate` operators call
     `BuiltIn().evaluate` and raise `RobotNotRunningError` outside a run (§7). Conversion
     cannot help these; they need a context shim or explicit non-support.
   - `Browser.__init__`'s own 4 Enum / 2 `timedelta` / 1 TypedDict arguments are not
     covered by keyword-level conversion at all (§6.5).
   `BuiltIn().robot_running` (`BuiltIn.py:116`) is the sanctioned probe for branching on
   "am I inside a run?" if a design needs it.
7. There is one external precedent for the exact technique — `manykarim/rf-mcp` converts
   arguments with `TypeInfo.convert` outside a run (§7) — so this would not be
   unprecedented territory, merely unprecedented *as a library-authoring pattern*.
6. Prefer `ArgumentSpec.convert` over `ArgumentSpec.resolve` — `resolve` implies
   `dry_run=True` without `variables`, which silently skips conversion for
   `${...}`-looking values (§5).

---

## 9. Reproduction

Scripts used (all in the session scratchpad, nothing written into the repo):

| Script | Purpose |
| --- | --- |
| `stubgen.py` | stubs `Browser.generated.*` + `grpc` so `import Browser` works in a source checkout |
| `verify_rf.py` | §2.4 conversion matrix with no execution context |
| `verify_pipeline.py` | `PythonArgumentParser` over real Browser keywords |
| `verify_roundtrip.py` | §5 full convert round-trip on `click_with_options` |
| `verify_dryrun.py` | `resolve` vs `convert` `dry_run` behaviour |
| `recount.py`, `analyze_kw_types.py` | §6 counts (two independent implementations, identical results) |

## 10. Primary sources

- RF source (local 7.4.2): `robot/api/__init__.py`, `robot/api/deco.py`,
  `robot/running/arguments/{__init__,typeinfo,typeconverters,customconverters,argumentconverter,argumentresolver,argumentspec,argumentparser}.py`
- RF master: <https://github.com/robotframework/robotframework/blob/master/src/robot/api/__init__.py>
- RF tags v6.1.1 / v7.0 / v7.1 / v7.2 / v7.3 / v7.4 via the GitHub contents API
- RF release notes: `doc/releasenotes/rf-7.4.rst` (lines 298-301)
- RF API reference: <https://robot-framework.readthedocs.io/en/master/autodoc/robot.running.arguments.html>
- PythonLibCore source (local 4.6.0): `robotlibcore/{__init__,core/hybrid,core/dynamic,keywords/builder,keywords/specification}.py`
- PythonLibCore repo: <https://github.com/robotframework/PythonLibCore>
- This repo: `Browser/browser.py`, `Browser/keywords/*.py`, `Browser/utils/data_types.py`,
  `Browser/keywords/promises.py`, `Browser/entry/__main__.py`, `utest/test_python_usage.py`,
  `pyproject.toml`
