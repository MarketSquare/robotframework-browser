# Client-side page event logger is a plain JS static file, not TypeScript

The client-side script that captures browser page events (`node/dynamic-test-app/static/test-app-logger.js`) is written as plain JavaScript and served directly by `express.static`. It is not compiled via the esbuild pipeline used for `server.ts`.

## Considered Options

- **Plain JS static file (chosen):** Zero build-step involvement. The file is served as-is and works immediately. No changes to `node/build.testapp.js`.
- **TypeScript compiled via esbuild:** Would require a new esbuild entry point in `node/build.testapp.js`, adding build complexity for a script with trivial logic (a few DOM event listeners and `navigator.sendBeacon` calls).

## Consequences

The script cannot use TypeScript types or imports. This is acceptable because the script is self-contained, has no dependencies, and its logic is simple enough that type safety provides no meaningful benefit. Adding TypeScript here would require every future contributor to understand the build pipeline in order to edit a ~50-line DOM script.
