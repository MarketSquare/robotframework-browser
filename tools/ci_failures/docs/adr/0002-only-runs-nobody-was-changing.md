# Only runs where nobody was changing anything

The database holds CI runs on `main` from `push` and `schedule`, and nothing else. Local runs
are not ingested and there is no way to ingest one. This is a decision rather than an omission,
and it does not look like one from the code: `parse.parse()` takes a plain path and knows
nothing about GitHub, so the parsing half reads as though a local door were simply missing.

A failure earns a row when its cause is not obvious and it repeats often enough to have a rate.
A failure from a run where somebody was actively changing the code has neither property. While
developing or refactoring, essentially every local failure is a bug just introduced in the test
or the library: the cause is apparent on sight and it happens once. Genuinely random failures do
occur locally, at something like one a month from one machine — against 315 matrix legs in nine
days of CI that never accumulates into evidence, and this tool's own threshold says how far
short it falls, since at a one-in-twenty rate it takes 58 runs before even a clean sheet means
anything.

That is the same reason pull request runs are excluded, and the two should be read as one rule:
a failure attributable to the change being made is not evidence about the library. `main` with
`push` and `schedule` is the set of runs where nobody was changing anything.

None of this argues against reading a local artifact. `0013` was closed a second time from an
ordinary `inv atest`'s `playwright-log.txt` with nothing downloaded, and that is the right way
to work one failure already picked off the list. Investigating a local failure needs no
database; it is accumulating local failures into rates that is ruled out.
