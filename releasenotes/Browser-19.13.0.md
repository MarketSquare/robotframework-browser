# Browser library 19.13.0


[Browser](https://github.com/MarketSquare/robotframework-browser) is a web testing
library for [Robot Framework](http://robotframework.org) that utilizes the
[Playwright](https://github.com/microsoft/playwright) tool internally. Browser
library 19.13.0 is a new release with new keyword to control presenter mode and changes
to internal dependencies. This release enables creation of unit test in NodeJSside and
changes NodeJS grpc protobuf creation. Both of these changes should not affect user,
but there was quite a lot of changes, so lets be careful out there.
All issues targeted for Browser library v19.13.0 can be found from the
[issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=state%3Aclosed%20milestone%3Av19.13.0).
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
install it manually. Browser library 19.13.0 was released on Wednesday April 1, 2026.
Browser supports Python 3.10+, Node 20/22/24 LTS and Robot Framework 6.1+.
Library was tested with Playwright 1.59.0



## Most important enhancements

**EXPLAIN** or remove these.

### Create unit test and coverage for NodeJS side ([#4767](https://github.com/MarketSquare/robotframework-browser/issues/4767))
Now, finaly Iwould say, it is possible to create unit test to the NodeJS side
of the library. Also we support collecting coverage from the NodeJS side. Coverage
collection needed small, controlled by an environment variable:
ROBOT_FRAMEWORK_BROWSER_NODE_COVERAGE, code change. If users do not have that
environment variable set, this change should not affect users.

### grpc_tools_node_protoc_ts is having security issues ([#4778](https://github.com/MarketSquare/robotframework-browser/issues/4778))
The grpc_tools_node_protoc_ts was not updated for few years and it started to
accumulate security issues. Therefore we changed this dependency to ts-proto. Also
we switched google-protobuf to @bufbuild/protobuf in runtime dependencies.

This change required quite a big refactoring in the NodeJS side, because
grpc_tools_node_protoc_ts did sit pretty central place in out architecture. Although
this change should be in theory invisible for the users, there was quite a lot of
changes. I know that our test coverage is not bullet proof, so this change can cause
unseen problems. So be careful out there and report any problems.

## Acknowledgements

## Feature request: Ability to enable/disable presenter mode during test execution ([#4772](https://github.com/MarketSquare/robotframework-browser/issues/4772))
Many thanks to Marko Rautiainen to suggesting and implement a keyword which
allows to control presented mode during test execution. In previous version
it was only possible to control it in the library import.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#4767](https://github.com/MarketSquare/robotframework-browser/issues/4767) | feature | critical | Create unit test and coverage for NodeJS side |
| [#4778](https://github.com/MarketSquare/robotframework-browser/issues/4778) | feature | critical | grpc_tools_node_protoc_ts is having security issues |
| [#4772](https://github.com/MarketSquare/robotframework-browser/issues/4772) | feature | medium | Feature request: Ability to enable/disable presenter mode during test execution |

Altogether 3 issues. View on the [issue tracker](https://github.com/MarketSquare/robotframework-browser/issues?q=milestone%3Av19.13.0).
