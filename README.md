# robotframework-playwright

[![Contributors](https://img.shields.io/github/contributors/commonality/readme-inspector.svg)](https://github.com/MarketSquare/robotframework-playwright/graphs/contributors)
[![Version](https://img.shields.io/pypi/v/robotframework-playwright.svg)](https://pypi.python.org/pypi/robotframework-playwright)
[![Actions Status](https://github.com/MarketSquare/robotframework-playwright/workflows/Python%20package/badge.svg)](https://github.com/MarketSquare/robotframework-playwright/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

----

Robot Framework [Playwright](https://playwright.dev/) library. Moving browser automation to year 2020 (or 2021)!

Official post about this [venture](https://forum.robotframework.org/t/moving-robot-framework-browser-automation-to-2020-or-2021/323).

# Development

- https://www.python.org/downloads/
- `python -m pip install poetry`
- https://nodejs.org/
- https://classic.yarnpkg.com/en/docs/install

Install `yarn install` and `poetry install`.

Run pytests `poetry run pytest`.

### Make it do magic

- `yarn ts-node src/index.ts`
- `poetry run robot atest`

## Architecture

Python Library <--> [gRPC](https://grpc.io/) <---> [TypeScript](https://www.typescriptlang.org/) and [Playwright](https://playwright.dev/)

## Contributors

This project is community driven and becomes a reality only through the work of all the people who contribute.
<a href="https://github.com/MarketSquare/robotframework-playwright/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=MarketSquare/robotframework-playwright" />
</a>
