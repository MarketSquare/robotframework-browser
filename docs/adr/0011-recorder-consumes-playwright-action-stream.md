# The recorder consumes Playwright's action stream, not generated code

Playwright's recorder can generate Python or JavaScript, which could then be translated into
Robot Framework. Instead, `Record Keyword` and `Record Keywords` enable Playwright's
programmatic recorder (`context._startRecording`, `context._enableRecorder` with `recorderMode: 'api'` before 1.64) and consume its
structured **Actions** directly. Every Action reaches us the moment it happens, with a
selector we can map to a Browser selector, so a **Keyword Call** is written live and can be
undone in the toolbar. That is what makes recording usable from the middle of a test run,
where names are given and mistakes corrected while recording. A code generator delivers
finished source and would have to be parsed back.

## Consequences

- **A core keyword depends on a private Playwright API.** `_startRecording` and the shape of
  its event payloads are not public and have already changed twice: up to 1.62 an Action
  arrives wrapped in its `ActionInContext`, from 1.63 bare; 1.64 replaced `_enableRecorder`
  with `_startRecording`. The toolbar also relies on the injected recorder ignoring events
  from inside an `x-pw-glass` element. Every Playwright upgrade must re-check the recorder
  (the checklist is in `Browser/recorder/README.md`). If the API is missing, the keyword
  fails with a clear message instead of recording nothing.
- **What Playwright does before the sink shapes what we get.** Consecutive keystrokes of a
  fill arrive as one `actionAdded` followed by `actionUpdated`, a double click as one
  `click` with `clickCount: 2`, and left clicks only after a 500 ms buffer. Popups,
  downloads and dialogs arrive as signals after the Action that caused them.
- **Playwright's own in-page toolbar cannot be hidden** in api mode, so its Record button is
  a second way to end a **Recording Session**.
