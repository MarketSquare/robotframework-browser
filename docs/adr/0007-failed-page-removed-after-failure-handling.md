# A failed page is removed after failure handling, not when its keyword fails

When `New Page` failed to navigate, Node closed the page inside the `newPage` catch, before
the error reached Python. `run_on_failure` then ran with that page already gone, so the
failure screenshot was either skipped or, worse, silently taken of some other open page and
embedded in the log as if it were evidence (#5261). We now keep the **failed page** open and
active until failure handling is done: Node records it instead of closing it, and Python
removes it through an internal `RemoveFailedPage` RPC once `keyword_error` and
`pause_on_failure` have finished. The user's own `run_on_failure` keyword therefore sees the
page that failed, whatever that keyword is.

## Considered options

- **Never remove the failed page**, as a failed `Go To` leaves its page. Rejected: `Go To`
  acts on a page the caller already holds, but a failing `New Page` never returns the page
  id, so the caller could not close or switch away from a page it never received. The page
  would stay in the catalog as the active page, with no id the caller ever received, and
  every later keyword would act on it. `New Page Will Timeout And Page Will Be Removed From
  Catalog` has asserted this contract since before #5261: after a failed `New Page` the
  catalog is unchanged. Keeping that contract while still letting failure handling see the
  page is what the RPC, the token, the Node map and the Python stack exist for.
- **Screenshot inside the Node catch**, as #5261 first proposed. Rejected: `run_on_failure`
  can be any keyword with any arguments, or `None`. Node would bypass the user's setting and
  have to duplicate `_failure_screenshot_path()` naming.
- **Keep the early close, only log honestly** that the failed page was gone. Rejected as the
  fix: it discards the only evidence of the failure. It remains the fallback when the
  screenshot itself fails.
- **Let `run_keyword` special-case `New Page` by name.** Rejected: the keyword that created
  the failed page asks `Browser` to remove it (`_remove_failed_page_after_failure_handling`),
  and `Browser` decides when.
- **A general "run this after failure handling" queue of callables.** Rejected: it would have
  one caller, would run at the end of every keyword call whether that call failed or not, and
  would invite unrelated "run this later" hooks. `Browser` keeps failed page tokens instead,
  and the method is private so plugins do not come to rely on it.
- **Close the current page afterwards.** Rejected: the on-failure keyword may have switched
  or opened pages.

## Consequences

- **Removal is scoped per `run_keyword` call.** `Browser` keeps a stack with one list of
  failed page tokens per `run_keyword` call; each call removes only the failed pages
  registered during it, in `finally`, so a failing
  `New Page` inside a user's on-failure keyword never removes the outer failed page early.
- **An empty stack means the Python path.** With no `run_keyword` in flight there is no
  failure handling to wait for, so `new_page` removes the failed page immediately.
- **The stack is per thread.** `Promise To` runs its keyword in an executor thread, outside
  `run_keyword`, while the main thread goes on with other keywords. With a shared stack a
  promised `New Page` would queue its removal on whatever keyword the main thread happened to
  be in, and could race that keyword's drain: lose the removal and leave the failed page
  active, or raise in place of the real error. A promise has no failure handling of its own,
  so its thread sees an empty stack and removes the failed page at once.
- **Removal always happens**, even when `run_on_failure` is `None`, `keyword_error` returns
  early, or the on-failure keyword raises. A failing `RemoveFailedPage` call is logged at
  `warn`; the original `New Page` error is what is raised. The browser catalog after a
  failed `New Page` is unchanged, as before.
- **The failed page is closed without waiting for it.** Node takes the page out of the page
  stack at once, then closes it fire-and-forget and logs a failed close only in the Node log,
  as the pre-#5261 code did. Awaiting `close()` hung in CI: a page closed milliseconds into
  its navigation, as with a 1 ms timeout, never finished closing, and the keyword ran into
  the test timeout.
- **Each `New Page` call names its failed page with a token.** Python sends a fresh token in
  the `NewPage` request; Node records a failed page under it, and `RemoveFailedPage` removes
  only the page recorded under that token. Without it, a nested `New Page` that fails before
  its page even exists would still queue a removal, and "remove the last failed page" would
  then remove the outer one early.
- **The failed page is removed by identity.** If it was still the active page, the page below
  it becomes active again; otherwise the active page is left as the on-failure keyword set it.
- **A keyword that swallows a `New Page` failure keeps the failed page until it returns.** A
  plugin keyword calling `new_page` runs inside the plugin keyword's own `run_keyword` call,
  so the removal waits for that call to finish. If the plugin catches the error and carries
  on, its later steps run against the failed page. Accepted: it needs a plugin that swallows a
  `New Page` failure, and such a plugin can switch back itself. This belongs in the plugin
  author documentation, not the `New Page` keyword documentation, which is for direct use of
  the library.
- **A page that never committed costs one more timeout and gives no screenshot.** When the
  server never answers, the failed page is still `about:blank` mid-navigation, and the default
  `Take Screenshot` waits for fonts until its own timeout, which `keyword_error` logs at
  `info`. So such a `New Page` fails after about twice the browser timeout, where it used to
  fail fast with a screenshot of another page or "no page open". Accepted: it only slows
  tests that are already failing, and the lost screenshot would have been blank anyway.
  Capping the failure screenshot's timeout would change failure screenshots for every
  keyword, and closing uncommitted pages at once would bring back the wrong-page screenshot.
  Stopping the navigation with `window.stop()` does not help: `evaluate` waits for the
  pending navigation. The load-state log line from #5272 will say why the screenshot is
  missing. When the page commits and then stalls, the screenshot is taken without delay.
- **During failure handling the failed page is visible** in `Get Browser Catalog` and
  `Get Page Ids`. That is the point, not a leak.
- **Only the page is removed.** A browser or context that `New Page` created stays, since they
  are reusable.
- **Load-state diagnostics** (`readyState`, navigation and resource timings) are a separate
  concern and not part of this decision.
