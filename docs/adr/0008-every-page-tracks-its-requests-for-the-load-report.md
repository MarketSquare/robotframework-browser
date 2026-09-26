# Every page tracks its outstanding requests, so a load timeout can say what was still loading

When a keyword's wait for a page to load times out, the error alone cannot tell "the page never
loaded" from "the wait missed the event" (#5272). The **load report** that answers this is
logged by all seven keywords that wait for a page to load: `New Page`, `Go To`, `Reload`,
`Go Back`, `Go Forward`, `Wait For Navigation` and `Wait For Load State`. To name the requests
still outstanding, every page listens to Playwright's `request`, `requestfinished` and
`requestfailed` events from the moment it is created, for its whole life.

## Considered options

- **The page's own Resource Timing** (`performance.getEntriesByType('resource')`), as #5272
  first proposed. Rejected: Chromium adds an entry only when its request completes, so a
  stalled request never appears, and a main document that never answers leaves no document to
  ask. Verified against Playwright 1.63.
- **Track only while one of the seven keywords runs.** Rejected: `Wait For Load State` starts
  no navigation of its own; the requests blocking it began before the keyword was called.
- **An import option that turns tracking on.** Rejected: the report would be missing exactly
  when a user did not expect to need it, and it would add a setting to the library.

## Consequences

- **Every page pays for the listeners.** Playwright sends request events for subresources only
  once someone subscribes, so this adds protocol traffic that did not exist before. Measured
  with headless Chromium: about 5% (+9 ms) on a page making ~1000 requests, about 10% (+52 ms)
  on one making ~4000.
- **A page forgets the requests of the document it left.** Chromium drops them when the main
  frame commits a new document, without Playwright firing `requestfailed`, so once the main
  frame navigates to a committed document, requests that started before its document request
  are no longer counted as outstanding.
- **A page adopted from an already running browser** (`Connect To Browser`) is tracked from
  the moment the library indexes it; requests that were already running then are not seen.
- **A page that never committed is not asked anything.** `evaluate` blocks while the main
  document has no response, even after the keyword's own wait gave up, so the report reads
  `readyState` and navigation timing only once the document request has a response.
- **Requests that never end by design** (EventSource, long polling) always appear as
  outstanding. The report lists each request's resource type and age rather than filtering
  them, because such a request can be the very thing blocking `networkidle`.
- **The report travels on the gRPC error as trailing metadata** under the binary key
  `load-report-bin` (UTF-8, since URLs may not be ASCII), and Python logs it where it turns
  every gRPC error into an `AssertionError`. The error message users match on is unchanged,
  and no keyword needs code of its own on the Python side. The report is capped in Node so
  that oversized metadata can never fail the call in place of the timeout.
- **The report never replaces the timeout.** A probe that fails is logged in the Node log and
  shown as unknown in the report; a report that cannot be built is logged in the Node log and
  left out, and the original timeout is raised either way.
