# Browser library 19.15.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 19.15.0 is a new release with enhancements to the playwright-log.txt. The
file now contains information from the executed suite and test and bug fixes for
starting the GRPC server. Also there are updates to teh NodeJS dependencies to
fix a security violation. This release also drops support for NodeJS 20, because
it is not anymore supported by NodeJS community. All issues targeted for Browser
library v19.15.0 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.15.0).
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
install it manually. Browser library 19.15.0 was released on Saturday May 9, 2026.
Browser supports Python 3.10+, Node 22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.59.1



## Most important enhancements

Drop NodeJS 20.x support ([#4876](https://github.com/MarketSquare/robotframework-browser/issues/4876))
------------------------------------------------------------------------------------------------------
This release drops support for NodeJS 20. NodeJS community is not anymore maintaining
NodeJS 20 version and it does not anymore receive updates. Also dependencies that
Browser library is using have started to complain about dropping support for the
NodeJS 20. Therefore we are dropping support for the NodeJS 20. We will not prevent
NodeJS 20 usage actively, but because we do not anymore test with NodeJS 20 in the CI,
we have lost visibility to detect such changes. User are strongly encouraged to update
their environment to a LTS version which is supported by the NodeJS community:
https://nodejs.org/en/about/previous-releases

Please remember that Playwright only support NodeJS LTS versions. At this time
it means that does not yet support NodeJS 26.

Sometimes starting the NodeJS side process fails on error. ([#4850](https://github.com/MarketSquare/robotframework-browser/issues/4850))
----------------------------------------------------------------------------------------------------------------------------------------
When doing testing, we have noticed that sometimes GRPC process does not always start,
we have improved the code the make few retries on startup.

## Acknowledgements

Set Presenter Mode keyword documentation arguments table is broken ([#4811](https://github.com/MarketSquare/robotframework-browser/issues/4811))
------------------------------------------------------------------------------------------------------------------------------------------------
Many thanks for Marko Rautiainen for raising issue about the Set Presenter Mode keyword
documentation and providing a fix for the documentation.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#4876](https://github.com/MarketSquare/robotframework-browser/issues/4876) | feature | critical | Drop NodoJS 20.x support |
| [#4850](https://github.com/MarketSquare/robotframework-browser/issues/4850) | bug | high | Sometimes starting the NodeJS side process fails on error. |
| [#4811](https://github.com/MarketSquare/robotframework-browser/issues/4811) | bug | medium | Set Presenter Mode keyword documentation arguments table is broken |
| [#3427](https://github.com/MarketSquare/robotframework-browser/issues/3427) | enhancement | medium | Support starting and stopping trace by a keyword |
| [#4855](https://github.com/MarketSquare/robotframework-browser/issues/4855) | feature | medium | playwright_log.txt improvements. |

Altogether 5 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.15.0).
