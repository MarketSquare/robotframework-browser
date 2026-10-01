---
name: ci-failure-triage
description: 'Triage one failing CI acceptance test to a verdict: cause, evidence, route. Use when the maintainer names a test from `inv ci-report` to triage.'
argument-hint: 'The Test Name, as `inv ci-report` spells it'
---

# CI failure triage

Takes one test the maintainer chose and ends on a **verdict**: the cause, the evidence that proves it, and the **route** it takes. Triage only — the fix itself belongs to this skill only when the route says "fix on the spot".

The words below — Test Name, Group, Occurrence, Leg, Attempt, Adjacent Run, Fixture Failure, Failure Scope, Configuration, Inconclusive Zero, Known Cause — mean what `tools/ci_failures/CONTEXT.md` says. `tools/ci_failures/README.md` has every task and flag. `inv ci-report` and `inv ci-artifact` are the whole data path: every question about CI goes through them, never straight to the database.

## Steps

### 1. Read the report

```bash
inv ci-report --test "<Test Name>" --days <n>
```

Start with `--days 7`; widen when the Group is rare. A name in no Result is refused with the Test Names it may mean; use one of those. A test that ran without failing gets one line saying how often it ran. Read every Group of the test, its `known_cause`, `where_to_look`, the per-Configuration `rates`, and each Occurrence's Adjacent Runs, `retry`, `log` and `also_failed_in_this_leg`. When the Group already has a Known Cause with `fixed_by` set, check each Occurrence's `commit` with `git merge-base --is-ancestor <fixed_by> <commit>`: a failure on a commit that contains the fix means the fix did not hold — say so first, it changes the question. Failures on commits without the fix are the old cause.

Done when you can state, with numbers: how often it fails and over what, on which Configurations, whether later Attempts pass, and which class below it most resembles.

### 2. Fetch artifacts, when the report is not enough

```bash
inv ci-artifact --run <run> --leg "<leg>" --attempt <attempt> --test "<Test Name>"
```

Pass all four from the same Occurrence — a re-run Leg uploads once per Attempt, and the wrong one holds a pass. It prints the files that bear on the test, by path inside the artifact: `output.xml` and `log.html`, the Executor's own files, the `test-app` log of each test app the test's suite setups started (`responseTimeMs` per request), and every file the test's log links to — screenshots, the node log — with `MISSING` for any the artifact lacks. Everything else is counted on the `also:` line. Done when the failing Attempt's files are local. The same call on a Leg where the test passed gives the control to compare against. No screenshot is normal when the failing keyword's `keyword_kind` is not `library` — an assertion in `atest/library`, say — because only the Browser library takes one on failure; it does not mean the artifact is broken. Exit code 3 means the download failed: **ask** the maintainer whether to retry or continue from the report alone — they are sometimes on a limited connection.

### 3. Prove the cause

Use the `mattpocock-skills:diagnosing-bugs` skill. A cause counts as proven when it is reproduced locally or shown by an artifact; anything less is a hypothesis and the verdict says so.

### 4. Give the verdict

Cause, evidence, route:

| library change needed? | fixable in this context? | route |
| --- | --- | --- |
| yes (any size) | — | GitHub issue, type **Bug** or **Feature** |
| no (test / test app) | yes | fix on the spot; the commit message carries the cause |
| no (test / test app) | no | GitHub issue, type **Task** |

The route follows from where the change lands, not from how big it is.

### 5. Propose the Known Cause, and wait for agreement

Record one only when all three hold: the cause is proven (step 3), the signature matches the Group, and it is agreed — either side proposes, the other accepts. Add it to `tools/ci_failures/known_causes.json` (gitignored) in the shape of the existing entries:

- `test`, `signature` — exactly as the report gives them
- `cause` — one line and a pointer, e.g. `Timing ceiling measured runner speed; fixed in #1234`. The PR is the best pointer: it explains what was done, references the issue, and everything else can be traced from it
- `reference` — the issue URL, or `null` for an on-the-spot fix
- `recorded` — today's date
- `fixed_by` — a bare commit SHA **on `main`**, filled only once the fix has landed there; `null` until then. Never the branch commit: a rebase or squash gives the fix another SHA on `main`, and `inv ci-verify-fixes` reports a SHA that is not on `origin/main` as `not on main` rather than counting it
- `fix_verified` — `null`; triage never fills it. `inv ci-verify-fixes --mark` does, once the fix has held for seven days

### 6. Act on the route

- **Fix on the spot**: make the change, run the test locally, commit with the cause and evidence in the message. Leave `fixed_by` `null`; once the change is on `main`, put the SHA it has there.
- **Issue**: draft title and body (cause, evidence, run links) and show it to the maintainer. File only on approval: `gh issue create --type <Bug|Feature|Task>`. The issue type field is what keeps Task out of the release notes, so it carries the classification on its own, with no label. Implementing it is a separate task for other skills.

Then `inv ci-artifact --clean`. Done when the route is acted on, the Known Cause is agreed or declined, and the artifacts are gone.

The Known Cause plus the commit message or issue is the whole record — the triage leaves no markdown write-up behind.

## Classes, and where to look for each

- **Shared node process state** — pabot workers share one node process (`tasks.py`), so module-level state in `node/playwright-wrapper` leaks between workers. Everything meant to be per-worker is keyed by gRPC peer in `grpc-service.ts`. Seen twice: `highlightDisposableCache` in `playwright-state.ts` (fixed per peer in #5211) and the logger's RF context (#5260).
- **Timing limits in tests** — a wall-clock ceiling measures runner speed, not the library. Examples: `atest/library/event_delay.py` (key timings), `08_Scope_Tests` (#5223).
- **Fixture failures** — one broken suite setup or teardown looks like many flaky tests. The report lists the Fixture Failures of the enclosing suites, counted per Leg (Failure Scope in `CONTEXT.md`).
- **Platform-only failures** — read the per-Configuration rates and the Inconclusive Zeros before calling any platform healthy.
- **Chromium protocol flakes** — e.g. `Page.captureScreenshot` refusing the first capture on `darwin` (#5237, closed as wontfix, worked around in the test).

## Reproducing CI timing locally

Learnt the hard way:

- Plain CPU busy-loops (`yes > /dev/null`) and `taskpolicy -c background` slow nothing down on Apple silicon.
- Chrome's `Emulation.setCPUThrottlingRate` over a CDP session does: 8–16× turned a 0.7% CI flake into 45–70% locally. Results drift between runs; compare modes within one session.
- A standalone Playwright script needs `PLAYWRIGHT_BROWSERS_PATH=0` to find the library's browsers (`Browser/playwright.py`).
- When the timing window lies entirely inside the node process (no gRPC hop), a script copying the node loop is a valid stand-in for the full robot run.
