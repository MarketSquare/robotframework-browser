# Robot Framework BrowserBatteries
Robot Framework
[BrowserBatteries](https://pypi.org/project/robotframework-browser-batteries/)
Python package contains all the required NodeJS dependencies prebuilt inside of the
 Python wheel. The only thing user needs to do, is to install the Playwright browser
 binaries and then run tests.

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
building. Binary is build with NodeJS 24.

## Browser Batteries purpose
BrowserBatteries does not provide extra keywords or functionally on
keywords or replace existing plugins or extensions. BrowserBatteries
sole purpose is to ease installation, specially in corporate networks.
But it can be used anyone, example if you do not have access public
internet you can download the wheels, example with
`pip download robotframework-browser-batteries`, copy wheels to you
target computer, install wheels on your target computer and use
Chromium based browser to run your tests.
