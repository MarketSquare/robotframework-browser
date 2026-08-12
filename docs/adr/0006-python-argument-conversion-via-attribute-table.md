# Python argument conversion by rebuilding the attribute table

Calling a Browser keyword from plain Python gave no argument conversion at all, so a Python
user had to write `browser.click("//button", MouseButton.middle)` while a Robot Framework
user could write `middle`. PythonLibCore keeps every keyword in two independent tables — the
**keyword table** (`self.keywords`), which `run_keyword` reads with arguments already
converted by RF, and the **attribute table** (`self.attributes`), which `__getattr__` reads
for every Python-path call — and `Browser` defines no `@keyword` methods on its own class, so
every Python-path call goes through the attribute table. We therefore rebuild only that table,
immediately after `DynamicCore.__init__`, wrapping each bound method in a proxy that converts
arguments with Robot Framework's own converters (`Browser/python_arguments.py`). The Robot
Framework path is left untouched by construction rather than by care.

## Considered options

- **A decorator on each keyword method.** Works, but touches all 151 keyword definitions
  across 17 modules, and sits on the Robot Framework path too — measured: 100 extra
  conversions for 100 `run_keyword` calls, re-validating what RF had already converted.
- **Routing Python calls through `run_keyword`.** This would also give Python callers trace
  groups and failure screenshots. Rejected: it puts the library's own execution machinery in
  the path of a plain function call. The Python-vs-RF behavioural gap stays a known, accepted
  property of the library, documented rather than closed.
- **Widening the runtime type hints** to `MouseButton | Literal["left", "middle", "right"]`.
  Rejected: it makes RF's automatic conversion harder and pushes a "str or Enum?" branch into
  every keyword body. Widening is allowed only in the generated `.pyi`, which RF never reads.
- **An opt-out flag** on the constructor. Rejected: it doubles the paths under test to buy an
  escape hatch that already exists — conversion is idempotent, so passing an already-typed
  value is the opt-out.

Full comparison, prototypes and measurements: `docs/research/python-api-options.md`.

## Consequences

- **A Python `None` is never converted.** From Python, a caller who means nothing passes the
  `None` object. Measured across every convertible parameter, converting `None` the way RF
  does would turn 126 of them into the string `'None'` and raise on 122 more. A string
  `"None"` is still converted per its hint — `"None"` is not `None`.
- **Conversion covers every type RF can convert**, not just the Enum / `timedelta` /
  `AssertionOperator` scope originally agreed. Reusing `get_keyword_types` was what made the
  mechanism small; the wider reach is the promise "the same conversion RF gives you".
- **Conversion never rewrites the caller's own object.** RF's TypedDict converter assigns
  converted items back into the mapping it is given and returns that same object. That is
  invisible when RF converts test data it just built, but on the Python path the mapping
  belongs to the caller, so mappings are copied before conversion — including mappings
  reached through a list, tuple, set or dict, because those converters build a new container
  around the caller's original dicts. A side effect of this is
  that Python ≤ 3.13 no longer sees the library rewrite a passed `recordVideo` dict into a
  resolved absolute `Path`, which makes the Python path behave the same on every Python
  version.
- **`@wraps` is load-bearing.** `rfbrowser translate` checksums `__doc__` off the attribute
  table; without `@wraps` every translation checksum in the project changes silently.
- **jsextension keywords are not covered.** They are code-generated without type annotations,
  so there is nothing to convert against and they pass through unwrapped.
- **This depends on `self.attributes`, a PythonLibCore internal**, which is why
  `robotframework-pythonlibcore` is pinned exactly. The clean long-term home is an opt-in flag
  in `HybridCore` upstream — ship here first, prove it over a release, then propose it with
  real usage behind it.
