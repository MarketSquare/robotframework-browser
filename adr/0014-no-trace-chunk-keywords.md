# No trace chunk keywords

Playwright's tracing has two levels: `start` / `stop` and, inside them, `startChunk` /
`stopChunk`. Ad-hoc tracing (#5122) exposes only the first level, as `Start Tracing` and
`Stop Tracing`. To get one small trace per scenario from one long-lived context, a test stops
tracing and starts it again. Chunks get no keywords and are not used by the library.

A prototype on Playwright 1.64.1 showed that chunks run one after another and never nest.
`startChunk` silently discards whatever was recorded since the last `start` or `startChunk`.
`stop({path})` saves only the chunk that is recording, and throws
`Must start tracing before stopping` when none is. So "one full trace plus smaller chunk traces"
cannot be built from them. They also break the **context trace** of `New Context    tracing=`,
which is saved with `stop({path})` when its context closes: after a `stopChunk` that call
throws, and after a `startChunk` everything recorded before it is lost. Calling `stop` and then
`start` again on the same context works and gives clean, separate traces.

## Considered options

- **Four keywords, as first proposed: `Start Tracing`, `Stop Tracing`, `Start Trace Chunk`,
  `Stop Trace Chunk`.** Rejected: the full trace the proposal promised cannot exist, chunks
  conflict with `tracing=`, and two more keywords bring nothing that stopping and starting
  again does not.
- **`Start Tracing` starts a chunk when tracing already runs.** Rejected: it would silently
  drop what the running trace has recorded so far. Starting a trace while one runs is a mistake
  in the test and fails instead.

## Consequences

- A context runs at most one trace at a time, a **context trace** or an **ad-hoc trace**.
  `Stop Tracing` stops either kind.
- Playwright's `name` and `live` options of `start` are not exposed: the library manages the
  temporary trace files itself, and `live` serves Playwright's UI mode, not a saved zip.
- The prototype is kept on the local branch `prototype/trace-chunks`; its results table is on
  #5122.
