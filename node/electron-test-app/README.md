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

The acceptance tests (``atest/test/01_Browser_Management/electron.robot``) run
**without skipping** on all platforms in CI. The suite setup runs `npm install`
inside this directory automatically, so the Electron binary is downloaded fresh
on each CI run — no pre-built binaries are committed to the repository.

### Step-by-step CI setup (Linux)

Electron always opens a native GUI window. On headless Linux agents you must
provide a virtual display **before** starting the test run:

```bash
# 1. Install Xvfb (once, during environment setup)
sudo apt-get install -y xvfb

# 2. Start a virtual display
Xvfb :99 -screen 0 1280x720x24 &
export DISPLAY=:99

# 3. Run the project build (compiles protobuf, builds the Node wrapper)
invoke build

# 4. Run the Electron acceptance tests
robot atest/test/01_Browser_Management/electron.robot
```

The `DISPLAY` variable must be set in the same shell that runs `robot`.

### Platform notes

| Platform | Electron binary path (after `npm install`) | Virtual display needed? |
|----------|--------------------------------------------|------------------------|
| Linux    | `node/electron-test-app/node_modules/.bin/electron` | Yes — Xvfb or Xvnc |
| macOS    | `node/electron-test-app/node_modules/.bin/electron` | No                    |
| Windows  | `node/electron-test-app/node_modules/.bin/electron.cmd` | No               |

### What the test suite setup does

The Robot Framework suite setup in `electron.robot` performs the following steps
automatically before any test case runs:

1. Detects the current platform (`sys.platform`).
2. Runs `npm install` in `node/electron-test-app/` to download the Electron
   binary for that platform.
3. Resolves the correct binary path for the platform and stores it in
   `${ELECTRON_BIN}`.

No manual setup beyond providing a `DISPLAY` on headless Linux is required.
