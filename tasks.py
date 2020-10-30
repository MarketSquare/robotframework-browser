import os
import subprocess
import sys
from pathlib import Path
import platform
import re
import shutil

from invoke import task, Exit
from robot import rebot_cli

try:
    from pabot import pabot
    import pytest
    from rellu import ReleaseNotesGenerator, Version
    from robot.libdoc import libdoc
    import robotstatuschecker
except ModuleNotFoundError:
    print('Assuming that this is for "inv deps" command and ignoring error.')

root_dir = Path(os.path.dirname(__file__))
atest_output = root_dir / "atest" / "output"
dist_dir = root_dir / "dist"
build_dir = root_dir / "build"
proto_sources = (root_dir / "protobuf").glob("*.proto")
python_src_dir = root_dir / "Browser"
python_protobuf_dir = python_src_dir / "generated"
node_protobuf_dir = root_dir / "node" / "playwright-wrapper" / "generated"
node_dir = root_dir / "node"
node_timestamp_file = node_dir / ".built"
node_lint_timestamp_file = node_dir / ".linted"
python_lint_timestamp_file = python_src_dir / ".linted"

RELEASE_NOTES_PATH = Path('docs/releasenotes/Browser-{version}.rst')
RELEASE_NOTES_TITLE = 'Browser library {version}'
REPOSITORY = 'MarketSquare/robotframework-browser'
VERSION_PATH = Path('Browser/version.py')
RELEASE_NOTES_INTRO = '''
Browser_ is a web testing library for `Robot Framework`_ that utilizes
the Playwright_ tool internally. Browser library {version} is a new release with
**UPDATE** enhancements and bug fixes.
All issues targeted for Browser library {version.milestone} can be found
from the `issue tracker`_.
If you have pip_ installed, just run
::
   pip install --upgrade robotframework-browser
   rfbrowser init
to install the latest available release or use
::
   pip install robotframework-browser=={version}
   rfbrowser init
to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.
Browser library {version} was released on {date}. Browser supports
Python **>=3.7**, and Robot Framework **>=3.2**.

.. _Robot Framework: http://robotframework.org
.. _Browser: https://github.com/MarketSquare/robotframework-browser
.. _Selenium: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3A{version.milestone}
'''


@task
def deps(c):
    c.run("pip install -U pip")
    c.run("pip install -r Browser/dev-requirements.txt")
    c.run("yarn")


@task
def clean(c):
    for target in [dist_dir, build_dir, python_protobuf_dir, node_protobuf_dir]:
        if target.exists():
            shutil.rmtree(target)
    for timestamp_file in [
        node_timestamp_file,
        node_lint_timestamp_file,
        python_lint_timestamp_file,
    ]:
        try:
            # python 3.7 doesn't support missing_ok so we need a try catch
            timestamp_file.unlink()
        except OSError as e:
            pass


@task
def protobuf(c):
    """Compile grpc protobuf files.

    Compiles for Python and node.
    """
    if not python_protobuf_dir.exists():
        python_protobuf_dir.mkdir()
        (python_protobuf_dir / "__init__.py").touch()
    if not node_protobuf_dir.exists():
        node_protobuf_dir.mkdir()
    gen_timestamp_file = python_protobuf_dir / ".generated"
    if _sources_changed(proto_sources, gen_timestamp_file):
        _python_protobuf_gen(c)
        _node_protobuf_gen(c)
        gen_timestamp_file.touch()
    else:
        print("no changes in .proto files, skipping protobuf build")


def _python_protobuf_gen(c):
    c.run(
        f"python -m grpc_tools.protoc -I protobuf --python_out=Browser/generated --grpc_python_out={python_protobuf_dir} --mypy_out={python_protobuf_dir} protobuf/*.proto"
    )
    genfile = python_protobuf_dir / "playwright_pb2_grpc.py"
    content = (
        open(genfile)
        .read()
        .replace(
            "import playwright_pb2 as playwright__pb2",
            "from Browser.generated import playwright_pb2 as playwright__pb2",
        )
    )
    with open(genfile, "w") as outfile:
        outfile.write(content)


def _node_protobuf_gen(c):
    plugin_suffix = ".cmd" if platform.platform().startswith("Windows") else ""
    protoc_plugin = (
        root_dir
        / "node_modules"
        / ".bin"
        / f"grpc_tools_node_protoc_plugin{plugin_suffix}"
    )
    protoc_ts_plugin = (
        root_dir / "node_modules" / ".bin" / f"protoc-gen-ts{plugin_suffix}"
    )
    c.run(
        f"yarn run grpc_tools_node_protoc \
		--js_out=import_style=commonjs,binary:{node_protobuf_dir} \
		--grpc_out=grpc_js:{node_protobuf_dir} \
		--plugin=protoc-gen-grpc={protoc_plugin} \
		-I ./protobuf \
		protobuf/*.proto"
    )
    c.run(
        f"yarn run grpc_tools_node_protoc \
		--plugin=protoc-gen-ts={protoc_ts_plugin} \
		--ts_out={node_protobuf_dir} \
		-I ./protobuf \
		protobuf/*.proto"
    )


@task(protobuf)
def node_build(c):
    if _sources_changed(
        node_dir.glob("**/*.ts"), node_timestamp_file
    ) or _sources_changed(node_dir.glob("**/*.tsx"), node_timestamp_file):
        c.run("yarn build")
        node_timestamp_file.touch()
    else:
        print("no changes in .ts files, skipping node build")


@task(deps, protobuf, node_build)
def build(c):
    c.run("python -m Browser.gen_stub")


def _sources_changed(source_files, timestamp_file):
    if timestamp_file.exists():
        last_built = timestamp_file.lstat().st_mtime
        src_last_modified = [f.lstat().st_mtime for f in source_files]
        return not all([last_built >= modified for modified in src_last_modified])
    return True


@task(build)
def watch(c):
    c.run("yarn watch")


@task
def utest(c, reporter=None, suite=None):
    """Run utest.

    Args:
        reporter: Defines which approval test reporter to use.
                  Must be full path to the diff program.
                  For more details see:
                  https://pypi.org/project/pytest-approvaltests/
                  https://github.com/approvals/ApprovalTests.Python
        suite:    Defines which test suite file to run. Same as: pytest path/to/test.py
                  Must be path to the test suite file
    """
    args = ["--showlocals"]
    if reporter:
        args.append(f"--approvaltests-add-reporter={reporter}")
    if suite:
        args.append(suite)
    status = pytest.main(args)
    raise Exit(status)


@task
def utest_watch(c):
    c.run("ptw --ignore ./node_modules --ignore ./.venv")


@task
def clean_atest(c):
    if atest_output.exists():
        shutil.rmtree(atest_output)


@task(clean_atest)
def atest(c, suite=None):
    """Runs Robot Framework acceptance tests.

    Args:
        suite: Select which suite to run.
    """
    args = ["--pythonpath", ".",]
    if suite:
        args.extend(["--suite", suite])
    _run_robot(args)


@task(clean_atest)
def atest_robot(c):
    os.environ["ROBOT_SYSLOG_FILE"] = str(atest_output / "syslog.txt")
    command = f"robot --exclude Not-Implemented --loglevel DEBUG --outputdir {str(atest_output)}"
    if platform.platform().startswith("Windows"):
        command += " --exclude No-Windows-Support"
    command += " atest/test"
    print(command)
    c.run(command)


@task(clean_atest)
def atest_global_pythonpath(c):
    _run_robot()


# Running failed tests can't clean be cause the old output.xml is required for parsing which tests failed
@task()
def atest_failed(c):
    _run_robot(["--rerunfailed", "atest/output/output.xml"])

@task()
def run_tests(c, tests):
    process = subprocess.Popen([sys.executable, "-m", "robot", tests])
    process.wait(600)

def _run_robot(extra_args=None):
    os.environ["ROBOT_SYSLOG_FILE"] = str(atest_output / "syslog.txt")
    pabot_args = [sys.executable, "-m", "pabot.pabot", "--pabotlib"]
    default_args = [
        "--exclude",
        "Not-Implemented",
        "--loglevel",
        "DEBUG",
        "--report",
        "NONE",
        "--log",
        "NONE",
        "--outputdir",
        str(atest_output),
    ]
    if platform.platform().startswith("Windows"):
        default_args.extend(["--exclude", "No-Windows-Support"])
    default_args.append("atest/test")
    process = subprocess.Popen(pabot_args + (extra_args or []) + default_args)
    process.wait(600)
    output_xml = str(atest_output / "output.xml")
    print(f"Process {output_xml}")
    robotstatuschecker.process_output(output_xml, verbose=False)
    rebot_cli(["--outputdir", str(atest_output), output_xml])
    print("DONE")


@task
def lint_python(c):
    all_py_sources = list(python_src_dir.glob("**/*.py")) + list(
        (root_dir / "utest").glob("**/*.py")
    )
    if _sources_changed(all_py_sources, python_lint_timestamp_file):
        c.run("mypy --config-file Browser/mypy.ini Browser/ utest/")
        c.run("black --config Browser/pyproject.toml Browser/")
        c.run("flake8 --config Browser/.flake8 Browser/ utest/")
        c.run("isort Browser/")
        python_lint_timestamp_file.touch()
    else:
        print("no changes in .py files, skipping python lint")


@task
def lint_node(c):
    if _sources_changed(node_dir.glob("**/*.ts"), node_lint_timestamp_file):
        c.run("yarn run lint")
        node_lint_timestamp_file.touch()
    else:
        print("no changes in .ts files, skipping node lint")


@task
def lint_robot(c):
    c.run("python -m robot.tidy --recursive atest/test")


@task(lint_python, lint_node, lint_robot)
def lint(c):
    pass


@task
def docker_base(c):
    c.run(
        "DOCKER_BUILDKIT=1 docker build --tag playwright-focal --file atest/docker/Dockerfile.playwright20.04 ."
    )


@task
def docker_builder(c):
    c.run(
        "DOCKER_BUILDKIT=1 docker build --tag rfbrowser --file atest/docker/Dockerfile ."
    )


@task
def docker_stable_image(c):
    from Browser.version import __version__ as VERSION

    c.run(
        f"DOCKER_BUILDKIT=1 docker build --tag docker.pkg.github.com/marketsquare/robotframework-browser/rfbrowser-stable:{VERSION} --file atest/docker/Dockerfile.latest_release ."
    )


@task(clean_atest, build)
def docker_test(c):
    c.run("mkdir atest/output")
    c.run(
        """docker run\
	    --rm \
	    --ipc=host\
	    --security-opt seccomp=atest/docker/chrome.json \
	    -v $(pwd)/atest/:/app/atest \
	    -v $(pwd)/node/:/app/node/ \
	    --workdir /app \
	    rfbrowser \
	    sh -c "ROBOT_SYSLOG_FILE=/app/atest/output/syslog.txt PATH=$PATH:~/.local/bin pabot --pabotlib --loglevel debug --exclude Not-Implemented --outputdir /app/atest/output /app/atest/test"
          """
    )


@task(build)
def run_test_app(c):
    c.run("node node/dynamic-test-app/dist/server.js")


@task
def docs(c):
    libdoc("Browser", str(root_dir / "docs" / "Browser.html"))


@task(clean, build, docs)
def package(c):
    shutil.copy(root_dir / "package.json", root_dir / "Browser" / "wrapper")
    c.run("python setup.py sdist bdist_wheel")


@task
def release_notes(c, version=None, username=None, password=None, write=False):
    """Generates release notes based on issues in the issue tracker.

    Args:
        version:  Generate release notes for this version. If not given,
                  generated them for the current version.
        username: GitHub username.
        password: GitHub password.
        write:    When set to True, write release notes to a file overwriting
                  possible existing file. Otherwise just print them to the
                  terminal.
    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively. If they aren't
    specified at all, communication with GitHub is anonymous and typically
    pretty slow.
    """
    pattern = '__version__ = "(.*)"'
    if write and not RELEASE_NOTES_PATH.parent.is_dir():
        RELEASE_NOTES_PATH.parent.mkdir(parents=True)
    version = Version(version, VERSION_PATH, pattern)
    file = RELEASE_NOTES_PATH if write else sys.stdout
    generator = ReleaseNotesGenerator(REPOSITORY, RELEASE_NOTES_TITLE,
                                      RELEASE_NOTES_INTRO)
    generator.generate(version, username, password, file)


@task(package)
def release(c):
    c.run("python -m twine upload --repository pypi dist/*")


@task(docs)
def version(c, version):
    from Browser.version import __version__ as VERSION

    os.rename("docs/Browser.html", f"docs/versions/Browser-{VERSION}.html")
    if not version:
        print("Give version with inv version <version>")
    py_version_file = root_dir / "Browser" / "version.py"
    py_version_matcher = re.compile("__version__ = .*")
    _replace_version(py_version_file, py_version_matcher, f'__version__ = "{version}"')
    node_version_file = root_dir / "package.json"
    node_version_matcher = re.compile('"version": ".*"')
    _replace_version(node_version_file, node_version_matcher, f'"version": "{version}"')
    setup_py_file = root_dir / "setup.py"
    _replace_version(setup_py_file, node_version_matcher, f'"version": "{version}"')
    # workflow_file = root_dir / ".github" / "workflows" / "python-package.yml"
    # workflow_version_matcher = re.compile("VERSION: .*")
    # _replace_version(workflow_file, workflow_version_matcher, f"VERSION: {version}")


def _replace_version(filepath, matcher, version):
    content = filepath.open().read()
    with open(filepath, "w") as out:
        out.write(matcher.sub(version, content))


@task
def gh_pages_index(c):
    import os

    links = [
        f"""<a href="versions/{i}">{i}</a>"""
        for i in sorted(os.listdir("docs/versions"))
    ]

    index_contents = f"""
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head>
            <meta charset="utf-8"/>
            <title>Robot Framework Browser</title>
            <link rel="stylesheet" href="style.css" type="text/css" />
        </head>
        <body>
            <p>
                Check out our GitHub homepage for details.
                <a href="https://github.com/MarketSquare/robotframework-browser">Project Home</a>
            </p>
            <p>
                <a href="Browser.html">Keyword Documentation</a>
            </p>
            <p>
                <h3> Old releases</h3>
                {links}
            </p>
        </body>
    </html>
    """

    with open("docs/index.html", "w") as f:
        f.write(index_contents)
