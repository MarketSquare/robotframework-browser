# RF listener is a library-as-listener using @library(listener='SELF'), not a standalone listener

The Robot Framework listener that ships RF lifecycle context (suite/test start/end) to the test app is implemented as a library imported via the `Library` setting in `atest/test/__init__.robot`, using `@library(scope='GLOBAL', listener='SELF')`. It is not a standalone listener file registered via `--listener` on the command line.

## Considered Options

- **Library-as-listener with `listener='SELF'` (chosen):** Imported like any other test library. No command-line flags needed; `atest/test/__init__.robot` is the single place where test infrastructure is configured. RF 7.0+ supports `listener='SELF'` on the `@library` decorator, making the pattern clean with no `BuiltIn().register_listener(self)` boilerplate.
- **Standalone listener via `--listener`:** Would require every invocation of `robot`, `pabot`, and `inv atest` to pass the `--listener` flag. The `tasks.py` invocation task, docker `robot` call, and BrowserBatteries smoke test invocations would all need updating — and any invocation that omits the flag silently loses the logging.

## Consequences

RF emits a warning "Imported library has no keywords" because `@library` disables auto-keyword discovery and no `@keyword` methods are defined. This warning is harmless and accepted. The listener is active precisely in the suites where the library is imported, which is the entire acceptance test run.
