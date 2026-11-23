# The gRPC boundary is internal and mirrors Playwright

The rpcs in `protobuf/playwright.proto` are an internal contract between the Python keywords
and the Node wrapper, not a public API. They are reshaped without a deprecation period. Plugins
and libraries built on Browser call keywords or internal `Browser` properties, never rpcs
directly. Each Playwright call maps to one rpc, and Playwright's optional arguments become fields
on that rpc's request message. That message is a typed proto message, not `Request.Json`. So
"no filter means all" is Playwright's rule, carried through Node unchanged, and not a branch in
Python between two rpcs.

This was decided on the cookie keywords (#5449) after both shapes were prototyped.
`GetCookies(Request.CookieQuery)` replaced the pair `GetCookies(Empty)` and
`GetCookiesForUrls(Json)`, and `DeleteAllCookies(Request.CookieFilter)` replaced the pair
`DeleteAllCookies(Empty)` and `DeleteCookies(Json)`.

## Considered options

- **Keep the `Request.Empty` rpcs for plugin callers and add Json rpcs beside them.**
  Rejected: it keeps two wire paths for one Playwright call, and the choice between them stays a
  branch in every keyword. Plugins get their stability from keywords instead.
- **`Request.Json` for the filter.** Rejected: neither side of the boundary is typed, the Node
  side parses into a hand-written interface, and a renamed field fails only at runtime.

## Consequences

- **Every optional argument of the Playwright call is a proto3 `optional` field.**
  `clearCookies({ name: '' })` deletes only cookies with an empty name, while a missing `name`
  matches every cookie. A plain `string` field cannot tell the two apart, so
  `Delete All Cookies    name=${EMPTY}` would delete every cookie. With `optional`, ts-proto
  generates `name?: string` and Python passes `None` as unset. The rule covers fields where empty
  and missing behave the same today too, such as `secure` in `Request.Cookie` (#5458): the
  message then mirrors Playwright's argument one for one, and nobody re-derives the difference
  field by field when Playwright's defaults change.
- **Keeping the rpc name is a free side effect, not a promise.** When an rpc moves from
  `Request.Empty` to a typed message whose fields are all unset by default, the old name costs
  nothing to keep: the empty message encodes to the same bytes as `Request.Empty`, so a stray
  outside caller still works. The rpc stays internal and may still change without notice.
