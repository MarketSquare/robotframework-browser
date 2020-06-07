# robotframework-playwright

[![Actions Status](https://github.com/MarketSquare/robotframework-playwright/workflows/Python%20package/badge.svg)](https://github.com/MarketSquare/robotframework-playwright/actions)

Robot Framework [Playwright](https://playwright.dev/) library. Moving browser automation to year 2020 (or 2021)!

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
