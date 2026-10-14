# Recorder internals

How `Record Keyword` / `Record Keywords` work. Vocabulary: `CONTEXT.md`. Requirements:
`docs/recorder/user-story.md`. Why: ADR 0010 (page under test is untrusted) and ADR 0011
(action stream instead of codegen). Usage: the keyword documentation.

## Architecture

    Browser/keywords/recorder.py   Recorder keywords, gRPC client
    Browser/recorder/driver.py     poll loop: every 200 ms RecorderPoll(state) -> events, commands
    Browser/recorder/session.py    state machine: idle / recording, commands, deferred finish
    Browser/recorder/model.py      RecordedKeyword: Keyword Calls in groups, Keyword Arguments
    Browser/recorder/action_mapper.py  Action -> Call, signal -> calls around it
    Browser/recorder/target.py     FileTarget (re-read, own block only) / LogTarget
    Browser/recorder/names.py      name validation and collision checks (ADR 0010)
    node/playwright-wrapper/recorder.ts         _enableRecorder, buffering, toolbar injection
    node/playwright-wrapper/static/recorder-toolbar.js   toolbar in a closed shadow root

Python is the only clock. The toolbar renders the state Python sends and sends commands
through `window.__rfbCommand`; it holds no recording logic.

## Action -> Keyword Call

Generated from `ActionMapper` in `action_mapper.py`. "Selectable" marks the values a person
can turn into a Keyword Argument; selectors and structural values (buttons, operators,
option strategies, states) never are.

| Playwright action | Keyword Call | Selectable values |
|-------------------|--------------|-------------------|
| `click` (left, once, no modifiers) | `Click    <selector>` | none |
| `click` (other button, modifiers or `clickCount` > 1) | `Click With Options    <selector>    [button]    [modifiers...]    [clickCount=N]` (`button` is written whenever a modifier follows) | none |
| `fill` | `Fill Text    <selector>    <text>` | text |
| `press` | `Press Keys    <selector>    [Modifier+...]Key` | none |
| `check` | `Check Checkbox    <selector>` | none |
| `uncheck` | `Uncheck Checkbox    <selector>` | none |
| `select` | `Select Options By    <selector>    value    <option>...` | each option |
| `navigate` | `Go To    <url>` (never `New Page`: a recorded keyword does not create its page) | url |
| `closePage` | `Close Page` | - |
| `openPage` | nothing, silently (existing pages, hand-opened tabs; a page opened by an Action arrives as a `popup` signal) | - |
| `assertText` | `Get Text    <selector>    contains    <text>` (`==` when not a substring assertion) | text |
| `assertValue` | `Get Property    <selector>    value    ==    <value>` | value |
| `assertChecked` | `Get Checkbox State    <selector>    ==    checked` (or `unchecked`) | none |
| `assertVisible` | `Get Element States    <selector>    *=    visible` (AC-47) | none |
| `assertSnapshot` | `Get Aria Snapshot    <selector>    yaml    ==    <snapshot>` (AC-46); the multi-line YAML comes from the action's `ariaSnapshot` field | snapshot |
| `hover` | `Hover    <selector>` | none |
| `setInputFiles` | `Upload File By Selector    <selector>    <file>...` | each file |

`hover` and `setInputFiles` are mapped, but Playwright 1.63 never emits them in api mode, so
in practice they are not recorded. Any other action name produces no Keyword Call and a
toolbar notice ("... has no Browser keyword and was not recorded."). A later
`actionUpdated` for that Action never updates the previous Keyword Call: if Playwright's
update maps to a Browser keyword it is added as a new Keyword Call, otherwise it gives the
same notice again.

### Signals

A signal is reported after the Action that raised it, but Browser needs some handling
before it. `ActionMapper.map_signal` attaches calls to the Action's group, so Undo removes
them together.

| Signal | Calls before the Action | Calls after the Action |
|--------|-------------------------|------------------------|
| `popup` | - | `Switch Page    NEW` |
| `dialog` | `Handle Future Dialogs    action=accept` | - |
| `download` | `${download}=    Promise To Wait For Download` | `Wait For    ${download}` |

The variable name is made unique within the keyword (`download`, `download_2`, ...). None
of the signal values is selectable.

## Selector mapping

| Playwright internal | Browser selector |
|---------------------|------------------|
| `internal:role=button[name="Submit"i]` | `role=button[name="Submit"i]` |
| `internal:text="Log in"i` | `text=Log in` |
| `internal:text="Log in"s` | `text="Log in"` |
| `internal:testid=[data-testid="x"]` | `[data-testid="x"]` |
| `internal:attr=[placeholder="Email"i]` | `[placeholder="Email"i]` |
| `... >> internal:control=enter-frame >> ...` | `... >>> ...` |
| anything else | unchanged (Browser resolves it with `page.locator`) |

`internal:text` is rewritten only when the body has no quotes, backslashes or edge
whitespace and (for the `i` flag) does not start with `/`; otherwise it is passed through.

## Toolbar contract

`session.py` is the source of truth: `RecorderSession.toolbar_state` for the state,
`handle_command` and `_argument_command` for the commands. This is a summary.

State, Python -> toolbar, sent with every poll and rendered by `__rfbToolbarRender`:

| Field | Meaning |
|-------|---------|
| `state` | `idle` or `recording` |
| `name` | keyword being recorded, or the name of one about to start |
| `fixedName` | true for `Record Keyword` (name is fixed, only ✕ ends it) |
| `target` | label of the file or log the keywords go to |
| `keywords` | names finished in this session |
| `calls` | `[{text, keyword, values: [{text, selectable, raw}]}]`; `raw` is the literal text of the value, `null` once it holds a reference |
| `arguments` | `[{name, default, useDefault}]` |

Every displayed text (`text`, `default`, the offer's `text`) is cut to `TOOLBAR_TEXT_LIMIT`
(200) characters. `raw` is sent only up to `MAX_RAW_LENGTH` (64 KiB of JSON) per value and
`MAX_RAW_TOTAL` (1 MiB) per state, in call order; a value beyond either limit is sent with
`selectable: false` and `raw: null`. So the state and the commands quoting `raw` stay below
the gRPC message limit.
| `offer` | after `argument`: `{argument, text, occurrences: [[call, value], ...]}` or `null` |
| `pending` | `new`/`finish`/`discard`/`stop` while it settles, else `null`; meanwhile every command but `stop` is refused |
| `notice` / `error` | one-shot message, cleared by the next command |
| `picking` | Playwright's Pick locator mode is on |

Commands, toolbar -> Python, through `window.__rfbCommand(command)`:

| `cmd` | Fields |
|-------|--------|
| `new` | `name` |
| `finish`, `discard`, `stop`, `undo` | - |
| `argument` | `call`, `value`, `start`, `end` (code point offsets into the value), `name`, `raw` |
| `replace` | `argument`, `occurrences` (`[[call, value], ...]`, possibly empty) |
| `default` | `argument`, `use` (boolean) |

`raw` on `argument` is the value text the person selected in. The session rejects the
command ("The keyword calls changed - please try again.") if the call now holds other text,
so a selection made against a stale view never marks the wrong text. All fields are
validated; the page can call the binding too (ADR 0010). Node accepts commands only while a
session runs (from the reset poll until `recorderStop`), drops and logs a command over
`MAX_COMMAND_BYTES` (256 KiB) and buffers at most `MAX_BUFFERED_COMMANDS` (100). An Action
over `MAX_EVENT_BYTES` (1 MiB) is dropped and logged. One poll reply carries at most
`MAX_EVENTS_PER_POLL` (500) events within `MAX_REPLY_EVENT_BYTES` (2 MiB) and commands within
`MAX_REPLY_COMMAND_BYTES` (1 MiB); the rest follow with the next poll. All sizes are UTF-8
bytes of JSON.

## Timing

- Playwright holds back left clicks and navigations for 500 ms before reporting them
  (`kActionBufferTimeout`).
- Hence `SETTLE_SECONDS = 0.6` in `session.py`: `new`, `finish`, `discard` and `stop` wait
  this long (`pending`) so a held-back Action lands in the keyword it was made in, and one
  made while idle does not land in the next keyword. `Stop` while another command is
  settling keeps the running wait; a pending discard still happens first.
- A session reset (first poll, `reset=true`) waits `HELD_BACK_MS` (600 ms) while the
  recorder is still stopped, drains buffered events and commands, and only then
  switches to `recording`, so no Action made after the switch is dropped with stale ones.
- The end of a session writes mode `none`: in Playwright 1.63 only `none` hides its overlay.
  Its Record button switches to `standby`; both count as stopped once the session was seen
  recording.
- Python polls every 200 ms (`POLL_INTERVAL`).

## What Playwright does before our sink (1.63)

- `fill`: one `actionAdded`, then one `actionUpdated` per keystroke.
- Double click: one `click` with `clickCount: 2`.
- Popups, dialogs and downloads arrive as `signalAdded` after the Action.
- `openPage` is reported for existing pages and hand-opened tabs; we ignore it.
- Main-frame navigation within 5 s of a click/fill/press is swallowed by Playwright.
- The in-page Playwright overlay cannot be hidden in api mode.
- `_enableRecorder` must be called once per context; `_disableRecorder` drops the sink.

## Limitations

- Pick locator: while it is on, Playwright's recorder is disabled and nothing is recorded
  (the toolbar shows a notice, from `picking`). The picked locator is not delivered in api
  mode, so it cannot be used.
- File uploads and hovers are not recorded (Playwright does not emit them in api mode).
- Playwright's own overlay cannot be hidden during a session and covers the top centre of
  the page; its Record button ends the session too. It is hidden after the session.
- A value longer than about 64 KiB, or one past the first MiB of values in the keyword,
  cannot be made an argument in the toolbar; edit the file instead.
- Keyboard isolation: keyboard, input, composition and clipboard events from inside the
  toolbar are stopped by a capture listener on `window`, so page shortcuts do not fire while
  typing in it. A `window` capture listener the page registered before the toolbar was
  injected still sees them.
- Headless: the reset poll fails if the active browser was launched headless. The
  acceptance suite sets the internal `Browser.recorder_allows_headless` to drive scripted
  sessions headless. Connected and adopted browsers count as visible.
- One browser context: the recorder works in the active context.
- `_enableRecorder` registers the recorder in the context for good. After a session it
  stays registered (in mode `none`), as do the `__rfbCommand` binding and the Action sink;
  the toolbar itself is removed.
- It rests on a private Playwright API (ADR 0011).

## Playwright upgrade checklist

1. `context._enableRecorder` still exists (`coreBundle.js`); `_disableRecorder` is still
   never called.
2. The sink still has `actionAdded`, `actionUpdated`, `signalAdded`; the payload shape is
   still handled by `toAction` (`npm run test -- recorder`).
3. Signal names `popup`, `dialog`, `download` unchanged.
4. Click buffer still <= 500 ms (`kActionBufferTimeout`), so `SETTLE_SECONDS` and
   `HELD_BACK_MS` still cover it.
5. `STOP_MODES` (`none`, `standby`) still match the overlay's modes, and `none` still hides
   the overlay (`recorderStop` writes it). `recording-inspecting`
   and `inspecting` (Pick locator, `PICKING_MODES`) are not stops; a new mode must be
   classified as stop, part of the recording, or picking.
6. `assertSnapshot` still carries its snapshot in `ariaSnapshot` (the only action that keeps
   it, see `toAction`), and `Get Aria Snapshot ... yaml ==` still accepts it.
7. The action names and fields in the table above (`assertVisible`, `assertChecked`, ...)
   are unchanged; re-check whether `hover` / `setInputFiles` are emitted now.
8. `inv atest --suite "Recorder"` passes (`atest/test/02_Content_Keywords/recorder.robot`);
   it replays a recorded keyword end to end.
