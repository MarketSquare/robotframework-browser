# Browser Library — Electron Test App

A minimal [Electron](https://www.electronjs.org/) application used exclusively
to run the Browser library acceptance tests for Electron support.  It is **not**
distributed with the library; it exists only to exercise the keywords in CI and
locally.

## Structure

| File | Purpose |
|------|---------|
| `main.js` | Electron main-process entry point — creates the `BrowserWindow`. |
| `index.html` | Renderer page with a heading, a counter button, a text input, a select box, and a checkbox so multiple keyword categories can be tested. |
| `package.json` | Declares `electron` as a dev-dependency so the binary is available after `npm install`. |

## Building / installing

```bash
cd node/electron-test-app
npm install          # downloads the Electron binary (~80 MB)
```

No compilation step is required; `main.js` and `index.html` are loaded directly
by the Electron runtime.

## Running manually

```bash
# from the repo root
node_modules/.bin/electron node/electron-test-app/main.js
# or from inside the test-app directory
npm start
```

## CI integration

The repository `tasks.py` exposes an `electron_test_app` task that runs
`npm install` in this directory.  The CI workflow calls this task before
executing the acceptance tests.

The acceptance tests (``atest/test/01_Browser_Management/electron.robot``) read
the Electron binary path and the main-process entry-point path from Robot
Framework variables that are automatically resolved relative to the repository
root, so no environment variables need to be set on CI.

### Platform notes

| Platform | Electron binary path (after `npm install`) |
|----------|--------------------------------------------|
| Linux | `node/electron-test-app/node_modules/.bin/electron` |
| macOS | `node/electron-test-app/node_modules/.bin/electron` |
| Windows | `node/electron-test-app/node_modules/.bin/electron.cmd` |

Tests that cover UI interactions work on all three platforms.  Tests that use
`Open Electron Dev Tools` require a display; on headless CI agents this keyword
is called but its visible effect is not asserted.
