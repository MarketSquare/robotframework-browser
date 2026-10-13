# User Story: Record Keywords in the Live Browser

**As** a test author working with the Browser library,
**I want to** record my interactions in the browser at any point during a test run, naming
keywords, turning values into arguments and undoing mistakes as I go,
**so that** I get reusable User Keywords built from Browser keywords, without whole tests
being generated and without translating generated Playwright code.

## Terms

Defined in `Browser/recorder/CONTEXT.md`.

- **Action**: one interaction as Playwright's recorder reports it.
- **Keyword Call**: one line in the body of a recorded User Keyword.
- **Recording Session**: everything from the call of `Record Keyword` / `Record Keywords`
  until it returns; **idle** between Keyword Recordings.
- **Keyword Recording**: the part of a Recording Session in which exactly one User Keyword is
  recorded, from *New* until *Finish* or *Discard*.
- **Keyword Argument**: a value, or a marked part of one, of a Keyword Call that was turned
  into an argument of the recorded keyword.

## Acceptance Criteria

### Invocation and interface

- **AC-01** `Record Keyword` and `Record Keywords` are keywords of the Browser library itself.
  They need no plugin import and can be called at any point of a running test, for example
  at a breakpoint.
- **AC-02** `Record Keyword    name    file='${SUITE_SOURCE}'    idle_timeout=None` starts a
  Recording Session with exactly one Keyword Recording, which starts immediately under the
  given name.
- **AC-03** `Record Keywords    file='${SUITE_SOURCE}'    idle_timeout=None` starts a
  Recording Session in which any number of Keyword Recordings are named and recorded one
  after another from the toolbar.
- **AC-04** The default value of `file` is the string `${SUITE_SOURCE}`. It is resolved as a
  Robot Framework variable, so recording goes into the file of the running suite.
- **AC-05** With `file=${None}`, nothing is written to a file. Each finished keyword is
  written as a complete block (`*** Keywords ***` …) to the console and to the log at INFO
  level when it is finished.
- **AC-06** Both keywords return the text of the recorded keywords. `Record Keyword` returns
  the text of its one keyword, `Record Keywords` the text of all keywords recorded in the
  session.
- **AC-07** With `idle_timeout`, the session ends after that long with neither an Action
  reported nor a toolbar command given. Actions while idle reset the timer too. Without
  `idle_timeout`, the session waits until it is ended.
- **AC-08** If the installed Playwright version does not offer the programmatic recorder,
  the keyword fails with a clear error message.

### Toolbar and operation

- **AC-09** During the session the page shows a Robot Framework toolbar. It shows the state
  (idle or recording), the name of the current keyword and its Keyword Calls, live.
- **AC-10** The toolbar can be dragged, collapsed and resized. Position, size and collapsed
  state survive navigation.
- **AC-11** Clicks and input in the toolbar itself are never recorded as Actions.
- **AC-12** In `Record Keywords`, *+ New Keyword* starts a Keyword Recording under a name to
  be entered, and *Finish* ends it. In `Record Keyword` these two buttons are not shown.
- **AC-13** *Undo* removes every Keyword Call the last Action produced. Later refinements of
  that Action by Playwright do not bring it back.
- **AC-14** *Discard* abandons the running Keyword Recording completely and leaves the file as
  it was before. In `Record Keyword` the keyword then starts again, empty, under the same name.
- **AC-15** Actions while idle produce no Keyword Calls.
- **AC-16** Actions with no Browser keyword equivalent (e.g. `assertSnapshot`) produce no
  Keyword Call, but a visible notice in the toolbar.

### Ending

- **AC-17** The session ends on *Stop* in the Robot Framework toolbar, on Playwright's Record
  button, when `idle_timeout` is reached, when all pages are closed, or on an error.
- **AC-18** A Keyword Recording still running when the session ends is saved, never
  discarded. A Keyword Recording with no Keyword Calls is not saved.
- **AC-19** *Finish*, *Discard* and *Stop* take effect only after Playwright has reported
  every Action it was still holding back, so a click right before *Finish* still lands in the
  right keyword. The toolbar shows that it is finishing in the meantime.
- **AC-20** After the session the toolbar is removed from all pages. Another session in the
  same browser context works, without recording any Action twice.

### Generated keywords

- **AC-21** Every Action is turned into a Keyword Call to a Browser keyword, with selectors
  translated into readable Browser selectors (`role=…`, `text=…`, CSS, `>>>` for frames).
- **AC-22** When Playwright refines an Action (each keystroke of a fill, a click becoming a
  double click), it stays exactly one Keyword Call, which is updated.
- **AC-23** Every recorded User Keyword carries the tag `recorded`.
- **AC-24** A recorded keyword never creates a page. An Action that opens a popup or new tab
  becomes `Switch Page    NEW`; closing a page becomes `Close Page`.
- **AC-25** An Action that opens a dialog is preceded by a matching `Handle Future Dialogs`.
- **AC-26** An Action that starts a download is written as `${dl}=    Promise To Wait For
  Download`, the Action, and `Wait For    ${dl}`.
- **AC-27** Password fields get no special treatment; the typed value is recorded like any
  other.

### Keyword Arguments

- **AC-28** While a Keyword Recording is running, a value of a Keyword Call (text, URL,
  option, file path) can be turned into a Keyword Argument from the toolbar. Selectors cannot
  become arguments.
- **AC-29** If part of a value is marked, only that part becomes the argument, e.g.
  `Go To    https://shop.example.com/item/${item_id}`.
- **AC-30** A new Keyword Argument starts with the recorded value as its default
  (`${email}=admin@example.com`); the default can be deselected in the toolbar.
- **AC-31** If the same value occurs in other Keyword Calls of the Keyword Recording, the
  toolbar offers to replace those too, with the occurrences preselected.
- **AC-32** A Keyword Argument no longer used by any Keyword Call after *Undo* is removed
  from `[Arguments]`.
- **AC-33** If typing continues after a value was turned into an argument, the Keyword Call
  keeps using the argument and its default follows the new text.
- **AC-34** Argument names are validated as strictly as keyword names.

### Target file

- **AC-35** Every Keyword Call is written to the target file immediately. The file is re-read
  before every save, so changes outside the recorder's own keyword block (e.g. from the IDE)
  are kept.
- **AC-36** The recorder owns the block of its running Keyword Recording. If that block was
  changed or deleted externally, the recorder rewrites it from its own state and the toolbar
  shows a notice.
- **AC-37** A Keyword Recording always creates a new User Keyword. A name that already exists
  in the target file is rejected, in `Record Keyword` too.
- **AC-38** A missing `*** Keywords ***` section or file is created. Existing content and
  formatting are preserved. *Discard* removes a section it created, but never deletes a file.

### Security

See ADR 0010.

- **AC-39** A keyword name is rejected if it would shadow a keyword the running suite can
  currently resolve: also in normalised spelling, with a BDD prefix, as a match of an
  embedded-argument keyword, owner-qualified, and with the target file reached through a
  symlink. In `Record Keywords` the rejection shows as a toolbar error; in `Record Keyword`
  the keyword fails.
- **AC-40** A malformed or hostile command or Action is logged and ignored; the session goes
  on.
- **AC-41** The keyword documentation states that the body of a recorded keyword contains
  values from the page and must be reviewed before it is committed.

### Quality

- **AC-42** A scripted acceptance suite under `atest/` covers at least:
  - a session with several keywords
  - *Undo* and *Discard*
  - log-only mode
  - Keyword Arguments
  - popup and dialog
  - ending by `idle_timeout`
- **AC-43** The unit tests (Python and jest) run without a browser; lint and type checks are
  clean.
- **AC-44** None of the proof of concept's working documents (handoff notes, its spec and
  plan, the plugin README) are part of the change. Usage is documented in the keyword documentation, rationale in
  `Browser/recorder/CONTEXT.md` and ADRs 0010 and 0011. Statements about the Playwright
  version match the version in use.

## Feature scope

The feature scope is fully described by acceptance criteria **AC-01 to AC-41**. Anything not
stated there is not part of v1.

## Out of scope (possible future extensions)

These are deliberately not part of v1. The design should not block them.

**Editing and structure**
- Editing keywords that are already finished
- Reordering Keyword Calls or editing them directly (keyword, selector, arguments)
- Appending to an existing User Keyword
- Recording or inserting control structures (`IF`, `FOR`, `TRY`)
- Extracting recorded values into variables (`${VAR}`) instead of Keyword Arguments
- Selectors as Keyword Arguments or as variables (page-object style)

**Recording**
- Several browser contexts in one session
- A non-blocking `Start Recording` / `Stop Recording` pair, with the test continuing
- A Browser keyword for `assertSnapshot` (ARIA snapshot)
- Merging Actions beyond what Playwright merges itself (e.g. `Fill Text` + `Enter`)
- Optional treatment of password fields, e.g. `Fill Secret` behind a toolbar switch

**Target and output**
- Changing the target file from the toolbar during a session, or one file per keyword
- Generating a test case that calls the recorded keywords
- Generating `[Documentation]` automatically

**Integration**
- Hiding Playwright's toolbar, or forwarding `modeChanged`, through a Playwright patch
- IDE integration, e.g. starting from RobotCode or a live preview in the editor
- Replacing the private Playwright API once a public one exists

## Documentation scope

**For users (keyword documentation, shown in Libdoc)**
- `Record Keyword` and `Record Keywords`, each with:
  - purpose and when to use which, each referring to the other
  - every argument: `name`, `file` (default `${SUITE_SOURCE}`, log-only mode with
    `${None}`), `idle_timeout`
  - return value
  - at least two examples: recording into the suite file and into a `.resource`
- The toolbar: every button, idle and recording state, *Undo* / *Discard*, Keyword
  Arguments (whole value, part of a value, default, replacing repeated values)
- Every way a session ends, and that a running Keyword Recording is always saved
- What gets generated: the `recorded` tag, popups → `Switch Page`, handling of dialogs and
  downloads, the notice for unsupported Actions
- Naming rules: why names are rejected (shadowing existing keywords), and that existing
  keywords are never extended
- **Security note:** the body contains values from the page and must be reviewed before
  committing; passwords are recorded in plain text
- Limitations: dependency on the Playwright version, a single browser context, and that the
  recorder stays registered in the context after the session

**For developers**
- `Browser/recorder/CONTEXT.md`: the glossary, kept up to date
- ADR 0010 (the page under test is untrusted) and ADR 0011 (action stream instead of
  codegen)
- `Browser/recorder/README.md`, short:
  - architecture (Python engine, TypeScript wrapper, toolbar, poll cycle)
  - selector translation
  - what Playwright does before the sink (fill merging, click buffer, signals)
  - **a checklist for Playwright upgrades**: what to check and which tests cover it
- Code comments where something is surprising without context (e.g. why
  `_disableRecorder` is never called)

**Release**
- A release notes entry: new feature, experimental dependency on the private Playwright API,
  security note
- The proof of concept's working documents are not carried over; what the plugin README
  says is absorbed into the documents above

## Expected test coverage

**Python unit tests (no browser)**
- **ActionMapper**
  - every supported Action type, including modifier keys, mouse buttons and double click
  - every row of the selector table; untranslatable selectors pass through unchanged
  - an unknown Action produces no Keyword Call
- **Writer**
  - creating a file and a section
  - writing live
  - re-reading after an external change outside the block: change is kept
  - external change or deletion of the own block: block is rewritten
  - *Discard* restores the original state
  - `[Arguments]` with and without defaults, partial values, `[Tags]    recorded`
  - log-only mode without a file
  - formatting of existing content is preserved
- **RecorderSession**
  - every command in every state (idle, recording, fixed name)
  - deferred *Finish*, *Discard* and *Stop*
  - *Undo* removes a group (dialog, download)
  - merging through `actionUpdated`, also after *Undo*
  - Keyword Arguments: create, partial value, replace repeated values, removal on *Undo*,
    default following continued typing
  - name validation as a matrix: duplicate, normalisation, BDD, embedded arguments,
    owner-qualified, symlink, invalid names, argument names
- **Session driver (poll loop with a fake stub)**
  - every way a session ends
  - `idle_timeout` reset by Actions and commands
  - cleanup always runs; the running Keyword Recording is saved on an exception
  - malformed events and commands are ignored
  - resolution of the `${SUITE_SOURCE}` default

**Node / jest**
- both payload shapes (1.62 wrapped, 1.63 bare)
- filtering of toolbar Actions
- buffering and draining of events and commands; the reset poll at session start
- signals (popup, dialog, download) attached to the right Action
- detecting whether Playwright is still holding back Actions
- rendering the toolbar state

**Acceptance (`atest/`, scripted, in CI on all platforms)**
- `Record Keywords` with at least two keywords and idle navigation in between that is not
  recorded
- `Record Keyword` with a fixed name, and its return value
- *Undo*, *Discard*, and a click right before *Finish*
- log-only mode (`file=${None}`): no file, block in the log
- Keyword Arguments, including a partial value and a default
- popup → `Switch Page    NEW`, dialog, download
- ending by `idle_timeout` and by closing all pages
- a rejected name that would shadow a library keyword
- **the generated keyword is then executed and does the same as the recording.** This round
  trip is the central evidence.
- a second session in the same context records nothing twice

**Targets**
- at least 90 % line coverage for `Browser/recorder/` and `Browser/keywords/recorder.py`;
  full branch coverage for name validation and the state machine
- the acceptance suite runs on every Playwright upgrade and fails when the action stream
  changes (see ADR 0011)
