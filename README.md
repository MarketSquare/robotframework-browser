# robotframework-playwright

Robot Framework [Playwright](https://playwright.dev/) library

# Goal

Porting [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary) based tests to Playwright.

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
