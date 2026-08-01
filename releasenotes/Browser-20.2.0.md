# Browser library 20.2.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 20.2.0 is a new release changed how BrowserBatteries wheel is build
and with the build change BrowserBattier wheel tags have been fixed, more
environment variables are support with BrowserBatteries and `spawn_node_process`
helper has been fixed. All issues targeted for Browser library v20.2.0 can
be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av20.2.0).
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
install it manually. Browser library 20.2.0 was released on Saturday August 1, 2026.
Browser supports Python 3.10+, Node 22/24 LTS and Node 26, and Robot Framework 6.1+.
Library was tested with Playwright 1.62.0

## Most important enhancements
### Update Playwright 1.62.0 ([#5073](https://github.com/MarketSquare/robotframework-browser/issues/5073))
The Playwright 1.62.0 changed internal and not public interface which BrowserBatteries
used to install Playwright browser binaries. This caused our installation process to
fail. After some research it was decided that we will drop @yao-pkg/pkg NodeJS, which
was used to build BrowserBatteries GRPC server executable. Instead library moves to
same direction as Playwright and bundles node executable inside of the wheel with
the Playwright core and other needed NodeJS dependencies.

User should not notice anything different from the usage point of view,
BrowserBatteries should work in same was as before and it should not affect using the
BrowserBatteries wheel. But with this change our build process has more responsibility
to get stuff right, which in past release was on shoulders of @yao-pkg/pkg. The most
noticeable for the Linux and Mac users is that wheel size has increased from +30Mb to
+50Mb. For Windows users ths size has slightly dropped.

### Wheel tags for Mac and Linus are wrong for ([#5078](https://github.com/MarketSquare/robotframework-browser/issues/5078))
The BrowserBatteries Linux and Mac wheel where not correctly tagged and use could
install the wheel on a platform which was not actually supported. The failure would
happen when users did try run the library with BrowserBatteries installed. Now with
the corrected tags, user will failure during the installation time, which is more
helpful for them.

### spawn_node_process helper to work without BrowserBatteries being installed ([#5082](https://github.com/MarketSquare/robotframework-browser/issues/5082))
The `spawn_node_process` helper, which can be used to start the Browser library GRPC
server did only work on very limited ways. This has not been enhanced to support
more usa cases and should work better if users want to launch GRPC server once and
use example pabot to execute their test in multiple processes. There is one small
backwards incompatible change, in the past, helper did set the
`PLAYWRIGHT_BROWSERS_PATH` environment variable to value `0`. This forcing is not
anymore done and if user did relay on it, they must now set the value in their
own environments.

### Support ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS and ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE with BrowserBatteries wheel ([#5081](https://github.com/MarketSquare/robotframework-browser/issues/5081))
In previous releases, the `ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS` and
`ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE with` where silently ignored, because the GRPC
server compiled with @yao-pkg/pkg did not allow us to use them. Now with the bundled
node executable, using those environment variables is possible.

### rfbrowser clean-node fails on Windows ([#5076](https://github.com/MarketSquare/robotframework-browser/issues/5076))
`rfbrowser clean-node` did crash on Windows, after clean, when it listed the remaining
folder structure. This is not fixed by suppressing the encoding error and continuing
the cleanup procedure.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#5076](https://github.com/MarketSquare/robotframework-browser/issues/5076) | bug | critical | rfbrowser clean-node fails on Windowns |
| [#5078](https://github.com/MarketSquare/robotframework-browser/issues/5078) | bug | critical | Wheel tags for Mac and Linus are wrong for |
| [#5073](https://github.com/MarketSquare/robotframework-browser/issues/5073) | bug | high | Update Playwright 1.62.0 |
| [#5082](https://github.com/MarketSquare/robotframework-browser/issues/5082) | bug | high | spawn_node_process helper to work without BrowserBatteries being installed |
| [#5081](https://github.com/MarketSquare/robotframework-browser/issues/5081) | feature | high | Support ROBOT_FRAMEWORK_BROWSER_NODE_DEBUG_OPTIONS and ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE with BrowserBatteries wheel |

Altogether 5 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av20.2.0).
