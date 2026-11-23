# Browser library 21.1.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 21.1.0 is a new release with several enhancements and bug fixes, for
full details read the issues in below. This release has been sponsored by Robot
Framework foundation ecosystem project. Browser library test Automation Runners / CI
are sponsored by namespace (namespace.so) All issues targeted for Browser library
v21.1.0 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av21.1.0).
For first time installation with [pip](https://pip.pypa.io/en/stable/) and
[BrowserBatteries](https://pypi.org/project/robotframework-browser-batteries/)
just run
```bash
   pip install robotframework-browser robotframework-browser-batteries
   rfbrowser install
```
to install the latest available release. If you upgrading
from previous release with [pip](http://pip-installer.org), run
```bash
   pip install --upgrade robotframework-browser robotframework-browser-batteries
   rfbrowser clean-node
   rfbrowser install
```
For first time installation with [pip](http://pip-installer.org) with Browser
library only, just run
```bash
   pip install robotframework-browser
   rfbrowser init
```
If you upgrading from previous release with [pip](http://pip-installer.org), run
```bash
   pip install --upgrade robotframework-browser
   rfbrowser clean-node
   rfbrowser init
```
Alternatively you can download the source distribution from
[PyPI](https://pypi.org/project/robotframework-browser/) and
install it manually. Browser library 21.1.0 was released on Monday November 23, 2026.
Browser supports Python 3.11+, Node 22/24 LTS and Node 26, and Robot Framework 7.1.1+.
Library was tested with Playwright 1.65.1. BrowserBatteries package was
released with NodeJS 26.13.1.


## Most important enhancements

### `HTTP` follows the browser fetch API ([#5109](https://github.com/MarketSquare/robotframework-browser/issues/5109))
`HTTP` sends a page request with `fetch` in the active page. Before, it supported
only `url`, `method`, `body` and `headers`, and `HEAD` did not work. Now `HTTP`
takes the arguments of the browser fetch API, with the same names. It can send a
form, a `multipart/form-data` file upload and a binary HTTP body. It returns the
response body as `bytes`, `text` and `json`, the same as `Wait For Response`.
Also, `HTTP` now stops after the library timeout, but before it had no time limit.
To wait without a limit, use `timeout=0`. Many thanks to René for this
enhancement.

### Abort Requests, Remove Route Rule, Remove All Route Rules ([#5617](https://github.com/MarketSquare/robotframework-browser/issues/5617))
This release adds route rules to Browser. A route rule controls the requests that
match a glob or a regular expression before they go to the network. You can add a
route rule to the active context or to the active page:
- A context rule applies to all pages of the context, also to pages that open
  later.
- A page rule applies only to the page that you add it to.

A route rule stays until its context or page closes, until you remove it, or until
it has run `times` times. It does not end at the end of a test or suite.

Each keyword that adds a route rule returns a rule id. `Remove Route Rule` removes
the rule with that id. `Remove All Route Rules` removes all rules of the active
context and of its pages. Both keywords log how many times each rule ran
([#5628](https://github.com/MarketSquare/robotframework-browser/issues/5628)).

`Abort Requests` is the first keyword that adds a route rule. It makes the matching
requests fail with an error code. Use it to test an error path, to block analytics,
or to make a server unavailable to the page.

### Mock Responses ([#5622](https://github.com/MarketSquare/robotframework-browser/issues/5622))
`Mock Responses` adds a route rule that gives a mock response to the page. The
request does not go to the server. You set the status, the headers and the HTTP
body of the mock response. Use it to test the frontend without the backend, or to
get an error status such as `500`. The rule uses the same `matcher`, `times` and
`on` arguments as `Abort Requests`.

### Modify Responses ([#5625](https://github.com/MarketSquare/robotframework-browser/issues/5625))
`Modify Responses` adds a route rule that sends the request to the server and then
changes the real response. The page gets the real response, and only the parts that
you specify are changed. You can change the status, the headers and the HTTP body.
With `json_patch` you can change one field of a JSON body. Before the request goes
to the server, the rule can also change its URL, method, headers and HTTP body.

### rfbrowser init and install offer chromium-tip-of-tree-headless-shell, which Playwright 1.63 removed ([#5492](https://github.com/MarketSquare/robotframework-browser/issues/5492))
Playwright 1.63 removed the `chromium-tip-of-tree-headless-shell` browser. But
`rfbrowser init` and `rfbrowser install` still showed it as a browser to install.
Now these commands do not show it.

### rfbrowser init offers bidi-chromium, which Playwright cannot install ([#5493](https://github.com/MarketSquare/robotframework-browser/issues/5493))
`rfbrowser init` showed `bidi-chromium` as a browser to install, but Playwright
cannot install it, so the installation failed. Now `rfbrowser init` does not show
`bidi-chromium`.

### Recorder writes English keyword names when Browser is imported with a translation ([#5509](https://github.com/MarketSquare/robotframework-browser/issues/5509))
When you import Browser with a translation, Robot Framework knows only the
translated keyword names. But `Record Keyword` and `Record Keywords` wrote the
English names, so the recorded keyword failed. Now each Keyword Call uses the
translated name in the file, in the returned text and in the toolbar. A keyword
without a translation keeps its English name. Many thanks to René for the fix.

### Recorder ignores the Robot Framework language of the target file ([#5510](https://github.com/MarketSquare/robotframework-browser/issues/5510))
`Record Keyword` and `Record Keywords` always wrote the keyword section header,
`[Tags]` and `[Arguments]` in English. Because of this, a file with `Language: de`
had two languages in it. Now the Recorder uses the language of the file. First it
uses the language that the file declares. If the file declares none, it uses the
language of the run (`--language` or `robot.toml`). Otherwise it uses English. The
Recorder also uses a keyword section that is already in the file, in any language.
Many thanks to René for the fix.

### Raise Python 3.11 minimum required version to 3.11.5 because of CVE-2026-126191 ([#5546](https://github.com/MarketSquare/robotframework-browser/issues/5546))
The soupsieve fix for CVE-2026-126191 needs Python 3.11.5 or later. Browser uses
soupsieve only in its development environment, not at run time. Because of this,
only the development environment now needs Python 3.11.5 or later. Browser still
supports Python 3.11 and later.

### Assertion retry deadline uses wall-clock time and ends early when the system clock jumps ([#5577](https://github.com/MarketSquare/robotframework-browser/issues/5577))
Browser used the system clock to measure how long an assertion can retry. When the
system clock moved forward, the retries stopped too early and the keyword failed.
Now Browser uses a monotonic clock, which does not change when the system clock
changes. `Wait For Download` had the same problem, and this release fixes it too.

### Expose Playwright's registerSelectorEngine() ([#4182](https://github.com/MarketSquare/robotframework-browser/issues/4182))
To register a Playwright selector engine, use a JavaScript extension keyword. The
keyword gets the injected argument `playwright` and calls
`await playwright.selectors.register(...)`. Run this keyword before you open a
page. After that, Browser selectors can use the new engine. For an example, see
[Custom Selector Strategies](https://robotframework-browser.org/docs/extending/javascript-extensions#custom-selector-strategies).
Many thanks to barambulka for the request.

## Acknowledgements

### IndexError masks failures from JavaScript extension keywords with *args ([#5306](https://github.com/MarketSquare/robotframework-browser/issues/5306))
A JavaScript extension keyword with an argument named `args` gets `*args` in
Python. When such a keyword failed with more than one argument, the library raised
`IndexError` while it handled the failure. This error hid the original error. Now
Browser shows the original error. Many thanks to wesleyke2 for the report and the
fix.

### Dependency updates ([#5481](https://github.com/MarketSquare/robotframework-browser/issues/5481))
Some dependencies were old. `rfbrowser init` also logged a "blocked post install
script" warning, because `allowScripts` named old versions of protobufjs and
unrs-resolver. Now Browser uses new versions of Playwright and other dependencies,
and the warning does not show. Many thanks to Houbein for the report.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#5306](https://github.com/MarketSquare/robotframework-browser/issues/5306) | bug | high | IndexError masks failures from JavaScript extension keywords with *args |
| [#5481](https://github.com/MarketSquare/robotframework-browser/issues/5481) | bug | high | Dependency updates |
| [#5492](https://github.com/MarketSquare/robotframework-browser/issues/5492) | bug | high | rfbrowser init and install offer chromium-tip-of-tree-headless-shell, which Playwright 1.63 removed |
| [#5493](https://github.com/MarketSquare/robotframework-browser/issues/5493) | bug | high | rfbrowser init offers bidi-chromium, which Playwright cannot install |
| [#5509](https://github.com/MarketSquare/robotframework-browser/issues/5509) | bug | high | Recorder writes English keyword names when Browser is imported with a translation |
| [#5510](https://github.com/MarketSquare/robotframework-browser/issues/5510) | bug | high | Recorder ignores the Robot Framework language of the target file |
| [#5546](https://github.com/MarketSquare/robotframework-browser/issues/5546) | bug | high | Raise Python 3.11 minimum required version to 3.11.5 because of CVE-2026-126191 |
| [#5577](https://github.com/MarketSquare/robotframework-browser/issues/5577) | bug | high | Assertion retry deadline uses wall-clock time and ends early when the system clock jumps |
| [#4182](https://github.com/MarketSquare/robotframework-browser/issues/4182) | feature | high | Expose Playwright's registerSelectorEngine() |
| [#5109](https://github.com/MarketSquare/robotframework-browser/issues/5109) | feature | high | `HTTP` follows the browser fetch API |
| [#5617](https://github.com/MarketSquare/robotframework-browser/issues/5617) | feature | high | Abort Requests, Remove Route Rule, Remove All Route Rules |
| [#5622](https://github.com/MarketSquare/robotframework-browser/issues/5622) | feature | high | Mock Responses |
| [#5625](https://github.com/MarketSquare/robotframework-browser/issues/5625) | feature | high | Modify Responses |
| [#5425](https://github.com/MarketSquare/robotframework-browser/issues/5425) | bug | medium | Record Selector does not work on a manually switched page |
| [#5484](https://github.com/MarketSquare/robotframework-browser/issues/5484) | bug | medium | Wait For Response returns no body key for an empty response body with Playwright 1.65 |
| [#5486](https://github.com/MarketSquare/robotframework-browser/issues/5486) | bug | medium | With two traced contexts, each trace shows the other context's keywords as empty groups |
| [#5487](https://github.com/MarketSquare/robotframework-browser/issues/5487) | bug | medium | Full tracing group mode adds trace groups for IF/ELSE branches that did not run |
| [#5488](https://github.com/MarketSquare/robotframework-browser/issues/5488) | bug | medium | Trace group names show keyword arguments as written, not their values |
| [#5491](https://github.com/MarketSquare/robotframework-browser/issues/5491) | bug | medium | On-failure keyword runs again for each keyword teardown inside a timed-out test's teardown |
| [#5529](https://github.com/MarketSquare/robotframework-browser/issues/5529) | bug | medium | Bump NodeJS bundled in BrowserBatteries to 26.13.1 |
| [#5544](https://github.com/MarketSquare/robotframework-browser/issues/5544) | bug | medium | Add Style Tag, Add Script Tag and Add Init Script handle an empty source differently |
| [#5551](https://github.com/MarketSquare/robotframework-browser/issues/5551) | bug | medium | The library can connect to another process's Node.js when its port was taken |
| [#5611](https://github.com/MarketSquare/robotframework-browser/issues/5611) | bug | medium | Wait For Response docs list ? and [] as glob wildcards, but Playwright matches them literally |
| [#524](https://github.com/MarketSquare/robotframework-browser/issues/524) | enhancement | medium | Intercepting and modifying responses (playwright page.route) |
| [#5541](https://github.com/MarketSquare/robotframework-browser/issues/5541) | feature | medium | `Add Style Tag` supports `url`, `path` and frames |
| [#5598](https://github.com/MarketSquare/robotframework-browser/issues/5598) | feature | medium | Add `Set HTTP Credentials` keyword to change HTTP credentials mid-test |
| [#5623](https://github.com/MarketSquare/robotframework-browser/issues/5623) | feature | medium | New keyword `Send API Request` for Playwright's `APIRequestContext.fetch` |
| [#5322](https://github.com/MarketSquare/robotframework-browser/issues/5322) | bug | low | Close Context leaves the context open when stopping the trace or saving coverage fails |
| [#5323](https://github.com/MarketSquare/robotframework-browser/issues/5323) | bug | low | Close Browser and Close All Browsers hide why closing a browser failed |
| [#5429](https://github.com/MarketSquare/robotframework-browser/issues/5429) | bug | --- | Fix the latest-page lookup on an empty page stack |
| [#5459](https://github.com/MarketSquare/robotframework-browser/issues/5459) | bug | --- | Failure screenshots are lost when Browser is imported with a translation |
| [#5099](https://github.com/MarketSquare/robotframework-browser/issues/5099) | feature | --- | Add `Add Init Script` keyword to run JavaScript before page scripts load |
| [#5100](https://github.com/MarketSquare/robotframework-browser/issues/5100) | feature | --- | Add `Add Script Tag` keyword to inject a script into the page |
| [#5102](https://github.com/MarketSquare/robotframework-browser/issues/5102) | feature | --- | Add `Blur` keyword to remove focus from an element |
| [#5106](https://github.com/MarketSquare/robotframework-browser/issues/5106) | feature | --- | Add cookie filters and partitioned-cookie support: `Delete All Cookies` filters, `Get Cookies    urls=`, `Add Cookie    partitionKey=` |
| [#5111](https://github.com/MarketSquare/robotframework-browser/issues/5111) | feature | --- | Add `timeout=`/`wait_until=` to `Go Back` and `Go Forward`, and `referer=` to `Go To` |
| [#5113](https://github.com/MarketSquare/robotframework-browser/issues/5113) | feature | --- | Support `content`, `mode` and `urlFilter` keys in the `recordHar` option of `New Context` |
| [#5115](https://github.com/MarketSquare/robotframework-browser/issues/5115) | feature | --- | Add `Set Extra HTTP Headers` keyword to change request headers mid-test |
| [#5119](https://github.com/MarketSquare/robotframework-browser/issues/5119) | feature | --- | Enrich `Wait For Request` / `Wait For Response`: metadata, binary body support, and sibling consistency |
| [#5120](https://github.com/MarketSquare/robotframework-browser/issues/5120) | feature | --- | Network request mocking with route rules |
| [#5122](https://github.com/MarketSquare/robotframework-browser/issues/5122) | feature | --- | Add `Start Tracing` / `Stop Tracing` / `Start Trace Chunk` / `Stop Trace Chunk` keywords for ad-hoc tracing |
| [#5628](https://github.com/MarketSquare/robotframework-browser/issues/5628) | feature | --- | Remove Route Rule and Remove All Route Rules log how many times each rule ran |

Altogether 42 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av21.1.0).
