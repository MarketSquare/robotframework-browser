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

- **Screenshot inside the Node catch**, as #5261 first proposed. Rejected: `run_on_failure`
  can be any keyword with any arguments, or `None`. Node would bypass the user's setting and
  have to duplicate `_failure_screenshot_path()` naming.
- **Keep the early close, only log honestly** that the failed page was gone. Rejected as the
  fix: it discards the only evidence of the failure. It remains the fallback when the
  screenshot itself fails.
- **Let `run_keyword` special-case `New Page` by name.** Rejected in favour of a cleanup
  queue owned by `Browser`: the keyword that created the failed page asks for its removal, and
  `Browser` decides when.
- **Close the current page afterwards.** Rejected: the on-failure keyword may have switched
  or opened pages.

## Consequences

- **Removal is scoped per `run_keyword` call.** `Browser` keeps a stack of cleanup queues; each
  `run_keyword` drains only what was queued during its own call, in `finally`, so a failing
  `New Page` inside a user's on-failure keyword never removes the outer failed page early.
- **An empty stack means the Python path.** With no `run_keyword` in flight there is no
  failure handling to wait for, so `new_page` removes the failed page immediately.
- **Removal always happens**, even when `run_on_failure` is `None`, `keyword_error` returns
  early, or the on-failure keyword raises. A failing removal is logged at `warn`; the
  original `New Page` error is what is raised. The browser catalog after a failed `New Page`
  is unchanged, as before.
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
- **During failure handling the failed page is visible** in `Get Browser Catalog` and
  `Get Page Ids`. That is the point, not a leak.
- **Only the page is removed.** A browser or context that `New Page` created stays, since they
  are reusable.
- **Load-state diagnostics** (`readyState`, navigation and resource timings) are a separate
  concern and not part of this decision.
