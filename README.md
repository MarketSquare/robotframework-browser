# robotframework-browser
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-15-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![Version](https://img.shields.io/pypi/v/robotframework-browser.svg)](https://pypi.python.org/pypi/robotframework-browser)
[![Actions Status](https://github.com/MarketSquare/robotframework-browser/workflows/Continuous%20integration/badge.svg)](https://github.com/MarketSquare/robotframework-browser/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

----

Robot Framework Browser library powered by [Playwright](https://playwright.dev/). Moving browser automation to year 2020 (or 2021)!

Aiming for :rocket: speed, :white_check_mark: reliability and :microscope: visibility.

Supporting testing and automation with [Robot Framework](https://robotframework.org)

    *** Settings ***
    Library   Browser
    
    *** Test Cases ***
    Example Test
        New Page    https://playwright.dev
        Get Text    h1    ==    🎭 Playwright

and [Python](https://python.org).

    import Browser
    browser = Browser.Browser()
    browser.new_page("https://playwright.dev")
    assert browser.get_text("h1") == '🎭 Playwright'
    browser.close_all_browsers()

Official post about this [venture](https://forum.robotframework.org/t/moving-robot-framework-browser-automation-to-2020-or-2021/323).

See [keyword documentation](https://marketsquare.github.io/robotframework-browser/Browser.html).

# Installation instructions

Only Python 3.8 or later is supported.

1. Install node.js e.g. from https://nodejs.org/en/download/
2. Install robotframework-browser from the commandline: `pip install robotframework-browser`

# Development

## Source code organization

These are the directories containing source code and tests:

 - `Browser`, contains the Python source code for the actual Robot Framework test library.
 - `node/playwright-wrapper`, contains a wrapper for Playwirght that implements the grpc protocol, implemented in Typescript.
 - `node/dynamic-test-app`, contains a test application used in the acceptance tests, implemented in Typescript + React.
 - `protobuf`, contains the Protocol Buffer definitions used by the communication between the library and Playwirght wrapper.
 - `utest`, unit tests for the Python code.
 - `atest`, acceptance tests written with Robot Framework.

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

Make sure to run `source .venv/bin/activate` to activate the correct virtualenv.

Run `make build` or `yarn build` to build the Typescript code. Also run `make build`
after changes to the protocol (protos/playwright.proto) to re-generate protobuffer code.

### Development in Windows

Install [Chocolatey](https://chocolatey.org/) and then install development tools with
`choco install sed make`.

After that, the development workflow should work as described in the previous chapter.
The only difference is that the virtualenv needs to be activated by running
`.venv\Scripts\activate` in the command prompt.

## Testing
There are both unit tests written with pytest and acceptance test written with
Robot Framework. These can be run manually with `make utest` and `make atest`.
To run continuously pytests in a watch mode `make utest-watch`.
To rerun failed tests you can use `make test-failed` The tests are also executed in a prepush hook.

## Running tests in docker container

Docker container builds a clean install package. This can be used to check that a builded package works correctly in a clean environment without development dependencies.

1. Build the container `make docker`
2. Run tests mounted from host machine `make docker-test`.
3. See results in `atest/output`

## Releasing
1. Ensure generated code and types are up to date with `make build`
2. Ensure tests and linting pass on CI
3. Check that you have permissions to release on Github and PyPi
4. Run `make version VERSION=<new_version>` to update the version information to both Python and Node components.
5. Use `make release` to create and release artifacts and upload to PyPi
6. Create Github release

## Code style
Python code style is enforced with flake8 and black. These are executed in a
precommit hook, but can also be invoked manually with `make lint-python`.

JS / TS code style is enforced with eslint. Lints are run in precommit hooks, but can be run manually with `make lint-node`.

## Architecture

There are 3 different interfaces that the library is targeting to use in browser automation and testing:

1. User interface: Interactions with DOM elements.
2. Internals of a webapp: State, Cookies, Storage, Methods.
3. Requests & Responses: Interface between a browser and servers .

Python Library <--> [gRPC](https://grpc.io/) <---> [TypeScript](https://www.typescriptlang.org/) and [Playwright](https://playwright.dev/)

## Contributors

This project is community driven and becomes a reality only through the work of all the people who contribute.
Supported by [Robocorp](https://robocorp.com/) through [Robot Framework Foundation](https://robotframework.org/foundation/).
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/mkorpela"><img src="https://avatars1.githubusercontent.com/u/136885?v=4" width="100px;" alt=""/><br /><sub><b>Mikko Korpela</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=mkorpela" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/aaltat"><img src="https://avatars0.githubusercontent.com/u/2665023?v=4" width="100px;" alt=""/><br /><sub><b>Tatu Aalto</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=aaltat" title="Code">💻</a></td>
    <td align="center"><a href="https://robocorp.com"><img src="https://avatars1.githubusercontent.com/u/8512727?v=4" width="100px;" alt=""/><br /><sub><b>Antti Karjalainen</b></sub></a><br /><a href="#fundingFinding-aikarjal" title="Funding Finding">🔍</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/ismoaro/"><img src="https://avatars2.githubusercontent.com/u/1047173?v=4" width="100px;" alt=""/><br /><sub><b>Ismo Aro</b></sub></a><br /><a href="#fundingFinding-IsNoGood" title="Funding Finding">🔍</a></td>
    <td align="center"><a href="https://twitter.com/janneharkonen"><img src="https://avatars3.githubusercontent.com/u/159146?v=4" width="100px;" alt=""/><br /><sub><b>Janne Härkönen</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=yanne" title="Code">💻</a></td>
    <td align="center"><a href="http://xylix.fi"><img src="https://avatars1.githubusercontent.com/u/13387304?v=4" width="100px;" alt=""/><br /><sub><b>Kerkko Pelttari</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=xylix" title="Code">💻</a></td>
    <td align="center"><a href="https://robocorp.com"><img src="https://avatars3.githubusercontent.com/u/54288445?v=4" width="100px;" alt=""/><br /><sub><b>Robocorp</b></sub></a><br /><a href="#financial-robocorp" title="Financial">💵</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Snooz82"><img src="https://avatars0.githubusercontent.com/u/41592183?v=4" width="100px;" alt=""/><br /><sub><b>René</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=Snooz82" title="Code">💻</a></td>
    <td align="center"><a href="https://wordpress.com/read/feeds/39696435"><img src="https://avatars0.githubusercontent.com/u/1123938?v=4" width="100px;" alt=""/><br /><sub><b>Bryan Oakley</b></sub></a><br /><a href="#ideas-boakley" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/idxn"><img src="https://avatars3.githubusercontent.com/u/2438992?v=4" width="100px;" alt=""/><br /><sub><b>Tanakiat Srisaranyakul</b></sub></a><br /><a href="#ideas-idxn" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="http://visible-quality.blogspot.com"><img src="https://avatars1.githubusercontent.com/u/5338157?v=4" width="100px;" alt=""/><br /><sub><b>Maaret Pyhäjärvi</b></sub></a><br /><a href="#userTesting-maaretp" title="User Testing">📓</a></td>
    <td align="center"><a href="http://www.tentamen.eu"><img src="https://avatars2.githubusercontent.com/u/777520?v=4" width="100px;" alt=""/><br /><sub><b>Karlo Smid</b></sub></a><br /><a href="#userTesting-karlosmid" title="User Testing">📓</a></td>
    <td align="center"><a href="https://github.com/aspargillus"><img src="https://avatars0.githubusercontent.com/u/4592889?v=4" width="100px;" alt=""/><br /><sub><b>Frank Schimmel</b></sub></a><br /><a href="#userTesting-Aspargillus" title="User Testing">📓</a></td>
    <td align="center"><a href="https://github.com/tuxmux28"><img src="https://avatars3.githubusercontent.com/u/2794048?v=4" width="100px;" alt=""/><br /><sub><b>Christoph</b></sub></a><br /><a href="https://github.com/MarketSquare/robotframework-browser/commits?author=tuxmux28" title="Tests">⚠️</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/mikahanninen"><img src="https://avatars2.githubusercontent.com/u/1019528?v=4" width="100px;" alt=""/><br /><sub><b>Mika Hänninen</b></sub></a><br /><a href="#question-mikahanninen" title="Answering Questions">💬</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
