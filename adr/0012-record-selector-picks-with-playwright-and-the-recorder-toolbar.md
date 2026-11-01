# Record Selector picks with Playwright and shows the result in the recorder toolbar

`Record Selector` used to inject its own panel and a copy of `@medv/finder` into the page:
the element under a pointer held still for three seconds became a CSS selector, chosen from
up to four variants. It now calls Playwright's public `page.pickLocator()` and shows the
result in the recorder toolbar's `selector` mode, driven from Python by polling like a
**Recording Session**. One click picks, the click never reaches the page, and the selector
is Playwright's, translated by the same `to_browser_selector` as recorded keywords use, so
`Record Selector` and `Record Keyword` write the same selector for the same element. CSS
selectors stay available as a second generator (`SelectorGenerator`), from the current
`@medv/finder`, bundled at build time and run on the picked element.

## Consequences

- **Picking uses public API; reading the result does not.** `pickLocator()` returns a
  `Locator`, whose selector is only reachable through the private `_selector`. The
  Playwright upgrade checklist in `Browser/recorder/README.md` covers it.
- **One command channel per context.** `__rfbCommand` can be exposed only once per browser
  context, so the recorder and the picker register their buffers on a shared channel, and
  `Record Selector` refuses to start while a Recording Session runs there:
  `pickLocator()` switches Playwright's recorder off.
- **The toolbar's isolation and look come for free**: closed shadow root, events stopped
  at the host and on window, usable over page modals, no Content Security Policy issue.
  Its commands are page-callable like the recorder's (ADR 0010); the selector it returns
  is to be checked like a recorded keyword.
- **Backwards incompatible default.** The selector is Playwright's unless
  `generator=css` is given; the hover countdown and the variant list are gone.
- **Further generators** are a new `SelectorGenerator` value and a function in
  `element-picker.ts`; a public plugin API for them is not built, but nothing in the
  toolbar or the protocol rules one out.
