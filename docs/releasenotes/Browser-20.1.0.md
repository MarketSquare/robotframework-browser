# Browser library 20.1.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 20.1.0 is a new release with enhancements to credential handling. Browser
library supports npm 12.x but some of dependencies used by Browser library
require users to manually approve npm packages post install script(s). More
details how that be done is documented example here: https://installsafe.dev/
All issues targeted for Browser library v20.1.0 can be found
from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av20.1.0).
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
install it manually. Browser library 20.1.0 was released on Wednesday July 22, 2026.
Browser supports Python 3.10+, Node 22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.61.1



## Most important enhancements

### Get Text Keyword returns value attribute instead of the text of an option element ([#4953](https://github.com/MarketSquare/robotframework-browser/issues/4953))
There was a regression in release 20.0 which caused Get Text keyword to return
attribute instead of the text of the select element. This is not fixed and
keyword returns a select element text.

### Playwright 1.61.1 ([#5020](https://github.com/MarketSquare/robotframework-browser/issues/5020))
Playwright 1.61.1 is now supported

### Support Playwright credentials ([#4979](https://github.com/MarketSquare/robotframework-browser/issues/4979))
Playwright https://playwright.dev/docs/api/class-credentials API is now
exposed as keywords to Browser library.


## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#4953](https://github.com/MarketSquare/robotframework-browser/issues/4953) | bug | critical | Get Text Keyword returns value attribute instead of the text of an option element |
| [#5020](https://github.com/MarketSquare/robotframework-browser/issues/5020) | feature | critical | Playwright 1.61.1 |
| [#4979](https://github.com/MarketSquare/robotframework-browser/issues/4979) | feature | high | Support Playwright credentials |

Altogether 3 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av20.1.0).
