# Robot Framework BrowserBatteries
Robot Framework
[BrowserBatteries](https://pypi.org/project/robotframework-browser-batteries/)
is Python package which contains all the required NodeJS and NodeJS dependencies
prebuilt as executable and distributed inside of the Python wheel. The only thing
user needs to do, is to install the Playwright browser binaries and then run tests.

## Installation
1. Update pip `pip install -U pip` to ensure latest version is used
2. Install robotframework-browser and robotframework-browser-batteries from the commandline:
`pip install robotframework-browser[bb]`
3. Install the Playwright browser binaries, run: `rfbrowser install`
  - if `rfbrowser` is not found, try `python -m Browser.entry install`

> NOTE: You can skip `rfbrowser install` if you want to use preinstalled browser,
like Chrome or Edge. Any Chromium based browser should be OK to go.

## Update instructions

To upgrade your already installed robotframework-browser and robotframework-browser-batteries
in follow steps below. Please note that robotframework-browser and
robotframework-browser-batteries packages are tied together and having different versions
of these packages is not supported.

1. Update from commandline: `pip install -U robotframework-browser robotframework-browser-batteries`
2. Clean old node side dependencies and browser binaries: `rfbrowser clean-node`
3. Install the node dependencies for the newly installed version: `rfbrowser install`

# Purpose
When using BrowserBatteries package, user can skip NodeJS installation and does not
need to install the NodeJS dependencies, like Playwright and GRPC. All those are
packed inside of a prebuilt binary which project build for following OS and
architectures:

| Node | Platform | Architecture |
| ---- | -------- | -------------|
| 22   | Linux    | x64          |
| 22   | Linux    | arm64        |
| 22   | Windows  | x64          |
| 22   | MacOs    | arm64        |
| 22   | MacOs    | x64          |

Build process relies on [yao-pkg](https://github.com/yao-pkg/pkg) and
[pkg-fetch](https://github.com/yao-pkg/pkg-fetch) for NodeJS binary
building. Binary is build with NodeJS 22.

## Browser Batteries purpose
BrowserBatteries does not provide extra keywords or functionally on
keywords or replace existing plugins or extensions. BrowserBatteries
sole purpose is to ease installation, specially in corporate networks.
But it can be used by anyone, example if you do not have access public
internet you can download the wheels, example with
`pip download robotframework-browser-batteries`, copy wheels to you
target computer, install wheels on your target computer and use
any Chromium based browser to run your tests.
