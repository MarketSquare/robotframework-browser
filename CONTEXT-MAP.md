# Context Map

## Contexts

- [Browser Library](./Browser/CONTEXT.md) — the keyword library itself: how a keyword call
  reaches a keyword body, from Robot Framework and from plain Python
- [Test App Rich Logging](./atest/CONTEXT.md) — correlating Robot Framework test execution
  with HTTP server activity in the acceptance test setup
- [CI Failure Analysis](./tools/ci_failures/CONTEXT.md) — which acceptance tests fail in CI and
  on which error, read out of the artifacts each run leaves behind. Maintainers only

## Relationships

- **Test App Rich Logging → Browser Library**: the acceptance suite drives the Browser Library
  over the **Robot Framework path** while the Test App records what the browser did. It
  observes the library from outside and shares no vocabulary with it.
- **CI Failure Analysis → Browser Library**: reads the `output.xml` the acceptance suite
  produces, and imports the Browser Library itself to resolve where a failing keyword is
  defined. So unlike Test App Rich Logging it does share the library's vocabulary — **keyword**,
  **library**, **owner** — and it resolves those against the working copy, not the commit the
  run used. `playwright-log.txt`, written by the Node process the library spawns, is read by
  hand when one failure warrants it rather than ingested.

System-wide decisions live in [`docs/adr/`](./docs/adr/).
