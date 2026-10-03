# Global and scoped state flows from Browser through LibraryComponent

Settings such as `timeout`, `strict_mode` and `run_on_failure` live in one place: the
`scope_stack` of `Browser(DynamicCore)`, which is the context object of the library. Keyword
classes reach that state through `LibraryComponent`, a thin base class that gives them easy
access to the context plus the logic every keyword needs. State flows in one direction only:
`Browser` → `LibraryComponent` → keyword classes such as `class Cookie(LibraryComponent)`.

For each setting, `Browser` defines a typed property that reads the stack
(`Browser.timeout` returns `self.scope_stack["timeout"].get()`), and `LibraryComponent`
delegates to it (`return self.library.timeout`). The `*_stack` accessors on `LibraryComponent`
(`timeout_stack` and the rest) are the mutation seam: `Set Timeout` and the other scoped setters
replace or push on the stack object through them, so they are the one place outside `Browser`
that names a stack key.

## Considered options

- **Let `LibraryComponent` read the stack itself**, `self.library.scope_stack["timeout"].get()`.
  Rejected: two classes then index the same private dict by string. A `SettingsStack` refactor
  or a renamed key can change what one reader sees and not the other, and the wrong value looks
  exactly like a right one. Delegating gives each setting one typed definition that mypy checks.
- **Expose the state as keywords**, so plugins and acceptance-test helpers can read it back.
  Rejected: it grows the keyword count for a need no user has asked for. Plugins and libraries
  built on Browser read the internal property on `Browser` instead.

## Consequences

- **A new scoped setting is defined on `Browser` first**: the stack entry in `Browser.__init__`
  and a typed property reading it. Then `LibraryComponent` gets a delegating property and, if a
  keyword sets it, a `*_stack` accessor.
- **Reads go through the property, never the dict**, in keyword classes and in
  `LibraryComponent` alike.
