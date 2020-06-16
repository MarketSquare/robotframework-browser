# robotframework-playwright
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-7-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
[![Version](https://img.shields.io/pypi/v/robotframework-playwright.svg)](https://pypi.python.org/pypi/robotframework-playwright)
[![Actions Status](https://github.com/MarketSquare/robotframework-playwright/workflows/Python%20package/badge.svg)](https://github.com/MarketSquare/robotframework-playwright/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

----

### :construction_worker: :construction: Work in Progress :construction: :performing_arts:

Robot Framework [Playwright](https://playwright.dev/) library. Moving browser automation to year 2020 (or 2021)!

Aiming for :rocket: speed, :white_check_mark: reliability and :microscope: visibility.

Official post about this [venture](https://forum.robotframework.org/t/moving-robot-framework-browser-automation-to-2020-or-2021/323).

# Installation

1. Install node.js e.g. from https://nodejs.org/en/download/
2. Install playwright on node.js from the commandline: `[sudo] npm install --global playwright`
3. Install robotframework-playwright from the commandline: `pip install robotframework-playwright`

# Development

- https://www.python.org/downloads/
- `python -m pip install poetry`
- https://nodejs.org/
- https://classic.yarnpkg.com/en/docs/install

Install `yarn install` and `poetry install`.

Run pytests `poetry run pytest`.

Run Robot Framework tests `poetry run robot --outputdir atest/output atest/test`

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
