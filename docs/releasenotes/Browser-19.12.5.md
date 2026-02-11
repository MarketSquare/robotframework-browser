# Browser library 19.12.5


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 19.12.5 is a new hotfix release which uses latest Playwright release.
Also AssertionEngine is updated to 4.0. All issues targeted for Browser library
v19.12.5 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.12.5).
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
install it manually. Browser library 19.12.5 was released on Wednesday February 11, 2026.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.58.2



## Most important enhancements


### Playwright 1.58.2 support ([#4661](https://github.com/MarketSquare/robotframework-browser/issues/4661))
Make new release with Playwright 1.58.2

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#4661](https://github.com/MarketSquare/robotframework-browser/issues/4661) | bug | high | Playwright 1.58.2 support |

Altogether 1 issue. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.12.5).
