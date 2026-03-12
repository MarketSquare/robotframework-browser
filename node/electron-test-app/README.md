# Electron Test App

A minimal Electron application used as the target for the Browser library's
Electron acceptance tests (`atest/test/01_Browser_Management/electron.robot`).

## What it contains

`main.js` — Electron main process. Opens a single `BrowserWindow` that loads
`index.html`. Node integration is disabled; context isolation is enabled.

`index.html` — Renderer page with interactive elements used by the test cases.

## Element map

| Selector | Type | What it does |
|---|---|---|
| `css=h1#title` | heading | Static heading text `"Electron Test App"` |
| `css=#click-counter` | span | Increments by 1 on each button click |
| `css=#btn-click` | button | Triggers the counter increment |
| `css=#text-input` | input | Editable text field; fires `input` event |
| `css=#description` | p | Mirrors `#text-input` value via `input` event |
| `css=#select-box` | select | Options: `one`, `two`, `three` |
| `css=#checkbox` | checkbox | Simple checkbox, initially unchecked |
| `css=#btn-toggle` | button | Toggles `#toggle-target` between hidden/visible |
| `css=#toggle-target` | div | Hidden by default; reveals `"Now you see me"` |
| `css=#btn-async` | button | Shows `#async-output` after an 800 ms delay |
| `css=#async-output` | div | Hidden by default; reveals `"Loaded"` after delay |
| `css=#file-input` | file input | Native file picker |
| `css=#file-name` | span | Shows selected filename after upload |
