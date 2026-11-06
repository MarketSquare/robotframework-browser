# Recorder

Recording what a person does in the live browser and writing it out as Robot Framework User
Keywords made of Browser keywords. Code generation is avoided on purpose: recording can start
anywhere in a test run, and the person names each keyword while recording.

## Language

### Time

**Recording Session**:
Everything from the call of `Record Keyword` or `Record Keywords` until it returns. It holds
one or more **Keyword Recordings**, and the session is **idle** between them.
_Avoid_: recording, session (on its own, when the meaning is unclear)

**Keyword Recording**:
The part of a **Recording Session** in which exactly one User Keyword is being recorded,
from *Record keyword* until *Save* or *Discard*. `Record Keyword` is a **Recording Session** with
exactly one **Keyword Recording**, which starts immediately.
_Avoid_: recording, active keyword

**Idle**:
The state of a **Recording Session** with no **Keyword Recording** running. **Actions** that
happen while idle produce no **Keyword Call**.
_Avoid_: paused, stopped

### What is recorded

**Action**:
One interaction as Playwright's recorder reports it: a click, a fill, a navigation, an
assertion. Raw material, not yet Robot Framework.
_Avoid_: event (that is the transport), step

**Keyword Call**:
One line in the body of a recorded User Keyword: a Browser keyword with its arguments. An
**Action** may produce no Keyword Call (no Browser equivalent, or the session was **idle**),
several Keyword Calls (a click that opens a dialog or starts a download needs its handling
written around it), and several **Actions** may become a single Keyword Call when Playwright
refines an action.
_Avoid_: step, statement, line

**Keyword Argument**:
A value of a **Keyword Call**, or a marked part of one, that the person turned into an argument of the recorded User
Keyword while recording, so the keyword can be called with other data.
_Avoid_: parameter, variable

## Relationships

- A **Recording Session** has one or more **Keyword Recordings**; between them it is **idle**
- A **Keyword Recording** produces exactly one User Keyword made of **Keyword Calls**, or
  nothing if it is discarded or has no **Keyword Calls** when it ends
- A **Keyword Recording** that is still running when its **Recording Session** ends (✕ in the toolbar,
  inactivity, all pages closed, error) is saved, never discarded
- A **Keyword Recording** always creates a new User Keyword; it never extends an existing one
- Every recorded User Keyword carries the tag `recorded`, so it can be found and reviewed
- A **Keyword Argument** is made from a value or a selector, or a part of one, never from a
  structural value (mouse button, operator), and only while its **Keyword Recording** is
  running. A **Keyword Argument** no **Keyword Call** uses any more
  is removed; a recorded keyword never has unused arguments
- Password fields get no special treatment: the person decides whether a typed value becomes
  a **Keyword Argument**, with or without its recorded value as default
- Undo removes every **Keyword Call** the last **Action** produced, never just part of them
- A recorded User Keyword never creates a page: it runs in the page its caller set up. A page
  opened by an **Action** becomes a switch to that page, not a new one

## Flagged ambiguities

- "keyword call" in the Browser Library context means a keyword *being invoked* at runtime.
  Here a **Keyword Call** is a *line in a file*. The two contexts are separate, so the word
  is kept in both.
- "recording" was used both for the whole session and for one keyword. Resolved: **Recording
  Session** versus **Keyword Recording**.
