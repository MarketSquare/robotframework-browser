# Development setup

## Source code organization

These are the directories containing source code and tests:

 - `Browser`, contains the Python source code for the actual Robot Framework test library.
 - `node/playwright-wrapper`, contains a wrapper for Playwirght that implements the grpc protocol, implemented in Typescript.
 - `node/dynamic-test-app`, contains a test application used in the acceptance tests, implemented in Typescript + React.
 - `protobuf`, contains the Protocol Buffer definitions used by the communication between the library and Playwirght wrapper.
 - `utest`, unit tests for the Python code.
 - `atest`, acceptance tests written with Robot Framework.

## Development environment

Install Python, nodejs and yarn.
- https://www.python.org/downloads/
- https://nodejs.org/
- https://classic.yarnpkg.com/en/docs/install

Create a Python virtualenv e.g. with https://docs.python.org/3/library/venv.html.
The minimum Python version is 3.8.
[Invoke](http://www.pyinvoke.org/index.html) is used as a task runner / build tool.

Activate your virtualenv and install `invoke` with

  > pip install invoke

Other dependencies can be installed/updated with `inv deps`. This command installs and updated both Python and nodejs dependecies.

Run `inv -l` to get list of current build commands.

## Testing
There are both unit tests written with pytest and acceptance test written with
Robot Framework. These can be run manually with `inv utest` and `inv atest`.
To run continuously pytests in a watch mode `inv utest-watch`.
To rerun failed tests you can use `inv atest-failed` The tests are also executed in a prepush hook.

## Running tests in docker container

Docker container builds a clean install package. This can be used to check that a builded package works correctly in a clean environment without development dependencies.

1. Build the container `inv docker`
2. Run tests mounted from host machine `inv docker-test`.
3. See results in `atest/output`

## Releasing
1. Ensure generated code and types are up to date with `inv build`
2. Ensure tests and linting pass on CI
3. Check that you have permissions to release on Github and PyPi
4. Run `inv <new_version>` to update the version information to both Python and Node components.
5. Use `inv release` to create and release artifacts and upload to PyPi
6. Create Github release

## Code style
Python code style is enforced with flake8 and black. These are executed in a
precommit hook, but can also be invoked manually with `inv lint-python`.

JS / TS code style is enforced with eslint. Lints are run in precommit hooks, but can be run manually with `inv lint-node`.

## Architecture

There are 3 different interfaces that the library is targeting to use in browser automation and testing:

1. User interface: Interactions with DOM elements.
2. Internals of a webapp: State, Cookies, Storage, Methods.
3. Requests & Responses: Interface between a browser and servers .

Python Library <--> [gRPC](https://grpc.io/) <---> [TypeScript](https://www.typescriptlang.org/) and [Playwright](https://playwright.dev/)

# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

This project uses [allcontributors.org](https://allcontributors.org/) bot to list contributors in README.md.
You may interact with the bot by following the [bot usage guide](https://allcontributors.org/docs/en/bot/usage).

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a
   build.
2. Update the README.md with details of changes to the interface, this includes new environment
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of another developer, or if you
   do not have permission to do that, you may request the reviewer to merge it for you.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at [Robot Framework slack](https://robotframework-slack-invite.herokuapp.com/). All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/
