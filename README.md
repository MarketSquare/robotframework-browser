# robotframework-browser
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-7-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![Version](https://img.shields.io/pypi/v/robotframework-browser.svg)](https://pypi.python.org/pypi/robotframework-browser)
[![Actions Status](https://github.com/MarketSquare/robotframework-browser/workflows/Python%20package/badge.svg)](https://github.com/MarketSquare/robotframework-browser/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

----

### :construction_worker: :construction: Work in Progress :construction: :performing_arts:

Robot Framework Browser library powered by [Playwright](https://playwright.dev/). Moving browser automation to year 2020 (or 2021)!

Aiming for :rocket: speed, :white_check_mark: reliability and :microscope: visibility.

Supporting testing and automation with [Robot Framework](https://robotframework.org) and [Python](https://python.org).

Official post about this [venture](https://forum.robotframework.org/t/moving-robot-framework-browser-automation-to-2020-or-2021/323).

# Installation instructions for users

1. Install node.js e.g. from https://nodejs.org/en/download/
2. Install robotframework-browser from the commandline: `pip install robotframework-browser`
3. Install the node dependencies needed to run Playwright from the commandline: `rfbrowser init`

# Development

## Development environment

Install Python, nodejs and yarn. Make sure you have `make` available.
- https://www.python.org/downloads/
- https://nodejs.org/
- https://classic.yarnpkg.com/en/docs/install

Setup development environment with `make dev-env`.
This creates a Python virtualenv in .venv directory, and install both Python and
nodejs dependencies.

To update the dependencies use either `make dev-env` to update all or
alternatively `make .venv` or `make node-deps` to update only Python or nodejs
dependencies, respectively.

Make sure to run `source .venv/bin/activate` to activate the correct virtualenv

### Development in Windows

Install [Chocolatey](https://chocolatey.org/) and then install development tools with
`choco install sed make`.

After that, the development workflow should work as described in the previous chapter.
The only difference is that the virtualenv needs to be activated by running
`.venv\Scripts\activate` in the command prompt.

## Testing
There are both unit tests written with pytest and acceptance test written with
Robot Framework. These can be run manually with `make utest` and `make atest`.
The tests are also executed in a prepush hook.

## Releasing
1. Ensure generated code and types are up to date with `make build`
2. Ensure tests and linting pass on CI
3. Check that you have permissions to release on Github and PyPi
4. Use `make release` to create and release artifacts and upload to PyPi
5. Create Github release

## Code style
Python code style is enforced with flake8 and black. These are executed in a
precommit hook, but can also be invoked manually with `make lint-python`.

## Architecture

Python Library <--> [gRPC](https://grpc.io/) <---> [TypeScript](https://www.typescriptlang.org/) and [Playwright](https://playwright.dev/)

## Contributors

This project is community driven and becomes a reality only through the work of all the people who contribute.
Supported by [Robocorp](https://robocorp.com/) through [Robot Framework Foundation](https://robotframework.org/foundation/).
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/mkorpela"><img src="https://avatars1.githubusercontent.com/u/136885?v=4" width="100px;" alt=""/><br /><sub><b>Mikko Korpela</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-playwright/commits?author=mkorpela" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/aaltat"><img src="https://avatars0.githubusercontent.com/u/2665023?v=4" width="100px;" alt=""/><br /><sub><b>Tatu Aalto</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-playwright/commits?author=aaltat" title="Code">💻</a></td>
    <td align="center"><a href="https://robocorp.com"><img src="https://avatars1.githubusercontent.com/u/8512727?v=4" width="100px;" alt=""/><br /><sub><b>Antti Karjalainen</b></sub></a><br /><a href="#fundingFinding-aikarjal" title="Funding Finding">🔍</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/ismoaro/"><img src="https://avatars2.githubusercontent.com/u/1047173?v=4" width="100px;" alt=""/><br /><sub><b>Ismo Aro</b></sub></a><br /><a href="#fundingFinding-IsNoGood" title="Funding Finding">🔍</a></td>
    <td align="center"><a href="https://twitter.com/janneharkonen"><img src="https://avatars3.githubusercontent.com/u/159146?v=4" width="100px;" alt=""/><br /><sub><b>Janne Härkönen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-playwright/commits?author=yanne" title="Code">💻</a></td>
    <td align="center"><a href="http://xylix.fi"><img src="https://avatars1.githubusercontent.com/u/13387304?v=4" width="100px;" alt=""/><br /><sub><b>Kerkko Pelttari</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-playwright/commits?author=xylix" title="Code">💻</a></td>
    <td align="center"><a href="https://robocorp.com"><img src="https://avatars3.githubusercontent.com/u/54288445?v=4" width="100px;" alt=""/><br /><sub><b>Robocorp</b></sub></a><br /><a href="#financial-robocorp" title="Financial">💵</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
