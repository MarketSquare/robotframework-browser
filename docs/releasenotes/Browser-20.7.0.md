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
Library was tested with Playwright 1.63.0. BrowserBatteries package was
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
  password fields. Review it before committing.

### Promise To converts non-string positional arguments
`Promise To` now converts non-string positional arguments like string ones, so the
promised keyword receives the same values as when it is called directly. This came out of the
recorder work.
