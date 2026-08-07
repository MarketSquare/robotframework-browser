# Browser library 20.3.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 20.3.0 is a new release with update to BrowserBatteries NodeJS version.
All issues targeted for Browser library v20.3.0 can be found
from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av20.3.0).
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
install it manually. Browser library 20.3.0 was released on Friday August 7, 2026.
Browser supports Python 3.10+, Node 22/24 LTS and Node 26, and Robot Framework 6.1+.
Library was tested with Playwright 1.62.1. BrowserBatteries package was
released with NodeJS 24.19.0.



## Most important enhancements

### Bumb BrowserBatteries node to 24.19 ([#5091](https://github.com/MarketSquare/robotframework-browser/issues/5091))
BrowserBatteries NodeJS version was updated to the 24.29.0 with this release.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#5091](https://github.com/MarketSquare/robotframework-browser/issues/5091) | bug | high | Bumb BrowserBatteries node to 24.19 |

Altogether 1 issue. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av20.3.0).
