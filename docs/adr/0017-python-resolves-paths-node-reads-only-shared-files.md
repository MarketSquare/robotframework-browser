# Python resolves every path; Node reads a file only when it shares it

Every file a keyword takes belongs to one category, and the category sets the base of a relative
path: **test content** is relative to the working directory of the Python process, an
**artifact** to `${OUTPUT_DIR}`, a **temp file** lives under `${OUTPUT_DIR}/browser`, and an
**environment path** is relative to the working directory of the Python process too. Python
resolves every relative path and Node only gets absolute ones; an empty value is never resolved
and keeps today's meaning. When the library starts Node, its working directory is the wrapper
folder inside the installed package, so any path Node resolves itself lands in `site-packages`.

Keyword rpcs keep taking paths, and one shared mechanism decides which path Node gets. When a
check proves that the path means the same file on both sides, Node gets the original path and
nothing is copied, which is the common case of Node on the same machine. Otherwise the file is
**staged**: Python streams it in byte chunks into a staging file on the Node side, or fetches a
file Node wrote there. Uploads, storage states and downloads go through this mechanism.

Content that Node only needs in memory never goes to disk on the Node side. Screenshots and PDFs
always come from Playwright's buffer and are written by Python. `FileUploadBuffer`, certificates,
a `bytes` body of `HTTP` and a `MultipartFile` `buffer` are sent as content. An `HTTP` multipart
file given by `path` is read by Node itself when Node shares the file; otherwise Python sends its
bytes like a `buffer`, because the page's `fetch` needs them in memory anyway. Files that
Playwright or Node write during the run (traces, videos, HAR, coverage) stay where Node runs. A
relative environment path fails only when the resolved file does not exist where Node runs.

The work is tracked in issue #5620.

## Considered options

- **Always stream file content over gRPC.** One code path, and the filesystem never matters.
  Rejected: the common setup, Node on the same machine, would copy every upload and download
  through gRPC and store it twice, although Playwright already reads from a path. The cost of
  two ways is accepted, and an internal switch forces the not-shared way so CI tests it.
- **Send every file as content in its own streaming rpc.** Rejected: every keyword would need
  its own streaming rpc and its own remote handling. With staging the keyword rpcs that take a
  path stay unary. Content is used where it is simpler or safer: screenshots and PDFs, whose
  buffer Playwright produces anyway; `FileUploadBuffer` and `HTTP` content, which are in memory
  already; and certificates, whose private keys must not land in a temp folder.
- **Stage an `HTTP` multipart file that Node does not share.** Rejected: Node would write the
  file to its disk only to read it back into memory for the page's `fetch` at once. Sending it
  like a `buffer` reuses the way that `HTTP` content takes anyway, and leaves nothing to clean
  up.
- **Detect a remote Node by its host.** Rejected: a Node process in a container behind a mapped
  port is `localhost` as well. The check compares the file itself (`st_dev`, `st_ino`, size,
  mtime) and probes directories with a token file that Node writes, so it can only fail towards
  the not-shared way.
- **Let Node resolve relative paths.** Rejected: the base would be the wrapper folder, or
  whichever directory a shared Node process was started in.
- **A relative `saveAs` always relative to the working directory, ignoring `downloadsPath`.**
  Rejected: `downloadsPath` is the user's own choice, so when the user sets it, a relative
  `saveAs` is relative to it. The library's default `${OUTPUT_DIR}/browser/downloads` is a temp
  folder and not a base.
- **Always set the default `downloadsPath`.** Rejected: with Node on another machine the
  browser would be told to download into a Python path, and downloads that work today in
  Playwright's temp folder would break. The default is set only when Node shares the
  filesystem; `tracesDir` follows the same rule.
- **Fail on every relative environment path when Node does not share the working directory.**
  Rejected: setups that work today, such as two containers from the same image, would break. A
  keyword fails only when the resolved file does not exist where Node runs.
- **Raise the gRPC receive limit instead of streaming.** Rejected: the ceiling only moves, and
  every request up to it is built and parsed as one message, so both sides hold the whole file in
  memory at once. Both sides would also have to raise the limit in step, for requests and
  responses alike.

## Consequences

- Relative paths that landed in the package folder before (`saveAs` without `downloadsPath`,
  `downloadsPath`, `executablePath`, `external_browser_executable`, `userDataDir`,
  certificates) are relative to the working directory now. Downloads without `saveAs` land in
  `${OUTPUT_DIR}/browser/downloads` when Node shares the filesystem. A relative coverage
  `config_file` takes effect instead of being ignored. All of this goes into the release notes.
- A staged upload lives as long as its context, because the browser may read the file only
  when the form is submitted. Playwright keeps its own upload copies the same way. A staged
  storage state is released when the keyword ends, a staged download after the fetch.
- The library stops Node with SIGKILL, so Node cannot clean up on exit. Python releases all
  staged files before it stops Node, and a starting Node removes the staging folders of Node
  processes that no longer run.
- A download with `wait_for_finished=False` is saved by a later `Get Download State`, so Python
  keeps a record per download id until the file is fetched.
- With a Node process on its own filesystem, traces, videos, HAR and coverage are not on the
  Python side, a download without `saveAs` returns a path that only Node can read, and
  `Merge Coverage Reports` fails. This is documented.
- `HttpRequest` becomes a client stream for its content, because a request over 4 MB fails
  today. The future `Send API Request` keyword takes the same `MultipartFile` and follows the
  same rules.
- The library sets no size limit of its own. gRPC limits a single message, not a stream, and
  every transfer is chunked, also the screenshot bytes, which can exceed 4 MB. Content held in
  memory (`HTTP` bodies and multipart files, `FileUploadBuffer`, screenshots) is bound by
  memory. Playwright's own limits stay and are documented: 50 MB for `FileUploadBuffer`, and
  50 MB for uploads over a CDP connection to a browser that does not run next to Node.
- Node hands out and deletes only files in its own staging folder, by handle, never by a free
  path, and only to the peer that staged them. Staging files are created readable by their
  owner only.
- `--load-extension=` inside `args` is a free-form argument and is only documented.
- The library intro gets one `File paths` section with the four categories, and every
  docstring that takes a path names its category and links to it.
