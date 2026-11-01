# Adopted contexts are registered by `call_js_keyword` from Node's report

A JavaScript extension hands Browser a context it created with `adoptContext`, for example the
context of an Electron app. Browser must then register it the way it registers the contexts of
`New Context`: open the keyword calls as trace groups, cache the video size, embed the video in
the log. Node writes a report on the response stream of the extension call as soon as
`adoptContext` resolves, with the context id, its trace file, the options the extension passed
as `contextOptions` and the video path of its active page. `call_js_keyword` registers each
report while it reads the stream. Every extension call goes through `call_js_keyword`, so a
plain `jsextension` keyword gets the same registration as a library built on Browser.

## Considered options

- **The caller registers**, with a public `register_adopted_context(context_id, options,
  video_path)` after the extension call. This was the first design (#5326), removed before it
  was released. The caller had to pass the same options twice, make the extension return the
  video path, and remember the call: forgetting it failed silently, with no trace groups and no
  video. A plain `jsextension` keyword had no way to make the call at all.
- **Register at the end of the call**, from the final message. Rejected: when the extension
  function throws after adopting, Python would never hear of a context that Node keeps.
- **Python as the source of truth**, registering from the options of `adopted_context_options`.
  Rejected: Python then believes what the options say, not what the extension did, for example
  whether it passed `tracing` to `adoptContext`. Node knows the trace file and the video it
  actually got.
- **Reuse the `json` field** of `Response.Json`, which extension calls leave empty. Rejected:
  it hides what the field means. `adoptedContext` is its own field.

## Consequences

- **`adopted_context_options` stays** as the one Python step. It holds what only Python
  knows: the trace path and `ROBOT_FRAMEWORK_BROWSER_TRACING`, the video folder and size, the
  HAR path and `tracesDir`.
- **`contextOptions` is optional.** Without it the video is still embedded, in the size of the
  viewport or 1280x720, and `Download` does not see `acceptDownloads`.
- **An extension function may adopt several contexts**; each one is reported and registered.
- **The report is registered on whatever path the call came from.** Trace groups exist only on
  the Robot Framework path, as for `New Context`.
