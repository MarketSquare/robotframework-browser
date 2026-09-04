# CI Failure Analysis

Terminology for `tools/ci_failures`, which answers which acceptance tests fail in CI and on
which error, by reading the artifacts each GitHub Actions run leaves behind. A maintainers'
tool: it reads this repository's CI, imports this repository's library, and ships with the
repository rather than with the package.

`README.md` beside this file is how to run it and how the pieces fit together. This file is
only what the words mean.

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

**Subject**:
What failed, and what its failures are counted against: a test, counted in Results, or a suite
fixture, counted in Legs. A Group and a Fixture Failure are each one Subject and one Error
Signature, which is why a Known Cause and a Snapshot can key on both with one key.
_Avoid_: entity, target, owner (which is the Scope Owner), thing

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

**Report**:
Everything one run of the tool has to say about a Window: every Group, every Fixture Failure,
every Occurrence and the rules they were counted under, complete and independent of how it is
displayed. One question asked of the database, answered once.
_Avoid_: document, payload, output, the page, the JSON

**Rendering**:
One display of a Report — the page a person reads, or the plain-data document an agent reads.
A Rendering may show less than the Report holds; it can never hold more, and what it leaves out
is a choice rather than an absence.
_Avoid_: renderer, view, output format, report (for the file on disk)

**Window**:
The span of whole local calendar days a report covers, counted back from today inclusive: one
day is today, two is today and yesterday. A hard scope — every count, rate and denominator in
a windowed report comes from Runs inside it, and a test that did not fail inside it does not
appear at all. That is what lets it answer "has what I fixed come back", which no all-history
report can.
_Avoid_: range, period, timeframe, since

**Short Window**:
A Window that asked for more days than the archive holds, and the report saying so: what was
asked from, what the archive begins at, and how many days of the question were never ingested.
Both halves were always in the report - the label said one and `since` said the other - and
nothing put them together, so `--days 60` over a sixteen-day database read as sixty days of
evidence. Absent, not zero, whenever the archive covers the question.
_Avoid_: gap, missing data, incomplete (which is about a Leg that would not parse)

**Reading**:
The database as one Report reads it: restricted to that Report's Window, with the Subject views
resolved on top of it. Made once and asked every question, because building one costs a pass over
every Result row and the answers all want the same restriction. Both halves have to have happened
before any query runs, and a Reading is the only thing the queries accept, so there is no way to
ask a question of an unrestricted database by accident.
_Avoid_: connection, session, scope (which is a Failure Scope) - and note that "reading the
artifacts", elsewhere in this file, is the ordinary verb rather than this.

**Known Cause**:
A conclusion someone reached by reading the artifacts, recorded by hand in `known_causes.json`
and matched against a Group at report time. The one thing here not derived from the database,
and gitignored all the same: this tool is run by one maintainer on one machine, and a conclusion
that matters is acted on rather than filed. It is therefore the only thing here that no rebuild
and no download can restore — which is accepted, not overlooked.
_Avoid_: annotation, note, triage

**Snapshot**:
What the last report said, written beside the database so the next report can say what is new,
gone or changed. Entirely derived and worth nothing once stale. Never taken from a windowed
report, and never read by one: a baseline that covered less data would make every Group look as
though it had grown, and one that covered more — after a rebuild shortened the archive — would
make every Group look as though it had shrunk. Both are silent, because both sets of numbers
are plausible.
_Avoid_: baseline (as the file), history

**Adjacent Run**:
The Run immediately before or after this one on the same Leg, and the outcome the same Subject
had in it. Compared per Leg and never per Run: a test that only fails on win32 has nothing to
learn from the linux run that happened to come next. The outcome is one of five - `pass`, `fail`,
`mixed`, `skip` or `suite broke`. A Subject marked failed by a Fixture Failure has no outcome here
at all: its suite broke, not it, and that is neither a pass nor a fail, which is what the fifth
value is for.
_Avoid_: neighbouring, surrounding, nearby - and never for the keywords before a failure inside
one test, which is a different question this tool does not answer.

**Inconclusive Zero**:
A configuration that has failed nothing yet, where a configuration exactly as broken as the
others would also have shown nothing this often. The distinction between evidence of health
and absence of evidence, reported next to the zero because the reader's next move depends on
which one it is.
_Avoid_: clean, passing, green


## Relationships

- A **Report** covers exactly one **Window** and is built of **Groups** and **Fixture Failures**
- A **Group** and a **Fixture Failure** are each one **Subject** and one **Error Signature**,
  and differ in what their **Occurrences** are counted in: Results for a test, Legs for a fixture
- A **Group** has one or more **Occurrences**; a **Fixture Failure**'s Occurrence is one **Leg**
- A **Report** has many **Renderings**, and every **Rendering** shows the same Report
- An **Occurrence** may have an **Adjacent Run** either side of it, on its own **Leg**
- A **Snapshot** is what one **Report** said, kept so the next one can say what changed
- A **Report** is built from exactly one **Reading**, and a **Reading** carries exactly one
  **Window**

## Flagged ambiguities

- "report" was used for three things — the Report, a Rendering of it, and the file a Rendering
  is written to. Resolved: the **Report** is the answer, a **Rendering** is a display of it, and
  a file is just where a Rendering was written.
- "scope" means three things here and only two of them are terms. A **Failure Scope** is what
  broke and a **Scope Owner** owns the fixture it names, while `window.py` calls the Window "a
  hard scope" in the ordinary English sense. That is why the restricted connection is a
  **Reading** and not a Scope.
