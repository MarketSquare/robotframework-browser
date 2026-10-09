# Test App Rich Logging

Terminology for the rich logging infrastructure that correlates Robot Framework test execution with HTTP server activity in the `node/dynamic-test-app` acceptance test setup.

## Language

### Infrastructure

**Test App**:
The Node.js Express server in `node/dynamic-test-app/dist/server.js` that serves as the system under test for acceptance tests.
_Avoid_: demo app, test server (ambiguous with "RF test")

**Test App Log File**:
The file `atest/output/test-app/test-app-{port}.log` that captures all stdout of one Test App process. One file per process, named by port.
_Avoid_: server log, node log

**RF Listener**:
The Python library in `atest/library/test_app_listener.py` that hooks into Robot Framework lifecycle events and POSTs **Context Events** to the Test App.
_Avoid_: listener library, event listener (collides with browser sense)

**Test App Logger**:
The plain JavaScript file `node/dynamic-test-app/static/test-app-logger.js` loaded by every test page in the browser. Captures user interaction and navigation and POSTs **Page Events** to the Test App.
_Avoid_: client logger, browser logger

### Log entries

**Log Entry**:
A single JSON line written to stdout by the Test App, captured into the Test App Log File. Every Log Entry has `timestamp` and `event`.
_Avoid_: log line, log record

**Server Event**:
A Log Entry written directly by the Test App process itself. Current Server Events are `server_start` and `http`. `http` carries request metadata such as `method`, `url`, `status`, `contentLength`, and `responseTimeMs`.
_Avoid_: access log, startup log

**Context Event**:
A Log Entry that describes a Robot Framework lifecycle moment: `start_suite`, `end_suite`, `start_test`, or `end_test`. Produced by the RF Listener. Carries `id` (structural RF id like `s1-s2-t3`), `name`, and `pid`.
_Avoid_: RF event, suite event, test event

**Page Event**:
A Log Entry that describes a browser interaction captured by the Test App Logger: clicks, form submissions, navigations, hover, drag-and-drop, checkbox/radio changes. Carries `tag`, `text`, `url`.
_Avoid_: browser event (ambiguous with DOM `Event`), UI event

### Identifiers

**RF Structural ID**:
The auto-generated positional path Robot Framework assigns to each suite and test (`s1`, `s1-s2`, `s1-s2-t3`). Found in `data.id` of listener v3 methods. Used in Context Events as the `id` field.
_Avoid_: suite id, test id (too vague)

## Relationships

- The **RF Listener** POSTs **Context Events** to the HTTP **Test App** via `POST /api/log/context`
- The **Test App Logger** POSTs **Page Events** to whichever **Test App** process served the page via `POST /api/log/event`
- The **Test App** itself writes **Server Events** directly to stdout, including `server_start` and `http`
- All three kinds of **Log Entry** are written to the same **Test App Log File** for that process (stdout → file)
- HTTP and HTTPS **Test App** processes are separate, each with their own **Test App Log File**, named by port
- `pid` is present on **Context Events** and distinguishes parallel pabot worker RF processes writing to the same file

## Example dialogue

> **Dev:** "I can see Page Events in the log but no Context Events — how do I know which test was running?"
> **Domain expert:** "The RF Listener only posts to `${SERVER}`, which is always the HTTP Test App. If you're looking at an HTTPS Test App Log File, you'll only see Page Events there — check the HTTP log file for the matching Context Events by timestamp and pid."

## Flagged ambiguities

- "event" was used for both DOM events in the browser and RF lifecycle events — resolved: **Page Event** (browser) vs **Context Event** (RF lifecycle).
- "server" was used for both the Node.js process and the RF variable `${SERVER}` (host:port string) — resolved: **Test App** for the process, `${SERVER}` for the variable.
