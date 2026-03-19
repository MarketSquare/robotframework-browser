# Browser library 19.12.7


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 19.12.7 is a new hotfix release which downgrades grpcio to 1.78.0.
All issues targeted for Browser library v19.12.7 can be found
from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.12.7).
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
install it manually. Browser library 19.12.7 was released on Thursday March 19, 2026.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.58.2



## Most important enhancements

### Downgrade grpcio to 1.78.0 ([#4746](https://github.com/MarketSquare/robotframework-browser/issues/4746))
The grpcio to 1.78.0 was downgraded, because 1.78.1 was yanked from PyPi.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#4746](https://github.com/MarketSquare/robotframework-browser/issues/4746) | bug | critical | Downgrade grpcio to 1.78.0 |

Altogether 1 issue. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.12.7).
