# Browser library 19.14.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 19.14.0 is a new release which brings support for Robot Framework
Secret type, updated Docker Python to 3.14 and removes
Browser/utils/robot_booleans.py. All issues targeted for Browser library
v19.14.0 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.14.0).
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
install it manually. Browser library 19.14.0 was released on Monday April 6, 2026.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.59.1


## Most important enhancements

### Add support for Robot Framework 7.4 Secret type ([#4269](https://github.com/MarketSquare/robotframework-browser/issues/4269))
Robot Framework 7.3 did bring support for type conversion in Robot Framework data
and Robot Framework 7.4 introduced new [Secret](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#secret-variables)
type. Browser library 19.14.0 brings support for Secret type in Proxy and
httpCredentials arguments. Also Type Secret and Fill Secret keywords secret
argument supports Robot Framework Secret types.

Using Secret type in Browser library requires that Robot Framework 7.4 is
user with Browser library. This does not increase the minimum required version
of Robot Framework for Browser library if you do not want to use Secret type.

### Update Docker Python to 3.14 ([#4791](https://github.com/MarketSquare/robotframework-browser/issues/4791))
Our [Docker](https://hub.docker.com/r/marketsquare/robotframework-browser/tags)
has been updated to use Python 3.14.

### Remove Browser/utils/robot_booleans.py ([#4800](https://github.com/MarketSquare/robotframework-browser/issues/4800))
Browser/utils/robot_booleans.py has been removed, if there is need to use
is_falsy or is_truthy, import them from robot.utils.robottypes.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#4269](https://github.com/MarketSquare/robotframework-browser/issues/4269) | feature | high | Add support for Robot Framework 7.4 Secret type |
| [#4791](https://github.com/MarketSquare/robotframework-browser/issues/4791) | feature | high | Update Docker Python to 3.14 |
| [#4800](https://github.com/MarketSquare/robotframework-browser/issues/4800) | feature | high | Remove Browser/utils/robot_booleans.py |

Altogether 3 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.14.0).
