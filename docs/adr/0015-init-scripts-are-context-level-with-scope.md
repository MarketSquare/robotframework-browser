# Init scripts are context level, with a scope

Playwright registers an **init script** on a page (`page.addInitScript`) or on a context
(`browserContext.addInitScript`), and both return a `Disposable`. `Add Init Script` (#5099)
exposes only the context level, on the active context, with the library's `scope` (`Test` by
default) deciding when the script is disposed: when that test or suite ends, or when its context
closes, whichever comes first. There is no page-level variant and no way to switch to one.

The two axes, where a script lives (page or context) and how long it lives (`scope`), could not
both be offered: together they are hard to build and harder to explain. With automatic closing
they mostly overlap anyway, since a page or context opened in a test already closes with that
test. They part ways when a suite shares one context opened in Suite Setup and one test needs a
script that covers the popups it opens without leaking into later tests. Only the context level
with a scope does both. A page-level script misses popups, and a context-level script without a
scope stays until the suite ends.

## Considered options

- **A target argument, page or context, with no scope.** This was the first proposal, under the
  name `scope=Page|Context`, which clashes with what `scope` means everywhere else in the library.
  Rejected: it cannot stop a context-level script from leaking into later tests in a shared
  context, and page level misses popups.
- **Both a target and a scope.** Rejected: one keyword with two lifetime rules, the page's and the
  scope's, is too hard to explain for the few cases it would add.

## Consequences

- A script for one page alone, leaving other pages of the same context untouched, cannot be
  added. The test opens its own `New Context` instead.
- Disposing of a script only stops it on later navigations. A page that already ran it keeps what
  it changed until the page reloads.
- `scope=Test` fails outside a test, meaning in suite setup or teardown; test setup and teardown
  belong to the test. Without a running suite, as when the library is used from Python, every
  scope behaves like `Global`, which keeps the script until its context closes.
- No `Remove Init Script` keyword: the scope removes it.
