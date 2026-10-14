# The recorder treats the page under test as untrusted

The recorder toolbar sends its commands (`new`, `finish`, `undo`, `discard`, `stop`) through
a binding registered with `context.exposeBinding`, and that binding is callable by **any**
script on the page, not only by the toolbar: a compromised dependency, a third-party widget,
an XSS payload. A recorded keyword lands in a `.robot`/`.resource` file, and keywords from
such files outrank library keywords in Robot Framework's resolution order. So a page that
names a recording `Click` or `Log` would silently replace that keyword on the next run. We
therefore treat every name that arrives over the command channel as hostile input, and the
recorder rejects any name that would collide with, shadow or squat a keyword the running
suite can currently resolve. That covers normalised spellings, BDD-prefixed forms,
embedded-argument patterns, owner-qualified names and the target file reached through a
symlink. This was decided deliberately even though the usual target is one's own application
under development. The checks look excessive for that case, and they must not be removed on
those grounds.

## Considered options

- **Trust the page and check only for exact duplicates against typos.** Rejected: it leaves
  the shadowing hole open for every page that loads third-party script, which is most of them.
- **Secure the channel instead, e.g. with a per-session token that only the toolbar knows.**
  Not chosen as the defence: `exposeBinding` cannot be unregistered and is visible to all
  page script, so the token would have to be hidden from that script. The name checks hold
  regardless of who sends the command.

## Consequences

- **The check protects structure, not meaning.** It keeps the generated file a well-formed
  keyword definition that shadows nothing. The recorded *body* still comes from page-supplied
  values (URLs, file paths, typed text, assertion expectations), so a generated keyword must
  be reviewed before it is committed.
- **The set of known keywords is a snapshot** taken when recording starts. Keywords imported
  later in the same run, or from a suite running in parallel, are not protected.
- **An owner-qualified name that does not resolve today is accepted**, e.g. `Beta.Beta
  Action` when that library is imported under a different name. It hijacks nothing that
  works now.
- **The toolbar state is visible to page script.** It is rendered into every page of the
  context, so during a session any script on any of those pages can read it, including the
  recorded values and anything typed into password fields, and can send toolbar commands.
  The keyword documentation says so; recording against pages that load untrusted script
  exposes what is typed.
- **The command channel is bounded.** Commands are accepted only while a session runs, and
  oversized commands and Actions are logged and dropped, so a page cannot end a session by
  pushing a poll reply past the gRPC message limit.
