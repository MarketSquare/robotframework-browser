# Electron Support — Handover & Developer Guide

This document covers everything about the Electron support feature added to the
Browser library: what changed, the new keywords, the test app, and how to get
everything running locally or in CI.

---

## Table of Contents

1. [What Was Done (PR Overview)](#1-what-was-done-pr-overview)
2. [Files Changed in the PR](#2-files-changed-in-the-pr)
3. [Architecture — How It Works](#3-architecture--how-it-works)
4. [New Keywords](#4-new-keywords)
   - [New Electron Application](#new-electron-application)
   - [Close Electron Application](#close-electron-application)
   - [Open Electron Dev Tools](#open-electron-dev-tools)
5. [The Test Application](#5-the-test-application)
6. [Acceptance Tests](#6-acceptance-tests)
7. [Local Setup — Run Everything From Scratch](#7-local-setup--run-everything-from-scratch)
8. [CI Setup](#8-ci-setup)
9. [Known Constraints & Design Decisions](#9-known-constraints--design-decisions)

---

## 1. What Was Done (PR Overview)

This PR adds **first-class Electron application support** to the Browser library.
Before this change, it was not possible to use Browser library keywords against
an Electron desktop application window. After this change, the standard keyword
set (`Click`, `Get Text`, `Fill Text`, `Wait For Elements State`, …) works
against any Electron app with no extra setup beyond calling `New Electron
Application`.

**Summary of changes:**

- Added 3 new Robot Framework keywords (`New Electron Application`,
  `Close Electron Application`, `Open Electron Dev Tools`).
- Added 3 new gRPC RPC methods to the protobuf definition
  (`LaunchElectron`, `CloseElectron`, `OpenElectronDevTools`).
- Implemented the RPC handlers in the Node.js Playwright wrapper
  (`playwright-state.ts`).
- Added a minimal Electron test application in `node/electron-test-app/`
  with source code in the repository (no pre-built binaries committed).
- Added a full acceptance-test suite (20 test cases) in
  `atest/test/01_Browser_Management/electron.robot`.
- Added an `inv electron_test_app` invoke task for local setup.

---

## 2. Files Changed in the PR

| File | What changed |
|------|-------------|
| `protobuf/playwright.proto` | Added `ElectronLaunch` message and three RPC methods: `LaunchElectron`, `CloseElectron`, `OpenElectronDevTools`. |
| `Browser/keywords/electron.py` | New file — implements the three Python keyword classes. |
| `Browser/keywords/__init__.py` | Registers the `Electron` keyword class so it is exposed by the library. |
| `Browser/browser.py` | Imports and mixes in the `Electron` keyword class. |
| `node/playwright-wrapper/playwright-state.ts` | Implements `launchElectron`, `closeElectron`, `openElectronDevTools` Node.js functions. |
| `node/playwright-wrapper/grpc-service.ts` | Wires the three new RPC handlers into the gRPC server. |
| `tasks.py` | Adds the `electron_test_app` invoke task (`inv electron_test_app`). |
| `node/electron-test-app/main.js` | Electron main-process entry point for the test app. |
| `node/electron-test-app/index.html` | Renderer page with interactive elements used by the tests. |
| `node/electron-test-app/package.json` | Declares `electron` as a dev-dependency for the test app. |
| `node/electron-test-app/.gitignore` | Ignores `node_modules/` and socket files inside the test app. |
| `node/electron-test-app/README.md` | This file — developer guide. |
| `atest/test/01_Browser_Management/electron.robot` | 20 acceptance test cases covering all new keywords. |

**Not in the PR (generated on the fly by `invoke build`):**

| Path | How to regenerate |
|------|-------------------|
| `Browser/generated/playwright_pb2.py` | `invoke protobuf` |
| `Browser/generated/playwright_pb2.pyi` | `invoke protobuf` |
| `Browser/generated/playwright_pb2_grpc.py` | `invoke protobuf` |
| `Browser/wrapper/index.js` | `invoke node_build` |
| `Browser/wrapper/static/selector-finder.js` | `invoke node_build` |
| `node/playwright-wrapper/generated/*.js` | `invoke protobuf` |

These paths are listed in `.gitignore` and must never be committed.

---

## 3. Architecture — How It Works

```
Robot Framework test
       |
       | keyword call
       v
Browser/keywords/electron.py   (Python)
       |
       | gRPC call  (LaunchElectron / CloseElectron / OpenElectronDevTools)
       v
node/playwright-wrapper/grpc-service.ts  (Node.js gRPC server)
       |
       | delegates to
       v
node/playwright-wrapper/playwright-state.ts  (launchElectron etc.)
       |
       | Playwright API
       v
electron.launch()  →  ElectronApplication  →  Page (first window)
```

The Electron window is attached to the Browser library's internal browser/context/page
stack in exactly the same way as a regular `New Persistent Context` call. This
means every existing Browser library keyword that works on a `Page` also works on
an Electron window — no special handling is required in test code.

**State management:**

`PlaywrightState` holds an `electronApp: ElectronApplication | null` field.
When `launchElectron` runs it stores the handle there. `closeElectron` reads
it back and calls `app.close()`, then pops the browser from the stack.
`openElectronDevTools` calls `app.evaluate(...)` to reach the main process where
the Node.js/Electron API is available (the renderer `Page` context cannot access
`BrowserWindow`).

---

## 4. New Keywords

### New Electron Application

```
New Electron Application
    executable_path    Path to the Electron binary or packaged app executable.
    args               List of CLI args forwarded to the Electron process.
    env                Dict of extra environment variables (merged on top of process.env).
    timeout            Max wait for the first window. Default: 30 seconds.
    acceptDownloads    Auto-download attachments. Default: True.
    bypassCSP          Bypass Content-Security-Policy. Default: False.
    colorScheme        Emulate prefers-color-scheme: dark | light | no-preference.
    cwd                Working directory for the Electron process.
    extraHTTPHeaders   Extra HTTP headers sent with every renderer request.
    geolocation        Emulate geolocation {latitude, longitude, accuracy?}.
    hasTouch           Enable touch events on the viewport.
    httpCredentials    HTTP Basic Auth credentials {username, password}.
    ignoreHTTPSErrors  Ignore HTTPS errors. Default: False.
    isMobile           Emulate a mobile device.
    javaScriptEnabled  Enable JS in the renderer. Default: True.
    locale             Renderer locale, e.g. en-GB.
    offline            Emulate offline network. Default: False.
    recordHar          Enable HAR recording {path, omitContent?}.
    recordVideo        Enable video recording {dir, size?}.
    slowMo             Slow down all operations by this duration. Default: 0.
    timezoneId         Override system timezone, e.g. Europe/Berlin.
    tracesDir          Directory for Playwright trace files.
    viewport           Viewport dimensions. Default: 1280x720. None = native size.
```

**Returns:** `(browser_id, context_id, NewPageDetails)` — the same tuple shape
as `New Persistent Context`. You can capture it and use `Switch Page` if multiple
windows are open.

**Bare electron binary example (development checkout):**
```robotframework
@{args}=    Create List    node/electron-test-app/main.js
New Electron Application
...    executable_path=node/electron-test-app/node_modules/.bin/electron
...    args=@{args}
Get Title    ==    My App
```

**Packaged application example:**
```robotframework
New Electron Application    executable_path=/usr/share/myapp/myapp
Get Title    ==    My App
```

**With locale and video recording:**
```robotframework
&{VIDEO}=    Create Dictionary    dir=output/videos
New Electron Application
...    executable_path=/usr/share/myapp/myapp
...    locale=fr-FR
...    viewport={'width': 1920, 'height': 1080}
...    recordVideo=${VIDEO}
```

---

### Close Electron Application

```
Close Electron Application
```

Closes the running Electron application and removes it from the Browser library
state stack. Equivalent to `Close Browser` for Electron apps.

- Safe to call when no app is open — logs a message and does nothing.
- After calling this there is no active browser; call `New Electron Application`
  or `New Browser` before any further page interactions.
- Always use in `[Teardown]` to ensure cleanup even on test failure.

**Example:**
```robotframework
New Electron Application    executable_path=/path/to/app
# ... test steps ...
[Teardown]    Close Electron Application
```

---

### Open Electron Dev Tools

```
Open Electron Dev Tools
```

Opens the Chromium DevTools panel for every window of the running Electron
application. Uses `ElectronApplication.evaluate()` to call
`BrowserWindow.getAllWindows().forEach(w => w.webContents.openDevTools())` in
the Electron **main process** (not the renderer).

- Intended as a **debug-time aid** — use it to inspect the DOM, find selectors,
  and debug JavaScript during local development.
- Has no visible effect on headless CI agents; the test suite calls it but does
  not assert the visual outcome.

**Example:**
```robotframework
New Electron Application    executable_path=/path/to/app
Open Electron Dev Tools
Sleep    30s    # inspect the DevTools panel manually
Close Electron Application
```

---

## 5. The Test Application

A minimal Electron app lives in `node/electron-test-app/`. It exists solely to
drive the acceptance tests and is never distributed with the library.

**Source files:**

| File | Purpose |
|------|---------|
| `main.js` | Creates an 800x600 `BrowserWindow` with `contextIsolation: true` and loads `index.html`. |
| `index.html` | Renderer page with interactive elements for every test category (see below). |
| `package.json` | Dev-dependency on `electron ^35`. No build step. |
| `.gitignore` | Ignores `node_modules/` and `.PIPE` socket files. |

**Interactive elements in `index.html`:**

| Element | Selector | Tests |
|---------|----------|-------|
| Heading | `css=h1#title` | `Get Text` |
| Click counter button | `css=#btn-click` | `Click`, `Get Text` |
| Counter display | `css=#click-counter` | `Get Text` |
| Text input | `css=#text-input` | `Fill Text`, `Get Property`, `Keyboard Key` |
| Description paragraph | `css=#description` | `Get Text` (live-mirrors the input) |
| Select box | `css=#select-box` | `Select Options By`, `Get Selected Options` |
| Checkbox | `css=#checkbox` | `Check Checkbox`, `Get Checkbox State` |
| Toggle button | `css=#btn-toggle` | `Click`, `Wait For Elements State` |
| Toggle target div | `css=#toggle-target` | `Wait For Elements State`, `Get Text` |
| Async load button | `css=#btn-async` | `Click`, `Wait For Elements State` (800 ms delay) |
| Async output span | `css=#async-output` | `Wait For Elements State`, `Get Text` |
| File input | `css=#file-input` | `Upload File By Selector` |
| File name display | `css=#file-name` | `Get Text` |

**Running the test app manually:**
```bash
cd node/electron-test-app
npm install
npm start
# or from the repo root:
node_modules/.bin/electron node/electron-test-app/main.js
```

---

## 6. Acceptance Tests

File: `atest/test/01_Browser_Management/electron.robot`

**Suite setup** (runs once before all tests):
1. Detects the current platform (`sys.platform`).
2. Runs `npm install` in `node/electron-test-app/` — downloads the Electron binary.
3. Sets `${ELECTRON_BIN}` to the platform-specific binary path.

**No tests are skipped.** Every test case runs on all platforms in CI.

**Test cases and what they cover:**

| Test case | Keyword(s) exercised |
|-----------|---------------------|
| New Electron Application Returns Browser Context And Page Ids | `New Electron Application` — return value shape |
| Title Is Correct After Launch | `Get Title` |
| Heading Text Is Readable | `Get Text` |
| Click Increments Counter | `Click`, `Get Text` |
| Fill Text Updates Input Value | `Fill Text`, `Get Property` |
| Fill Text Triggers Input Event | `Fill Text`, `Get Text` (JS event listener) |
| Select Option Works | `Select Options By`, `Get Selected Options` |
| Check Checkbox Works | `Check Checkbox`, `Get Checkbox State` |
| Wait For Elements State Works | `Wait For Elements State` (hidden → visible → hidden) |
| Async Content Appears After Delay | `Wait For Elements State` with timeout (promise path) |
| Keyboard Input Works | `Keyboard Key` (Ctrl+A, Delete) |
| File Input Accepts A File | `Upload File By Selector`, `Get Text` |
| Evaluate JavaScript Returns Promise Result | `Evaluate JavaScript` with async function |
| New Electron Application With Explicit Timeout | `New Electron Application` `timeout=` param |
| Close Electron Application Removes Active Browser | `Close Electron Application` — post-close state |
| Close Electron Application When No App Open Is Safe | `Close Electron Application` — idempotent |
| New Electron Application With Invalid Path Raises Error | Error handling |
| New Electron Application With Extra Args | `args=` param |
| New Electron Application With slowMo | `slowMo=` param |
| New Electron Application With colorScheme Dark | `colorScheme=` param |
| New Electron Application With acceptDownloads False | `acceptDownloads=` param |
| New Electron Application With bypassCSP | `bypassCSP=` param |
| Open Electron Dev Tools Does Not Raise | `Open Electron Dev Tools` |

---

## 7. Local Setup — Run Everything From Scratch

Follow these steps to check out the branch and run the Electron acceptance tests
on your machine.

### Prerequisites

- Python 3.9+ with `pip`
- Node.js 18+ with `npm`
- (Linux only) Xvfb: `sudo apt-get install -y xvfb`

### Step 1 — Clone and check out the branch

```bash
git clone https://github.com/shenthils-ui/robotframework-browser.git
cd robotframework-browser
git checkout claude/add-electron-support-rrujh
```

### Step 2 — Install Python dependencies

```bash
pip install invoke
pip install -r requirements.txt        # or: pip install -e ".[dev]"
```

### Step 3 — Install Node dependencies (repo root)

```bash
npm install
```

### Step 4 — Build the project (protobuf + Node wrapper)

This step regenerates the files that are NOT committed (they are in `.gitignore`):

```bash
invoke build
```

What `invoke build` does:
1. `invoke deps` — installs Python dev dependencies.
2. `invoke protobuf` — compiles `protobuf/playwright.proto` into
   `Browser/generated/*.py` and `node/playwright-wrapper/generated/*.js`.
3. `invoke node_build` — bundles the Node.js wrapper into `Browser/wrapper/index.js`.
4. `invoke create_test_app` — builds any other test assets.

### Step 5 — Install Electron test app dependencies

```bash
invoke electron_test_app
# equivalent to: npm install --prefix node/electron-test-app
```

This downloads the Electron binary (~80 MB) into
`node/electron-test-app/node_modules/`.

### Step 6 — (Linux only) Start a virtual display

Electron always opens a native GUI window. On headless Linux machines you need
a virtual display:

```bash
Xvfb :99 -screen 0 1280x720x24 &
export DISPLAY=:99
```

On macOS and Windows this step is not required.

### Step 7 — Run the Electron acceptance tests

```bash
robot atest/test/01_Browser_Management/electron.robot
```

Or to run only a specific test:

```bash
robot --test "Click Increments Counter" atest/test/01_Browser_Management/electron.robot
```

### Full one-liner (Linux)

```bash
git checkout claude/add-electron-support-rrujh \
  && pip install invoke \
  && npm install \
  && invoke build \
  && invoke electron_test_app \
  && Xvfb :99 -screen 0 1280x720x24 & export DISPLAY=:99 \
  && robot atest/test/01_Browser_Management/electron.robot
```

---

## 8. CI Setup

The suite is designed to run in CI without any skipping on all three platforms.

### Linux (headless)

```yaml
- name: Install Xvfb
  run: sudo apt-get install -y xvfb

- name: Build
  run: invoke build

- name: Install Electron test app
  run: invoke electron_test_app

- name: Run Electron tests
  run: |
    Xvfb :99 -screen 0 1280x720x24 &
    export DISPLAY=:99
    robot atest/test/01_Browser_Management/electron.robot
```

### macOS / Windows

Same steps, minus the Xvfb lines.

### Platform binary paths (after `invoke electron_test_app`)

| Platform | Binary path |
|----------|-------------|
| Linux    | `node/electron-test-app/node_modules/electron/dist/electron` |
| macOS    | `node/electron-test-app/node_modules/electron/dist/Electron.app/Contents/MacOS/Electron` |
| Windows  | `node/electron-test-app/node_modules/electron/dist/electron.exe` |

The suite setup in `electron.robot` resolves the correct path automatically —
no CI environment variables need to be set.

---

## 9. Known Constraints & Design Decisions

| Topic | Decision |
|-------|----------|
| **Headless mode** | Playwright does not expose a `headless` option for Electron. The app always opens a GUI window. Use Xvfb on Linux CI. |
| **`wait_until` parameter** | Deliberately not exposed. Playwright's `electron.launch()` does not support a `waitUntil` option; the keyword blocks on `firstWindow()` only. |
| **Splash screen handling** | If `firstWindow()` returns a window with no title (a splash screen), `launchElectron` waits for the next window event automatically. |
| **env merging** | Caller-supplied `env` is merged on top of `process.env` so `PATH` and other system variables are always inherited. |
| **Single active app** | Only one Electron app can be active at a time (one `electronApp` slot in `PlaywrightState`). Multiple apps would need multiple Browser library instances. |
| **Generated files** | `Browser/generated/`, `Browser/wrapper/index.js`, and `node/playwright-wrapper/generated/` are all in `.gitignore` and regenerated by `invoke build`. Never commit them. |
| **AI-generated code** | The `launchElectron`, `closeElectron`, and `openElectronDevTools` functions in `playwright-state.ts` were developed with AI assistance. They are marked with SPDX snippet tags and are not attributed to the Robot Framework Foundation copyright. |
