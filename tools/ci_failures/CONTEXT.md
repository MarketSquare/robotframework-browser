# CI Failure Analysis

Terminology for `tools/ci_failures`, which answers which acceptance tests fail in CI and on
which error, by reading the artifacts each GitHub Actions run leaves behind. A maintainers'
tool: it reads this repository's CI, imports this repository's library, and ships with the
repository rather than with the package.

## Language

### What a run leaves behind

**Run**:
One GitHub Actions workflow run on `main`, identified by its GitHub run id. Only `push` and
`schedule` runs are considered; a pull request run fails because of the pull request.
_Avoid_: build, job, CI run

**Leg**:
One execution of the acceptance suite within a Run — one point of the matrix, one uploaded
artifact, one `output.xml`. A Run has many Legs, each with its own platform, Python, Robot
Framework and Node versions.
_Avoid_: matrix job, matrix entry, shard

**Attempt**:
Which try of a Leg's job produced the artifact. Nothing in this CI retries automatically, so
anything above the first was a failed job re-run by hand — which is why a rate counted over
first Attempts only asks a different, cleaner question than one counted over all of them.
_Avoid_: retry, rerun (as nouns for the number)

**Result**:
One test's outcome in one Leg: pass, fail or skip. Passing Results are stored too, because a
failure count without a run count is not a rate.
_Avoid_: test run, execution

### What a failure is

**Error Signature**:
A failure message with the parts that vary between occurrences — ids, counts, timings —
masked out, so that the same problem seen five times reads as one thing. Compared
case-insensitively, because two libraries spell the same gRPC deadline differently.
_Avoid_: error type, fingerprint, hash

**Group**:
A (test, Error Signature) pair, and the unit the report is built on. One test failing on two
different errors is two Groups, because they are two problems.
_Avoid_: failure, issue, cluster

**Occurrence**:
One individual failure behind a Group — this test, this error, this Leg, this Run. A Group's
counts cannot say whether four failures are one bad commit seen four times or a problem that
survived four of them; the Occurrences can.
_Avoid_: instance, event, hit

**Failure Scope**:
What actually broke: the test itself, its setup or teardown, or a suite setup or teardown. A
suite fixture fails every test beneath it and Robot Framework records that only on the tests,
so without this one broken teardown looks like as many flaky tests as the suite has tests.
_Avoid_: failure type, level

**Scope Owner**:
The suite or test owning the fixture named by a Failure Scope. For a suite fixture this may be
an ancestor rather than the parent suite.
_Avoid_: parent, suite

**Fixture Failure**:
A suite setup or teardown that broke, counted once per Leg it broke in rather than once per
test it marked. Its denominator is Legs that ran the suite, never test rows.
_Avoid_: setup failure, teardown error

### What the report says

**Window**:
The span of whole local calendar days a report covers, counted back from today inclusive: one
day is today, two is today and yesterday. A hard scope — every count, rate and denominator in
a windowed report comes from Runs inside it, and a test that did not fail inside it does not
appear at all. That is what lets it answer "has what I fixed come back", which no all-history
report can.
_Avoid_: range, period, timeframe, since

**Known Cause**:
A conclusion someone reached by reading the artifacts, recorded by hand in `known_causes.json`
and matched against a Group at report time. Kept in version control because it is the one
thing here not derived from the database, and re-ingesting would otherwise delete it.
_Avoid_: annotation, note, triage

**Snapshot**:
What the last report said, written beside the database so the next report can say what is new,
gone or changed. Entirely derived and worth nothing once stale, which is why it is not in
version control. Never taken from a windowed report: a baseline that covered less data would
make every Group look as though it had shrunk.
_Avoid_: baseline (as the file), history

**Inconclusive Zero**:
A configuration that has failed nothing yet, where a configuration exactly as broken as the
others would also have shown nothing this often. The distinction between evidence of health
and absence of evidence, reported next to the zero because the reader's next move depends on
which one it is.
_Avoid_: clean, passing, green
