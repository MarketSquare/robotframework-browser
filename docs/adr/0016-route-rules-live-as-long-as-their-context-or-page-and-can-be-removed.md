# Route rules live as long as their context or page, and can be removed

A **route rule** (#5120) is added to the active context or the active page, chosen with
`on=Context|Page` (default `Context`), the same way as for `Set Extra HTTP Headers` and
`Add Init Script` (ADR 0015). It ends in one of three ways: its context or page closes, a
keyword removes it, or it has used up its `times`. It has no `scope` argument, and the library
never removes it when a test or suite ends. Unlike an init script it can be removed, because
a test has to be able to end a simulated outage in the middle of the test and then check
that the application recovers.

## Considered options

- **Removed when the library's `Scope` ends.** Rejected for the reasons in ADR 0015: it adds
  a second lifetime rule next to automatic closing, and on the **Python path** every scope
  becomes `Global`.
- **No removal, as with init scripts.** Rejected: an outage could then only end through
  `times` or by closing the context, and neither lets a test decide when the outage ends.

## Consequences

- A Page rule stays on the page it was added to. It does not follow `Switch Page` or move to
  a new page, and it ends when that page closes. Context rules keep applying to the context's
  other pages and to pages opened later.
- When one context is shared by a whole suite, a Context rule added in one test also applies
  in the tests after it. A test that needs a clean slate opens its own `New Context` or
  removes all route rules in its teardown.
- A rule is removed by the id its adding keyword returned, not by its matcher as with
  `Remove Locator Handler`: two rules with the same matcher stay distinguishable, and a Page
  rule can be removed while another page is active. Removing all rules covers the active
  context and every page in it, and only the rules this library added.
- The Robot Framework path and the Python path behave the same.
