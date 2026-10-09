# Every test artifact of a Run is a Leg, whatever job uploaded it

The database used to hold only the `testing` job's artifacts, `Test results-*`. The clean
install check (`test-install`), the BrowserBatteries wheel check and the docker image check
upload a full `output.xml` from the same Run and were never read. That was a deliberate choice:
their Linux Legs run the smoke selection, so they would not share a denominator with the rest.
It was the wrong one. A test that failed only on an installed wheel, only with the bundled Node.js,
or only in the container was invisible. So was the batteries check failing roughly one run in
ten on real test failures (`Add Valid Credential With Secret` twice on Windows in twenty runs)
while nothing reported it.

The denominator worry did not hold up. A rate is a test's failures over that test's own
executions, so a Leg that ran a subset adds to both sides for the tests it ran and to neither
side for the rest. What differs between the jobs is recorded instead of filtered out: each Leg
has an **Install** (`source`, `wheel`, `batteries`, `docker`), read from its artifact name,
and the Install is part of its **Configuration**. So "fails only on wheel installs" reads the
same way as "fails only on darwin". The non-`source` Legs also run serially rather than as
parallel shards, and that is a feature. They miss what parallel execution provokes and show
what it hides.

`on-release.yml` stays out. The reason is no longer that it runs smoke; it is a separate
workflow run about once a month, which is too few Runs to move a rate.

## Consequences

- The docker job used to run `robot` on the mount root, which gave every test name an extra
  `Test.` level and put its metadata where the parser does not look. It now mounts `atest/` at
  `/home/pwuser/atest` and runs `atest/test`, like every other Leg. Older docker artifacts are not
  special-cased. Every Leg's root suite has to be `atest/test`, and one that is not is marked
  unusable with the layout it had. The same check catches the next job whose layout drifts,
  which would otherwise quietly split every test into two.
- A zip that opens but holds an `output.xml` that will not parse is remembered as unusable, like
  one that holds none. It is what a job killed by its timeout leaves, and it never parses however
  often it is downloaded. A download that fails, or a zip that will not open, is still retried.
- A Leg is shown under one name shape whichever job ran it: its Install, then the runner, shard,
  Python and Node the artifact name carries (`wheel · ubuntu-latest · 3.13 · 24.x`). The raw
  names follow four conventions that only say how each upload step was written.
- Failures per leg are counted per platform *and* Install. A `source` Leg is one parallel shard
  and every other Leg a whole suite, so counting both as "one leg" would make the ratio mean
  something different on every platform. "Never ran on" stays platform-only: the smoke selection
  leaves the slow tests out of most non-`source` Legs by design, and saying so on every slow test
  would be noise.
