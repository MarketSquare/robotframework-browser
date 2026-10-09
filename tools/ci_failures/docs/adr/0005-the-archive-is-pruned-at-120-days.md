# The archive is pruned at 120 days

Every ingest ends by deleting each Run older than 120 days and everything recorded under it, and
then vacuums the file if anything went. Before this the database only ever grew: 521 MB over 109
days on 2026-09-24, about five megabytes a day. Nearly all of that was passing Results and their
two largest indexes, which the rates cannot do without.

The database used to be treated as history worth keeping, the only copy of anything older than
the 90 days GitHub keeps artifacts. It is not. CI changes fast enough that a failure from four
months ago says little about the library today, and old data is almost never looked at. Losing
the database costs a rebuild of 90 days, which is accepted. 120 is past those 90 days on
purpose. Ingest recognises what it already has by artifact id, and a pruned Leg's artifact has
always expired before the Leg is deleted, so pruning can never cause a download.

The limit is a constant with no flag and no command of its own. It is maintenance, not a
question anyone asks, and a prune that has to be remembered does not happen. `--days` is still
how to ask about less.

## Considered Options

- **Delete only the passing Results.** This removes almost all of the bulk and keeps every
  failure, but it leaves old Groups with no denominators, and a failure count without a run
  count is not a rate.
- **Collapse old passing Results into counts.** This keeps the rates, but every query that
  computes one would have to read two storage models.
