# Recorder internals

How `Record Keyword` / `Record Keywords` work. Vocabulary: `CONTEXT.md`. Requirements:
`docs/recorder/user-story.md`. Why: ADR 0010 (page under test is untrusted) and ADR 0011
(action stream instead of codegen). Usage: the keyword documentation.

## Architecture

    Browser/keywords/recorder.py   Recorder keywords, gRPC client
    Browser/recorder/driver.py     poll loop: every 200 ms RecorderPoll(state) -> ordered entries
    Browser/recorder/session.py    state machine: idle / recording, commands, deferred finish
    Browser/recorder/model.py      RecordedKeyword: Keyword Calls in groups, Keyword Arguments
    Browser/recorder/cells.py      escaping of values into Robot cells
    Browser/recorder/parameters.py parameters of the recorded keywords (named-argument escaping)
    Browser/recorder/action_mapper.py  Action -> Call, signal -> calls around it
    Browser/recorder/target.py     FileTarget (re-read, own block only) / LogTarget
    Browser/recorder/names.py      name validation and collision checks (ADR 0010)
    node/playwright-wrapper/recorder.ts         _startRecording, buffering, toolbar injection
    node/playwright-wrapper/static/recorder-toolbar.js   toolbar: x-pw-glass > host > closed shadow root

Python is the only clock. The toolbar renders the state Python sends and sends commands
through `window.__rfbCommand`; it holds no recording logic. Node keeps Actions, signals and
commands in one buffer, in the order they happened, and Python applies them in that order.

The toolbar's host element sits in an `x-pw-glass` element. Playwright's injected recorder
ignores every event whose composed path holds one (`_ignoreOverlayEvent`, which also guards
its own overlay), so clicking or typing in the toolbar is never an Action. That matters
beyond not recording the toolbar: Playwright folds a navigation into the last Action, so a
toolbar click it saw would swallow a `Go To` made within 5 s. `contextmenu` is the one event
it does not check this way; the toolbar stops it on `window` before the recorder sees it.

## Writing values

`cells.py` escapes every value so Robot reads back exactly the recorded string: `#`, variable
syntax, runs of spaces, edge spaces and exotic whitespace. A `[` right after an emitted
`${SPACE}` or a Keyword Argument is written `\[`, as `${x}[0]` is item access. A value
starting with `name=` gets its `=` escaped when `name` is a parameter of the called keyword
(`parameters.py`, checked against the real signatures by `test_recorder_parameters.py`):
`Fill Text    #n    txt\=hello`, but `Click    text=Log in`. A keyword not in that table may
take any name, so every such value is escaped there. Deliberate named arguments
(`action=accept`, `clickCount=2`) are marked `named` and stay as they are.

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

Playwright 1.64 never emits `hover` or `setInputFiles` in api mode, so neither is mapped.
Any other action name produces no Keyword Call and a
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
| `calls` | `[{text, assign, keyword, values: [{text, selectable, raw}]}]`; `assign` is `${name}=` or `null`; `raw` is the literal text of the value, `null` once it holds a reference |
| `arguments` | `[{name, default, useDefault}]` |
| `offer` | after `argument`: `{argument, text, occurrences: [[call, value], ...]}` or `null` |
| `pending` | `new`/`finish`/`discard`/`stop` while it settles, else `null`; meanwhile every command but `stop` is refused |
| `notice` / `error` | one-shot message, cleared by the next command |
| `picking` | Playwright's Pick locator mode is on |
| `answered` | `id` of the last command Python handled; with `error` it tells a dialog whether its command was refused |

Every displayed text (`text`, `default`, the offer's `text`) is cut to `TOOLBAR_TEXT_LIMIT`
(200) characters. `raw` is sent only up to `MAX_RAW_LENGTH` (64 KiB of JSON) per value and
`MAX_RAW_TOTAL` (1 MiB) per state, in call order; a value beyond either limit is sent with
`selectable: false` and `raw: null`. So the state and the commands quoting `raw` stay below
the gRPC message limit. Node sends a page the state only when it changed or when the page
lost the toolbar by navigating.

Commands, toolbar -> Python, through `window.__rfbCommand(command)`. Every command also
carries `id` (unique per toolbar instance, at most 64 characters) and `quietMs` (how long
ago the page saw its last click or finished loading, see Timing):

| `cmd` | Fields |
|-------|--------|
| `new` | `name` |
| `finish`, `discard`, `stop`, `undo` | - |
| `argument` | `call`, `value`, `start`, `end` (code point offsets into the value), `name`, `raw`, `useDefault` (boolean, default `true`: the marked text becomes the default) |
| `replace` | `argument`, `occurrences` (`[[call, value], ...]`, possibly empty) |

`raw` on `argument` is the value text the person selected in. The session rejects the
command ("The keyword calls changed - please try again.") if the call now holds other text,
so a selection made against a stale view never marks the wrong text. All fields are
validated; the page can call the binding too (ADR 0010). Node accepts commands only while a
session runs (from the reset poll until `recorderStop`), drops and logs a command over
`MAX_COMMAND_BYTES` (256 KiB) and buffers at most `MAX_BUFFERED_COMMANDS` (100). An Action
over `MAX_EVENT_BYTES` (1 MiB) is dropped and logged. One poll reply carries at most
`MAX_ENTRIES_PER_POLL` (500) entries within `MAX_REPLY_BYTES` (3 MiB); the rest follow with
the next poll. All sizes are UTF-8 bytes of JSON. Keyword and argument names are at most
`NAME_LIMIT` (200) characters. A reply Python cannot read fails the keyword.

## Timing

- Playwright holds back left clicks and navigations for 500 ms before reporting them
  (`kActionBufferTimeout`).
- Hence `new`, `finish`, `discard` and `stop` wait (`pending`) until `SETTLE_SECONDS`
  (0.8 s) after the page's last click or load, so a held-back Action lands in the keyword it
  was made in, and one made while idle does not land in the next keyword. The toolbar
  measures that quiet time (`quietMs`, from trusted `click`/`dblclick`/`auxclick` outside the
  toolbar and the page's `domInteractive`); a Save a second after the last click does not
  wait at all. A command without `quietMs` waits the whole 0.8 s. `Stop` while another
  command is settling keeps the running wait; a pending discard still happens first.
- A session reset (first poll, `reset=true`) waits `HELD_BACK_MS` (600 ms) while the
  recorder is still stopped, drops buffered entries, and only then switches to
  `recording`, so no Action made after the switch is dropped with stale ones. If no page
  could take the mode (the only one was navigating), every poll tries again until the
  recorder is seen recording.
- The end of a session writes mode `none`: in Playwright 1.64 only `none` hides its overlay.
  Its Record button switches to `standby`; both count as stopped once the session was seen
  recording.
- Python polls every 200 ms (`POLL_INTERVAL`).

## What Playwright does before our sink (1.64)

- `fill`: one `actionAdded`, then one `actionUpdated` per keystroke.
- Double click: one `click` with `clickCount: 2`.
- Popups, dialogs and downloads arrive as `signalAdded` after the Action.
- `openPage` is reported for existing pages and hand-opened tabs; we ignore it.
- Main-frame navigation within 5 s of a click/fill/press is swallowed by Playwright (it
  belongs to that Action). Toolbar clicks never count, see Architecture.
- The in-page Playwright overlay cannot be hidden in api mode.
- `_startRecording` is called once per context (a second call throws); `_stopRecording`
  drops the sink. In 1.63 the same was `_enableRecorder` / `_disableRecorder`.

## Limitations

- Pick locator: while it is on, Playwright's recorder is disabled and nothing is recorded
  (the toolbar shows a notice, from `picking`). The picked locator is not delivered in api
  mode, so it cannot be used.
- File uploads and hovers are not recorded (Playwright does not emit them in api mode).
- Playwright's own overlay cannot be hidden during a session and covers the top centre of
  the page; its Record button ends the session too. It is hidden after the session.
- A value longer than about 64 KiB, or one past the first MiB of values in the keyword,
  cannot be made an argument in the toolbar; edit the file instead.
- Event isolation: keyboard, input, composition, clipboard and `contextmenu` events from
  inside the toolbar are stopped by a capture listener on `window`, so page shortcuts do not
  fire while typing in it. A `window` capture listener the page registered before the
  toolbar was injected still sees them.
- The quiet time counts clicks, not other input that Playwright might hold back; a
  same-document navigation by script (`history.pushState`) shortly before Save is not seen.
- Headless: the reset poll fails if the active browser was launched headless. The
  acceptance suite sets the internal `Browser.recorder_allows_headless` to drive scripted
  sessions headless. Connected and adopted browsers count as visible.
- One browser context: the recorder works in the active context.
- `_startRecording` registers the recorder in the context for good. After a session it
  stays registered (in mode `none`), as do the `__rfbCommand` binding and the Action sink;
  the toolbar itself is removed.
- It rests on a private Playwright API (ADR 0011).

## Playwright upgrade checklist

1. `context._startRecording` still exists (`coreBundle.js`, `ProgrammaticRecorderApp`);
   `_stopRecording` is still never called.
2. The sink still has `actionAdded`, `actionUpdated`, `signalAdded`; the payload shape is
   still handled by `toAction` (`npm run test -- recorder`).
3. Signal names `popup`, `dialog`, `download` unchanged.
4. Click buffer still <= 500 ms (`kActionBufferTimeout`), so `SETTLE_SECONDS` and
   `HELD_BACK_MS` still cover it, and only left clicks and navigations are held back
   (`_shouldBuffer`), which the toolbar's quiet time is based on.
5. `STOP_MODES` (`none`, `standby`) still match the overlay's modes, and `none` still hides
   the overlay (`recorderStop` writes it). `recording-inspecting`
   and `inspecting` (Pick locator, `PICKING_MODES`) are not stops; a new mode must be
   classified as stop, part of the recording, or picking.
6. `assertSnapshot` still carries its snapshot in `ariaSnapshot` (the only action that keeps
   it, see `toAction`), and `Get Aria Snapshot ... yaml ==` still accepts it.
7. The action names and fields in the table above (`assertVisible`, `assertChecked`, ...)
   are unchanged; re-check whether `hover` / `setInputFiles` are emitted now (neither is
   mapped, as Playwright never emitted them).
8. The injected recorder still skips events whose composed path holds an `x-pw-glass`
   element (`_ignoreOverlayEvent`) for clicks, input and keys, and `contextmenu` is still the
   only one it records without that check; Playwright does not restyle other `x-pw-glass`
   elements (it only styles its own instance inline).
9. `inv atest --suite "Recorder"` passes (`atest/test/02_Content_Keywords/recorder.robot`);
   it replays a recorded keyword end to end.
