# Robot Framework Browser Batteries
Robot Framework Browser Batteries Python package contains all the required NodeJS dependencies
prebuilt inside of the the Python wheel. The only thing user needs to do, is to install
the Playwright browser binaries and then run tests.

When using Browser Batteries package, user can skip NodeJS installation and does not
need to install the NodeJS dependencies, like Playwright and GRPC. All those are
packed inside of a prebuilt binary which project build for following OS and
architectures:

| Node | Platform | Architecture |
----------------------------------
| 22   | Linux    | x64          |
| 22   | Linux    | arm64        |
| 22   | Windows  | x64          |
| 22   | MacOs    | arm64        |
| 22   | MacOs    | x64          |

Build process relies on [yao-pkg](https://github.com/yao-pkg/pkg) and
[pkg-fetch](https://github.com/yao-pkg/pkg-fetch) for NodeJS binary
building.
