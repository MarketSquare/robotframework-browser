# `rfbrowser` CLI — what is verified, and what is deliberately not

> **An evidence record, not documentation. Documentation lives on robotframework-browser.org.**
>
> This file records which `rfbrowser` commands have their *results* checked, which are covered
> only indirectly, and which are deliberately left to a human — with the reason written down
> rather than inferred from a missing test. It is kept in this repository because its claims are
> claims about the tests here.
>
> **Point-in-time record, 2026-08-19.** Measured against Browser 20.4.0, Robot Framework 7.4.1,
> Python 3.14.7, macOS. Ticket 0011.
>
> **Two markers are used and they mean different things.**
>
> - **[M] measured** — proven by a named test that was run green on the date above.
> - **[R] read** — verified against source at a named line, never executed.
>
> The distinction earns its place here: ticket 0011 arrived with an inventory that had been read
> rather than run, and it was wrong about four of its nine rows. §2 records what it got wrong,
> because the *way* it was wrong is the thing worth remembering.

## 1. The inventory

| command | how it is exercised | result verified | decision |
| --- | --- | --- | --- |
| `init` | `on-push.yml:332`, setup for the clean-install job | indirectly — the atest run that follows would fail | **accept**: indirect coverage is sufficient |
| `install` | `on-push.yml:490,498`, `on-release.yml:173,181` | indirectly, same | **accept**: indirect coverage is sufficient |
| `launch-browser-server` | atest `Launch Browser Server Via CLI`, `… With Proxy` (`playwright_state.robot:445,487`) | **[M] directly** | **automated**; Ctrl-C path manual, see §4 |
| `show-trace` | atest `Check Show-Trace Command Help`, `Check Show-Trace Command` (`tracing.robot:48,61`) | **[M] directly** | **automated** — newly, see §3 |
| `clean-node` | `on-push.yml:354,538`, `on-release.yml:221` | **[M] asserted after the fact**, see §5 | **assert after the fact** |
| `uninstall` | nowhere end to end | **[M] delegation only**, `utest/test_entry_uninstall.py` | **accept as manual**, see §6 |
| `transform` | atest `Tranform Wait Until Network Is Idle Keyword` (`11_tidy_transformer/network_idle_test.robot`) | **[M] directly** — asserts the rewritten file line by line | **automated**, no work needed |
| `translation` | atest `12_rfbrowser/translation.robot`, 5 cases | **[M] directly** — incl. `--plugings`, `--jsextension`, `--compare` | **automated**, no work needed |
| `coverage` | atest `01_Browser_Management/coverage.robot`, 6 cases | **[M] directly** — 3 happy paths, 3 error paths (rc 1 and 2) | **automated**, no work needed |

Command definitions in `Browser/entry/__main__.py`: `init:207`, `clean_node:253`, `show_trace:324`,
`launch_browser_server:391`, `install:502`, `uninstall:542`, `transform:573`, `translation:618`,
`coverage:688`.

## 2. What ticket 0011's inventory got wrong

Recorded because the error has a pattern, not to relitigate the ticket. Four of nine rows:

- **`transform`, `translation` and `coverage` were listed as run "nowhere".** All three have
  direct acceptance coverage, and `coverage` has the most thorough coverage of any command in
  the CLI. A grep for the command names would have found them; the inventory appears to have
  been assembled from the workflow files alone, which is where the *installation* commands live.
- **`show-trace` was listed as verified "directly — help output plus the viewer process".** It
  was verified neither way. See §3.

The inventory also asserted that the workflows use `pip uninstall` "instead of" `rfbrowser
uninstall`. They are not substitutes: `rfbrowser uninstall` runs `npx playwright uninstall` to
remove browser *binaries*, `pip uninstall` removes the Python *package*. The workflows pair
`rfbrowser clean-node` with `pip uninstall`, which is exactly the sequence `__main__.py:150-154`
tells users to follow. **[R]**

## 3. `show-trace` — was covered three ways over, none of them real

Before ticket 0011 this command had a test that could not fail. Three independent reasons, each
sufficient on its own:

1. **It never ran.** `tracing.robot` gated the body on `IF '${SYS_VAR_CI}' == 'False'` and logged
   a message otherwise. `${SYS_VAR_CI}` is the literal `False` (`atest/test/variables.resource:47`)
   and is set to `True` only by `inv atest-global-pythonpath` (`tasks.py:1158`) — **which no
   workflow invokes**. CI runs `inv atest` and `invoke atest-robot`, which set
   `SYS_VAR_CI_INSTALL_TEST`, a different variable. **[M]**
2. **The helpers dropped their arguments.** All three functions in
   `atest/library/show_trace_tool.py` passed a *list* to `subprocess.Popen` together with
   `shell=True`. On POSIX that runs `/bin/sh -c <first element>` and every remaining element
   becomes a shell positional parameter, so `rfbrowser` was started with no arguments. Measured:

   ```
   shell=True  -> rfbrowser received argv:
   shell=False -> rfbrowser received argv: show-trace --help
   ```

   The help check therefore asserted `Should Contain ${help} Possible commands are` against bare
   `rfbrowser`, and that string is in the top-level group docstring (`__main__.py:114`), not in
   `show_trace`, whose help reads "Start the Playwright trace viewer." The assertion passed
   without the command under test being involved. **[M]**
3. **The viewer was started with an option that does not exist.** The helper passed the trace as
   `-F <file>`; `show_trace` takes it as a positional argument and has no `-F`. Running the
   fixed helper surfaced `Error: No such option '-F'` immediately — which is also proof that the
   command had never once been executed by this test. **[M]**

**What changed.** The helpers now run without a shell and resolve the entry point the same way
the rest of atest does (`rfbrowser` when `SYS_VAR_CI_INSTALL_TEST` is set, `python -m
Browser.entry` otherwise). That removed the *reason* for the gate — its own message,
"This is only for CI when installation is done", described the hardcoded `rfbrowser` console
script — so the gate is gone and both checks run in every atest run. The check is split in two:

- **`Check Show-Trace Command Help`** — asserts against `show-trace`'s own help. Pure text: it
  needs no display, no installed console script and no trace file, so it carries no tags and runs
  on every platform in every run.
- **`Check Show-Trace Command`** — starts a real viewer and asserts the node and chromium child
  processes come up. Keeps `no-windows-support`, which predates this work, and is tagged **`slow`**
  — see below.

Both were run green ungated on macOS; the whole `Tracing` suite passes in 7.7 s. **[M] If the
viewer check proves flaky on a runner, the fix is a tag with the reason written here — not a
condition that makes it pass by not running.**

**The viewer must be torn down.** `Start Show Trace` launches the viewer with
`subprocess.Popen`, outside Robot Framework's Process library, so `Terminate All Processes` does
not know about it — and the original test had no teardown at all. That was harmless only while the
test never ran; ungating it leaked a viewer plus its npm, node and chromium children on every run,
reparented to init. `Stop Show Trace` now takes down the whole process tree, and the helper tracks
what it started so teardown works even when the test failed before getting a handle back. Verified
both ways: no processes survive a passing run or a failing one. **[M]**

**The `slow` tag is load-bearing, not a performance note.** The viewer check consumes
`${OUTPUT_DIR}/trace_1.zip`, which only `Enable Tracing To File With Two Browsers` produces, and
that test is `[Tags] slow`. `invoke atest-robot --smoke` adds `--exclude slow` (`tasks.py:1120`)
and two CI jobs run exactly that (`on-push.yml:343,521`). Ungating the test without inheriting the
tag left it running in smoke jobs with its input never created, failing on
`Path(zip_file).resolve(strict=True)` — reproduced, two jobs would have gone red. **[M]** Tagging
it `slow` keeps producer and consumer excluded together. Anything that later gives this test its
own trace file can drop the tag.

**`${SYS_VAR_CI}` is gone.** Removing the gate left it with no reader, so the variable
(`atest/test/variables.resource`) and `inv atest-global-pythonpath`'s `--variable SYS_VAR_CI:True`
(`tasks.py:1158`) were both deleted. The task itself stays; it is about the global pythonpath, not
about this variable.

**Why `robotstatuschecker` matters here.** An intermediate version of this work used `Skip If`
instead of deleting the gate. `robotstatuschecker` failed the run — *"Expected PASS status, got
SKIP"* — because a skip is only allowed when the test documentation declares it. The repository
already refuses silent skips; that tooling is the reason this class of bug is worth hunting
rather than assuming. **[M]**

## 4. `launch-browser-server` — covered, with one documented hole

`Launch Browser Server Via CLI` and `Launch Browser Server Via CLI With Proxy`
(`playwright_state.robot:445,487`) start the real command with `Start Process` and *separate
arguments*, so the shell bug in §3 never applied to them. The proxy case points the server at a
dead proxy on port 1 and requires `net::ERR_PROXY_CONNECTION_FAILED`, so the option provably
reaches the browser rather than being accepted and ignored. **[M]**

**Accepted as manual:** the `KeyboardInterrupt` branch (`__main__.py:459`). The acceptance
test tears the server down with `Terminate All Processes`, i.e. SIGTERM, so the Ctrl-C path is
never entered in CI. Hand-checked under ticket 0005.

## 5. `clean-node` — asserted after the fact

The command runs in CI three times and always as the last step before uninstalling, so nothing
observed anything but its exit code — and it exits 0 whether it deleted the dependencies or found
nothing to delete. Two additions:

- **`.github/scripts/verify_clean_node.py`**, run immediately after `rfbrowser clean-node` and
  before `pip uninstall` at all three sites (`on-push.yml:355,539`, `on-release.yml:222`). It
  locates the *installed* package with `importlib.util.find_spec` and fails if
  `wrapper/node_modules` survives. Both branches were exercised locally. **[M]**
- **`utest/test_clean_node.py`**, which pins the deletion semantics against a stand-in
  installation directory, including two things worth knowing:
  - browser binaries go with the dependencies **because they live inside them** —
    `get_playwright_browser_path()` returns `node_modules/playwright-core/.local-browsers` when
    `PLAYWRIGHT_BROWSERS_PATH` is unset. `clean_node` does not remove them separately, so if that
    default ever moves outside `node_modules` the command needs a second deletion; the test goes
    red if it does. **[M]**
  - browsers installed **outside** the default location survive `clean-node`. That is a
    documented limit, matching the command's "from the library default installation location"
    wording — not a defect. A user who set `PLAYWRIGHT_BROWSERS_PATH` removes them themselves.
    **[M]**

The utests were mutation-checked: removing the `shutil.rmtree` call turns three of them red. **[M]**

## 6. `uninstall` — accepted as manual, with the delegation automated

**It cannot run end to end on a runner.** `npx playwright uninstall` removes the shared browser
binaries, which every test after it in the same job needs. Running it for real would either break
the job or require a dedicated one whose only purpose is to delete browsers and stop.

What is automated instead, in `utest/test_entry_uninstall.py`: that the command delegates to
`npx playwright uninstall`, that `--all` is forwarded, and that
`ensure_playwright_browsers_path()` runs *before* the library is constructed — without which npx
looks in Playwright's own default location rather than this installation's, and removes nothing.
**[M]**

**A side effect worth knowing about.** `ensure_playwright_browsers_path()`
(`Browser/entry/constant.py:121`) writes `PLAYWRIGHT_BROWSERS_PATH` into `os.environ` and never
removes it. Harmless for a one-shot CLI process, but it means the command cannot be invoked
in-process without isolating that variable: an early version of
`utest/test_entry_uninstall.py` did not, and it pointed the other 23 browser-backed unit tests
at a browser directory that does not exist. The fixture stubs it for that reason. **[M]**

One property pinned deliberately rather than fixed: the npx call is wrapped in
`contextlib.suppress(Exception)` (`__main__.py:555`), so a failure to remove the binaries still
exits 0 and reports nothing. **That is why the exit code alone was never evidence**, and why the
test asserts on the delegation. Whether the suppression should stay is a separate question and
was not opened here.

## 7. Decision: `convert_options_types` keeps its conversion

`launch-browser-server` converts its options twice — once in `convert_options_types`
(`__main__.py:470`), once again when line 451 calls the keyword by attribute access and ticket
0003's proxy converts them a second time. Conversion is idempotent and this is safe. The question
raised in the 0003 review was whether the first conversion still earns its place.

**Decision: keep it.** Maintainer's call, 2026-08-19. Three reasons:

1. **The error contract stays in one style.** The function's two failure modes both report as a
   `RuntimeError` naming the *CLI option*. Dropping the conversion moves bad *values* onto Robot
   Framework's `ValueError`, which names the *keyword argument* instead, while bad *names* keep
   the old wording — two failure modes, two vocabularies, for one command.
2. **The lookup is already paid for.** Key validation has to stay whatever happens, and it
   already calls `get_keyword_types`. The conversion on top of it is nearly free.
3. **It keeps the CLI self-sufficient.** Deleting it would make the command's correctness depend
   on the `attributes` proxy, which rests on a PythonLibCore internal (ADR 0006). Six explicit
   lines are cheaper than that coupling.

`utest/test_convert_options_types.py` now pins the contract — it did not exist before, despite
both ticket 0011 and the handoff stating that it did. **If the conversion is ever dropped, the
two error-shape tests in that file are the ones to rewrite, and the argument belongs there.**

**Also fixed:** `converter_for(...)` was called with `.convert` chained directly onto it, with no
`None` guard. On Robot Framework <= 7.2 an unconvertible option type returns `None` there and the
user would get `AttributeError: 'NoneType' object has no attribute 'convert'`. It is now guarded
and raises the same CLI-shaped `RuntimeError` as the neighbouring failures. **Not reachable
today** — all 21 `launch_browser_server` option types convert on both supported Robot Framework
versions, and `test_every_launch_browser_server_option_is_convertible` fails and names the option
if that ever stops being true. **[M]**

## 8. Standing rules this ticket leaves behind

- **A command that runs as CI setup or teardown is not covered.** Its exit code is the only thing
  observed, and `clean-node` and `uninstall` both exit 0 on doing nothing.
- **Never gate a test on a condition that makes it log and pass.** Skip it, so it reports as
  skipped, or delete the condition. `robotstatuschecker` enforces this as long as the test
  actually reaches a skip.
- **Never pass a list to `subprocess` with `shell=True`.** On POSIX every argument after the
  first is silently dropped. `atest/library/os_wrapper.py:get_enty_command` returns a *string*
  for keywords that use `Run Process    shell=True`; `show_trace_tool.py` keeps its own argv
  *list* because it starts processes without a shell. Do not mix the two.
- **A test that consumes another test's artifact must carry that test's exclusion tags.**
  Otherwise a filtered run keeps the consumer and drops the producer, and the consumer fails on a
  missing input rather than on the thing it tests.
- **Verify an inventory before extending it.** Four of nine rows here were wrong, in the
  direction of claiming more coverage than existed.
