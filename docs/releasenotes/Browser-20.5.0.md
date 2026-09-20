# Browser library 20.5.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 20.5.0 is a new release with several smaller enhancements and bug fixes.
We increase the minimum required Robot Framework version officially to 7.1.1
and bump BrowserBatteries NodeJS LTS version to 24.21.0. Also there are fixes on
Browser library crashing or and handling timeouts incorrectly.  All issues targeted
for Browser library v20.5.0 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av20.5.0).
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
install it manually. Browser library 20.5.0 was released on Sunday September 20, 2026.
Browser supports Python 3.10+, Node 22/24 LTS and Node 26, and Robot Framework 7.1.1+.
Library was tested with Playwright 1.63.0. BrowserBatteries package was
released with NodeJS 24.21.0.

## Most important enhancements

### Raise minimum needed Robot Framework version to 7.1.1 ([#5133](https://github.com/MarketSquare/robotframework-browser/issues/5133))
We raised minimum needed Robot Framework version to 7.1.1, this helps keeping Browser
library code architecture more clean and clean. This also allowed us to make simpler
usage when library is used directly from Python side. This actually happened already
in the previous release, but we did forget to put the issue in the release notes.

### Playwright highlights are shared between parallel workers: one worker's highlight teardown erases every other worker's highlights ([#5211](https://github.com/MarketSquare/robotframework-browser/issues/5211))
There has been long lasting bug in the Browser library, when used from with
[Pabot](https://pabot.org/) and if there is only one GRPC server running. In this scenario
if highlight is removed from one test, it actually removes from all Browser/Context and
Pages from all pabot parallel runs. This functionality has been changed that cache is not
anymore global, but instead it is tied to the pabot worker.

### Update BrowserBatteries NodeJS version to latest LTS ([#5253](https://github.com/MarketSquare/robotframework-browser/issues/5253))
BrowserBatteries package is now released with NodeJS 24.21.0. Which is the latest LTS
version when release was made.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#5133](https://github.com/MarketSquare/robotframework-browser/issues/5133) | feature | critical | Raise minimum needed Robot Framework version to 7.1.1 |
| [#5211](https://github.com/MarketSquare/robotframework-browser/issues/5211) | bug | high | Playwright highlights are shared between parallel workers: one worker's highlight teardown erases every other worker's highlights |
| [#5253](https://github.com/MarketSquare/robotframework-browser/issues/5253) | feature | high | Update BrowserBatteries NodeJS version to latest LTS |
| [#5185](https://github.com/MarketSquare/robotframework-browser/issues/5185) | bug | medium | Timeout argument not used in ``Promise to wait for download`` keyword in specific case |
| [#5187](https://github.com/MarketSquare/robotframework-browser/issues/5187) | bug | medium | Switch Browser can terminate Node process because page.bringToFront() is not awaited |
| [#5214](https://github.com/MarketSquare/robotframework-browser/issues/5214) | bug | medium | Closing gRPC deadline is computed in the wrong unit, so it is 5.5 hours by default and 2 seconds after Set Browser Timeout 1ms |
| [#5220](https://github.com/MarketSquare/robotframework-browser/issues/5220) | bug | medium | Translation __init__ entry duplicates __intro__: import-argument documentation is never translated |
| [#5219](https://github.com/MarketSquare/robotframework-browser/issues/5219) | bug | --- | Translation checksums are Python-version dependent: raw __doc__ vs inspect.getdoc() breaks at Python 3.13 |

Altogether 8 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av20.5.0).
