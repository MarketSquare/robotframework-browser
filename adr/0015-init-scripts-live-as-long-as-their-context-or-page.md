# Init scripts live as long as their context or page

`Add Init Script` (#5099) registers an **init script** on the active context or the active page,
chosen with `on=Context|Page`, and the script lives until that context or page closes. It has no
`scope` argument and nothing removes it when a test or suite ends. Contexts and pages already
close by the automatic closing level, so the script follows a lifetime users already know, and
the keyword has one rule to explain, build and document instead of two.

## Considered options

- **Context level only, removed when the library's `Scope` (`Test`, `Suite`, `Global`) ends.**
  Prototyped in PR #5516. Rejected: it puts a second lifetime rule beside automatic closing,
  needs bookkeeping in Node and hooks at the end of every test and suite, and on the **Python
  path** every scope collapses to `Global` anyway.
- **Both a target and a scope.** Rejected: two lifetime rules on one keyword.

## Consequences

- When one context is shared by a whole suite, a context-level script added in one test also
  runs in the later tests, and a page-level script misses the popups of its page. A test that
  needs neither opens its own `New Context`, which closes with the test.
- No `Remove Init Script` keyword and no return value. Playwright drops the script when its
  context or page closes.
- The order of several init scripts is not defined, also between context and page level: this
  comes from Playwright.
