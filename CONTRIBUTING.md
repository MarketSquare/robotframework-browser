# Development setup

## Source code organization

These are the directories containing source code and tests:

 - `Browser`, contains the Python source code for the actual Robot Framework test library.
 - `node/playwright-wrapper`, contains a wrapper for Playwright that implements the grpc protocol, implemented in TypeScript.
 - `node/dynamic-test-app`, contains a test application used in the acceptance tests, implemented in TypeScript + React.
 - `protobuf`, contains the Protocol Buffer definitions used by the communication between the library and Playwright wrapper.
 - `utest`, unit tests for the Python code.
 - `atest`, acceptance tests written with Robot Framework.

## Development environment

Install Python and nodejs.
- https://www.python.org/downloads/
- https://nodejs.org/

N.B. The minimum Python version is 3.8.

Run `python bootstrap.py` to create a virtual environment with correct dependencies.
After that, make sure to activate the virtual env before running other development commands.

```
python bootstrap.py
source .venv/bin/activate  # On linux and OSX
.venv\Scripts\activate.bat  # On Windows
```

[Invoke](http://www.pyinvoke.org/index.html) is used as a task runner / build tool.

Other dependencies can be installed/updated with `inv deps`. This command installs and updates both Python and nodejs dependencies.
After dependencies are installed, run `inv build` to compile node code and gRPC protocol. Also this invoke command will create
Python stub file.

Run `inv -l` to get list of current build commands.

## Testing

There are both unit tests written with pytest and acceptance tests written with
Robot Framework. These can be run manually with `inv utest` and `inv atest`.
To run continuously pytests in a watch mode `inv utest-watch`.
To rerun failed tests you can use `inv atest-failed` The tests are also executed in a pre-push hook.

If there changes inv TypeScript side, remember to run `inv build` before executing unit or acceptance tests.

## Running tests in docker container

Docker container builds a clean install package. This can be used to check that a built package works correctly in a clean environment without development dependencies.

1. Build the container `inv docker`
2. Run tests mounted from host machine `inv docker-test`
3. See results in `atest/output`

## Releasing

### Prerequisite
1. Ensure tests and linting pass on CI
1. Check that you have permissions to release on Github and PyPi

### Install dependencies
Ensure generated code and types are up to date with `inv build`

### Create previous version docs
Set `VERSION=<version>`. Version number should match to the milestone to the 
[issue tracker](https://github.com/MarketSquare/robotframework-browser/milestones)

Checkout previously released tag, generate the keyword documentation from the
previous release and add the keyword documentation to the repository main branch.

```
export VERSION=<version>
git describe --tags --abbrev=0 | xargs git checkout
git describe --tags --abbrev=0 | xargs inv docs -v
git checkout main
git add docs/versions/Browser-*.html
git commit -m "Add `git describe --tags --abbrev=0` keyword documentation to repository."
git push
```

### Set version number
Run `inv version $VERSION` to update the version information to both Python
and Node components.

```
inv version $VERSION
inv build
git add Browser/version.py package.json package-lock.json setup.py docker/Dockerfile.latest_release
git commit -m "Updateversion to: $VERSION"
```

### Generate release notes
Set GitHub user information into shell variables to ease copy-pasting the following command:
```
export GITHUB_USERNAME=<username>
export GITHUB_PASSWORD=<password>
```

Generate a template for the release notes:
```
invoke release-notes -w -v $VERSION -u $GITHUB_USERNAME -p $GITHUB_PASSWORD
```

Fill the missing details in the generated release notes template.

Make sure that issues have correct information:
* All issues should have type (bug, enhancement or task) and priority set. Notice that issues with the task type are
automatically excluded from the release notes.
* Issue priorities should be consistent.
* Issue titles should be informative. Consistency is good here too, but no need to overdo it.

If information needs to be added or edited, its better to edit it in the issue tracker than in the generated release
notes. This allows re-generating the list of issues later if more issues are added.

Add, commit and push:
```
git add docs/releasenotes/Browser-$VERSION.rst
git commit -m "Release notes for $VERSION"
git tag -fa v$VERSION
git push --tags --force
```
Update later if necessary.

Also update Browser libdoc.

### Create release
1. Use `inv release` to create and release artifacts and upload to PyPi
2. [Create Github release](https://github.com/MarketSquare/robotframework-browser/releases/new)
3. Check that [PyPi](https://pypi.org/project/robotframework-browser/) looks good.
4. Install package from PyPi and test that it works.

### Announce release
Announce new release, at least in Slack, [Forum](https://forum.robotframework.org/t/browser-library-releases/685)
and user group mailing list.

## Code style
Python code style is enforced with flake8 and black. These are executed in a
pre-commit hook, but can also be invoked manually with `inv lint-python`.

JS / TS code style is enforced with eslint. Lints are run in pre-commit hooks, but can be run manually with `inv lint-node`.

## Architecture

There are 3 different interfaces that the library is targeting to use in browser automation and testing:

1. User interface: Interactions with DOM elements.
2. Internals of a webapp: State, Cookies, Storage, Methods.
3. Requests & Responses: Interface between a browser and servers.

Python Library <--> [gRPC](https://grpc.io/) <---> [TypeScript](https://www.typescriptlang.org/) and [Playwright](https://playwright.dev/)

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note that we have a [Code of Conduct](CODE_OF_CONDUCT.md).  Please familiarise yourself with this document
and follow the code in all your interactions with the project.

This project uses [allcontributors.org](https://allcontributors.org/) bot to list contributors in README.md.
You may interact with the bot by following the [bot usage guide](https://allcontributors.org/docs/en/bot/usage).

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any example files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request once you have sign-off from another developer. If you do not have
   permission to perform the merge, you may request the reviewer merges your pull request for you.
