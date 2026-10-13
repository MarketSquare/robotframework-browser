# Record Keywords (core) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the `Record Keyword` / `Record Keywords` proof of concept (an opt-in plugin in
`Browser/plugins/`) into core Browser keywords that meet every acceptance criterion in
`docs/recorder/user-story.md`.

**Starting point:** branch `feature/record-keywords`, created fresh from `main`. The proof of
concept lives on branch `claude/robot-framework-browser-recorder-om26t8` (referred to as
`$POC` below) and stays there unchanged as a reference. Code and tests are *imported* from it
in Task 2; nothing of its plugin layout, handoff notes or `docs/superpowers/` ever lands on
this branch. Set once per shell:

```bash
POC=claude/robot-framework-browser-recorder-om26t8
```

**Architecture:** A pure Python engine in `Browser/recorder/` holds everything that decides
what gets written: names, the in-memory model of a recorded keyword, the action mapper, the
targets (file / log), the session state machine and the poll loop. None of it needs a
browser. A thin keyword class `Browser/keywords/recorder.py` wires the engine to two native
gRPC calls, `RecorderPoll` and `RecorderStop`, implemented in
`node/playwright-wrapper/recorder.ts`. The Node side drives Playwright's programmatic
recorder and injects `static/recorder-toolbar.js` into every page. Python is the only clock:
every 200 ms it pushes the toolbar state down and drains Actions, signals and toolbar
commands up.

**Tech Stack:** Python 3.10+, Robot Framework parsing API (`robot.api.get_model`), pytest,
TypeScript, grpc-js, esbuild, jest, Playwright 1.63 (`context._enableRecorder`, private API),
Robot Framework acceptance tests run with `inv atest`.

**Spec:** `docs/recorder/user-story.md` (acceptance criteria AC-01 to AC-44, documentation
scope, expected test coverage). Vocabulary: `Browser/recorder/CONTEXT.md`. Decisions:
`docs/adr/0010-recorder-treats-page-under-test-as-untrusted.md`,
`docs/adr/0011-recorder-consumes-playwright-action-stream.md`.

## Global Constraints

- Keyword names stay exactly `Record Keyword` and `Record Keywords`.
- Signatures: `Record Keyword    name    file=${SUITE_SOURCE}    idle_timeout=None` and
  `Record Keywords    file=${SUITE_SOURCE}    idle_timeout=None`; the default of `file` is
  the literal string `${SUITE_SOURCE}`, resolved as a Robot Framework variable; `file=${None}`
  means log-only.
- Both keywords return text: one keyword block, or every block of the session.
- Every recorded keyword carries `[Tags]    recorded`.
- A Keyword Recording always creates a new User Keyword and never extends an existing one.
- Every name that arrives over the command channel is untrusted (ADR 0010); this includes
  argument names.
- Never call `_disableRecorder()`; call `_enableRecorder` once per context (ADR 0011).
- Python is formatted and linted with `inv lint-python`, Node with `inv lint-node`, Robot with
  `inv lint-robot`. All must be clean.
- Commit messages are semantic (`feat(recorder): …`, `fix(recorder): …`, `test(recorder): …`,
  `docs(recorder): …`) and contain **no** Claude attribution lines (user's global
  instruction overrides the default trailer).
- Do not commit `package-lock.json` changes unless a task changes `package.json`.
- Terms in code, docs and toolbar follow `Browser/recorder/CONTEXT.md`: **Action**, **Keyword
  Call** (never "step"), **Recording Session**, **Keyword Recording**, **Keyword Argument**.

## Review Focus

1. **`openPage` without a popup.** Playwright reports `openPage` for pages that already exist
   when the recorder is enabled and for tabs the person opens by hand. Expected: no Keyword
   Call and no toolbar notice. Test: Task 5, `test_open_page_produces_nothing`.
2. **An argument name that collides with a download variable.** After a recorded download
   wrote `${download}=    Promise To Wait For Download`, naming an argument `download` must
   be rejected, not shadow the variable. Test: Task 4,
   `test_argument_name_must_not_reuse_an_assigned_variable`.
3. **Literal `${` around a partial argument.** A typed value `price ${x} is 42` with only
   `42` marked must still render the literal `${x}` escaped. Test: Task 4,
   `test_partial_argument_keeps_literal_parts_escaped`.
4. **The target file cannot be written** (read-only, locked, directory removed). Expected:
   the session keeps the keyword in memory, shows the error in the toolbar and keeps
   recording. Test: Task 7, `test_save_failure_is_reported_and_recording_continues`.
5. **A command while Finish is pending.** *Undo* or *+ New Keyword* during the settle window
   must be rejected with a toolbar error, never applied to a keyword that is about to be
   written. Test: Task 7, `test_commands_are_rejected_while_finishing`.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `Browser/recorder/__init__.py` | Package marker; exports nothing public. |
| `Browser/recorder/CONTEXT.md` | Glossary (exists). |
| `Browser/recorder/README.md` | Developer notes: architecture, Playwright facts, upgrade checklist. |
| `Browser/recorder/cells.py` | `cell()`: escape a recorded value into one Robot cell. |
| `Browser/recorder/names.py` | Keyword/argument name validation, normalisation, `KnownKeywords`, `collect_known_keywords`, `NameGuard`. |
| `Browser/recorder/model.py` | In-memory `RecordedKeyword` (groups of Keyword Calls, Keyword Arguments, rendering). |
| `Browser/recorder/action_mapper.py` | Action → `Call`, signal → `SignalEffect`, selector translation. |
| `Browser/recorder/target.py` | `FileTarget` (re-read, splice, save) and `LogTarget`. |
| `Browser/recorder/session.py` | `RecorderSession` state machine, commands, deferred finish. |
| `Browser/recorder/driver.py` | `run_session()` poll loop, end conditions, idle timeout, cleanup. |
| `Browser/keywords/recorder.py` | `Recorder` keyword class and its gRPC client. |
| `node/playwright-wrapper/recorder.ts` | Playwright recorder lifecycle, buffering, toolbar injection, RPC bodies. |
| `node/playwright-wrapper/static/recorder-toolbar.js` | The injected toolbar (closed shadow root). |
| `protobuf/playwright.proto` | `RecorderPoll`, `RecorderStop`. |
| `utest/test_recorder_*.py` | Python unit tests, one file per engine module. |
| `node/playwright-wrapper/__tests__/recorder.test.ts` | jest tests for `recorder.ts`. |
| `atest/test/02_Content_Keywords/recorder.robot` | Scripted acceptance suite. |

Imported from `$POC` in Task 2 and removed again by Task 11: `Browser/recorder/plugin.py`,
`Browser/recorder/recorder.js`, `utest/test_recorder_plugin.py`. Never imported:
`Browser/plugins/README.md` (its content is re-homed in Task 13), `utest/js/` (ported in
Task 9), `RECORDER_PLUGIN_HANDOFF.md`, `docs/superpowers/`.

---

### Task 1: Commit the design documents

**Files:**
- Add: `Browser/recorder/CONTEXT.md`, `CONTEXT-MAP.md`,
  `docs/adr/0010-recorder-treats-page-under-test-as-untrusted.md`,
  `docs/adr/0011-recorder-consumes-playwright-action-stream.md`,
  `docs/recorder/user-story.md`, `docs/recorder/implementation-plan.md`

**Interfaces:** none.

- [ ] **Step 1: Check the branch and what is pending**

Run: `git branch --show-current && git status --short`
Expected: `feature/record-keywords`, and exactly the six paths above as new/modified.

- [ ] **Step 2: Commit only the documents**

```bash
git add Browser/recorder/CONTEXT.md CONTEXT-MAP.md docs/adr/0010-recorder-treats-page-under-test-as-untrusted.md docs/adr/0011-recorder-consumes-playwright-action-stream.md docs/recorder/user-story.md docs/recorder/implementation-plan.md
git commit -m "docs(recorder): add glossary, ADRs, user story and implementation plan"
```

---

### Task 2: Import the proof-of-concept engine into `Browser/recorder/`

Bring the POC code and its tests over from `$POC` unchanged except for their location and
imports, so the following tasks diff against known-good code. The POC plugin class keeps
working from its new place until Task 11 replaces it with core keywords.

**Files:**
- Import: `$POC:Browser/plugins/action_mapper.py` → `Browser/recorder/action_mapper.py`
- Import: `$POC:Browser/plugins/keyword_writer.py` → `Browser/recorder/keyword_writer.py`
- Import: `$POC:Browser/plugins/session.py` → `Browser/recorder/session.py`
- Import: `$POC:Browser/plugins/recorder_plugin.py` → `Browser/recorder/plugin.py`
- Import: `$POC:Browser/plugins/recorder.js`, `$POC:Browser/plugins/toolbar.js` → `Browser/recorder/`
- Import: `$POC:utest/test_recorder_plugin.py`, `$POC:utest/test_recorder_session.py`, `$POC:utest/test_recorder_driver.py` → `utest/`
- Create: `Browser/recorder/__init__.py`
- Modify: `pyproject.toml` (`[tool.setuptools.package-data]`)

**Interfaces:**
- Produces: modules `Browser.recorder.action_mapper`, `.keyword_writer`, `.session`, `.plugin`
  with exactly the names they had in `Browser.plugins.*` on `$POC`.

- [ ] **Step 1: Import the files**

```bash
POC=claude/robot-framework-browser-recorder-om26t8
mkdir -p Browser/recorder
git show "$POC:Browser/plugins/action_mapper.py"   > Browser/recorder/action_mapper.py
git show "$POC:Browser/plugins/keyword_writer.py"  > Browser/recorder/keyword_writer.py
git show "$POC:Browser/plugins/session.py"         > Browser/recorder/session.py
git show "$POC:Browser/plugins/recorder_plugin.py" > Browser/recorder/plugin.py
git show "$POC:Browser/plugins/recorder.js"        > Browser/recorder/recorder.js
git show "$POC:Browser/plugins/toolbar.js"         > Browser/recorder/toolbar.js
for t in plugin session driver; do
  git show "$POC:utest/test_recorder_$t.py" > "utest/test_recorder_$t.py"
done
```

`Browser/plugins/README.md`, `utest/js/`, `RECORDER_PLUGIN_HANDOFF.md` and
`docs/superpowers/` are deliberately **not** imported. Read the README on `$POC` when Task 13
writes `Browser/recorder/README.md`, and `utest/js/recorder.test.js` when Task 9 writes the
jest tests (`git show "$POC:<path>"`).

- [ ] **Step 2: Create the package marker**

`Browser/recorder/__init__.py`:

```python
# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The engine behind `Record Keyword` and `Record Keywords`. See CONTEXT.md."""
```

- [ ] **Step 3: Ship the JS files as package data (temporarily)**

In `pyproject.toml`, under `[tool.setuptools.package-data]`, add after the `"*"` entry:

```toml
"Browser.recorder" = [
    "*.js",
]
```

(This entry disappears again in Task 9, when the JS moves into the Node wrapper.)

- [ ] **Step 4: Fix imports in the imported module and the tests**

```bash
sed -i '' 's/Browser\.plugins\.recorder_plugin/Browser.recorder.plugin/g; s/from Browser\.plugins import recorder_plugin/from Browser.recorder import plugin as recorder_plugin/g; s/Browser\.plugins/Browser.recorder/g' utest/test_recorder_plugin.py utest/test_recorder_session.py utest/test_recorder_driver.py Browser/recorder/plugin.py
grep -rn "Browser.plugins\|Browser/plugins" Browser utest atest pyproject.toml || true
```

Expected: the final `grep` prints nothing. Update the module docstring of
`Browser/recorder/plugin.py` to say `plugins=Browser.recorder.plugin.RecorderPlugin`.

- [ ] **Step 5: Run the imported tests**

Run: `pytest utest/test_recorder_plugin.py utest/test_recorder_session.py utest/test_recorder_driver.py -q --no-cov`
Expected: all pass, with the same test count as `pytest` reports for the same three files on
`$POC`.

- [ ] **Step 6: Commit**

```bash
inv lint-python --fix
git add Browser/recorder pyproject.toml utest/test_recorder_*.py
git commit -m "feat(recorder): import the recorder engine from the proof of concept"
```

---

### Task 3: `cells.py` and `names.py` — one home for escaping and naming

Split the pure helpers out of `keyword_writer.py` and `plugin.py`, drop the "reuse" exception
(AC-37), add argument-name validation (AC-34) and gather the shadow checks into `NameGuard`.

**Files:**
- Create: `Browser/recorder/cells.py`, `Browser/recorder/names.py`
- Modify: `Browser/recorder/keyword_writer.py` (import from the new modules), `Browser/recorder/session.py` (use `NameGuard`), `Browser/recorder/plugin.py` (import from `names`)
- Test: `utest/test_recorder_names.py` (new; receives the naming tests from `utest/test_recorder_plugin.py`)

**Interfaces:**
- Produces:
  - `cells.cell(value: str, *, at_start: bool = True, at_end: bool = True) -> str` — `at_start` / `at_end` say whether the text sits at the start / end of the whole cell; only then do a leading `#`, leading/trailing spaces and the empty string need escaping (a value can be split into literal parts around a Keyword Argument)
  - `names.keyword_name_error(name: object) -> str | None`
  - `names.argument_name_error(name: object) -> str | None`
  - `names.normalize_keyword_name(name: str) -> str`
  - `names.existing_keyword_names(target: Path) -> set[str]`
  - `names.KnownKeywords(names: frozenset[str], embedded: tuple[tuple[str, Callable[[str], bool]], ...], bdd_prefixes: tuple[str, ...])`
  - `names.collect_known_keywords() -> KnownKeywords` (no `target` parameter any more)
  - `names.NameGuard(known: KnownKeywords)` with `.error(name: str, taken: Iterable[str] = ()) -> str | None`

- [ ] **Step 1: Move the tests first**

Create `utest/test_recorder_names.py` with the license header and move these tests (and the
`_PROBE_LIBRARY` / `_run_probe` helpers and the `parametrize` tables they use) out of
`utest/test_recorder_plugin.py`, unchanged except for imports:
`test_usable_keyword_names_are_accepted`, `test_unusable_keyword_names_are_reported`,
`test_non_string_keyword_name_is_reported_not_raised`,
`test_normalize_keyword_name_matches_robots_own_comparison`, `test_existing_keyword_names`,
`test_collect_known_keywords_is_empty_without_a_running_suite`,
`test_collect_known_keywords_warns_when_the_keyword_store_is_missing`,
`test_collect_known_keywords_sees_the_whole_running_suite`,
`test_collect_known_keywords_covers_bdd_prefix_stripping`,
`test_recording_rejects_the_bdd_variant_of_a_target_file_keyword`,
`test_recording_rejects_an_embedded_argument_instantiation`,
`test_recording_rejects_an_embedded_keyword_of_the_target_file`,
`test_recording_rejects_an_embedded_keyword_of_the_default_target`,
`test_an_ordinary_name_is_still_accepted_inside_a_real_run`,
`test_embedded_matcher_claims_robot_normalised_names`,
`test_embedded_matcher_leaves_unclaimed_names_alone`,
`test_embedded_matcher_is_none_for_a_literal_name`,
`test_recording_rejects_a_normalised_embedded_instantiation`,
`test_collect_known_keywords_includes_owner_qualified_names`,
`test_recording_rejects_an_owner_qualified_name_on_the_default_target`,
`test_a_name_an_embedded_owner_does_not_claim_stays_accepted`.

Imports at the top of the new file:

```python
from Browser.recorder import names
from Browser.recorder.names import (
    KnownKeywords,
    NameGuard,
    _embedded_matcher,
    argument_name_error,
    collect_known_keywords,
    existing_keyword_names,
    keyword_name_error,
    normalize_keyword_name,
)
```

Replace `_PROBE_LIBRARY` with this version (no reuse, uses `NameGuard`):

```python
_PROBE_LIBRARY = '''\
import json
import pathlib

from robot.libraries.BuiltIn import BuiltIn

from Browser.recorder.names import NameGuard, collect_known_keywords, existing_keyword_names


def _target(file=None):
    if file:
        return pathlib.Path(file).resolve()
    return pathlib.Path(BuiltIn().get_variable_value("${SUITE_SOURCE}")).resolve()


def _report(payload):
    pathlib.Path(__file__).with_name("probe.json").write_text(json.dumps(payload))


def dump_known_keywords(file=None):
    known = collect_known_keywords()
    _report(
        {
            "names": sorted(known.names),
            "embedded": sorted(name for name, _ in known.embedded),
            "prefixes": sorted(known.bdd_prefixes),
        }
    )


def try_to_record(name, file=None):
    """Check a name exactly as `Record Keyword` does, and report the outcome."""
    guard = NameGuard(collect_known_keywords())
    error = guard.error(name, taken=existing_keyword_names(_target(file)))
    _report({"outcome": "rejected", "error": error} if error else {"outcome": "accepted"})
'''
```

Every probe test that called `monkeypatch.setattr(recorder_plugin.logger, ...)` now patches
`names.logger`.

Delete from `utest/test_recorder_plugin.py` (the behaviour is gone, AC-37):
`test_collect_known_keywords_excludes_the_recording_targets_own_names`,
`test_bdd_variants_of_the_target_file_survive_its_exclusion`,
`test_recording_reuse_with_different_spelling_survives_a_real_robot_run`.

Replace `test_recording_reuses_a_keyword_of_a_symlinked_suite_file` with (in
`utest/test_recorder_names.py`):

```python
def test_recording_rejects_a_suite_keyword_behind_a_symlink(tmp_path):
    """AC-39: a name the suite file already defines is taken, symlink or not."""
    outcome = _run_probe(
        tmp_path, "Try To Record    Suite Local Keyword", via_symlink=True
    )
    assert outcome["outcome"] == "rejected"
    assert "Suite Local Keyword" in outcome["error"]


def test_recording_rejects_a_keyword_of_the_target_file(tmp_path):
    """AC-37: no reuse - an existing name in the target is a collision."""
    outcome = _run_probe(
        tmp_path, "Try To Record    My Helper    file=helpers.resource"
    )
    assert outcome["outcome"] == "rejected"
```

Add the new argument-name tests:

```python
@pytest.mark.parametrize("name", ["email", "item_id", "_x", "Password2"])
def test_usable_argument_names_are_accepted(name):
    assert argument_name_error(name) is None


@pytest.mark.parametrize(
    "name",
    ["", "2fa", "e mail", "a-b", "${email}", "x}", "a\nb", "ä", None, 42],
)
def test_unusable_argument_names_are_reported(name):
    assert argument_name_error(name)


def test_name_guard_rejects_a_taken_name_in_any_spelling():
    guard = NameGuard(KnownKeywords())
    assert guard.error("l_ogin as ADMIN", taken=["Login As Admin"])


def test_name_guard_reports_an_invalid_name_before_collisions():
    guard = NameGuard(KnownKeywords(names=frozenset({"Log"})))
    assert "must not be empty" in guard.error("")


def test_name_guard_rejects_a_known_library_keyword():
    guard = NameGuard(KnownKeywords(names=frozenset({"Click"})))
    assert "Click" in guard.error("click")
```

- [ ] **Step 2: Run the moved tests to verify they fail**

Run: `pytest utest/test_recorder_names.py -q --no-cov`
Expected: FAIL with `ModuleNotFoundError: No module named 'Browser.recorder.names'`.

- [ ] **Step 3: Create `cells.py`**

Move `_VARIABLE_START`, `_MULTI_SPACE` and the body of `LiveKeywordWriter._cell` out of
`keyword_writer.py` into `Browser/recorder/cells.py` as a module function (same docstring,
same code, plus the two edge flags):

```python
def cell(value: str, *, at_start: bool = True, at_end: bool = True) -> str:
    # (docstring moved from LiveKeywordWriter._cell, plus:)
    # ``at_start`` / ``at_end`` say whether ``value`` begins / ends the whole
    # cell. A value split around a Keyword Argument (`id-${n}`) is escaped part
    # by part, and only the real cell edges need the `#`, edge-space and empty
    # rules.
    if value == "":
        return "${EMPTY}" if at_start and at_end else ""
    cell = value.replace("\\", "\\\\")
    for char, escape in (("\t", "\\t"), ("\r", "\\r"), ("\n", "\\n")):
        cell = cell.replace(char, escape)
    cell = "".join(
        f"\\u{ord(char):04x}" if char.isspace() and char != " " else char
        for char in cell
    )
    cell = _VARIABLE_START.sub(r"\\\g<0>", cell)
    if at_start and cell.startswith("#"):
        cell = "\\" + cell
    cell = _MULTI_SPACE.sub(lambda m: "${SPACE}" * len(m.group()), cell)
    if at_start and cell.startswith(" "):
        cell = "${SPACE}" + cell[1:]
    if at_end and cell.endswith(" "):
        cell = cell[:-1] + "${SPACE}"
    return cell
```

Add to `utest/test_recorder_names.py` (or a small `utest/test_recorder_cells.py`):

```python
from Browser.recorder.cells import cell


def test_inner_part_keeps_edge_spaces_and_hash():
    assert cell("price ", at_end=False) == "price "
    assert cell(" #x", at_start=False) == " #x"
    assert cell(" x ") == "${SPACE}x${SPACE}"
    assert cell("#x") == "\\#x"
```

In `keyword_writer.py`, make `_cell` and `_display` call `cells.cell`. `_VARIABLE_START` is
also needed by `names.py`; import it from `cells`.

- [ ] **Step 4: Create `names.py`**

Move into `Browser/recorder/names.py`, unchanged: `_CONTROL_CHARS`, `_ANY_DOUBLE_WHITESPACE`,
`_PIPE_SEPARATOR`, `_surrogates`, `_NAME_RULES`, `_exotic_whitespace_error`,
`keyword_name_error`, `normalize_keyword_name`, `existing_keyword_names` (from
`keyword_writer.py`) and `KnownKeywords`, `_embedded_matcher`, `_normalized_embedded_pattern`,
`_bdd_variants` (from `plugin.py`). Then change and add:

```python
def _shadowable_forms(
    name: str, owner_name: str | None, prefixes: tuple[str, ...]
) -> list[str]:
    """Every name a call can reach ``name`` by.

    That is the name itself, every form a BDD-prefixed call also reaches, and -
    for an owner a call may qualify with - each of those prefixed by the owner
    name.
    """
    forms = []
    for form in (name, *_bdd_variants(name, prefixes)):
        forms.append(form)
        if owner_name:
            forms.append(f"{owner_name}.{form}")
    return forms
```

`collect_known_keywords()` loses its `target` parameter, the `is_target` computation and the
`reusable` branch; its loop body becomes:

```python
        for kw in getattr(owner, "keywords", ()):
            if not kw.name:
                continue
            for candidate in _shadowable_forms(kw.name, owner_name, prefixes):
                matches = _embedded_matcher(candidate)
                if matches is not None:
                    embedded.append((candidate, matches))
                else:
                    names.add(candidate)
```

Update its docstring: drop the paragraph about ``target`` and reuse.

Argument names:

```python
# A Keyword Argument becomes `${name}` in `[Arguments]` and in every Keyword
# Call that uses it. The name arrives over the page-callable command channel
# (ADR 0010), so only the plainest shape Robot accepts is allowed: anything
# else could close the variable early or smuggle in extended variable syntax.
_ARGUMENT_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def argument_name_error(name: object) -> str | None:
    """Why ``name`` is unusable as a Keyword Argument name, or ``None``."""
    if not isinstance(name, str):
        return "Argument name must be a string."
    if not name:
        return "Argument name must not be empty."
    if not _ARGUMENT_NAME.fullmatch(name):
        return (
            "Argument name must start with a letter or '_' and contain only "
            "letters, digits and '_'."
        )
    return None
```

`NameGuard` takes over `_shadow_error`, `_name_forms` and `_embedded_shadow` from
`session.py`:

```python
class NameGuard:
    """Decide whether a keyword name may be recorded (ADR 0010).

    ``taken`` names - keywords already in the target file and keywords recorded
    earlier in this session - are collisions too, since a Keyword Recording never
    extends an existing keyword.
    """

    def __init__(self, known: KnownKeywords) -> None:
        self._known = {normalize_keyword_name(n): n for n in known.names}
        self._embedded = known.embedded
        self._prefixes = known.bdd_prefixes

    def error(self, name: str, taken: Iterable[str] = ()) -> str | None:
        invalid = keyword_name_error(name)
        if invalid:
            return invalid
        taken_map = {normalize_keyword_name(t): t for t in taken}
        if normalize_keyword_name(name) in taken_map:
            return f"Keyword '{taken_map[normalize_keyword_name(name)]}' already exists."
        for form in self._name_forms(name):
            normalized = normalize_keyword_name(form)
            existing = (
                self._known.get(normalized)
                or taken_map.get(normalized)
                or self._embedded_shadow(form)
            )
            if existing is not None:
                return (
                    f"Keyword '{existing}' already exists in this suite and would be "
                    f"shadowed by '{name}'. Please choose another name."
                )
        return None
```

`_name_forms` and `_embedded_shadow` are copied from `session.py` as methods (the latter
logs via `logger.debug` instead of `self.log`).

- [ ] **Step 5: Use the new modules from the old ones**

- `keyword_writer.py`: delete everything that moved; `from .cells import cell` and
  `from .names import normalize_keyword_name`.
- `plugin.py`: delete everything that moved; `from .names import collect_known_keywords`;
  call `collect_known_keywords()` without `target`.
- `session.py`: replace `known_keywords`, `embedded_keywords`, `bdd_prefixes` constructor
  parameters with `known: KnownKeywords | None = None`; build `self._guard = NameGuard(known or KnownKeywords())`;
  `_new` uses `self._guard.error(name, taken=[*self._keywords, *existing_keyword_names(self.target)])`;
  the fixed-name check uses `self._guard.error(fixed_name, taken=existing_keyword_names(self.target))`;
  delete `_duplicate_error`, `_shadow_error`, `_name_forms`, `_embedded_shadow`.
- `plugin.py::_run_session` passes `known=collect_known_keywords()`.
- Update `utest/test_recorder_session.py` / `utest/test_recorder_driver.py` call sites that
  passed `known_keywords=` etc. to `known=KnownKeywords(names=frozenset(...), ...)`. Tests that
  assert a fixed name is *reused* now assert it is rejected.

- [ ] **Step 6: Run all recorder tests**

Run: `pytest utest/test_recorder_names.py utest/test_recorder_plugin.py utest/test_recorder_session.py utest/test_recorder_driver.py -q --no-cov`
Expected: PASS.

- [ ] **Step 7: Lint and commit**

```bash
inv lint-python --fix
git add Browser/recorder utest/test_recorder_*.py
git commit -m "refactor(recorder): gather naming rules in names.py, drop keyword reuse"
```

---

### Task 4: `model.py` — the in-memory recorded keyword

The model is the single source of truth for a Keyword Recording. Targets only render it.

**Files:**
- Create: `Browser/recorder/model.py`
- Test: `utest/test_recorder_model.py`

**Interfaces:**
- Consumes: `cells.cell`, `names.argument_name_error`, `names.normalize_keyword_name`
- Produces:
  - `ArgRef(name: str)` (frozen dataclass)
  - `Value(segments: list[str | ArgRef], selectable: bool = True)`, `Value.literal(text: str, selectable: bool = True) -> Value`, `.text -> str | None`, `.references() -> set[str]`, `.render() -> str`
  - `Call(keyword: str, args: list[Value], assign: str | None = None)`, `.render() -> str`
  - `Argument(name: str, default: str, use_default: bool = True)`, `.render() -> str`
  - `RecordedKeyword(name: str)` with `.add(call)`, `.update_last(call) -> bool`, `.attach(before: list[Call], after: list[Call]) -> bool`, `.undo() -> bool`, `.calls() -> list[Call]`, `.unique_variable(base: str) -> str`, `.make_argument(call: int, value: int, start: int, end: int, name: str) -> list[tuple[int, int]]`, `.replace(name: str, occurrences: list[tuple[int, int]]) -> None`, `.set_default(name: str, use: bool) -> None`, `.lines() -> list[str]`, `.block() -> str`, `.text() -> str`, `__len__` (number of Keyword Calls)
  - `TAG = "recorded"`

- [ ] **Step 1: Write the failing tests**

`utest/test_recorder_model.py`:

```python
from __future__ import annotations

import pytest

from Browser.recorder.model import ArgRef, Call, RecordedKeyword, Value


def fill(text: str) -> Call:
    return Call("Fill Text", [Value.literal("#name", selectable=False), Value.literal(text)])


def test_block_has_tag_and_calls():
    kw = RecordedKeyword("Fill Name")
    kw.add(fill("Alice"))
    assert kw.block() == (
        "Fill Name\n    [Tags]    recorded\n    Fill Text    \\#name    Alice\n"
    )
    assert kw.text().startswith("*** Keywords ***\nFill Name\n")


def test_update_last_replaces_the_primary_call():
    kw = RecordedKeyword("K")
    kw.add(fill("A"))
    assert kw.update_last(fill("Al"))
    assert [c.render() for c in kw.calls()] == ["Fill Text    \\#name    Al"]


def test_undo_removes_the_whole_group():
    kw = RecordedKeyword("K")
    kw.add(Call("Click", [Value.literal("#b", False)]))
    kw.attach([Call("Handle Future Dialogs", [Value.literal("action=accept", False)])], [])
    assert len(kw) == 2
    assert kw.undo()
    assert len(kw) == 0
    assert not kw.undo()


def test_make_argument_whole_value_with_default():
    kw = RecordedKeyword("K")
    kw.add(fill("admin@example.com"))
    assert kw.make_argument(0, 1, 0, len("admin@example.com"), "email") == []
    assert kw.lines() == [
        "[Tags]    recorded",
        "[Arguments]    ${email}=admin@example.com",
        "Fill Text    \\#name    ${email}",
    ]


def test_make_argument_partial_value():
    kw = RecordedKeyword("K")
    kw.add(Call("Go To", [Value.literal("https://shop/item/42")]))
    kw.make_argument(0, 0, 18, 20, "item_id")
    assert kw.calls()[0].render() == "Go To    https://shop/item/${item_id}"
    assert kw.arguments[0].default == "42"


def test_partial_argument_keeps_literal_parts_escaped():
    kw = RecordedKeyword("K")
    kw.add(fill("price ${x} is 42"))
    kw.make_argument(0, 1, 14, 16, "amount")
    assert kw.calls()[0].render() == "Fill Text    \\#name    price \\${x} is ${amount}"


def test_selectors_cannot_become_arguments():
    kw = RecordedKeyword("K")
    kw.add(fill("x"))
    with pytest.raises(ValueError, match="Selectors"):
        kw.make_argument(0, 0, 0, 1, "sel")


def test_make_argument_reports_other_occurrences():
    kw = RecordedKeyword("K")
    kw.add(fill("admin@example.com"))
    kw.add(Call("Fill Text", [Value.literal("#search", False), Value.literal("admin@example.com")]))
    assert kw.make_argument(0, 1, 0, 17, "email") == [(1, 1)]
    kw.replace("email", [(1, 1)])
    assert kw.calls()[1].render() == "Fill Text    \\#search    ${email}"


def test_unused_argument_is_removed_on_undo():
    kw = RecordedKeyword("K")
    kw.add(fill("a"))
    kw.add(fill("b"))
    kw.make_argument(1, 1, 0, 1, "second")
    kw.undo()
    assert kw.arguments == []


def test_default_follows_continued_typing():
    kw = RecordedKeyword("K")
    kw.add(fill("adm"))
    kw.make_argument(0, 1, 0, 3, "email")
    kw.update_last(fill("admin@example.com"))
    assert kw.calls()[0].render() == "Fill Text    \\#name    ${email}"
    assert kw.arguments[0].default == "admin@example.com"


def test_partial_default_follows_when_prefix_still_matches():
    kw = RecordedKeyword("K")
    kw.add(fill("id-4"))
    kw.make_argument(0, 1, 3, 4, "n")
    kw.update_last(fill("id-42"))
    assert kw.arguments[0].default == "42"


def test_partial_argument_is_dropped_when_typing_breaks_the_prefix():
    kw = RecordedKeyword("K")
    kw.add(fill("id-4"))
    kw.make_argument(0, 1, 3, 4, "n")
    kw.update_last(fill("xd-42"))
    assert kw.calls()[0].render() == "Fill Text    \\#name    xd-42"
    assert kw.arguments == []


def test_required_arguments_come_before_defaulted_ones():
    kw = RecordedKeyword("K")
    kw.add(fill("a"))
    kw.add(fill("b"))
    kw.make_argument(0, 1, 0, 1, "first")
    kw.make_argument(1, 1, 0, 1, "second")
    kw.set_default("second", False)
    assert kw.lines()[1] == "[Arguments]    ${second}    ${first}=a"


def test_argument_name_must_be_unique_in_any_spelling():
    kw = RecordedKeyword("K")
    kw.add(fill("a"))
    kw.add(fill("b"))
    kw.make_argument(0, 1, 0, 1, "email")
    with pytest.raises(ValueError, match="already"):
        kw.make_argument(1, 1, 0, 1, "E_mail")


def test_argument_name_must_not_reuse_an_assigned_variable():
    kw = RecordedKeyword("K")
    kw.add(Call("Click", [Value.literal("#dl", False)]))
    var = kw.unique_variable("download")
    kw.attach(
        [Call("Promise To Wait For Download", [], assign=var)],
        [Call("Wait For", [Value([ArgRef(var)], selectable=False)])],
    )
    kw.add(fill("x"))
    with pytest.raises(ValueError, match="already"):
        kw.make_argument(3, 1, 0, 1, "download")


def test_unique_variable_counts_up():
    kw = RecordedKeyword("K")
    kw.add(Call("Click", [Value.literal("#a", False)]))
    first = kw.unique_variable("download")
    kw.attach([Call("Promise To Wait For Download", [], assign=first)], [])
    assert (first, kw.unique_variable("download")) == ("download", "download_2")


def test_empty_value_renders_as_empty_marker():
    assert Value.literal("").render() == "${EMPTY}"


@pytest.mark.parametrize("start,end", [(0, 0), (2, 1), (-1, 1), (0, 99)])
def test_bad_marks_are_rejected(start, end):
    kw = RecordedKeyword("K")
    kw.add(fill("ab"))
    with pytest.raises(ValueError):
        kw.make_argument(0, 1, start, end, "x")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest utest/test_recorder_model.py -q --no-cov`
Expected: FAIL with `ModuleNotFoundError: No module named 'Browser.recorder.model'`.

- [ ] **Step 3: Implement `model.py`**

```python
# (license header as in Task 2)
"""The in-memory model of one User Keyword being recorded.

It is the single source of truth for a Keyword Recording: targets only render
it. Keyword Calls are kept in *groups*, one per Action, because one Action may
need several Keyword Calls (a dialog handler before a click, a download promise
around it) and Undo must remove all of them together.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .cells import cell
from .names import argument_name_error, normalize_keyword_name

TAG = "recorded"
_INDENT = "    "


@dataclass(frozen=True)
class ArgRef:
    """A reference to a Keyword Argument (or an assigned variable) in a value."""

    name: str


@dataclass
class Value:
    """One argument cell of a Keyword Call.

    ``selectable`` is False for selectors and for structural values (buttons,
    operators, option strategies): those can never become Keyword Arguments.
    """

    segments: list[str | ArgRef]
    selectable: bool = True

    @classmethod
    def literal(cls, text: str, selectable: bool = True) -> Value:
        return cls([text] if text else [], selectable)

    @property
    def text(self) -> str | None:
        """The literal text, or ``None`` once a reference is part of it."""
        if any(isinstance(s, ArgRef) for s in self.segments):
            return None
        return "".join(s for s in self.segments if isinstance(s, str))

    def references(self) -> set[str]:
        return {s.name for s in self.segments if isinstance(s, ArgRef)}

    def render(self) -> str:
        if not self.segments:
            return "${EMPTY}"
        last = len(self.segments) - 1
        return "".join(
            f"${{{s.name}}}"
            if isinstance(s, ArgRef)
            else cell(s, at_start=i == 0, at_end=i == last)
            for i, s in enumerate(self.segments)
        )


@dataclass
class Call:
    """One Keyword Call: ``[${assign}=]    Keyword    args...``."""

    keyword: str
    args: list[Value]
    assign: str | None = None

    def render(self) -> str:
        cells = [f"${{{self.assign}}}="] if self.assign else []
        cells.append(self.keyword)
        cells.extend(value.render() for value in self.args)
        return _INDENT.join(cells)


@dataclass
class Argument:
    name: str
    default: str
    use_default: bool = True

    def render(self) -> str:
        if self.use_default:
            return f"${{{self.name}}}={cell(self.default)}"
        return f"${{{self.name}}}"


@dataclass
class _Group:
    primary: Call
    before: list[Call] = field(default_factory=list)
    after: list[Call] = field(default_factory=list)

    def calls(self) -> list[Call]:
        return [*self.before, self.primary, *self.after]


class RecordedKeyword:
    def __init__(self, name: str) -> None:
        self.name = name
        self.arguments: list[Argument] = []
        self._groups: list[_Group] = []

    def __len__(self) -> int:
        return sum(len(group.calls()) for group in self._groups)

    def calls(self) -> list[Call]:
        return [call for group in self._groups for call in group.calls()]

    # -- recording --------------------------------------------------------- #

    def add(self, call: Call) -> None:
        self._groups.append(_Group(call))

    def update_last(self, call: Call) -> bool:
        """Replace the last Action's Keyword Call with Playwright's refinement.

        Values that were turned into Keyword Arguments stay arguments; their
        default follows the newly typed text (AC-33).
        """
        if not self._groups:
            return False
        group = self._groups[-1]
        old = group.primary
        if old.keyword == call.keyword and len(old.args) == len(call.args):
            call.args = [self._carry(o, n) for o, n in zip(old.args, call.args)]
        group.primary = call
        self._drop_unused()
        return True

    def attach(self, before: list[Call], after: list[Call]) -> bool:
        """Wrap the last Action's Keyword Call with signal handling."""
        if not self._groups:
            return False
        self._groups[-1].before.extend(before)
        self._groups[-1].after.extend(after)
        return True

    def undo(self) -> bool:
        if not self._groups:
            return False
        self._groups.pop()
        self._drop_unused()
        return True

    # -- variables and arguments ------------------------------------------ #

    def _taken_variables(self) -> set[str]:
        names = {normalize_keyword_name(a.name) for a in self.arguments}
        names.update(
            normalize_keyword_name(c.assign) for c in self.calls() if c.assign
        )
        return names

    def unique_variable(self, base: str) -> str:
        taken = self._taken_variables()
        candidate, number = base, 1
        while normalize_keyword_name(candidate) in taken:
            number += 1
            candidate = f"{base}_{number}"
        return candidate

    def argument(self, name: str) -> Argument:
        for argument in self.arguments:
            if argument.name == name:
                return argument
        raise ValueError(f"No argument '{name}'.")

    def make_argument(
        self, call: int, value: int, start: int, end: int, name: str
    ) -> list[tuple[int, int]]:
        """Turn ``text[start:end]`` of one value into ``${name}``.

        Returns the other values that contain the same text, for the toolbar
        to offer (AC-31).
        """
        error = argument_name_error(name)
        if error:
            raise ValueError(error)
        if normalize_keyword_name(name) in self._taken_variables():
            raise ValueError(f"A variable named '{name}' already exists.")
        target = self._value(call, value)
        if not target.selectable:
            raise ValueError("Selectors and fixed options cannot become arguments.")
        text = target.text
        if text is None:
            raise ValueError("This value already contains an argument.")
        if not (0 <= start < end <= len(text)):
            raise ValueError("Mark a non-empty part of the value.")
        marked = text[start:end]
        target.segments = _split(text, start, end, ArgRef(name))
        self.arguments.append(Argument(name, marked))
        return [
            (c, v)
            for c, v, other in self._values()
            if (c, v) != (call, value)
            and other.selectable
            and other.text is not None
            and marked in other.text
        ]

    def replace(self, name: str, occurrences: list[tuple[int, int]]) -> None:
        marked = self.argument(name).default
        for call, value in occurrences:
            target = self._value(call, value)
            text = target.text
            if not target.selectable or text is None or marked not in text:
                continue
            target.segments = _split_all(text, marked, ArgRef(name))

    def set_default(self, name: str, use: bool) -> None:
        self.argument(name).use_default = bool(use)

    # -- rendering --------------------------------------------------------- #

    def lines(self) -> list[str]:
        """The keyword's body rows, unindented."""
        rows = [f"[Tags]{_INDENT}{TAG}"]
        if self.arguments:
            ordered = [a for a in self.arguments if not a.use_default] + [
                a for a in self.arguments if a.use_default
            ]
            rows.append(_INDENT.join(["[Arguments]", *(a.render() for a in ordered)]))
        rows.extend(call.render() for call in self.calls())
        return rows

    def block(self) -> str:
        return "\n".join([self.name, *(_INDENT + row for row in self.lines())]) + "\n"

    def text(self) -> str:
        return "*** Keywords ***\n" + self.block()

    # -- helpers ----------------------------------------------------------- #

    def _values(self):
        for c, call in enumerate(self.calls()):
            for v, value in enumerate(call.args):
                yield c, v, value

    def _value(self, call: int, value: int) -> Value:
        try:
            return self.calls()[call].args[value]
        except (IndexError, TypeError):
            raise ValueError("No such value.") from None

    def _carry(self, old: Value, new: Value) -> Value:
        text = new.text
        refs = [s for s in old.segments if isinstance(s, ArgRef)]
        if text is None or len(refs) != 1:
            return new
        index = old.segments.index(refs[0])
        prefix = "".join(s for s in old.segments[:index] if isinstance(s, str))
        suffix = "".join(s for s in old.segments[index + 1 :] if isinstance(s, str))
        if not (
            text.startswith(prefix)
            and text.endswith(suffix)
            and len(text) > len(prefix) + len(suffix)
        ):
            return new
        argument = next((a for a in self.arguments if a.name == refs[0].name), None)
        if argument is None:
            return new
        argument.default = text[len(prefix) : len(text) - len(suffix)]
        return Value([*_nonempty(prefix), refs[0], *_nonempty(suffix)], old.selectable)

    def _drop_unused(self) -> None:
        used: set[str] = set()
        for call in self.calls():
            for value in call.args:
                used |= value.references()
        self.arguments = [a for a in self.arguments if a.name in used]


def _nonempty(text: str) -> list[str]:
    return [text] if text else []


def _split(text: str, start: int, end: int, ref: ArgRef) -> list[str | ArgRef]:
    return [*_nonempty(text[:start]), ref, *_nonempty(text[end:])]


def _split_all(text: str, marked: str, ref: ArgRef) -> list[str | ArgRef]:
    parts = text.split(marked)
    segments: list[str | ArgRef] = list(_nonempty(parts[0]))
    for part in parts[1:]:
        segments.append(ref)
        segments.extend(_nonempty(part))
    return segments
```

- [ ] **Step 4: Run the tests**

Run: `pytest utest/test_recorder_model.py -q --no-cov`
Expected: PASS.

- [ ] **Step 5: Lint and commit**

```bash
inv lint-python --fix
git add Browser/recorder/model.py utest/test_recorder_model.py
git commit -m "feat(recorder): add the in-memory recorded keyword model with Keyword Arguments"
```

---

### Task 5: Action mapper returns `Call`s and handles signals

**Files:**
- Modify: `Browser/recorder/action_mapper.py`
- Test: `utest/test_recorder_mapper.py` (new; receives the mapper tests from `utest/test_recorder_plugin.py`)

**Interfaces:**
- Consumes: `model.Call`, `model.Value`, `model.ArgRef`
- Produces:
  - `ActionMapper.map(action: dict) -> Call | None`
  - `ActionMapper.map_signal(signal: dict, unique: Callable[[str], str]) -> SignalEffect | None`
  - `SignalEffect(before: list[Call], after: list[Call])` (dataclass)
  - `SILENT_ACTIONS: frozenset[str]` — Action names that produce nothing and no notice (`{"openPage"}`)
  - `to_browser_selector(selector: str) -> str` (unchanged)

- [ ] **Step 1: Move and adapt the tests**

Move `test_to_browser_selector` and every `test_map_*` / `test_unknown_action_returns_none`
from `utest/test_recorder_plugin.py` into `utest/test_recorder_mapper.py`. They compare
`(keyword, args)` tuples today; compare through a helper instead:

```python
from Browser.recorder.action_mapper import SILENT_ACTIONS, ActionMapper, to_browser_selector
from Browser.recorder.model import RecordedKeyword


def rendered(action: dict) -> str | None:
    call = ActionMapper().map(action)
    return None if call is None else call.render()
```

e.g. `assert rendered({"name": "click", "selector": "internal:role=button[name=\"Go\"i]"}) == 'Click    role=button[name="Go"i]'`.
Delete `test_map_open_page` and add:

```python
def test_open_page_produces_nothing():
    assert ActionMapper().map({"name": "openPage", "url": "https://x"}) is None
    assert "openPage" in SILENT_ACTIONS


def test_selector_and_fixed_values_are_not_selectable():
    call = ActionMapper().map({"name": "select", "selector": "#s", "options": ["a"]})
    assert [v.selectable for v in call.args] == [False, False, True]


def test_fill_text_is_selectable():
    call = ActionMapper().map({"name": "fill", "selector": "#n", "text": "Al"})
    assert [v.selectable for v in call.args] == [False, True]


def test_popup_signal_switches_to_the_new_page():
    effect = ActionMapper().map_signal({"name": "popup"}, lambda b: b)
    assert [c.render() for c in effect.after] == ["Switch Page    NEW"]
    assert effect.before == []


def test_dialog_signal_accepts_before_the_action():
    effect = ActionMapper().map_signal({"name": "dialog"}, lambda b: b)
    assert [c.render() for c in effect.before] == ["Handle Future Dialogs    action=accept"]


def test_download_signal_wraps_the_action():
    kw = RecordedKeyword("K")
    effect = ActionMapper().map_signal({"name": "download"}, kw.unique_variable)
    assert [c.render() for c in effect.before] == ["${download}=    Promise To Wait For Download"]
    assert [c.render() for c in effect.after] == ["Wait For    ${download}"]


@pytest.mark.parametrize("name", ["expect", "navigation", "unknown"])
def test_other_signals_produce_nothing(name):
    assert ActionMapper().map_signal({"name": name}, lambda b: b) is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest utest/test_recorder_mapper.py -q --no-cov`
Expected: FAIL (`ImportError: cannot import name 'SILENT_ACTIONS'`).

- [ ] **Step 3: Implement**

In `action_mapper.py`:

```python
from dataclasses import dataclass

from .model import ArgRef, Call, Value

#: Actions that never produce a Keyword Call and need no notice: Playwright
#: reports `openPage` for pages that already exist and for tabs opened by hand,
#: and a page opened by an Action arrives as a `popup` signal on that Action.
SILENT_ACTIONS = frozenset({"openPage"})


@dataclass
class SignalEffect:
    before: list[Call]
    after: list[Call]


def _selector(action: dict) -> Value:
    return Value.literal(to_browser_selector(action.get("selector", "")), selectable=False)


def _fixed(text: str) -> Value:
    return Value.literal(text, selectable=False)


def _data(text: object) -> Value:
    return Value.literal("" if text is None else str(text))
```

Every handler now returns `Call(keyword, [values...])`. Selectors use `_selector(action)`,
user data (`url` of navigate, `text` of fill/assertText, `value` of assertValue, select
`options`, upload `files`) use `_data(...)`, everything else (`"value"` strategy, operators
`==`/`contains`, `checked`/`unchecked`, `visible`, mouse button, modifier names,
`clickCount=N`, `Press Keys` key chord) uses `_fixed(...)`. Remove `_map_open_page` and its
`_HANDLERS` entry. `map` keeps its shape:

```python
    def map(self, action: dict) -> Call | None:
        handler = self._HANDLERS.get(action.get("name"))
        return None if handler is None else handler(self, action)

    def map_signal(
        self, signal: dict, unique: Callable[[str], str]
    ) -> SignalEffect | None:
        """The Keyword Calls a signal adds around the Action that raised it.

        Playwright reports dialogs, downloads and popups *after* the Action, but
        Browser needs dialog handling and the download promise *before* it.
        """
        name = signal.get("name")
        if name == "popup":
            return SignalEffect([], [Call("Switch Page", [_fixed("NEW")])])
        if name == "dialog":
            return SignalEffect(
                [Call("Handle Future Dialogs", [_fixed("action=accept")])], []
            )
        if name == "download":
            variable = unique("download")
            return SignalEffect(
                [Call("Promise To Wait For Download", [], assign=variable)],
                [Call("Wait For", [Value([ArgRef(variable)], selectable=False)])],
            )
        return None
```

Update the `_HANDLERS` type to `dict[str, Callable[[ActionMapper, dict], Call]]`.
`session.py` still uses tuples: adapt its `handle_event` minimally to `call.keyword` /
`[v.render() for v in call.args]` so the old session tests keep passing until Task 7 replaces
it (the writer re-escapes rendered cells, so pass `v.text or ""` instead of `v.render()`).

- [ ] **Step 4: Run tests**

Run: `pytest utest/test_recorder_mapper.py utest/test_recorder_session.py utest/test_recorder_driver.py -q --no-cov`
Expected: PASS.

- [ ] **Step 5: Lint and commit**

```bash
inv lint-python --fix
git add Browser/recorder/action_mapper.py Browser/recorder/session.py utest/test_recorder_mapper.py utest/test_recorder_plugin.py
git commit -m "feat(recorder): map Actions to Calls, popups to Switch Page, wrap dialogs and downloads"
```

---

### Task 6: `target.py` — file target with re-read and block ownership, log target

Replaces `keyword_writer.py`.

**Files:**
- Create: `Browser/recorder/target.py`
- Delete: `Browser/recorder/keyword_writer.py` (in Task 7, once the session no longer imports it)
- Test: `utest/test_recorder_target.py` (new; port the useful writer tests from `utest/test_recorder_plugin.py`, delete all `test_writer_*` there)

**Interfaces:**
- Consumes: `model.RecordedKeyword`, `names.normalize_keyword_name`, `names.existing_keyword_names`
- Produces:
  - `Target` (typing `Protocol`): `label: str`, `existing_names() -> set[str]`, `save(keyword: RecordedKeyword) -> str | None` (returns a toolbar notice), `remove(name: str) -> None`, `finish(keyword: RecordedKeyword) -> None`
  - `FileTarget(path: Path)`
  - `LogTarget(console: Callable[[str], None] = logger.console, info: Callable[[str], None] = logger.info)`

- [ ] **Step 1: Write the failing tests**

```python
from __future__ import annotations

import subprocess
import sys

from Browser.recorder.model import Call, RecordedKeyword, Value
from Browser.recorder.target import FileTarget, LogTarget

ORIGINAL = (
    "*** Settings ***\nLibrary    Browser\n\n"
    "*** Keywords ***\nExisting\n    Log    hi\n"
)


def keyword(name: str = "Fill Name", *texts: str) -> RecordedKeyword:
    kw = RecordedKeyword(name)
    for text in texts or ("Alice",):
        kw.add(Call("Fill Text", [Value.literal("#n", False), Value.literal(text)]))
    return kw


def test_save_creates_file_and_section(tmp_path):
    path = tmp_path / "new.resource"
    FileTarget(path).save(keyword())
    assert path.read_text() == (
        "*** Keywords ***\nFill Name\n    [Tags]    recorded\n    Fill Text    \\#n    Alice\n"
    )


def test_save_appends_after_existing_content(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    FileTarget(path).save(keyword())
    assert path.read_text() == ORIGINAL + (
        "\nFill Name\n    [Tags]    recorded\n    Fill Text    \\#n    Alice\n"
    )


def test_external_edit_outside_the_block_is_kept(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    target = FileTarget(path)
    kw = keyword()
    target.save(kw)
    path.write_text(path.read_text().replace("Log    hi", "Log    changed"))
    kw.add(Call("Click", [Value.literal("#b", False)]))
    assert target.save(kw) is None
    text = path.read_text()
    assert "Log    changed" in text
    assert text.endswith("    Click    \\#b\n")


def test_external_edit_inside_the_block_is_overwritten_with_notice(tmp_path):
    path = tmp_path / "k.resource"
    target = FileTarget(path)
    kw = keyword()
    target.save(kw)
    path.write_text(path.read_text().replace("Alice", "Bob"))
    notice = target.save(kw)
    assert "changed outside the recorder" in notice
    assert "Alice" in path.read_text()


def test_deleted_block_is_written_again_with_notice(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    target = FileTarget(path)
    kw = keyword()
    target.save(kw)
    path.write_text(ORIGINAL)
    assert "written again" in target.save(kw)
    assert "Fill Name" in path.read_text()


def test_remove_restores_the_file_byte_for_byte(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    target = FileTarget(path)
    target.save(keyword())
    target.remove("Fill Name")
    assert path.read_text() == ORIGINAL


def test_remove_drops_a_section_it_created(tmp_path):
    path = tmp_path / "k.robot"
    original = "*** Settings ***\nLibrary    Browser\n"
    path.write_text(original)
    target = FileTarget(path)
    target.save(keyword())
    target.remove("Fill Name")
    assert path.read_text() == original


def test_remove_never_deletes_the_file(tmp_path):
    path = tmp_path / "new.resource"
    target = FileTarget(path)
    target.save(keyword())
    target.remove("Fill Name")
    assert path.exists()


def test_remove_of_an_unsaved_keyword_is_a_no_op(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    FileTarget(path).remove("Never Saved")
    assert path.read_text() == ORIGINAL


def test_saving_an_empty_keyword_removes_its_block(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    target = FileTarget(path)
    kw = keyword()
    target.save(kw)
    kw.undo()
    target.save(kw)
    assert path.read_text() == ORIGINAL


def test_formatting_of_existing_content_is_preserved(tmp_path):
    path = tmp_path / "k.resource"
    odd = "*** Keywords ***\nExisting\n  Log  two  spaces    # comment\n"
    path.write_text(odd)
    FileTarget(path).save(keyword())
    assert path.read_text().startswith(odd)


def test_two_keywords_are_separated_by_one_blank_line(tmp_path):
    path = tmp_path / "k.resource"
    target = FileTarget(path)
    target.finish(keyword("One"))
    target.finish(keyword("Two"))
    assert "Alice\n\nTwo\n" in path.read_text()


def test_existing_names(tmp_path):
    path = tmp_path / "k.resource"
    path.write_text(ORIGINAL)
    assert FileTarget(path).existing_names() == {"Existing"}


def test_log_target_writes_block_to_console_and_log():
    seen: list[tuple[str, str]] = []
    target = LogTarget(
        console=lambda t: seen.append(("console", t)),
        info=lambda t: seen.append(("info", t)),
    )
    kw = keyword()
    assert target.save(kw) is None
    target.finish(kw)
    assert seen == [("console", kw.text()), ("info", kw.text())]
    assert target.existing_names() == set()


def test_written_keyword_runs_in_a_real_robot_run(tmp_path):
    """Escaped values come back as the exact recorded strings."""
    path = tmp_path / "k.resource"
    kw = RecordedKeyword("Echo")
    tricky = "#a  b ${x} \u00a0\n"
    kw.add(Call("Should Be Equal", [Value.literal(tricky), Value.literal(tricky)]))
    FileTarget(path).finish(kw)
    suite = tmp_path / "s.robot"
    suite.write_text(f"*** Settings ***\nResource    {path}\n*** Test Cases ***\nT\n    Echo\n")
    result = subprocess.run(
        [sys.executable, "-m", "robot", "--outputdir", str(tmp_path), str(suite)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest utest/test_recorder_target.py -q --no-cov`
Expected: FAIL with `ModuleNotFoundError: No module named 'Browser.recorder.target'`.

- [ ] **Step 3: Implement `target.py`**

```python
# (license header)
"""Where a recorded keyword goes: a `.robot`/`.resource` file, or the log.

`FileTarget` re-reads the file before every save and owns only the block of the
keyword it is recording (AC-35, AC-36): everything outside that block is
whatever is on disk at that moment, so edits made in an IDE meanwhile survive.
"""

from __future__ import annotations

import io
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from robot.api import get_model, logger
from robot.api.parsing import EmptyLine, SectionHeader, Token
from robot.parsing.model.blocks import Block, File, Keyword, KeywordSection
from robot.parsing.model.statements import Statement

from .model import RecordedKeyword
from .names import existing_keyword_names, normalize_keyword_name

_EOL = "\n"


class Target(Protocol):
    label: str

    def existing_names(self) -> set[str]: ...

    def save(self, keyword: RecordedKeyword) -> str | None: ...

    def remove(self, name: str) -> None: ...

    def finish(self, keyword: RecordedKeyword) -> None: ...


class LogTarget:
    """`file=${None}`: nothing is written; finished keywords go to console and log."""

    label = "the log"

    def __init__(
        self,
        console: Callable[[str], None] = logger.console,
        info: Callable[[str], None] = logger.info,
    ) -> None:
        self._console = console
        self._info = info

    def existing_names(self) -> set[str]:
        return set()

    def save(self, keyword: RecordedKeyword) -> str | None:
        return None

    def remove(self, name: str) -> None:
        return None

    def finish(self, keyword: RecordedKeyword) -> None:
        text = keyword.text()
        self._console(text)
        self._info(text)


@dataclass
class _Owned:
    signature: tuple
    created_section: bool
    separated: bool


class FileTarget:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.label = self.path.name
        self._owned: dict[str, _Owned] = {}

    def existing_names(self) -> set[str]:
        return existing_keyword_names(self.path)

    def save(self, keyword: RecordedKeyword) -> str | None:
        key = normalize_keyword_name(keyword.name)
        if len(keyword) == 0:
            self.remove(keyword.name)
            return None
        owned = self._owned.get(key)
        model = self._read()
        block = _parse_block(keyword.block())
        notice = None
        found = _find(model, keyword.name)
        if found is not None:
            body, index = found
            old = body[index]
            if owned is not None and _signature(old) != owned.signature:
                notice = (
                    f"'{keyword.name}' was changed outside the recorder and has "
                    "been rewritten."
                )
            block.body.extend(_trailing_empty_lines(old))
            body[index] = block
        else:
            if owned is not None:
                notice = (
                    f"'{keyword.name}' was removed outside the recorder and has "
                    "been written again."
                )
            section, created = self._keyword_section(model)
            separated = bool(section.body) and _ensure_blank_line(section.body)
            section.body.append(block)
            owned = _Owned(
                (),
                created or (owned.created_section if owned else False),
                separated,
            )
        owned.signature = _signature(block)
        self._owned[key] = owned
        model.save(str(self.path))
        return notice

    def finish(self, keyword: RecordedKeyword) -> None:
        self.save(keyword)
        self._owned.pop(normalize_keyword_name(keyword.name), None)

    def remove(self, name: str) -> None:
        owned = self._owned.pop(normalize_keyword_name(name), None)
        if owned is None or not self.path.exists():
            return
        model = self._read()
        found = _find(model, name)
        if found is None:
            return
        body, index = found
        del body[index]
        if owned.separated and index > 0:
            _pop_trailing_empty_line(body[index - 1])
        if owned.created_section:
            for position, section in enumerate(model.sections):
                if section.body is body and not any(
                    isinstance(item, Keyword) for item in body
                ):
                    del model.sections[position]
                    if position > 0:
                        _pop_trailing_empty_line(model.sections[position - 1])
                    break
        model.save(str(self.path))

    # -- helpers ----------------------------------------------------------- #

    def _read(self) -> File:
        if self.path.exists():
            return get_model(str(self.path))
        return File(source=str(self.path))

    @staticmethod
    def _keyword_section(model: File) -> tuple[KeywordSection, bool]:
        for section in model.sections:
            if isinstance(section, KeywordSection):
                return section, False
        if model.sections:
            _ensure_blank_line(model.sections[-1].body)
        header = SectionHeader(
            [Token(Token.KEYWORD_HEADER, "*** Keywords ***"), Token(Token.EOL, _EOL)]
        )
        section = KeywordSection(header=header)
        model.sections.append(section)
        return section, True


def _parse_block(text: str) -> Keyword:
    model = get_model(io.StringIO("*** Keywords ***\n" + text))
    return model.sections[0].body[0]


def _find(model: File, name: str) -> tuple[list, int] | None:
    wanted = normalize_keyword_name(name)
    for section in model.sections:
        if not isinstance(section, KeywordSection):
            continue
        for index, item in enumerate(section.body):
            if (
                isinstance(item, Keyword)
                and item.name
                and normalize_keyword_name(item.name) == wanted
            ):
                return section.body, index
    return None


def _statements(node: Block | Statement) -> Iterator[Statement]:
    if isinstance(node, Statement):
        yield node
        return
    for field in node._fields:
        value = getattr(node, field, None)
        items = value if isinstance(value, list) else [value]
        for item in items:
            if isinstance(item, (Block, Statement)):
                yield from _statements(item)


def _signature(block: Keyword) -> tuple:
    """The block's content, ignoring blank lines, separators and line ends."""
    return tuple(
        tuple(
            token.value
            for token in statement.tokens
            if token.type not in (Token.SEPARATOR, Token.EOL)
        )
        for statement in _statements(block)
        if not isinstance(statement, EmptyLine)
    )


def _trailing_empty_lines(block: Keyword) -> list[EmptyLine]:
    trailing: list[EmptyLine] = []
    for item in reversed(block.body):
        if not isinstance(item, EmptyLine):
            break
        trailing.insert(0, item)
    return trailing


def _ends_with_empty_line(body: list) -> bool:
    if not body:
        return False
    last = body[-1]
    if isinstance(last, EmptyLine):
        return True
    return isinstance(last, Block) and _ends_with_empty_line(getattr(last, "body", []))


def _ensure_blank_line(body: list) -> bool:
    """Append a blank line unless ``body`` already ends with one. True if added."""
    if _ends_with_empty_line(body):
        return False
    body.append(EmptyLine([Token(Token.EOL, _EOL)]))
    return True


def _pop_trailing_empty_line(node: Block) -> None:
    body = getattr(node, "body", None)
    if not body:
        return
    last = body[-1]
    if isinstance(last, EmptyLine):
        body.pop()
    elif isinstance(last, Block):
        _pop_trailing_empty_line(last)
```

- [ ] **Step 4: Run tests**

Run: `pytest utest/test_recorder_target.py -q --no-cov`
Expected: PASS. If `test_remove_restores_the_file_byte_for_byte` fails, compare
`repr()` of both texts: the separator logic must remove exactly the blank line it added.

- [ ] **Step 5: Lint and commit**

```bash
inv lint-python --fix
git add Browser/recorder/target.py utest/test_recorder_target.py utest/test_recorder_plugin.py
git commit -m "feat(recorder): add FileTarget with re-read and block ownership, and LogTarget"
```

---

### Task 7: Rewrite `RecorderSession`

**Files:**
- Modify (rewrite): `Browser/recorder/session.py`
- Delete: `Browser/recorder/keyword_writer.py`
- Test (rewrite): `utest/test_recorder_session.py`

**Interfaces:**
- Consumes: `ActionMapper`, `SILENT_ACTIONS`, `RecordedKeyword`, `Target`, `NameGuard`, `KnownKeywords`
- Produces:
  - `RecorderSession(target: Target, fixed_name: str | None = None, known: KnownKeywords | None = None, clock: Callable[[], float] = time.monotonic)`
  - `.handle_event(event: str, action: dict) -> None` with `event` in `{"added", "updated", "signal"}`
  - `.handle_command(command: dict) -> None` with `cmd` in `{"new", "finish", "undo", "discard", "stop", "argument", "replace", "default"}`
  - `.tick() -> None` — runs a deferred command once its settle time is over
  - `.toolbar_state() -> dict` (contract below)
  - `.close() -> list[str]`, `.keywords -> list[str]`, `.text() -> str`, `.stopped: bool`, `.log: list[str]`, `.state -> str`
  - `SETTLE_SECONDS = 0.6`

Toolbar state contract (Python → toolbar), also documented in `Browser/recorder/README.md`:

```json
{
  "state": "idle | recording",
  "name": "Fill Name | null",
  "fixedName": false,
  "target": "k.resource | the log",
  "keywords": ["names finished so far"],
  "calls": [{"text": "Fill Text    #n    Alice",
             "keyword": "Fill Text",
             "values": [{"text": "#n", "selectable": false},
                        {"text": "Alice", "selectable": true}]}],
  "arguments": [{"name": "email", "default": "a@b", "useDefault": true}],
  "offer": {"argument": "email", "text": "a@b", "occurrences": [[1, 1]]},
  "pending": "finish | discard | stop | null",
  "notice": "string | null",
  "error": "string | null"
}
```

`values[].text` is the *rendered* cell (`Value.render()`), so arguments show as `${email}`.

Command contract (toolbar → Python):

```json
{"cmd": "new", "name": "Fill Name"}
{"cmd": "finish"} {"cmd": "undo"} {"cmd": "discard"} {"cmd": "stop"}
{"cmd": "argument", "call": 0, "value": 1, "start": 0, "end": 5, "name": "email"}
{"cmd": "replace", "argument": "email", "occurrences": [[1, 1]]}
{"cmd": "default", "argument": "email", "use": false}
```

- [ ] **Step 1: Write the failing tests**

Rewrite `utest/test_recorder_session.py`:

```python
from __future__ import annotations

import pytest

from Browser.recorder.model import RecordedKeyword
from Browser.recorder.names import KnownKeywords
from Browser.recorder.session import SETTLE_SECONDS, RecorderSession


class FakeTarget:
    label = "fake.resource"

    def __init__(self, existing=(), fail=False):
        self.saved: list[str] = []
        self.finished: list[str] = []
        self.removed: list[str] = []
        self._existing = set(existing)
        self.fail = fail

    def existing_names(self):
        return set(self._existing)

    def save(self, keyword: RecordedKeyword):
        if self.fail:
            raise OSError("read-only")
        self.saved.append(keyword.block())
        return None

    def remove(self, name):
        self.removed.append(name)

    def finish(self, keyword):
        self.finished.append(keyword.block())


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


FILL = {"name": "fill", "selector": "#n", "text": "Alice"}
CLICK = {"name": "click", "selector": "#b", "button": "left", "clickCount": 1, "modifiers": 0}


def session(**kwargs):
    clock = kwargs.pop("clock", Clock())
    target = kwargs.pop("target", FakeTarget())
    return RecorderSession(target, clock=clock, **kwargs), target, clock


def settle(s, clock):
    clock.now += SETTLE_SECONDS
    s.tick()


def test_idle_actions_are_not_recorded():
    s, target, _ = session()
    s.handle_event("added", FILL)
    assert target.saved == []
    assert s.toolbar_state()["calls"] == []


def test_new_record_finish():
    s, target, clock = session()
    s.handle_command({"cmd": "new", "name": "Fill Name"})
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "finish"})
    assert s.toolbar_state()["pending"] == "finish"
    assert target.finished == []
    settle(s, clock)
    assert s.keywords == ["Fill Name"]
    assert "Fill Text" in target.finished[0]
    assert s.state == "idle"


def test_click_arriving_after_finish_lands_in_the_finished_keyword():
    s, target, clock = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_command({"cmd": "finish"})
    clock.now += 0.4
    s.handle_event("added", CLICK)
    settle(s, clock)
    assert "Click" in target.finished[0]


def test_commands_are_rejected_while_finishing():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "finish"})
    s.handle_command({"cmd": "undo"})
    assert "finishing" in s.toolbar_state()["error"].lower()
    assert len(s.toolbar_state()["calls"]) == 1


def test_stop_overrides_a_pending_finish():
    s, _, clock = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "finish"})
    s.handle_command({"cmd": "stop"})
    settle(s, clock)
    assert s.stopped


def test_finish_of_an_empty_keyword_saves_nothing():
    s, target, clock = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_command({"cmd": "finish"})
    settle(s, clock)
    assert target.finished == [] and s.keywords == []


def test_undo_ignores_later_updates_of_the_undone_action():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "undo"})
    s.handle_event("updated", {**FILL, "text": "Alicia"})
    assert s.toolbar_state()["calls"] == []


def test_update_after_a_skipped_action_appends():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", CLICK)
    s.handle_event("added", {"name": "assertSnapshot", "selector": "#x"})
    s.handle_event("updated", FILL)
    assert [c["keyword"] for c in s.toolbar_state()["calls"]] == ["Click", "Fill Text"]


def test_unsupported_action_shows_a_notice():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", {"name": "assertSnapshot", "selector": "#x"})
    assert "assertSnapshot" in s.toolbar_state()["notice"]


def test_open_page_is_silent():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", {"name": "openPage", "url": "about:blank"})
    assert s.toolbar_state()["notice"] is None
    assert s.toolbar_state()["calls"] == []


def test_dialog_signal_and_undo_as_a_group():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", CLICK)
    s.handle_event("signal", {"name": "dialog"})
    assert [c["keyword"] for c in s.toolbar_state()["calls"]] == [
        "Handle Future Dialogs",
        "Click",
    ]
    s.handle_command({"cmd": "undo"})
    assert s.toolbar_state()["calls"] == []


def test_discard_removes_and_returns_to_idle():
    s, target, clock = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "discard"})
    settle(s, clock)
    assert target.removed == ["K"] and s.state == "idle"


def test_fixed_name_discard_restarts_the_same_keyword():
    s, _, clock = session(fixed_name="K")
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "discard"})
    settle(s, clock)
    assert s.state == "recording" and s.toolbar_state()["name"] == "K"


def test_fixed_name_rejects_new_and_finish():
    s, _, _ = session(fixed_name="K")
    s.handle_command({"cmd": "new", "name": "Other"})
    assert s.toolbar_state()["error"]
    s.handle_command({"cmd": "finish"})
    assert s.toolbar_state()["error"]


def test_fixed_name_existing_in_target_raises():
    with pytest.raises(ValueError, match="already exists"):
        session(fixed_name="Existing", target=FakeTarget(existing={"Existing"}))


def test_new_rejects_shadowing_names():
    s, _, _ = session(known=KnownKeywords(names=frozenset({"Click"})))
    s.handle_command({"cmd": "new", "name": "click"})
    assert "shadowed" in s.toolbar_state()["error"]
    assert s.state == "idle"


def test_new_rejects_a_name_recorded_earlier_in_the_session():
    s, _, clock = session()
    for _ in range(2):
        s.handle_command({"cmd": "new", "name": "K"})
        s.handle_event("added", FILL)
        s.handle_command({"cmd": "finish"})
        settle(s, clock)
    assert s.keywords == ["K"]


def test_close_saves_a_running_keyword():
    s, target, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", FILL)
    assert s.close() == ["K"]
    assert target.finished


def test_text_of_all_finished_keywords():
    s, _, clock = session()
    for name in ("A", "B"):
        s.handle_command({"cmd": "new", "name": name})
        s.handle_event("added", FILL)
        s.handle_command({"cmd": "finish"})
        settle(s, clock)
    assert s.text().count("*** Keywords ***") == 1
    assert "\nA\n" in s.text() and "\nB\n" in s.text()


def test_argument_offer_and_replace():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", FILL)
    s.handle_event("added", {"name": "fill", "selector": "#m", "text": "Alice"})
    s.handle_command({"cmd": "argument", "call": 0, "value": 1, "start": 0, "end": 5, "name": "who"})
    assert s.toolbar_state()["offer"] == {"argument": "who", "text": "Alice", "occurrences": [[1, 1]]}
    s.handle_command({"cmd": "replace", "argument": "who", "occurrences": [[1, 1]]})
    state = s.toolbar_state()
    assert state["offer"] is None
    assert [c["values"][1]["text"] for c in state["calls"]] == ["${who}", "${who}"]


def test_default_toggle():
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", FILL)
    s.handle_command({"cmd": "argument", "call": 0, "value": 1, "start": 0, "end": 5, "name": "who"})
    s.handle_command({"cmd": "default", "argument": "who", "use": False})
    assert s.toolbar_state()["arguments"] == [{"name": "who", "default": "Alice", "useDefault": False}]


@pytest.mark.parametrize(
    "command",
    [
        {"cmd": "argument", "call": "x", "value": 1, "start": 0, "end": 1, "name": "a"},
        {"cmd": "argument", "call": 0, "value": 1, "start": 0, "end": 1, "name": "${a}"},
        {"cmd": "argument", "call": 0, "value": 0, "start": 0, "end": 1, "name": "a"},
        {"cmd": "replace", "argument": "nope", "occurrences": [[0, 1]]},
        {"cmd": "replace", "argument": "a", "occurrences": "bad"},
        {"cmd": "default", "argument": "nope", "use": True},
    ],
)
def test_bad_argument_commands_become_toolbar_errors(command):
    s, _, _ = session()
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", FILL)
    s.handle_command(command)
    assert s.toolbar_state()["error"]


def test_save_failure_is_reported_and_recording_continues():
    s, target, _ = session(target=FakeTarget(fail=True))
    s.handle_command({"cmd": "new", "name": "K"})
    s.handle_event("added", FILL)
    assert "read-only" in s.toolbar_state()["error"]
    target.fail = False
    s.handle_event("added", CLICK)
    assert len(s.toolbar_state()["calls"]) == 2
    assert s.toolbar_state()["error"] is None


def test_unknown_command_is_logged():
    s, _, _ = session()
    s.handle_command({"cmd": "explode"})
    assert any("explode" in entry for entry in s.log)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest utest/test_recorder_session.py -q --no-cov`
Expected: FAIL (`ImportError: cannot import name 'SETTLE_SECONDS'`).

- [ ] **Step 3: Implement `session.py`**

```python
# (license header)
"""The Recording Session state machine.

It applies recorder events and toolbar commands to a `RecordedKeyword` and tells
its `Target` to save. It has no I/O of its own beyond the target, and its clock
is injected, so the whole interaction model is unit-testable in milliseconds.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from .action_mapper import SILENT_ACTIONS, ActionMapper
from .model import RecordedKeyword
from .names import KnownKeywords, NameGuard
from .target import Target

IDLE = "idle"
RECORDING = "recording"

#: Playwright holds a left click back for 500 ms before reporting it (ADR 0011).
#: Finish, Discard and Stop wait this long so such a click still lands in the
#: keyword it was made in (AC-19).
SETTLE_SECONDS = 0.6
_DEFERRED = ("finish", "discard", "stop")


class RecorderSession:
    def __init__(
        self,
        target: Target,
        fixed_name: str | None = None,
        known: KnownKeywords | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.target = target
        self.stopped = False
        self.log: list[str] = []
        self._guard = NameGuard(known or KnownKeywords())
        self._mapper = ActionMapper()
        self._clock = clock
        self._fixed_name = fixed_name
        self._finished: list[RecordedKeyword] = []
        self._keyword: RecordedKeyword | None = None
        self._pending: tuple[str, float] | None = None
        self._error: str | None = None
        self._notice: str | None = None
        self._offer: dict | None = None
        self._undone = False
        self._skipped = False
        if fixed_name is not None:
            error = self._guard.error(fixed_name, taken=target.existing_names())
            if error:
                raise ValueError(error)
            self._keyword = RecordedKeyword(fixed_name)

    # -- introspection ----------------------------------------------------- #

    @property
    def state(self) -> str:
        return RECORDING if self._keyword is not None else IDLE

    @property
    def keywords(self) -> list[str]:
        return [keyword.name for keyword in self._finished]

    def text(self) -> str:
        if not self._finished:
            return ""
        return "*** Keywords ***\n" + "\n".join(k.block() for k in self._finished)

    def toolbar_state(self) -> dict:
        keyword = self._keyword
        return {
            "state": self.state,
            "name": keyword.name if keyword else None,
            "fixedName": self._fixed_name is not None,
            "target": self.target.label,
            "keywords": self.keywords,
            "calls": [
                {
                    "text": call.render(),
                    "keyword": call.keyword,
                    "values": [
                        {"text": value.render(), "selectable": value.selectable}
                        for value in call.args
                    ],
                }
                for call in (keyword.calls() if keyword else [])
            ],
            "arguments": [
                {"name": a.name, "default": a.default, "useDefault": a.use_default}
                for a in (keyword.arguments if keyword else [])
            ],
            "offer": self._offer,
            "pending": self._pending[0] if self._pending else None,
            "notice": self._notice,
            "error": self._error,
        }

    # -- events ------------------------------------------------------------ #

    def handle_event(self, event: str, action: dict) -> None:
        keyword = self._keyword
        if keyword is None:
            return
        if event == "signal":
            effect = self._mapper.map_signal(action, keyword.unique_variable)
            if effect and not self._undone and not self._skipped:
                if keyword.attach(effect.before, effect.after):
                    self._save()
            return
        call = self._mapper.map(action)
        if call is None:
            name = action.get("name")
            if name not in SILENT_ACTIONS:
                self._notice = f"'{name}' has no Browser keyword and was not recorded."
                self.log.append(f"action {name!r} has no Browser keyword equivalent")
                self._skipped = True
            return
        if event == "updated":
            if self._undone:
                return
            if not self._skipped and keyword.update_last(call):
                self._save()
                return
        keyword.add(call)
        self._undone = False
        self._skipped = False
        self._save()

    # -- commands ---------------------------------------------------------- #

    def handle_command(self, command: dict) -> None:
        self._error = None
        self._notice = None
        cmd = str(command.get("cmd", ""))
        if self._pending is not None and cmd != "stop":
            self._error = "Still finishing the last command - please wait."
            return
        if cmd in _DEFERRED:
            self._defer(cmd)
        elif cmd == "new":
            self._new(str(command.get("name", "")))
        elif cmd == "undo":
            self._undo()
        elif cmd in ("argument", "replace", "default"):
            self._argument_command(cmd, command)
        else:
            self.log.append(f"unknown recorder command {cmd!r}")

    def tick(self) -> None:
        if self._pending is None or self._clock() < self._pending[1]:
            return
        cmd = self._pending[0]
        self._pending = None
        if cmd == "finish":
            self._finish()
        elif cmd == "discard":
            self._discard()
        else:
            self.stopped = True

    def close(self) -> list[str]:
        """End the session now; a running Keyword Recording is saved (AC-18)."""
        self._pending = None
        if self._keyword is not None:
            if len(self._keyword):
                self._finish()
            else:
                self._keyword = None
        return self.keywords

    # -- command handlers -------------------------------------------------- #

    def _defer(self, cmd: str) -> None:
        if cmd != "stop":
            if self._keyword is None:
                self._error = "No keyword is being recorded."
                return
            if cmd == "finish" and self._fixed_name is not None:
                self._error = "Use Stop to end this recording."
                return
        self._pending = (cmd, self._clock() + SETTLE_SECONDS)

    def _new(self, name: str) -> None:
        if self._fixed_name is not None:
            self._error = f"This recording writes only '{self._fixed_name}'."
            return
        if self._keyword is not None:
            self._error = f"Still recording '{self._keyword.name}'. Finish it first."
            return
        taken = [*self.keywords, *self.target.existing_names()]
        error = self._guard.error(name, taken=taken)
        if error:
            self._error = error
            return
        self._keyword = RecordedKeyword(name)
        self._undone = self._skipped = False

    def _finish(self) -> None:
        keyword = self._keyword
        assert keyword is not None
        self._keyword = None
        self._offer = None
        if not len(keyword):
            self.log.append(f"'{keyword.name}' had no Keyword Calls and was discarded")
            self.target.remove(keyword.name)
            return
        try:
            self.target.finish(keyword)
        except OSError as error:
            self._error = f"Could not write {self.target.label}: {error}"
        self._finished.append(keyword)
        self.log.append(f"finished '{keyword.name}' with {len(keyword)} Keyword Calls")

    def _undo(self) -> None:
        if self._keyword is None:
            self._error = "No keyword is being recorded."
            return
        if self._keyword.undo():
            self._undone = True
            self._offer = None
            self._save()

    def _discard(self) -> None:
        keyword = self._keyword
        assert keyword is not None
        self.target.remove(keyword.name)
        self.log.append(f"discarded '{keyword.name}'")
        self._keyword = (
            RecordedKeyword(self._fixed_name) if self._fixed_name is not None else None
        )
        self._offer = None
        self._undone = self._skipped = False

    def _argument_command(self, cmd: str, command: dict) -> None:
        keyword = self._keyword
        if keyword is None:
            self._error = "No keyword is being recorded."
            return
        try:
            if cmd == "argument":
                name = command.get("name")
                occurrences = keyword.make_argument(
                    _int(command, "call"),
                    _int(command, "value"),
                    _int(command, "start"),
                    _int(command, "end"),
                    name if isinstance(name, str) else "",
                )
                self._offer = (
                    {
                        "argument": name,
                        "text": keyword.argument(name).default,
                        "occurrences": [list(o) for o in occurrences],
                    }
                    if occurrences
                    else None
                )
            elif cmd == "replace":
                keyword.replace(
                    str(command.get("argument")), _pairs(command.get("occurrences"))
                )
                self._offer = None
            else:
                keyword.set_default(
                    str(command.get("argument")), bool(command.get("use"))
                )
        except ValueError as error:
            self._error = str(error)
            return
        self._save()

    def _save(self) -> None:
        if self._keyword is None:
            return
        try:
            notice = self.target.save(self._keyword)
        except OSError as error:
            self._error = f"{_WRITE_FAILED} {self.target.label}: {error}"
            return
        if self._error and self._error.startswith(_WRITE_FAILED):
            # The file is writable again; the keyword in memory was never lost.
            self._error = None
        if notice:
            self._notice = notice


def _int(command: dict, key: str) -> int:
    value = command.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"'{key}' must be a number.")
    return value


def _pairs(value: object) -> list[tuple[int, int]]:
    if not isinstance(value, list):
        raise ValueError("'occurrences' must be a list.")
    pairs = []
    for item in value:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not all(isinstance(i, int) and not isinstance(i, bool) for i in item)
        ):
            raise ValueError("Each occurrence must be [call, value].")
        pairs.append((item[0], item[1]))
    return pairs
```

Define `_WRITE_FAILED = "Could not write"` next to `SETTLE_SECONDS`, and use it in
`_finish` too (`f"{_WRITE_FAILED} {self.target.label}: {error}"`).

- [ ] **Step 4: Delete the old writer and fix the plugin**

```bash
git rm Browser/recorder/keyword_writer.py
```

In `Browser/recorder/plugin.py::_run_session`: build `FileTarget(target)` and pass it as the
session's first argument; call `session.tick()` after applying commands. (The plugin is
deleted in Task 11; this only keeps it importable.)

- [ ] **Step 5: Run tests**

Run: `pytest utest/test_recorder_session.py utest/test_recorder_target.py utest/test_recorder_model.py -q --no-cov`
Expected: PASS. `utest/test_recorder_driver.py` may fail now; it is rewritten in Task 8.

- [ ] **Step 6: Lint and commit**

```bash
inv lint-python --fix
git add -A Browser/recorder utest/test_recorder_session.py
git commit -m "feat(recorder): rewrite the session on the model, with deferred finish and arguments"
```

---

### Task 8: `driver.py` — the poll loop

**Files:**
- Create: `Browser/recorder/driver.py`
- Test (rewrite): `utest/test_recorder_driver.py`

**Interfaces:**
- Consumes: `RecorderSession`
- Produces:
  - `RecorderClient` (Protocol): `poll(state: dict, reset: bool) -> dict`, `stop() -> None`
  - `run_session(session: RecorderSession, client: RecorderClient, idle_timeout: float | None = None, clock: Callable[[], float] = time.monotonic, sleep: Callable[[float], None] = time.sleep) -> str` returning one of `"stop"`, `"playwright"`, `"pages"`, `"idle"`
  - `POLL_INTERVAL = 0.2`
  - Poll reply shape: `{"mode": "recording" | "stopped", "pages": int, "events": [{"event": str, "action": dict}], "commands": [dict]}`

- [ ] **Step 1: Write the failing tests**

```python
from __future__ import annotations

import pytest

from Browser.recorder.driver import run_session
from Browser.recorder.session import RecorderSession

from .test_recorder_session import FILL, Clock, FakeTarget


class Client:
    def __init__(self, replies, clock=None, step=0.2):
        self.replies = list(replies)
        self.polls: list[tuple[dict, bool]] = []
        self.stopped = False
        self.clock = clock
        self.step = step

    def poll(self, state, reset):
        self.polls.append((state, reset))
        if self.clock is not None:
            self.clock.now += self.step
        if self.replies:
            return self.replies.pop(0)
        return {"mode": "recording", "pages": 1, "events": [], "commands": []}

    def stop(self):
        self.stopped = True


def reply(events=(), commands=(), mode="recording", pages=1):
    return {"mode": mode, "pages": pages, "events": list(events), "commands": list(commands)}


def make(clock=None, **kwargs):
    clock = clock or Clock()
    return RecorderSession(FakeTarget(), clock=clock, **kwargs), clock


def test_first_poll_resets_later_ones_do_not():
    s, clock = make()
    client = Client([reply(commands=[{"cmd": "stop"}])], clock)
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "stop"
    assert [reset for _, reset in client.polls][:2] == [True, False]
    assert client.stopped


def test_playwright_stop_drains_once_more_then_ends():
    s, clock = make()
    client = Client(
        [
            reply(commands=[{"cmd": "new", "name": "K"}]),
            reply(mode="stopped"),
            reply(events=[{"event": "added", "action": FILL}]),
        ],
        clock,
    )
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "playwright"
    assert s.keywords == ["K"]


def test_all_pages_closed_ends_the_session():
    s, clock = make()
    client = Client([reply(pages=0)], clock)
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "pages"


def test_idle_timeout_is_reset_by_activity():
    s, clock = make()
    activity = [reply(commands=[{"cmd": "new", "name": "K"}])] + [
        reply(events=[{"event": "added", "action": FILL}]) for _ in range(10)
    ]
    client = Client(activity, clock, step=0.2)
    reason = run_session(s, client, idle_timeout=1.0, clock=clock, sleep=lambda _: None)
    assert reason == "idle"
    assert len(client.polls) >= 11 + 5


def test_idle_timeout_also_counts_idle_actions():
    s, clock = make()
    client = Client([reply(events=[{"event": "added", "action": FILL}])] * 8, clock, step=0.2)
    run_session(s, client, idle_timeout=1.0, clock=clock, sleep=lambda _: None)
    assert len(client.polls) >= 8 + 5


def test_exception_still_saves_and_stops():
    s, clock = make()

    class Boom(Client):
        def poll(self, state, reset):
            if len(self.polls) == 2:
                raise RuntimeError("grpc down")
            return super().poll(state, reset)

    client = Boom(
        [reply(commands=[{"cmd": "new", "name": "K"}]), reply(events=[{"event": "added", "action": FILL}])],
        clock,
    )
    with pytest.raises(RuntimeError, match="grpc down"):
        run_session(s, client, clock=clock, sleep=lambda _: None)
    assert s.keywords == ["K"]
    assert client.stopped


def test_malformed_events_and_commands_are_ignored():
    s, clock = make()
    client = Client(
        [
            reply(events=[None, {"event": "added", "action": "nope"}], commands=[None, 42]),
            reply(commands=[{"cmd": "stop"}]),
        ],
        clock,
    )
    assert run_session(s, client, clock=clock, sleep=lambda _: None) == "stop"


def test_stop_failure_does_not_mask_the_real_error():
    s, clock = make()

    class Both(Client):
        def poll(self, state, reset):
            raise RuntimeError("real")

        def stop(self):
            raise RuntimeError("cleanup")

    with pytest.raises(RuntimeError, match="real"):
        run_session(s, Both([], clock), clock=clock, sleep=lambda _: None)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest utest/test_recorder_driver.py -q --no-cov`
Expected: FAIL with `ModuleNotFoundError: No module named 'Browser.recorder.driver'`.

- [ ] **Step 3: Implement `driver.py`**

```python
# (license header)
"""The poll loop of a Recording Session.

Python is the only clock: each poll pushes the toolbar state down and drains
Actions, signals and toolbar commands up. That keeps every end condition -
Stop, Playwright's Record button, closed pages, the idle timeout - in one place.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Protocol

from robot.api import logger

from .session import RecorderSession

POLL_INTERVAL = 0.2


class RecorderClient(Protocol):
    def poll(self, state: dict, reset: bool) -> dict: ...

    def stop(self) -> None: ...


def run_session(
    session: RecorderSession,
    client: RecorderClient,
    idle_timeout: float | None = None,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> str:
    """Drive ``session`` until it ends and return why it ended."""
    last_activity = clock()
    reset = True
    try:
        while True:
            reply = client.poll(session.toolbar_state(), reset)
            reset = False
            if _apply(session, reply):
                last_activity = clock()
            session.tick()
            _drain_log(session)
            if session.stopped:
                return "stop"
            if reply.get("mode") == "stopped":
                # Playwright flushes the Action it was holding back when its
                # Record button stops the recording; take it before closing.
                _apply(session, client.poll(session.toolbar_state(), False))
                return "playwright"
            if not reply.get("pages"):
                logger.info("recorder: all pages closed, ending the session")
                return "pages"
            if idle_timeout is not None and clock() - last_activity >= idle_timeout:
                logger.info("recorder: idle timeout reached, ending the session")
                return "idle"
            sleep(POLL_INTERVAL)
    finally:
        # An aborted run must still leave a well-formed keyword behind, and no
        # cleanup failure may replace an exception already propagating.
        names: list[str] = []
        try:
            names = session.close()
        except Exception as error:
            logger.debug(f"recorder: close failed: {error!r}")
        _drain_log(session)
        try:
            client.stop()
        except Exception as error:
            logger.debug(f"recorder: stop failed: {error!r}")
        logger.info(f"Recorded {len(names)} keyword(s): {', '.join(names) or '-'}")


def _apply(session: RecorderSession, reply: dict) -> bool:
    """Apply one poll reply. True if it carried any Action or command."""
    events = reply.get("events") or []
    commands = reply.get("commands") or []
    for entry in events:
        _safely(
            lambda entry=entry: session.handle_event(
                str(entry.get("event", "added")), dict(entry.get("action") or {})
            ),
            f"event {entry!r}",
        )
    for command in commands:
        _safely(lambda command=command: session.handle_command(dict(command)), f"command {command!r}")
    return bool(events or commands)


def _safely(action: Callable[[], None], what: str) -> None:
    """Survive one malformed event or command: the channel is page-callable (ADR 0010)."""
    try:
        action()
    except Exception as error:
        logger.warn(f"recorder: ignoring {what}: {error!r}")


def _drain_log(session: RecorderSession) -> None:
    for entry in session.log:
        logger.info(f"recorder: {entry}")
    session.log.clear()
```

- [ ] **Step 4: Run tests**

Run: `pytest utest/test_recorder_driver.py utest/test_recorder_session.py -q --no-cov`
Expected: PASS. (`utest/__init__.py` exists, so the relative import of `test_recorder_session` works.)

- [ ] **Step 5: Lint and commit**

```bash
inv lint-python --fix
git add Browser/recorder/driver.py utest/test_recorder_driver.py
git commit -m "feat(recorder): add the poll loop with idle timeout and guaranteed cleanup"
```

---

### Task 9: Native Node side — proto, `recorder.ts`, toolbar as a static asset

**Files:**
- Modify: `protobuf/playwright.proto` (before the closing `}` of `service Playwright`, ~line 703)
- Create: `node/playwright-wrapper/recorder.ts`
- Move: `Browser/recorder/toolbar.js` → `node/playwright-wrapper/static/recorder-toolbar.js` (made self-invoking; UI changes come in Task 10)
- Modify: `node/playwright-wrapper/grpc-service.ts`
- Modify: `pyproject.toml` (`"*"` package-data list gets `"recorder-toolbar.js"`)
- Test: `node/playwright-wrapper/__tests__/recorder.test.ts` (ports `$POC:utest/js/recorder.test.js`)

**Interfaces:**
- Produces (gRPC): `rpc RecorderPoll(Request.Json) returns (Response.Json);` body `{"state": <toolbar state>, "reset": bool}`, reply JSON as in Task 8; `rpc RecorderStop(Request.Empty) returns (Response.Empty);`
- Produces (TS): `toAction(payload: unknown): Action | null`, `isToolbarAction(action: Action): boolean`, `drain<T>(list: T[]): T[]`, `toolbarScript(): string`, `recorderPoll(request: pb.Request_Json, state: PlaywrightState): Promise<pb.Response_Json>`, `recorderStop(request: pb.Request_Empty, state: PlaywrightState): Promise<pb.Response_Empty>`, `TOOLBAR_TAG = 'rfb-recorder-toolbar'`
- Produces (page globals): `window.__rfbCommand(command)`, `window.__rfbToolbarRender(state)`, `window.__rfbToolbarRemove()`, `window.__rfbToolbarState` (last rendered state, read-only mirror used by acceptance tests)

- [ ] **Step 1: Write the failing jest test**

`node/playwright-wrapper/__tests__/recorder.test.ts`:

```ts
/// <reference types="jest" />
import { describe, expect, it, jest } from '@jest/globals';

jest.mock('../browser_logger', () => ({ logger: { info: jest.fn(), error: jest.fn() } }));

import { TOOLBAR_TAG, drain, ensureRecorder, isToolbarAction, toAction, toolbarScript } from '../recorder';

describe('toAction', () => {
    it('unwraps the 1.62 ActionInContext shape', () => {
        expect(toAction({ action: { name: 'click', selector: '#a' }, pageGuid: 'p' })).toEqual({ name: 'click', selector: '#a' });
    });
    it('accepts the bare 1.63 Action and drops ariaSnapshot', () => {
        expect(toAction({ name: 'fill', text: 'x', ariaSnapshot: 'big' })).toEqual({ name: 'fill', text: 'x' });
    });
    it('rejects garbage', () => {
        expect(toAction(null)).toBeNull();
        expect(toAction({ action: { selector: '#a' } })).toBeNull();
    });
});

describe('isToolbarAction', () => {
    it('matches actions on the toolbar host', () => {
        expect(isToolbarAction({ name: 'click', selector: `internal:role=button >> ${TOOLBAR_TAG}` })).toBe(true);
        expect(isToolbarAction({ name: 'click', selector: '#other' })).toBe(false);
    });
});

describe('drain', () => {
    it('empties in place', () => {
        const list = [1, 2];
        expect(drain(list)).toEqual([1, 2]);
        expect(list).toEqual([]);
    });
});

describe('toolbarScript', () => {
    it('is a self-invoking script that defines the toolbar tag', () => {
        const source = toolbarScript();
        expect(source).toContain(TOOLBAR_TAG);
        expect(() => new Function(source)).not.toThrow();
    });
});

describe('ensureRecorder', () => {
    function fakeContext() {
        const sinks: any[] = [];
        return {
            sinks,
            _enableRecorder: jest.fn(async (_params: unknown, sink: unknown) => {
                sinks.push(sink);
            }),
            exposeBinding: jest.fn(async () => undefined),
        } as any;
    }

    it('enables the recorder once per context', async () => {
        const context = fakeContext();
        await ensureRecorder(context);
        await ensureRecorder(context);
        expect(context._enableRecorder).toHaveBeenCalledTimes(1);
        expect(context.exposeBinding).toHaveBeenCalledTimes(1);
    });

    it('buffers actions, updates and signals, but not toolbar actions', async () => {
        const context = fakeContext();
        const state = await ensureRecorder(context);
        const sink = context.sinks[0];
        sink.actionAdded({}, { name: 'click', selector: '#a' });
        sink.actionUpdated({}, { name: 'fill', selector: '#a', text: 'x' });
        sink.signalAdded({}, { name: 'popup', popupPageGuid: 'g' });
        sink.actionAdded({}, { name: 'click', selector: TOOLBAR_TAG });
        expect(state.events.map((e) => e.event)).toEqual(['added', 'updated', 'signal']);
    });

    it('fails clearly without the programmatic recorder', async () => {
        await expect(ensureRecorder({ exposeBinding: jest.fn() } as any)).rejects.toThrow('programmatic recorder');
    });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `npm run test -- recorder`
Expected: FAIL with `Cannot find module '../recorder'`.

- [ ] **Step 3: Add the RPCs to the proto and regenerate**

In `protobuf/playwright.proto`, inside `service Playwright { ... }` before its closing brace:

```proto
  rpc RecorderPoll(Request.Json) returns (Response.Json);
  rpc RecorderStop(Request.Empty) returns (Response.Empty);
```

Run: `inv protobuf`
Expected: regenerated `Browser/generated/` and `node/playwright-wrapper/generated/` (not committed).

- [ ] **Step 4: Move the toolbar to a static asset**

```bash
git mv Browser/recorder/toolbar.js node/playwright-wrapper/static/recorder-toolbar.js
```

Edit `node/playwright-wrapper/static/recorder-toolbar.js`: keep the license header and the
comment about the closed shadow root, keep `installToolbar(TAG)` as is, and replace the tail
(`const TOOLBAR_SOURCE = ...` and the three `exports` lines) with:

```js
installToolbar('rfb-recorder-toolbar');
```

Wrap the whole file body after the header in `(function () { ... })();` so nothing leaks into
the page's global scope except the `window.__rfb*` functions. In the render function add,
as its first line after `if (!state) return;`:

```js
        window.__rfbToolbarState = state;
```

and in `__rfbToolbarRemove` add `delete window.__rfbToolbarState;`. Rename every "step"
wording in the toolbar to "Keyword Call" (`no steps yet` → `no keyword calls yet`), and read
`state.calls.map((c) => c.text)` instead of `state.steps`, `state.target` instead of
`state.file`.

Add `"recorder-toolbar.js"` to the `"*"` list in `[tool.setuptools.package-data]` in
`pyproject.toml`, and delete the `"Browser.recorder" = ["*.js"]` entry added in Task 2.

- [ ] **Step 5: Implement `recorder.ts`**

Port `Browser/recorder/recorder.js` to TypeScript (keep its four "load-bearing" comments,
updated to say 1.63 is the version in use and that `actionUpdated` still exists there):

```ts
// (license header)
import * as fs from 'fs';
import * as path from 'path';
import { BrowserContext } from 'playwright';

import * as pb from './generated/playwright';
import { PlaywrightState } from './playwright-state';
import { emptyWithLog, jsonResponse } from './response-util';

export const TOOLBAR_TAG = 'rfb-recorder-toolbar';
const RECORDER = Symbol.for('robotframework-browser.recorder.state');
const STOP_MODES = new Set(['none', 'standby']);

export type Action = Record<string, unknown> & { name: string; selector?: string };
interface Buffered {
    event: 'added' | 'updated' | 'signal';
    action: Record<string, unknown>;
}
export interface RecorderBuffers {
    events: Buffered[];
    commands: unknown[];
    armed: boolean;
}

export function toAction(payload: unknown): Action | null {
    if (!payload || typeof payload !== 'object') return null;
    const record = payload as Record<string, unknown>;
    const inner = record.action && typeof record.action === 'object' ? (record.action as Record<string, unknown>) : record;
    if (typeof inner.name !== 'string') return null;
    const { ariaSnapshot, ...rest } = inner; // eslint-disable-line @typescript-eslint/no-unused-vars
    return rest as Action;
}

export function isToolbarAction(action: Action): boolean {
    return typeof action.selector === 'string' && action.selector.includes(TOOLBAR_TAG);
}

export function drain<T>(list: T[]): T[] {
    return list.splice(0, list.length);
}

let toolbarSource: string | undefined;
export function toolbarScript(): string {
    if (toolbarSource === undefined) {
        // `__dirname` is Browser/wrapper at runtime (static/ is copied next to
        // index.js by `inv node-build`) and node/playwright-wrapper under jest.
        toolbarSource = fs.readFileSync(path.join(__dirname, 'static', 'recorder-toolbar.js'), 'utf8');
    }
    return toolbarSource;
}

export async function ensureRecorder(context: BrowserContext): Promise<RecorderBuffers> {
    const holder = context as unknown as Record<symbol, RecorderBuffers | undefined>;
    const existing = holder[RECORDER];
    if (existing) return existing;
    const enable = (context as unknown as { _enableRecorder?: (...args: unknown[]) => Promise<void> })._enableRecorder;
    if (typeof enable !== 'function') {
        throw new Error(
            'This Playwright version does not offer the programmatic recorder ' +
                '(BrowserContext._enableRecorder), which Record Keyword and Record Keywords need.',
        );
    }
    const buffers: RecorderBuffers = { events: [], commands: [], armed: false };
    const forward = (event: 'added' | 'updated') => (_page: unknown, payload: unknown) => {
        const action = toAction(payload);
        if (!action || isToolbarAction(action)) return;
        buffers.events.push({ event, action });
    };
    await enable.call(
        context,
        { mode: 'recording', recorderMode: 'api' },
        {
            actionAdded: forward('added'),
            actionUpdated: forward('updated'),
            signalAdded: (_page: unknown, signal: unknown) => {
                if (signal && typeof signal === 'object' && typeof (signal as Action).name === 'string') {
                    buffers.events.push({ event: 'signal', action: signal as Record<string, unknown> });
                }
            },
        },
    );
    await context.exposeBinding('__rfbCommand', (_source: unknown, command: unknown) => {
        buffers.commands.push(command);
    });
    holder[RECORDER] = buffers;
    return buffers;
}
```

Port `readMode`, `writeMode` and `renderToolbars` from `recorder.js` unchanged in logic, typed
with `BrowserContext`, using `toolbarScript()` instead of `TOOLBAR_SOURCE`. Then:

```ts
export async function recorderPoll(request: pb.Request_Json, state: PlaywrightState): Promise<pb.Response_Json> {
    const context = state.getActiveContext();
    if (!context) throw new Error('No browser context is open. Open a page before recording.');
    const { state: toolbarState, reset } = JSON.parse(request.body || '{}');
    const buffers = await ensureRecorder(context);
    if (reset) {
        // A previous session leaves the recorder in `standby`, `armed` set and
        // possibly Actions buffered in between; all three would end this
        // session on its first poll.
        buffers.armed = false;
        drain(buffers.events);
        drain(buffers.commands);
        await writeMode(context, 'recording');
    }
    await renderToolbars(context, toolbarState ?? {});
    const mode = await readMode(context);
    if (mode !== undefined && !STOP_MODES.has(mode)) buffers.armed = true;
    const stopped = buffers.armed && mode !== undefined && STOP_MODES.has(mode);
    return jsonResponse(
        JSON.stringify({
            mode: stopped ? 'stopped' : 'recording',
            pages: context.pages().length,
            events: drain(buffers.events),
            commands: drain(buffers.commands),
        }),
        '',
    );
}

export async function recorderStop(_request: pb.Request_Empty, state: PlaywrightState): Promise<pb.Response_Empty> {
    const context = state.getActiveContext();
    if (!context) return emptyWithLog('No context to stop recording in.');
    // Deliberately not `_disableRecorder()`: it drops the event sink, and
    // re-installing it would deliver every Action of the next session twice.
    await writeMode(context, 'standby');
    for (const page of context.pages()) {
        try {
            await page.evaluate(() => (window as any).__rfbToolbarRemove?.()); // eslint-disable-line @typescript-eslint/no-explicit-any
        } catch {
            // Page closed or navigating.
        }
    }
    return emptyWithLog('Recording stopped.');
}
```

- [ ] **Step 6: Wire the RPCs**

In `node/playwright-wrapper/grpc-service.ts` add `import * as recorder from './recorder';`
next to the other module imports, and two methods on `PlaywrightServer`. They are written
out (not via `wrapping`) so the 5-per-second poll does not flood `playwright-log.txt`:

```ts
    async recorderPoll(
        call: ServerUnaryCall<pb.Request_Json, pb.Response_Json>,
        callback: sendUnaryData<pb.Response_Json>,
    ): Promise<void> {
        try {
            callback(null, await recorder.recorderPoll(call.request, this.getState(call)));
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }

    async recorderStop(
        call: ServerUnaryCall<pb.Request_Empty, pb.Response_Empty>,
        callback: sendUnaryData<pb.Response_Empty>,
    ): Promise<void> {
        try {
            callback(null, await recorder.recorderStop(call.request, this.getState(call)));
        } catch (e) {
            callback(errorResponse(e), null);
        }
    }
```

- [ ] **Step 7: Run node tests, build, lint**

Run: `npm run test -- recorder` → PASS.
Run: `inv node-build` → builds; `ls Browser/wrapper/static/recorder-toolbar.js` exists.
Run: `inv lint-node` → clean.

- [ ] **Step 8: Commit**

```bash
git add protobuf/playwright.proto node/playwright-wrapper/recorder.ts node/playwright-wrapper/grpc-service.ts node/playwright-wrapper/static/recorder-toolbar.js node/playwright-wrapper/__tests__/recorder.test.ts pyproject.toml Browser/recorder
git commit -m "feat(recorder): add native RecorderPoll/RecorderStop RPCs and ship the toolbar as a static asset"
```

---

### Task 10: Toolbar UI — Keyword Calls, Keyword Arguments, notices, finishing state

All logic stays in Python; the toolbar only renders the state from Task 7 and sends the
commands from Task 7. Behaviour is verified by the acceptance suite (Task 12) because jest
runs without a DOM.

**Files:**
- Modify: `node/playwright-wrapper/static/recorder-toolbar.js`

**Interfaces:**
- Consumes: toolbar state and command contracts from Task 7.

- [ ] **Step 1: Replace the step list with a call list**

In the shadow-root template, replace `<div class="steps" id="steps"></div>` with
`<ol class="calls" id="calls"></ol>` and add below the hint:

```html
    <div class="notice" id="notice" hidden></div>
    <div class="offer" id="offer" hidden>
      <div id="offerText"></div>
      <div id="offerList"></div>
      <div class="row"><button id="offerSkip">Skip</button><button class="primary" id="offerApply">Replace</button></div>
    </div>
    <div class="args" id="args"></div>
```

and a second modal for creating an argument:

```html
<div class="modal" id="argModal" hidden>
  <div class="dialog">
    <div>Mark the part that becomes an argument (or leave it unmarked for the whole value)</div>
    <input id="argValue" readonly>
    <input id="argName" placeholder="argument name, e.g. email" autocomplete="off">
    <div class="err" id="argErr" hidden></div>
    <div class="row"><button id="argCancel">Cancel</button><button class="primary" id="argOk">Make argument</button></div>
  </div>
</div>
```

CSS additions inside the existing `<style>`:

```css
  .calls { max-height: 220px; overflow: auto; background: #141414; border-radius: 4px;
           margin: 0; padding: 6px 6px 6px 28px; font-family: ui-monospace, monospace; font-size: 11px; }
  .calls:empty::after { content: 'no keyword calls yet'; opacity: .5; }
  .calls li { white-space: pre; }
  .cell { margin-left: 8px; }
  .cell.pick { cursor: pointer; text-decoration: underline dotted; }
  .cell.pick:hover { background: #0a6ebd55; }
  .notice { color: #ffd479; }
  .args label { display: block; }
  .busy button { opacity: .5; pointer-events: none; }
```

- [ ] **Step 2: Render calls with clickable values**

In `window.__rfbToolbarRender`:

```js
        const list = $('calls');
        list.textContent = '';
        state.calls.forEach((call, callIndex) => {
            const item = document.createElement('li');
            const kw = document.createElement('span');
            kw.textContent = call.keyword;
            item.appendChild(kw);
            call.values.forEach((value, valueIndex) => {
                const cell = document.createElement('span');
                cell.className = value.selectable && recording ? 'cell pick' : 'cell';
                cell.textContent = value.text;
                if (value.selectable && recording) {
                    cell.title = 'Make this value an argument';
                    cell.addEventListener('click', () => openArgModal(callIndex, valueIndex, value.text));
                }
                item.appendChild(cell);
            });
            list.appendChild(item);
        });
        $('count').textContent = recording ? `(${state.calls.length})` : '';
        $('notice').textContent = state.notice || '';
        $('notice').hidden = !state.notice;
        $('panel').classList.toggle('busy', !!state.pending);
        if (state.pending) $('title').textContent = `${state.name || 'Recording'} - finishing…`;
```

`value.text` is the rendered cell. Only literal cells are selectable for a new argument:
skip `openArgModal` when `value.text.includes('${')` (show the hint "This value already
contains an argument." in `#err` instead).

- [ ] **Step 3: The argument modal**

```js
    let argTarget = null;
    const openArgModal = (call, value, text) => {
        if (text.includes('${')) {
            $('err').textContent = 'This value already contains an argument.';
            $('err').hidden = false;
            return;
        }
        argTarget = { call, value, text };
        $('argValue').value = text;
        $('argName').value = '';
        $('argErr').hidden = true;
        $('argModal').hidden = false;
        $('argValue').focus();
    };
    $('argCancel').addEventListener('click', () => { $('argModal').hidden = true; argTarget = null; });
    $('argOk').addEventListener('click', () => {
        if (!argTarget) return;
        const input = $('argValue');
        let start = input.selectionStart ?? 0;
        let end = input.selectionEnd ?? 0;
        if (start === end) { start = 0; end = argTarget.text.length; }
        send({ cmd: 'argument', call: argTarget.call, value: argTarget.value, start, end, name: $('argName').value.trim() });
        $('argModal').hidden = true;
        argTarget = null;
    });
```

Note: `#argValue` shows the *rendered* cell; for values with escapes (`\#`, `${SPACE}`) the
offsets differ from the raw text. Python therefore must receive raw offsets: extend the
state contract in Task 7 by also sending `"raw"` (the literal `Value.text`) next to `"text"`
for every value, show `raw` in `#argValue`, and use `raw.length` for the whole-value case.
Add `"raw": value.text` in `RecorderSession.toolbar_state()` and the assertion
`assert state["calls"][0]["values"][1]["raw"] == "Alice"` to `test_new_record_finish`.

- [ ] **Step 4: Offer and argument list**

```js
        const offer = state.offer;
        $('offer').hidden = !offer;
        if (offer) {
            $('offerText').textContent = `Also use \${${offer.argument}} for "${offer.text}" in:`;
            const box = $('offerList');
            box.textContent = '';
            offer.occurrences.forEach(([c, v]) => {
                const label = document.createElement('label');
                const check = document.createElement('input');
                check.type = 'checkbox';
                check.checked = true;
                check.dataset.c = String(c);
                check.dataset.v = String(v);
                label.appendChild(check);
                label.append(` ${state.calls[c] ? state.calls[c].text : ''}`);
                box.appendChild(label);
            });
        }
        const args = $('args');
        args.textContent = '';
        state.arguments.forEach((arg) => {
            const label = document.createElement('label');
            const check = document.createElement('input');
            check.type = 'checkbox';
            check.checked = arg.useDefault;
            check.addEventListener('change', () => send({ cmd: 'default', argument: arg.name, use: check.checked }));
            label.appendChild(check);
            label.append(` \${${arg.name}} default: ${arg.default}`);
            args.appendChild(label);
        });
```

Wire the offer buttons once, outside render:

```js
    $('offerApply').addEventListener('click', () => {
        const chosen = [...$('offerList').querySelectorAll('input:checked')].map((i) => [Number(i.dataset.c), Number(i.dataset.v)]);
        const name = (window.__rfbToolbarState && window.__rfbToolbarState.offer || {}).argument;
        send({ cmd: 'replace', argument: name, occurrences: chosen });
    });
    $('offerSkip').addEventListener('click', () => {
        const name = (window.__rfbToolbarState && window.__rfbToolbarState.offer || {}).argument;
        send({ cmd: 'replace', argument: name, occurrences: [] });
    });
```

- [ ] **Step 5: Smoke-check by hand**

Run: `inv node-build`, then a scratch suite (do not commit) with
`New Page    ${FORM_URL}` and `Record Keywords    ${OUTPUT_DIR}/scratch.resource` in
`headless=False`. Record a fill, click its value, make it an argument, toggle the default,
finish, stop. Check the file.
Expected: `[Arguments]    ${name}=…` and `Fill Text    …    ${name}`.

- [ ] **Step 6: Lint and commit**

```bash
inv lint-node
inv lint-python --fix
git add node/playwright-wrapper/static/recorder-toolbar.js Browser/recorder/session.py utest/test_recorder_session.py
git commit -m "feat(recorder): toolbar shows Keyword Calls and creates Keyword Arguments"
```

---

### Task 11: Core keywords `Record Keyword` / `Record Keywords`; remove the plugin

**Files:**
- Create: `Browser/keywords/recorder.py`
- Modify: `Browser/keywords/__init__.py`, `Browser/browser.py` (~line 566 list, ~line 43 import)
- Delete: `Browser/recorder/plugin.py`, `Browser/recorder/recorder.js`, `utest/test_recorder_plugin.py` (must be empty of tests by now)
- Test: `utest/test_recorder_keywords.py`

**Interfaces:**
- Consumes: `FileTarget`, `LogTarget`, `RecorderSession`, `run_session`, `collect_known_keywords`, gRPC `RecorderPoll` / `RecorderStop`
- Produces: keywords `Record Keyword(name: str, file: str | None = "${SUITE_SOURCE}", idle_timeout: timedelta | None = None) -> str` and `Record Keywords(file: str | None = "${SUITE_SOURCE}", idle_timeout: timedelta | None = None) -> str`

- [ ] **Step 1: Write the failing tests**

```python
from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest

from Browser.keywords import recorder as module
from Browser.keywords.recorder import SUITE_SOURCE, Recorder
from Browser.recorder.target import FileTarget, LogTarget


def test_none_means_log_only():
    assert isinstance(Recorder._target(None), LogTarget)


def test_explicit_file_is_resolved(tmp_path):
    target = Recorder._target(str(tmp_path / "k.resource"))
    assert isinstance(target, FileTarget)
    assert target.path == (tmp_path / "k.resource").resolve()


def test_default_resolves_suite_source(monkeypatch, tmp_path):
    suite = tmp_path / "s.robot"
    monkeypatch.setattr(module, "_suite_source", lambda: str(suite))
    assert Recorder._target(SUITE_SOURCE).path == suite.resolve()


def test_default_without_running_suite_fails_clearly(monkeypatch):
    monkeypatch.setattr(module, "_suite_source", lambda: None)
    with pytest.raises(ValueError, match="file"):
        Recorder._target(SUITE_SOURCE)


def test_record_keywords_runs_a_session_and_returns_text(monkeypatch, tmp_path):
    seen = {}

    def fake_run(session, client, idle_timeout=None):
        seen["idle"] = idle_timeout
        session.handle_command({"cmd": "new", "name": "K"})
        session.handle_event("added", {"name": "fill", "selector": "#n", "text": "x"})
        session.close()
        return "stop"

    monkeypatch.setattr(module, "run_session", fake_run)
    monkeypatch.setattr(module, "collect_known_keywords", lambda: module.KnownKeywords())
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    text = recorder.record_keywords(str(tmp_path / "k.resource"), timedelta(seconds=3))
    assert seen["idle"] == 3.0
    assert text.startswith("*** Keywords ***\nK\n")
    assert Path(tmp_path / "k.resource").exists()


def test_record_keyword_rejects_a_shadowing_name(monkeypatch, tmp_path):
    monkeypatch.setattr(
        module, "collect_known_keywords",
        lambda: module.KnownKeywords(names=frozenset({"Click"})),
    )
    recorder = Recorder.__new__(Recorder)
    recorder._client = lambda: object()
    with pytest.raises(ValueError, match="shadowed"):
        recorder.record_keyword("Click", str(tmp_path / "k.resource"))
```

- [ ] **Step 2: Run to verify it fails**

Run: `pytest utest/test_recorder_keywords.py -q --no-cov`
Expected: FAIL with `ModuleNotFoundError: No module named 'Browser.keywords.recorder'`.

- [ ] **Step 3: Implement the keyword class**

```python
# (license header)
from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..recorder.driver import run_session
from ..recorder.names import KnownKeywords, collect_known_keywords
from ..recorder.session import RecorderSession
from ..recorder.target import FileTarget, LogTarget, Target
from ..utils import keyword, logger

SUITE_SOURCE = "${SUITE_SOURCE}"


def _suite_source() -> str | None:
    try:
        return BuiltIn().get_variable_value("${SUITE_SOURCE}")
    except RobotNotRunningError:
        return None


class _GrpcRecorderClient:
    def __init__(self, library: LibraryComponent) -> None:
        self._library = library

    def poll(self, state: dict, reset: bool) -> dict:
        body = json.dumps({"state": state, "reset": reset})
        with self._library.playwright.grpc_channel() as stub:
            response = stub.RecorderPoll(Request().Json(body=body))
        return json.loads(response.json) if response.json else {}

    def stop(self) -> None:
        with self._library.playwright.grpc_channel() as stub:
            stub.RecorderStop(Request().Empty())


class Recorder(LibraryComponent):
    @keyword(tags=("Recorder",))
    def record_keyword(
        self,
        name: str,
        file: str | None = SUITE_SOURCE,
        idle_timeout: timedelta | None = None,
    ) -> str:
        """(docstring: see Step 4)"""
        return self._record(file, idle_timeout, fixed_name=name).text()

    @keyword(tags=("Recorder",))
    def record_keywords(
        self,
        file: str | None = SUITE_SOURCE,
        idle_timeout: timedelta | None = None,
    ) -> str:
        """(docstring: see Step 4)"""
        return self._record(file, idle_timeout, fixed_name=None).text()

    def _record(
        self, file: str | None, idle_timeout: timedelta | None, fixed_name: str | None
    ) -> RecorderSession:
        target = self._target(file)
        session = RecorderSession(target, fixed_name=fixed_name, known=collect_known_keywords())
        logger.info(f"Recording into {target.label}")
        run_session(
            session,
            self._client(),
            idle_timeout=idle_timeout.total_seconds() if idle_timeout else None,
        )
        return session

    def _client(self) -> _GrpcRecorderClient:
        return _GrpcRecorderClient(self)

    @staticmethod
    def _target(file: str | None) -> Target:
        if file is None:
            return LogTarget()
        if file == SUITE_SOURCE:
            source = _suite_source()
            if not source:
                raise ValueError(
                    "No 'file' given and no running suite to record into. Give the "
                    "target file explicitly, e.g. Record Keywords    ${CURDIR}/keywords.resource"
                )
            file = source
        # `${SUITE_SOURCE}` is an abspath, not a realpath: resolve so a suite
        # reached through a symlink is the same file as its collected keywords.
        return FileTarget(Path(file).resolve())
```

Check `Browser/keywords/cookie.py` for the exact `keyword` / `logger` import used in this
package and copy it (the snippet above assumes `from ..utils import keyword, logger`).
`KnownKeywords` is imported only so tests can reach it as `module.KnownKeywords`; keep the
import and add it to a `__all__` if ruff flags it.

Register: in `Browser/keywords/__init__.py` add `from .recorder import Recorder` and
`"Recorder"` to `__all__` (alphabetical); in `Browser/browser.py` add `Recorder` to the
`from .keywords import (...)` list and `Recorder(self),` to `libraries = [...]` after
`Promises(self),`.

- [ ] **Step 4: Write the keyword documentation**

`record_keyword` docstring:

```
Record browser interactions as one User Keyword named ``name``.

Shows the Robot Framework recorder toolbar on the page of the *current* browser
context and blocks until the recording ends. Every Action becomes a Keyword Call
to a Browser keyword and is written to ``file`` immediately. The toolbar shows
the Keyword Calls; *Undo* removes the last Action's Keyword Calls, *Discard*
starts the keyword again empty. Click a value in the toolbar to turn it, or a
marked part of it, into a Keyword Argument; its recorded value becomes the
default, which can be deselected.

The recording ends with *Stop* in the toolbar, with Playwright's Record button,
when ``idle_timeout`` passes without any Action or toolbar command, or when all
pages are closed. The keyword being recorded is saved in every case.

| =Arguments= | =Description= |
| ``name`` | Name of the User Keyword to create. It must not exist in ``file`` and must not shadow any keyword the running suite can call. |
| ``file`` | Target ``.robot`` or ``.resource`` file. Defaults to ``${SUITE_SOURCE}``, the file of the running suite. With ``${None}`` nothing is written; the keyword is logged to the console and to the log at INFO level instead. |
| ``idle_timeout`` | Ends the recording after this long without activity. Default: no timeout. |

Returns the text of the recorded keyword, including the ``*** Keywords ***`` header.

What is generated: every keyword gets ``[Tags]    recorded``. A popup or new tab
becomes ``Switch Page    NEW``; a dialog gets ``Handle Future Dialogs`` before the
Action; a download is wrapped in ``Promise To Wait For Download`` and ``Wait For``.
Actions without a Browser keyword are only reported in the toolbar.

*Review a recorded keyword before you commit it.* Its values come from the page
under test, including anything typed into password fields.

Requires a Playwright version that offers the programmatic recorder. The context
stays prepared for recording after the session ends.

Example:
| ${text} =    Record Keyword    Login As Admin
| Record Keyword    Search Product    ${CURDIR}/shop.resource    idle_timeout=5 min
| Record Keyword    Try Something    file=${None}

See `Record Keywords` to record several keywords in one session.
```

`record_keywords` docstring: same structure; first paragraph:

```
Record several User Keywords in one session.

Use *+ New Keyword* in the toolbar to name and start a keyword, record it, and
*Finish* it; then start the next one. Actions while no keyword is being recorded
are not captured, so you can navigate freely between keywords. A name must not
exist in ``file``, must not have been recorded earlier in the session, and must
not shadow any keyword the running suite can call - such names are rejected in
the toolbar.
```

Arguments table without ``name``; returns "the text of all keywords recorded in the
session, under one ``*** Keywords ***`` header"; examples:

```
| ${text} =    Record Keywords
| Record Keywords    ${CURDIR}/resources/shop.resource    idle_timeout=10 min
```

End with "See `Record Keyword` to record exactly one keyword."

- [ ] **Step 5: Remove the plugin**

```bash
git rm Browser/recorder/plugin.py Browser/recorder/recorder.js utest/test_recorder_plugin.py
grep -rn "RecorderPlugin\|recorder_plugin\|rfbRecorderPoll" Browser utest node atest || true
```

Expected: no matches. If `utest/test_recorder_plugin.py` still holds tests, they were not
moved in Tasks 3/5/6 — move them now before deleting.

- [ ] **Step 6: Run the whole Python suite**

Run: `inv node-build && pytest utest -q`
Expected: PASS, including `test_docs.py::test_all_keywords_have_docs` and
`test_python_arguments.py`.

- [ ] **Step 7: Lint and commit**

```bash
inv lint-python --fix
git add -A Browser utest
git commit -m "feat(recorder): make Record Keyword(s) core keywords and remove the plugin"
```

---

### Task 12: Acceptance suite

**Files:**
- Create: `atest/test/02_Content_Keywords/recorder.robot`

**Interfaces:**
- Consumes: keywords from Task 11; page globals `window.__rfbCommand`, `window.__rfbToolbarState` from Task 9.

- [ ] **Step 1: Write the suite**

```robotframework
*** Settings ***
Documentation       Scripted recording sessions. The toolbar's closed shadow root cannot be
...                 clicked from a test, so commands go through `window.__rfbCommand`, the
...                 same channel the toolbar uses, and the page is driven by Browser keywords.
Resource            imports.resource
Library             OperatingSystem

Test Setup          Open Form And Name Resource
Test Teardown       Run Keywords    Wait For All Promises    AND    Close Page    ALL

Test Tags           recorder


*** Test Cases ***
Session Records Two Keywords And Skips Idle Actions
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar Is Ready
    Fill Text    id=input_name    ignored while idle
    Send Command    {cmd: 'new', name: 'Fill Name'}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Finish Keyword
    Send Command    {cmd: 'new', name: 'Check Sms'}
    Toolbar State Should Be    recording
    Check Checkbox    [data-testid="testid-sms"]
    Finish Keyword
    Send Command    {cmd: 'stop'}
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    Fill Name
    Should Contain    ${text}    Check Sms
    ${file} =    Get File    ${RESOURCE}
    Should Not Contain    ${file}    ignored while idle
    Should Contain    ${file}    [Tags]    recorded
    Recorded Keyword Replays    ${RESOURCE}    Fill Name
    Get Property    id=input_name    value    ==    Alice

Record Keyword Returns Its Text
    ${promise} =    Promise To    Record Keyword    Fill Alice    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Alice
    Send Command    {cmd: 'stop'}
    ${text} =    Wait For    ${promise}
    Should Start With    ${text}    *** Keywords ***\nFill Alice\n

Undo And Discard
    ${promise} =    Promise To    Record Keywords    ${RESOURCE}
    Toolbar Is Ready
    Send Command    {cmd: 'new', name: 'Undone'}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    first
    Check Checkbox    [data-testid="testid-sms"]
    Wait Until Calls    2
    Send Command    {cmd: 'undo'}
    Wait Until Calls    1
    Finish Keyword
    Send Command    {cmd: 'new', name: 'Thrown Away'}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    second
    Wait Until Calls    1
    Send Command    {cmd: 'discard'}
    Toolbar State Should Be    idle
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    Undone
    Should Not Contain    ${file}    Check Checkbox
    Should Not Contain    ${file}    Thrown Away

Click Right Before Finish Lands In The Keyword
    ${promise} =    Promise To    Record Keyword    Click Then Finish    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    [data-testid="testid-sms"]
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    testid-sms

Log Only Mode Writes No File
    # Positional ${None}: the whole argument stays the None object through Promise To.
    ${promise} =    Promise To    Record Keyword    Logged Only    ${None}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Bob
    Send Command    {cmd: 'stop'}
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    Logged Only
    File Should Not Exist    ${RESOURCE}

Keyword Arguments With Partial Value And Default
    ${promise} =    Promise To    Record Keyword    Fill Parametrised    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    id-42
    Wait Until Calls    1
    Send Command    {cmd: 'argument', call: 0, value: 1, start: 3, end: 5, name: 'number'}
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    [Arguments]    \${number}=42
    Should Contain    ${file}    id-\${number}
    Import Resource    ${RESOURCE}
    Fill Parametrised    number=7
    Get Property    id=input_name    value    ==    id-7

Popup Becomes Switch Page New
    Go To    ${CREATE_POPUPS_URL}
    ${promise} =    Promise To    Record Keyword    Open Popup    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    id=first_popup
    Wait Until Calls    2
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Contain    ${file}    Switch Page    NEW
    Should Not Contain    ${file}    New Page

Dialog Gets Handled Before The Click
    Go To    ${DIALOGS_URL}
    Handle Future Dialogs    action=accept
    ${promise} =    Promise To    Record Keyword    Confirm Something    ${RESOURCE}
    Toolbar State Should Be    recording
    Click    id=confirm_btn
    Wait Until Calls    2
    Send Command    {cmd: 'stop'}
    Wait For    ${promise}
    ${file} =    Get File    ${RESOURCE}
    Should Match Regexp    ${file}    Handle Future Dialogs\\s+action=accept\\n\\s+Click

Idle Timeout Ends The Session
    ${text} =    Record Keywords    ${RESOURCE}    idle_timeout=1s
    Should Be Empty    ${text}

Closing All Pages Ends The Session
    ${promise} =    Promise To    Record Keyword    Until Closed    ${RESOURCE}
    Toolbar State Should Be    recording
    Fill Text    id=input_name    Carol
    Wait Until Calls    1
    Close Page    ALL
    ${text} =    Wait For    ${promise}
    Should Contain    ${text}    Until Closed
    New Page    ${FORM_URL}

Shadowing Name Is Rejected
    Run Keyword And Expect Error    *would be shadowed*    Record Keyword    click    ${RESOURCE}

Second Session In Same Context Records Nothing Twice
    FOR    ${name}    IN    First Run    Second Run
        ${promise} =    Promise To    Record Keyword    ${name}    ${RESOURCE}
        Toolbar State Should Be    recording
        Fill Text    id=input_name    ${name}
        Wait Until Calls    1
        Send Command    {cmd: 'stop'}
        Wait For    ${promise}
    END
    ${file} =    Get File    ${RESOURCE}
    Should Contain X Times    ${file}    Fill Text    2


*** Keywords ***
Open Form And Name Resource
    New Page    ${FORM_URL}
    ${slug} =    Evaluate    "${TEST_NAME}".lower().replace(" ", "_")
    Set Test Variable    ${RESOURCE}    ${OUTPUT_DIR}${/}recorded_${slug}.resource
    Remove File    ${RESOURCE}

Toolbar Is Ready
    Wait For Function    () => typeof window.__rfbCommand === 'function' && !!window.__rfbToolbarState

Send Command
    [Arguments]    ${command}
    Evaluate JavaScript    ${None}    () => window.__rfbCommand(${command})

Toolbar State Should Be
    [Arguments]    ${state}
    Wait For Function    () => window.__rfbToolbarState && window.__rfbToolbarState.state === '${state}' && !window.__rfbToolbarState.pending

Wait Until Calls
    [Arguments]    ${count}
    Wait For Function    () => window.__rfbToolbarState && window.__rfbToolbarState.calls.length === ${count}

Finish Keyword
    Send Command    {cmd: 'finish'}
    Toolbar State Should Be    idle

Recorded Keyword Replays
    [Arguments]    ${resource}    ${name}
    Go To    ${FORM_URL}
    Import Resource    ${resource}
    Run Keyword    ${name}
```

- [ ] **Step 2: Run it**

Run: `inv atest --suite "Recorder"`
Expected: all tests pass. Typical first failures and their meaning:
- `Toolbar State Should Be` times out → the toolbar is not injected: check `Browser/wrapper/static/recorder-toolbar.js` exists (`inv node-build`).
- A recorded `Fill Text` is missing → Playwright did not report Browser-driven input; check `playwright-log.txt` for `actionAdded`; record that finding in `Browser/recorder/README.md`.

- [ ] **Step 3: Lint and commit**

```bash
inv lint-robot
git add atest/test/02_Content_Keywords/recorder.robot
git commit -m "test(recorder): add scripted acceptance suite including a replay round trip"
```

---

### Task 13: Documentation

**Files:**
- Create: `Browser/recorder/README.md`
- Create or modify: `docs/releasenotes/Browser-20.6.0.md` (the next unreleased version; if a maintainer has already created a later file, add to that one instead)
- Modify: `docs/adr/0011-recorder-consumes-playwright-action-stream.md` only if Task 12 found a deviating Playwright behaviour

- [ ] **Step 1: Write `Browser/recorder/README.md`**

```markdown
# Recorder internals

How `Record Keyword` / `Record Keywords` work. Vocabulary: `CONTEXT.md`. Why: ADR 0010
(page under test is untrusted) and ADR 0011 (action stream instead of codegen). Usage:
the keyword documentation.

## Architecture

    Browser/keywords/recorder.py   Recorder keywords, gRPC client
    Browser/recorder/driver.py     poll loop: every 200 ms RecorderPoll(state) -> events, commands
    Browser/recorder/session.py    state machine: idle / recording, commands, deferred finish
    Browser/recorder/model.py      RecordedKeyword: Keyword Calls in groups, Keyword Arguments
    Browser/recorder/action_mapper.py  Action -> Call, signal -> calls around it
    Browser/recorder/target.py     FileTarget (re-read, own block only) / LogTarget
    Browser/recorder/names.py      name validation and collision checks (ADR 0010)
    node/playwright-wrapper/recorder.ts         _enableRecorder, buffering, toolbar injection
    node/playwright-wrapper/static/recorder-toolbar.js   toolbar in a closed shadow root

Python is the only clock. The toolbar renders the state Python sends and sends commands
through `window.__rfbCommand`; it holds no recording logic.

## Toolbar contract

State (Python → toolbar) and commands (toolbar → Python) are defined in
`session.py` (`RecorderSession.toolbar_state`, `handle_command`).

## Selector mapping

| Playwright internal | Browser selector |
|---------------------|------------------|
| `internal:role=button[name="Submit"i]` | `role=button[name="Submit"i]` |
| `internal:text="Log in"i` | `text=Log in` |
| `internal:text="Log in"s` | `text="Log in"` |
| `internal:testid=[data-testid="x"]` | `[data-testid="x"]` |
| `internal:attr=[placeholder="Email"i]` | `[placeholder="Email"i]` |
| `... >> internal:control=enter-frame >> ...` | `... >>> ...` |
| anything else | unchanged (Browser resolves it with `page.locator`) |

## What Playwright does before our sink (1.63)

- `fill`: one `actionAdded`, then one `actionUpdated` per keystroke.
- Double click: one `click` with `clickCount: 2`.
- Left clicks are held back 500 ms; hence `SETTLE_SECONDS` in `session.py`.
- Popups, dialogs and downloads arrive as `signalAdded` after the Action.
- `openPage` is reported for existing pages and hand-opened tabs; we ignore it.
- Main-frame navigation within 5 s of a click/fill/press is swallowed by Playwright.
- The in-page Playwright toolbar cannot be hidden in api mode.
- `_enableRecorder` must be called once per context; `_disableRecorder` drops the sink.

## Playwright upgrade checklist

1. `context._enableRecorder` and `_disableRecorder` still exist (`coreBundle.js`).
2. The sink still has `actionAdded`, `actionUpdated`, `signalAdded`; payload shape still
   handled by `toAction` (`npm run test -- recorder`).
3. Signal names `popup`, `dialog`, `download` unchanged.
4. Click buffer still ≤ 500 ms (`kActionBufferTimeout`).
5. `inv atest --suite "Recorder"` passes; it replays a recorded keyword end to end.
```

- [ ] **Step 2: Release notes entry**

Add to `docs/releasenotes/Browser-20.6.0.md` (create the file following the structure of
`docs/releasenotes/Browser-20.5.0.md` if it does not exist) a section:

```markdown
## Record Keyword and Record Keywords

New keywords record interactions in the live browser as Robot Framework User Keywords made
of Browser keywords, from any point in a test run: name keywords while recording, undo
mistakes, turn values into keyword arguments, and write into a `.robot`/`.resource` file or
only to the log. See the keyword documentation.

- The recorder uses Playwright's programmatic recorder, which is not a public Playwright API.
  It may need adapting after a Playwright upgrade.
- A recorded keyword contains values from the page under test, including anything typed into
  password fields. Review it before committing.
```

- [ ] **Step 3: Check for stale references**

The POC documents (`RECORDER_PLUGIN_HANDOFF.md`, `docs/superpowers/`, the plugin README) were
never imported to this branch, so nothing needs deleting. Make sure nothing points at them:

```bash
grep -rn "1.62.1\|Browser.plugins\|RecorderPlugin\|HANDOFF\|superpowers/specs" Browser docs/adr docs/recorder/user-story.md node/playwright-wrapper/recorder.ts || true
```

Expected: no matches except the historical `1.62` mention in ADR 0011 ("up to 1.62 …").

- [ ] **Step 4: Commit**

```bash
git add Browser/recorder/README.md docs
git commit -m "docs(recorder): add developer notes and release notes"
```

---

### Task 14: Final verification against the acceptance criteria

**Files:** none changed unless a check fails.

- [ ] **Step 1: Full checks**

```bash
inv build
inv lint
pytest utest -q --cov=Browser/recorder --cov=Browser/keywords/recorder.py --cov-branch --cov-report=term-missing
inv utest-node --coverage
inv atest --suite "Recorder"
```

Expected: everything passes; line coverage ≥ 90 % for `Browser/recorder/` and
`Browser/keywords/recorder.py`; no uncovered branches in `names.py` (`NameGuard`) and
`session.py`. Add tests for any gap before continuing.

- [ ] **Step 2: Walk the acceptance criteria**

Open `docs/recorder/user-story.md` and, for each AC-01 … AC-44, write down in the PR
description the test (file::name) or document that proves it. Any AC without proof is a
gap: fix it in the owning task's files, commit, and re-run Step 1.

- [ ] **Step 3: Manual smoke test**

Run a scratch suite headed (`New Browser    headless=False`) against a real site, record two
keywords with an argument, and replay them. Note anything surprising in
`Browser/recorder/README.md`.

- [ ] **Step 4: Commit any fixes**

```bash
git add -A
git commit -m "fix(recorder): close gaps found in final acceptance review"
```
