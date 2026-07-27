# Robot Framework BrowserBatteries
Robot Framework
[BrowserBatteries](https://pypi.org/project/robotframework-browser-batteries/)
is Python package which contains the NodeJS runtime and all the required NodeJS
dependencies, distributed inside of the Python wheel. The only thing user needs to
do, is to install the Playwright browser binaries and then run tests.

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
need to install the NodeJS dependencies, like Playwright and GRPC. The wheel contains
a NodeJS 24 runtime together with those dependencies, and a wheel is published for
each of these platforms:

| Platform | Architecture | Minimum version                        |
| -------- | -------------| ---------------------------------------|
| Linux    | x64          | glibc 2.28 (Debian 10, RHEL 8, Ubuntu 20.04) |
| Linux    | arm64        | glibc 2.28 (Debian 10, RHEL 8, Ubuntu 20.04) |
| Windows  | x64          | Windows 10 / Windows Server 2016       |
| MacOs    | arm64        | macOS 13.5                             |
| MacOs    | x64          | macOS 13.5                             |

The minimum versions are the ones the official NodeJS 24 builds require, and the
wheels are tagged accordingly, so `pip` will not install BrowserBatteries on a
platform where the shipped NodeJS cannot start. On an older platform, install
plain `robotframework-browser` and provide NodeJS yourself.

The NodeJS runtime is the official build from [nodejs.org](https://nodejs.org/dist),
verified against its published checksums at build time and shipped unmodified next to
the library's own NodeJS sources. This is the same arrangement Playwright uses for its
Python, Java and .NET packages, which means Playwright runs on the NodeJS it is
developed and tested against.

## Browser Batteries purpose
BrowserBatteries does not provide extra keywords or functionally on
keywords or replace existing plugins or extensions. BrowserBatteries
sole purpose is to ease installation, specially in corporate networks.
But it can be used by anyone, example if you do not have access public
internet you can download the wheels, example with
`pip download robotframework-browser-batteries`, copy wheels to you
target computer, install wheels on your target computer and use
any Chromium based browser to run your tests.
