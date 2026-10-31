# Recorder internals

How `Record Keyword` / `Record Keywords` work. Vocabulary: `CONTEXT.md`. Why: ADR 0010
(page under test is untrusted) and ADR 0011 (action stream instead of codegen). Usage: the
keyword documentation.

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
syntax (including the reserved `*{`), runs of spaces, edge spaces and exotic whitespace.
Spaces are escaped with backslashes so that no two plain spaces meet: `a \ b` inside a cell,
`\ \ lead` at its start and `trail \ \` at its end, where Robot drops a backslash before the
next separator or the line end. A `[` right after a Keyword Argument is written `\[`, as
`${x}[0]` is item access. A value
starting with `name=` gets its `=` escaped when `name` is a parameter of the called keyword
(`parameters.py`, checked against the real signatures by `test_recorder_parameters.py`):
`Fill Text    #n    txt\=hello`, but `Click    text=Log in`. A keyword not in that table may
take any name, so every such value is escaped there. Deliberate named arguments
(`action=accept`, `clickCount=2`) are marked `named` and stay as they are.

## Action -> Keyword Call

Generated from `ActionMapper` in `action_mapper.py`. "Selectable" marks the values a person
can turn into a Keyword Argument, wholly or in part; structural values (buttons, modifiers,
operators, option strategies) never are.

| Playwright action | Keyword Call | Selectable values |
|-------------------|--------------|-------------------|
| `click` (left, once, no modifiers) | `Click    <selector>` | selector |
| `click` (other button, modifiers or `clickCount` > 1) | `Click With Options    <selector>    [button]    [modifiers...]    [clickCount=N]` (`button` is written whenever a modifier follows) | selector |
| `fill` | `Fill Text    <selector>    <text>` | selector, text |
| `press` | `Press Keys    <selector>    [Modifier+...]Key` | selector, keys |
| `check` | `Check Checkbox    <selector>` | selector |
| `uncheck` | `Uncheck Checkbox    <selector>` | selector |
| `select` | `Select Options By    <selector>    value    <option>...` | selector, each option |
| `navigate` | `Go To    <url>` (never `New Page`: a recorded keyword does not create its page) | url |
| `closePage` | nothing: Playwright drops it, because its page is gone; the wrapper reports a closed page as a `closed` event instead (see Pages) | - |
| `openPage` | nothing, silently (existing pages, hand-opened tabs; a page opened by an Action arrives as a `popup` signal) | - |
| `assertText` | `Get Text    <selector>    contains    <text>` (`==` when not a substring assertion) | selector, text |
| `assertValue` | `Get Property    <selector>    value    ==    <value>` | selector, value |
| `assertChecked` | `Get Checkbox State    <selector>    ==    checked` (or `unchecked`) | selector, state |
| `assertVisible` | `Get Element States    <selector>    *=    visible` | selector |
| `assertSnapshot` | `Get Aria Snapshot    <selector>    yaml    ==    <snapshot>`; the multi-line YAML comes from the action's `ariaSnapshot` field | selector, snapshot |

A file chosen in a file chooser arrives in api mode as a `fill` of the browser's fake path
`C:\fakepath\<name>` (only the first file), from other recorder tools as `setInputFiles`
with every name. Either becomes an upload of `<define_path_to_file>/<name>`
(`UPLOAD_FOLDER`), with a toolbar notice to complete the path:

| Upload | Keyword Calls |
|--------|---------------|
| one file, after an Action (the click that opened the chooser) | `${upload}=    Promise To Upload File    <path>` before that Action, `Wait For    ${upload}` after it; Undo removes them together |
| no such Action (it was undone, or the click went straight to the file input, which Playwright does not record), or several files | `Upload File By Selector    <file input>    <path>...` |
| an empty file list (chooser cancelled) | nothing |
| a name that is not a plain file name (`../x`, `a\\b`, `..`, empty, control characters) | nothing, and a toolbar notice: the page can rewrite the reported value, and a path would make a later run upload another file |

Playwright 1.64 never emits `hover` in api mode, so it is not mapped.
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

### Pages

Every event carries the guid of its page (`page`), as Playwright's `popupPageGuid` names
pages, and the first poll reply names Browser's active page (`activePage`). The session
keeps the page the keyword is on:

- An Action on another page gets `Switch Page    ${page_n}` in its group's `before`.
- The variable is the return value of the Switch Page that left that page: the `popup`'s
  `Switch Page    NEW` or an earlier switch. It gets its `${page_n}=` only when first
  used, and loses it again when Undo removes the last use.
- `closed` (from the wrapper's own `page.once('close')`) becomes `Close Page` for the
  active page, `Close Page    ${page_n}` for another one with an id, and nothing for a
  page without one. After closing the active page, the next Action switches to its page
  if it has an id; otherwise Browser's fallback to the previous page is relied on.
- A page without an id, opened before the recording or by hand, gets no switch and a
  toolbar notice.
- Each keyword starts on the page the last one ended on, with no ids.

The variable name is made unique within the keyword (`download`, `download_2`, ...). None
of the signal values is selectable.

## Selector mapping

Playwright's selector generator uses eight engines; each is rewritten into public syntax
with the same meaning (`action_mapper.to_browser_selector`). Only what has no public form
stays internal, with a toolbar notice, such as an attribute with an empty value.

| Playwright internal | Browser selector |
|---------------------|------------------|
| `internal:role=button[name="Submit"i]` (case-insensitive substring) | `role=button[name*="Submit"i]` |
| `internal:role=button[name="Submit"s]` (exact) | `role=button[name="Submit"s]` |
| `internal:text="Log in"i` (case-insensitive substring) | `text=Log in`, or `text=/Log\s+in/i` when the text starts with a quote or slash or holds `>>` |
| `internal:text="Log in"s` (exact, whole text) | `text=/^\s*Log\s+in\s*$/` |
| `div >> internal:has-text="Twin"i` | `div:has-text("Twin")` |
| `div >> internal:has-text=/^Twin$/` | `div:text-matches("^Twin$")` |
| `internal:testid=[data-testid="x"s]` (exact) | `[data-testid="x"]` |
| `internal:attr=[placeholder="Email"i]` (case-insensitive substring) | `[placeholder*="Email"i]` |
| `... >> internal:control=enter-frame >> ...` | `... >>> ...` |
| `css`, `nth` | unchanged |
| `internal:label="Map"i` | `label="Map"i` (Browser's label engine takes the same values) |
| `internal:control=any-frame >> iframe[name="b"] >> internal:control=enter-frame >> ...` (a frame path of two or more frames, shortened) | `>>> iframe[name="b"] >>> ...` (a leading `>>>` searches every frame) |

Why each form, all read from Playwright 1.64:

- Role (`queryRole`): the internal engine matches a `name` or `description` without the `s`
  flag as a substring, the public one exactly; `*=` restores the substring.
- Text (`createTextMatcher`): the internal engine compares the element's whole normalized
  text; the public `text="X"` compares only its own text nodes, so `<button>Split
  <b>text</b></button>` is not `text="Split text"`. An anchored regex that tolerates the
  whitespace Playwright normalizes away is.
- Has-text: the public `:has-text()` matches like the internal substring filter. The public
  `:text-matches()` additionally skips an element whose whole text sits in one child, so it
  finds the clicked element or none, never another one.
- Attributes (`createAttributeMatcher`): without a flag or with `s` an exact match, with `i`
  a case-insensitive substring; CSS has no `s` flag. An empty `i` value is passed through.
- Label (`getElementLabels`): matches `aria-labelledby`, `aria-label` or a `<label>`, which no
  public selector can express. The generator picks it for an element without a role that
  can carry a name, such as `<div aria-label="Map">`. The selector stays internal; the
  toolbar says so, as it may break with a Playwright upgrade. Any other form that cannot
  be rewritten safely stays internal with the same notice.

Two acceptance tests guard this: "Translated Selectors Match Like Playwright" compares each
rewritten form with its internal original in a browser, and "Every Recorded Selector Finds
Exactly The Clicked Element" records a click on every element of
`node/dynamic-test-app/static/recorder/selectors.html` and checks that the translated
selector finds exactly that element.

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
| `calls` | `[{assign, keyword, values: [{tokens, selectable, raw}]}]`; `assign` is `${name}=` or `null`; `tokens` is the value as written into the file, split by Robot's own tokenizer into `["argument" or "variable", text]` pairs for the toolbar's syntax colours; `raw` is the literal text of the value, `null` once it holds a reference |
| `arguments` | `[{name, default, useDefault}]` |
| `offer` | after `argument`: `{argument, text, occurrences: [[call, value], ...]}` or `null` |
| `pending` | `new`/`finish`/`discard`/`stop` while it settles, else `null`; meanwhile every command but `stop` is refused |
| `notice` / `error` | one-shot message, cleared by the next command |
| `picking` | Playwright's Pick locator mode is on and could not be handed to the toolbar's picker |
| `picker` | the toolbar picker's state while the Pick button is in use, else `null` (see Record Selector) |
| `paused` | the keyword is recording but paused: Actions and signals are ignored until `resume` |
| `answered` | `id` of the last command Python handled; with `error` it tells a dialog whether its command was refused |

Every displayed text (a value's `tokens` together, `default`, the offer's `text`) is cut to `TOOLBAR_TEXT_LIMIT`
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
| `finish`, `discard`, `stop`, `undo`, `pause`, `resume` | - |
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

## Record Selector

`Record Selector` reuses the toolbar in its `selector` mode and the `__rfbCommand` channel,
but not Playwright's recording: Node calls the public `page.pickLocator()` on the active
page (`element-picker.ts`, driven by `selector-picker.ts` and `recorder.ts`), so the hover
highlight, the tooltip and a pick that never reaches the page are Playwright's. Python
drives it like a Recording Session, polling `SelectorPickerPoll` every 200 ms (`picker.py`);
it translates the picked selector with `to_browser_selector` and owns the toolbar state.

- `__rfbCommand` is exposed once per context (`commandListeners`); the recorder and the
  picker each register their buffers, and a command reaches the session that is running.
  A picker refuses to start while a Recording Session runs in the context:
  `pickLocator()` would switch Playwright's recorder off.
- The `css` generator is `@medv/finder`, bundled by `node/build.wrapper.js` from
  `node/playwright-wrapper/page/css-selector.ts` into `static/css-selector.js` and evaluated
  in the frame of the picked element, then of each `iframe` element outward, joined by
  ` >>> `. Inside an open shadow root the host's selector and the inner one are joined by
  ` >> `.
- State, Python -> toolbar: `mode` (`selector`), `label`, `phase` (`picking`/`picked`),
  `generator`, `generators`, `unavailable` (generator -> why it has no selector),
  `selector`, `version` (raised when the selector changes other than by typing; only then
  the toolbar replaces its input), `count` (`{selector, count}` or `{selector, error}`),
  `notice`, `error`, `answered`.
- Commands: `generator` (`name`), `edit` (`selector`, at most 10 000 characters, sent once
  typing pauses for a second), `highlight` (`on`: boolean), `reselect`, `use`, `stop`.
  State field `highlight` says whether the matches are highlighted; a recording session
  keeps it for its next pick.
- Poll request fields besides `state` and `reset`: `pick` (keep a pick running),
  `highlight` (`false` removes the highlight and counts without one) and
  `count` (a selector to count with `findLocator`, not strict, and to highlight with
  Playwright's `locator.highlight()` until the next count, a new pick or the end). The
  reply carries `picked` (`{selector, css}` or `{error}`), the toolbar `entries` and
  `count`. `element-picker.ts` does this for both keywords.
- **The Pick button of Record Keyword(s)** opens the same picker inside a Recording
  Session (`RecorderSession._picker`, state field `picker`, commands `pick` and
  `pick-<command>`, `pick-cancel` instead of `stop`). *Use* adds the selector as a comment
  row `# Picked Selector    <selector>` (`RecordedKeyword.add_picked_selector`), which
  Undo removes like a Keyword Call; Playwright's later refinement of the previous Action
  still updates that Action (`_last_action`). The recorder poll carries the same `pick`
  and `count` fields. `pickLocator()` sets Playwright's mode to `inspecting` and then to
  `none`; `RecorderBuffers.ownPick` keeps that from ending the session until the poll has
  switched back to `recording`. Playwright's own Pick locator (mode `recording-inspecting`
  or `inspecting` outside our pick) is switched back to `recording` and reported as
  `pickRequested`, which opens our picker: its pick would never reach us.

## Timing

- Playwright holds back left clicks and navigations for 500 ms before reporting them
  (`kActionBufferTimeout`).
- Hence `new`, `finish`, `discard`, `stop`, `pause` and `resume` wait (`pending`) until `SETTLE_SECONDS`
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

- Playwright's Pick locator does not deliver its pick in api mode; the toolbar's own picker
  takes over (see Record Selector). While picking, nothing is recorded. `picking` (the
  notice) is left for the case that Playwright's mode cannot be switched back.
- Hovers are not recorded (Playwright does not emit them in api mode).
- An uploaded file's folder is unknown to the page; the recorded path has to be completed.
- Playwright's own overlay cannot be hidden during a session and covers the top centre of
  the page; its Record button ends the session too. It is hidden after the session.
- A value longer than about 64 KiB, or one past the first MiB of values in the keyword,
  cannot be made an argument in the toolbar; edit the file instead.
- Event isolation: keyboard, input, composition, clipboard, focus and `contextmenu` events
  from inside the toolbar are stopped by a capture listener on `window`, so page shortcuts
  do not fire while typing in it and a page modal's focus trap does not pull the focus
  back. Pointer, mouse, touch and wheel events are stopped at the host after the toolbar
  handled them, so a page modal does not close on a toolbar click ("click outside") or
  block its scrolling; the host also sets `pointer-events: auto` against a `body` without
  pointer events. A `window` capture listener the page registered before the toolbar was
  injected still sees all of them.
- A native modal `<dialog>` (`showModal()`) makes the rest of the page inert, the toolbar
  included; close it to use the toolbar.
- The quiet time counts clicks, not other input that Playwright might hold back; a
  same-document navigation by script (`history.pushState`) shortly before Save is not seen.
- Headless: the reset poll fails if the active browser was launched headless. The
  acceptance suite sets the internal `Browser.recorder_allows_headless` to drive scripted
  sessions headless. Connected and adopted browsers count as visible.
- One browser context: the recorder works in the active context. Closing that context during a session ends
  the session like closing its last page; what was recorded is saved.
- A page that swaps its `body` without navigating (Turbo, htmx) drops the toolbar; the next
  poll finds it detached and attaches it again.
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
6. The selector translation still holds: the atests "Translated Selectors Match Like
   Playwright" (every rewritten form against its internal original) and "Every Recorded
   Selector Finds Exactly The Clicked Element" (the generator's real output on
   `recorder/selectors.html`) pass. If the generator uses a new engine, add an element for
   it to that page.
7. `assertSnapshot` still carries its snapshot in `ariaSnapshot` (the only action that keeps
   it, see `toAction`), and `Get Aria Snapshot ... yaml ==` still accepts it.
8. The action names and fields in the table above (`assertVisible`, `assertChecked`, ...)
   are unchanged; re-check whether `hover` is emitted now, and that a file chooser still
   arrives as a `fill` of `C:\fakepath\<name>` (atest "A File Chooser Upload Becomes An
   Upload Promise Around The Click").
9. The injected recorder still skips events whose composed path holds an `x-pw-glass`
   element (`_ignoreOverlayEvent`) for clicks, input and keys, and `contextmenu` is still the
   only one it records without that check; Playwright does not restyle other `x-pw-glass`
   elements (it only styles its own instance inline).
10. Playwright still leaves `body[data-pw-cursor=pointer]` behind when it switches from
   Pick locator or an assertion tool to a tool without a cursor; `resetPlaywrightCursor`
   removes it (atests "An Assertion Tool Leaves The Page Its Own Pointer" and "The Page
   Has Its Own Pointer Again"). Once Playwright clears it itself, the workaround can go.
11. `page.pickLocator()` and `page.cancelPickLocator()` still exist, and the returned
   locator still carries the selector in `_selector` (`internalSelector` in
   `element-picker.ts`); `inv atest --suite record_selector` passes.
12. `inv atest --suite "Recorder"` passes (`atest/test/02_Content_Keywords/recorder.robot`);
   it replays a recorded keyword end to end.

## Robot Framework upgrade checklist

`names.py` reuses parts of Robot Framework that are not public API, to know which keywords a
recorded name would collide with or shadow:

1. `BuiltIn()._get_context().namespace._kw_store` (`resources`, `suite_file`) - without it a
   warning is logged and only library keywords are checked.
2. `EmbeddedArgumentParser._parse_arg` (7.3+) or `_get_name_and_pattern` (7.1, 7.2), and
   `_format_custom_regexp` - without them a warning is logged once and only exact
   embedded-argument matches are rejected, not normalized ones such as `Open_Login_Page`.
3. `EmbeddedArguments.matches` (7.3+) or `match` (all versions) - public; `_literal_matcher`
   takes whichever exists.

Run `utest/test_recorder_names.py` against the lowest supported Robot Framework too; CI does on
its 7.1.1 leg.

## Where keywords go when something is in the way

- `file` not given: `${SUITE_SOURCE}`. In a suite initialisation file Robot reports the
  directory and keeps no record of the init file it read, so `_suite_file` takes the
  directory's `__init__.robot`; without one the keyword fails.
- Before recording starts, `unwritable_reason` checks that the folder exists and an existing
  file is writable. `FileTarget._write` checks again before every write: it replaces the
  file by renaming a temporary one, which needs only the folder's permission, so without
  the check a read-only file would be overwritten.
- A keyword whose final write fails is kept in `RecorderSession.unsaved` and written once
  more on close. If that fails too, `Record Keyword(s)` logs its text as a warning and fails.
