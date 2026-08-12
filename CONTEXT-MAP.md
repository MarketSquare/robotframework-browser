# Context Map

## Contexts

- [Browser Library](./Browser/CONTEXT.md) — the keyword library itself: how a keyword call
  reaches a keyword body, from Robot Framework and from plain Python
- [Test App Rich Logging](./atest/CONTEXT.md) — correlating Robot Framework test execution
  with HTTP server activity in the acceptance test setup

## Relationships

- **Test App Rich Logging → Browser Library**: the acceptance suite drives the Browser Library
  over the **Robot Framework path** while the Test App records what the browser did. It
  observes the library from outside and shares no vocabulary with it.

System-wide decisions live in [`docs/adr/`](./docs/adr/).
