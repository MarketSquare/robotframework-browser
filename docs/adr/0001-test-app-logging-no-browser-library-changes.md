# Rich test-app logging must not touch the Browser library

The rich logging feature for `node/dynamic-test-app` — capturing RF lifecycle context and browser page events — is implemented entirely in the test infrastructure layer (`atest/library/` and `node/dynamic-test-app/`). No changes are made to the Browser library itself (`Browser/` Python package or `node/playwright-wrapper/`).

## Considered Options

- **Test infrastructure only (chosen):** A new RF listener library in `atest/library/` and new HTTP endpoints in the test app handle all logging. The Browser library is untouched.
- **Browser library integration:** Hooking into the Browser library's gRPC layer or Python keywords to emit context signals.

## Consequences

The logging is specific to this project's acceptance test setup, not a general-purpose feature of the library. Changes stay isolated to files that are clearly "test infrastructure", which makes the boundary visible and prevents the feature from leaking into the shipped library.
