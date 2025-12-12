# Browser library 19.12.1


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 19.12.1 is a new hotfix release with bug fixes to rfbrowser clean-node
command when there is not NodeJS installed. All issues targeted for Browser
library v19.12.1 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.12.1).
For first time installation with pip_ and BrowserBatteries_ just run
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
install it manually. Browser library 19.12.1 was released on Saturday December 13, 2025.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.57.0



## Most important enhancements

### rfbrowser clean-node does not work when using browser batteries on Ubuntu server ([#4592](https://github.com/MarketSquare/robotframework-browser/issues/4592))
When running `rfbrowser clean-node` command and there was not NodeJS installed,
it resulted in an error. This is now fixed and NodeJS check is not done, if
BrowserBatteries is installed.

## Acknowledgements

### Improve New Context example how to use credentials ([#4573](https://github.com/MarketSquare/robotframework-browser/issues/4573))
Many thanks for BastiaanTenBroeke24 for providing fix for the HttpCredentials
argument type documentation. Now the credentials example is correct.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#4592](https://github.com/MarketSquare/robotframework-browser/issues/4592) | bug | critical | rfbrowser clean-node does not work when using browser batteries on Ubuntu server |
| [#4573](https://github.com/MarketSquare/robotframework-browser/issues/4573) | bug | medium | Improve New Context example how to use credentials |

Altogether 2 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.12.1).
