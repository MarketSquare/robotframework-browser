# Browser library 21.0.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 21.0.0 is a new release with several new enhancements and bug fixes.
The highlight of the release it the new record keywords in the live browser feature
which allows users to inspect and interact the system under test by an UI and create
new keywords based actions. Also the Plugin API has been enhanced and it supports
adding context, which are created outside of the Browser library internal, to the
Browser library. This is done to ease the extending on top of the Browser library.
The reason for this being backwards incompatible release is that NodeJS 26 moved
to LTS and ship NodeJS 26 LTS in BrowserBatteries wheel. The most important bug fix
is that we now splitting a large response with a better logic which improved
library performance greatly.  All issues targeted for Browser library v21.0.0 can
be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av21.0.0).
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
install it manually. Browser library 21.0.0 was released on Sunday November 1, 2026.
Browser supports Python 3.11+, Node 22/24 LTS and Node 26, and Robot Framework 7.1.1+.
Library was tested with Playwright 1.64.1. BrowserBatteries package was
released with NodeJS 26.13.0.



## Most important enhancements

### Record keywords in the live browser: `Record Keyword` and `Record Keywords` ([#5408](https://github.com/MarketSquare/robotframework-browser/issues/5408))
Now can record their interactions in the browser at any point during a test run, naming
keywords, turning values into arguments and undoing mistakes as they go, so that they
can get reusable User Keywords built from Browser keywords, without whole tests being
generated and without translating generated Playwright code.

### Let libraries built on Browser hand over their own BrowserContext ([#5317](https://github.com/MarketSquare/robotframework-browser/issues/5317))
Playwright can drive more than Chromium, Firefox and WebKit. It can drive Electron
applications with playwright._electron, and Chrome on Android devices with
playwright._android. Requests to support such platforms in Browser come up again
and again in different issues. Each platform needs its own lifecycle, its own test
setup and people who know it well. None of that fits into Browser or should land on
its maintainers. Now we have opened the Plugin API to build on top of Browser library
to support other platforms too. Stay tuned for new libraries in this front.

### Splitting a large response body blocks the Node event loop ([#5349](https://github.com/MarketSquare/robotframework-browser/issues/5349))
Splitting a large response body blocks the Node event loop was done by one character
at the time. With large response this causes blocking operation in the NodeJS side
and caused problems with Pabot. Now there is better logic for splitting large
response and it should improve the performance of the library

### Extending the selector syntax with frame and label selectors ([#5410](https://github.com/MarketSquare/robotframework-browser/issues/5410))
we now support `>>> id=btn` syntax in with the frame locator. See the issue
for more details.

### Rebuild `Record Selector` on Playwright's element picker and the recorder toolbar ([#5411](https://github.com/MarketSquare/robotframework-browser/issues/5411))
We have enhanced Record Selector feature. There has been several problems with it
and we have made several enhancement to the feature. See issue for more details.

## Backwards incompatible changes

### Ship NodeJS 26 LTS in BrowserBatteries ([#5400](https://github.com/MarketSquare/robotframework-browser/issues/5400))
NodeJS 26 moved to LTS and we moved BrowserBatteries to use NodeJS 26 in the
BrowserBatteries wheels. This is the main reason to mark this release as
Backwards incompatible.

## Acknowledgements
### When a keyword fails and presenter_mode is enabled the browser is not closed ([#3644](https://github.com/MarketSquare/robotframework-browser/issues/3644))
When a keyword fails and presenter_mode is enabled the browser is not closed when
the test finishes. he reason is that the keyword Record Selector is called when a
keyword fails and presenter_mode is enabled. This is now fixed. Many thanks for
Marduk Bolaños reporting the problem and ShryukGrandhi to provide a fix for
the bug.


### New Browser fails with FileNotFoundError for playwright-log.txt when all output files are disabled ([#5313](https://github.com/MarketSquare/robotframework-browser/issues/5313))
If ${OUTPUT_DIR} did not exist, then starting the Browser library would fail in error,
this can happen example when output is disabled with these: --output NONE --log NONE
--report NONE command line switches. This problem has been reported and fixed by
Daniel Biehl

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#3644](https://github.com/MarketSquare/robotframework-browser/issues/3644) | bug | critical | When a keyword fails and presenter_mode is enabled the browser is not closed |
| [#5313](https://github.com/MarketSquare/robotframework-browser/issues/5313) | bug | high | New Browser fails with FileNotFoundError for playwright-log.txt when all output files are disabled |
| [#5349](https://github.com/MarketSquare/robotframework-browser/issues/5349) | bug | high | Splitting a large response body blocks the Node event loop |
| [#5317](https://github.com/MarketSquare/robotframework-browser/issues/5317) | feature | high | Let libraries built on Browser hand over their own BrowserContext |
| [#5400](https://github.com/MarketSquare/robotframework-browser/issues/5400) | feature | high | Ship NodeJS 26 LTS in BrowserBatteries |
| [#5408](https://github.com/MarketSquare/robotframework-browser/issues/5408) | feature | high | Record keywords in the live browser: `Record Keyword` and `Record Keywords` |
| [#5410](https://github.com/MarketSquare/robotframework-browser/issues/5410) | feature | high | Extending the selector syntax with frame and label selectors |
| [#5411](https://github.com/MarketSquare/robotframework-browser/issues/5411) | feature | high | Rebuild `Record Selector` on Playwright's element picker and the recorder toolbar |
| [#5260](https://github.com/MarketSquare/robotframework-browser/issues/5260) | bug | medium | RF suite/test context in the node logger is module-global, so log lines are attributed to the wrong worker when a node process is shared |
| [#5302](https://github.com/MarketSquare/robotframework-browser/issues/5302) | bug | medium | Keyword documentation bugs found while translating 20.6.0 |
| [#5320](https://github.com/MarketSquare/robotframework-browser/issues/5320) | bug | medium | JavaScript extensions get the string "RESERVED" instead of null or undefined when there is no page, context or browser |
| [#5321](https://github.com/MarketSquare/robotframework-browser/issues/5321) | feature | medium | defaultTimeout is a reserved argument name for JavaScript extension keywords |
| [#5346](https://github.com/MarketSquare/robotframework-browser/issues/5346) | feature | medium | Support fps and showActions in recordVideo of New Context |
| [#5378](https://github.com/MarketSquare/robotframework-browser/issues/5378) | feature | medium | Drop Python 3.10 and support Python 3.11 to 3.15 |
| [#5324](https://github.com/MarketSquare/robotframework-browser/issues/5324) | --- | medium | New Persistent Context indexes only the first page, and a failed close leaves the persistent context open |
| [#5357](https://github.com/MarketSquare/robotframework-browser/issues/5357) | bug | low | Tracing with tracing_group_mode=Browser fails with IndexError when a context is created from plain Python |
| [#5368](https://github.com/MarketSquare/robotframework-browser/issues/5368) | bug | low | Pages that exist when Connect To Browser connects stay in the page stack after they close |
| [#5325](https://github.com/MarketSquare/robotframework-browser/issues/5325) | bug | --- | Processes forked after a gRPC channel opens can crash on macOS |

Altogether 18 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av21.0.0).
