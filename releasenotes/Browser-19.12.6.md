# Browser library 19.12.6


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 19.12.6 is a new hotfix release with fixes to supporting large responses
from NodeJS side to Python side, timeout argument was added to gRPC messaging when
browser and context was closed, @yao-pkg/pkg reference was fixed and run on failure
was not always called when keyword failed. There are also formatting changes
to NodeJS side, caused by using the Eslint latest major release and fixing the
linting errors (which should not affect users of the library.) All issues targeted
for Browser library v19.12.6 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.12.6).
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
install it manually. Browser library 19.12.6 was released on Wednesday March 18, 2026.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.58.2



## Acknowledgements

### grpc message size limits causes keyword failures with large DOMs ([#4391](https://github.com/MarketSquare/robotframework-browser/issues/4391))
Keywords could fail, if returned message exceeded the default gRPC maximum message
size. This is now avoided by making messaging using a streaming API in gRPC
messaging in several places in the library. Many thanks for Frank Stenzhorn
for reporting the problem and tonyr-qf for providing a PR to fix the problem.

### Get Attribute should take page screenshot when test failure when either selector or attribute is fail ([#4711](https://github.com/MarketSquare/robotframework-browser/issues/4711))
if keywords failed in AttributeError, it did not execute the run on failure
functionality. This is now fixed and run on failure is executed also with
AttributeError error raised. Many thanks for SiongWaiVidispine to reporting
the problem and providing a PR to fix it.

## avoid github references in package.json ([#4735](https://github.com/MarketSquare/robotframework-browser/issues/4735))
@yao-pkg/pkg reference pointed to GitHub release and not a release in the NPM
side. This is now fixed.

## Eternal freeze when calling Close Browser keyword on robotframework-browser ([#4124](https://github.com/MarketSquare/robotframework-browser/issues/4124))
If Browser library was used with pabot, in some cases it could lead in
freeze when browser or context was closed. This is now fixed by adding
timeout argument in gRPC messages.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#4391](https://github.com/MarketSquare/robotframework-browser/issues/4391) | bug | high | grpc message size limits causes keyword failures with large DOMs |
| [#4711](https://github.com/MarketSquare/robotframework-browser/issues/4711) | bug | high | Get Attribute should take page screenshot when test failure when either selector or attribute is fail |
| [#4735](https://github.com/MarketSquare/robotframework-browser/issues/4735) | bug | high | avoid github references in package.json |
| [#4124](https://github.com/MarketSquare/robotframework-browser/issues/4124) | bug | medium | Eternal freeze when calling Close Browser keyword on robotframework-browser |

Altogether 4 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.12.6).
