# Browser library 20.6.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 20.6.0 is a new release with which takes in use the Robot Framework 7.5
new argument syntax. Also if New Page, Go To, Reload, Go Back, Go Forward,
Wait For Navigation or Wait For Load Stat keyword fails, keywords logs load-state
diagnostics. There small fix for download timeout timer is never cleared and
fix for run on failure functionality if New Page keyword fails. All issues
targeted for Browser library v20.6.0 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av20.6.0).
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
install it manually. Browser library 20.6.0 was released on Saturday October 3, 2026.
Browser supports Python 3.10+, Node 22/24 LTS and Node 26, and Robot Framework 7.1.1+.
Library was tested with Playwright 1.63.0. BrowserBatteries package was
released with NodeJS 24.21.0.



## Most important enhancements

### Implement documented arguments for Robot Framework 7.5 ([#5267](https://github.com/MarketSquare/robotframework-browser/issues/5267))
René converted library keyword documentation to use Robot Framework 7.5 argument syntax
which makes reading documentation easier. It also helps maintainers in documentation
writing, because arguments documentation is not easier to make.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#5267](https://github.com/MarketSquare/robotframework-browser/issues/5267) | feature | high | Implement documented arguments for Robot Framework 7.5 |
| [#5261](https://github.com/MarketSquare/robotframework-browser/issues/5261) | bug | medium | Failing New Page closes the page before run_on_failure, so the failure screenshot is missing or shows a different page |
| [#5272](https://github.com/MarketSquare/robotframework-browser/issues/5272) | feature | medium | Log load-state diagnostics when New Page navigation fails |
| [#5274](https://github.com/MarketSquare/robotframework-browser/issues/5274) | bug | low | Download timeout timer is never cleared, Jest worker is force exited |

Altogether 4 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av20.6.0).
