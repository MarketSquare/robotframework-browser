# Browser library 20.7.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 20.7.0 is a new release with the new Record Keyword and Record Keywords keywords. All issues
targeted for Browser library v20.7.0 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av20.7.0).
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
install it manually. Browser library 20.7.0 has not been released yet.
Browser supports Python 3.10+, Node 22/24 LTS and Node 26, and Robot Framework 7.1.1+.
Library was tested with Playwright 1.64.1. BrowserBatteries package was
released with NodeJS 24.21.0.



## Most important enhancements

### Record Keyword and Record Keywords
New keywords record interactions in the live browser as Robot Framework User Keywords made
of Browser keywords, from any point in a test run: name keywords while recording, undo
mistakes, turn values into keyword arguments, and write into a `.robot`/`.resource` file or
only to the log. See the keyword documentation.

- Clicks, typing, key presses, checkboxes, selects, navigation and Playwright's assertions
  are recorded. *Assert snapshot* becomes `Get Aria Snapshot    <selector>    yaml    ==
  <snapshot>` and *Assert visibility* becomes `Get Element States    <selector>    *=    visible`.
- The recorder uses Playwright's programmatic recorder, which is not a public Playwright API.
  It may need adapting after a Playwright upgrade.
- A recorded keyword contains values from the page under test, including anything typed into
  password fields. Review it before committing. During a session these values are also
  readable by scripts on the recorded pages.
- Playwright's own recorder toolbar is shown at the top centre of the page while recording
  and cannot be hidden.
- A session ends after 5 minutes without activity by default (`idle_timeout`), so a
  forgotten recording cannot block a run for good. Recording needs a visible browser; in a
  headless one both keywords fail.

### Record Selector rebuilt on the recorder toolbar
`Record Selector` now uses Playwright's own element picker and the recorder toolbar. Hover an
element, click to pick it - the click does not reach the page - and use, edit or re-pick the
selector in the toolbar, which counts the elements it finds while you type.

- **Backwards incompatible:** the default selector is now Playwright's, in Browser syntax,
  for example `role=button[name="Save"s]`, instead of a CSS selector. `generator=css` keeps
  CSS selectors (now from the current release of the same finder library), and the toolbar
  switches between both for the picked element.
- Picking needs a click; the 3 second hover countdown and the variant list are gone. The
  selector's matches stay highlighted with Playwright's highlight until it is used, re-picked
  or the keyword ends; an edited selector is counted and highlighted once typing pauses.
- The recorder toolbar of Record Keyword(s) has the same picker behind a *Pick* button, and
  Playwright's own Pick locator opens it too: the picked selector is added to the keyword as
  a comment row `# Picked Selector    <selector>`.
- New `idle_timeout` argument, 5 minutes by default; cancelling with *✕* or Escape fails the
  keyword. Record Selector fails while a Record Keyword(s) session runs in the same context.
- Works without `bypassCSP=True` on pages with a Content Security Policy.

### New Persistent Context records headless correctly
A context opened with `New Persistent Context    headless=False` was recorded internally as
headless. This came out of the recorder work.

### Promise To converts non-string positional arguments
`Promise To` now converts non-string positional arguments like string ones, so the
promised keyword receives the same values as when it is called directly. This came out of the
recorder work.
