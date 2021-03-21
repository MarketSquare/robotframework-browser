import os
import subprocess
import sys
import zipfile
from pathlib import Path, PurePath
import platform
import re
import shutil

from invoke import task, Exit
from robot import rebot_cli
from robot import __version__ as robot_version

try:
    from pabot import pabot
    import pytest
    from rellu import ReleaseNotesGenerator, Version
    from robot.libdoc import libdoc
    import robotstatuschecker
    import bs4
except ModuleNotFoundError:
    print('Assuming that this is for "inv deps" command and ignoring error.')

ROOT_DIR = Path(os.path.dirname(__file__))
ATEST_OUTPUT = ROOT_DIR / "atest" / "output"
dist_dir = ROOT_DIR / "dist"
build_dir = ROOT_DIR / "build"
proto_sources = (ROOT_DIR / "protobuf").glob("*.proto")
python_src_dir = ROOT_DIR / "Browser"
python_protobuf_dir = python_src_dir / "generated"
node_protobuf_dir = ROOT_DIR / "node" / "playwright-wrapper" / "generated"
node_dir = ROOT_DIR / "node"
node_timestamp_file = node_dir / ".built"
node_lint_timestamp_file = node_dir / ".linted"
python_lint_timestamp_file = python_src_dir / ".linted"

ZIP_DIR = ROOT_DIR / "zip_results"
RELEASE_NOTES_PATH = Path("docs/releasenotes/Browser-{version}.rst")
RELEASE_NOTES_TITLE = "Browser library {version}"
REPOSITORY = "MarketSquare/robotframework-browser"
VERSION_PATH = Path("Browser/version.py")
RELEASE_NOTES_INTRO = """
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
.. _Playwright: https://github.com/microsoft/playwright
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-browser
.. _issue tracker: https://github.com/MarketSquare/robotframework-browser/milestones%3A{version.milestone}
"""


@task
def deps(c):
    c.run("pip install -U pip")
    c.run("pip install -r Browser/dev-requirements.txt")
    if os.environ.get("CI"):
        shutil.rmtree("node_modules")
    c.run("yarn", env={"PLAYWRIGHT_BROWSERS_PATH": "0"})


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
        ROOT_DIR
        / "node_modules"
        / ".bin"
        / f"grpc_tools_node_protoc_plugin{plugin_suffix}"
    )
    protoc_ts_plugin = (
        ROOT_DIR / "node_modules" / ".bin" / f"protoc-gen-ts{plugin_suffix}"
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
    if ATEST_OUTPUT.exists():
        shutil.rmtree(ATEST_OUTPUT)
    if ZIP_DIR.exists():
        shutil.rmtree(ZIP_DIR)


@task(clean_atest)
def atest(c, suite=None, include=None, zip=None):
    """Runs Robot Framework acceptance tests.

    Args:
        suite: Select which suite to run.
        include: Select test by tag
        zip: Create zip file from output files.
    """
    args = [
        "--pythonpath",
        ".",
    ]
    if suite:
        args.extend(["--suite", suite])
    if include:
        args.extend(["--include", include])
    exit = False if zip else True
    os.mkdir(ATEST_OUTPUT)
    logfile = open(Path(ATEST_OUTPUT, "playwright-log.txt"), "w")
    os.environ["DEBUG"] = "pw:api"
    process = subprocess.Popen([
        "node",
        "Browser/wrapper/index.js",
        "18771",
    ], stdout=logfile, stderr=subprocess.STDOUT)
    os.environ["ROBOT_FRAMEWORK_BROWSER_NODE_PORT"] = str(18771)
    rc = _run_pabot(args, exit)
    process.kill()
    if zip:
        _clean_zip_dir()
        print(f"Zip file created to: {_create_zip()}")
    sys.exit(rc)


def _clean_zip_dir():
    if ZIP_DIR.exists():
        shutil.rmtree(ZIP_DIR)


def _create_zip():
    zip_dir = ZIP_DIR / "output"
    zip_dir.mkdir(parents=True)
    python_version = platform.python_version()
    zip_name = f"{sys.platform}-rf-{robot_version}-python-{python_version}.zip"
    zip_path = zip_dir / zip_name
    print(f"Creating zip  in: {zip_path}")
    zip_file = zipfile.ZipFile(zip_path, "w")
    for file in ATEST_OUTPUT.glob("**/*.*"):
        file = PurePath(file)
        arc_name = file.relative_to(str(ATEST_OUTPUT))
        zip_file.write(file, arc_name)
    zip_file.close()
    return zip_path


@task(clean_atest)
def atest_robot(c):
    os.environ["ROBOT_SYSLOG_FILE"] = str(ATEST_OUTPUT / "syslog.txt")
    command = f"robot --exclude Not-Implemented --loglevel DEBUG --outputdir {str(ATEST_OUTPUT)}"
    if platform.platform().startswith("Windows"):
        command += " --exclude No-Windows-Support"
    command += " atest/test"
    print(command)
    c.run(command)


@task(clean_atest)
def atest_global_pythonpath(c):
    _run_pabot()


# Running failed tests can't clean be cause the old output.xml is required for parsing which tests failed
@task()
def atest_failed(c):
    _run_pabot(["--rerunfailed", "atest/output/output.xml"])


@task()
def run_tests(c, tests):
    """
    Run robot with dev Browser. Parameter [tests] is the path to tests to run.
    """
    process = subprocess.Popen(
        [sys.executable, "-m", "robot", "--loglevel", "DEBUG", tests]
    )
    process.wait(600)


def _run_pabot(extra_args=None, exit=True):
    os.environ["ROBOT_SYSLOG_FILE"] = str(ATEST_OUTPUT / "syslog.txt")
    pabot_args = [
        sys.executable,
        "-m",
        "pabot.pabot",
        "--pabotlib",
        "--artifacts",
        "png,webm",
        "--artifactsinsubfolders",
    ]
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
        str(ATEST_OUTPUT),
    ]
    if platform.platform().startswith("Windows"):
        default_args.extend(["--exclude", "No-Windows-Support"])
    default_args.append("atest/test")
    process = subprocess.Popen(pabot_args + (extra_args or []) + default_args)
    process.wait(600)
    output_xml = str(ATEST_OUTPUT / "output.xml")
    print(f"Process {output_xml}")
    robotstatuschecker.process_output(output_xml, verbose=False)
    rc = rebot_cli(["--outputdir", str(ATEST_OUTPUT), output_xml], exit=exit)
    print("DONE")
    return rc


@task
def lint_python(c):
    all_py_sources = list(python_src_dir.glob("**/*.py")) + list(
        (ROOT_DIR / "utest").glob("**/*.py")
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

@task()
def docker_run_tmp_tests(c):
    """
    Run robot with dev Browser from docker against tmp dir.
    """
    c.run(
        """docker run\
        --rm \
        --ipc=host\
        --security-opt seccomp=atest/docker/chrome.json \
        -v $(pwd)/tmp/:/app/tmp \
        -v $(pwd)/node/:/app/node/ \
        --workdir /app \
        rfbrowser \
        sh -c "ROBOT_SYSLOG_FILE=/app/atest/output/syslog.txt PATH=$PATH:~/.local/bin robot --loglevel debug --outputdir /app/tmp/output /app/tmp/"
        """
    )

@task(build)
def run_test_app(c):
    c.run("node node/dynamic-test-app/dist/server.js")


@task
def docs(c):
    """Generate library keyword documentation."""
    output = ROOT_DIR / "docs" / "Browser.html"
    libdoc("Browser", str(output))
    with output.open("r") as file:
        data = file.read()
    soup = bs4.BeautifulSoup(data, "html.parser")
    script_async = soup.new_tag(
        "script", src="https://www.googletagmanager.com/gtag/js?id=UA-106835747-3"
    )
    script_async.attrs["async"] = None
    soup.head.append(script_async)
    script_data = soup.new_tag("script")
    script_data.string = """
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'UA-106835747-3', {
            'anonymize_ip': true,
            'page_path': location.pathname+location.search+location.hash });
      window.onhashchange = function() {
            gtag('event', 'HashChange', {
            'event_category': 'Subsection',
            'event_label': window.location.hash
            });
       }
    """
    soup.head.append(script_data)
    with output.open("w") as file:
        file.write(str(soup))

@task
def create_package(c):
    shutil.copy(ROOT_DIR / "package.json", ROOT_DIR / "Browser" / "wrapper")
    c.run("python setup.py sdist bdist_wheel")


@task(clean, build, docs, create_package)
def package(c):
    pass

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
    generator = ReleaseNotesGenerator(
        REPOSITORY, RELEASE_NOTES_TITLE, RELEASE_NOTES_INTRO
    )
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
    py_version_file = ROOT_DIR / "Browser" / "version.py"
    py_version_matcher = re.compile("__version__ = .*")
    _replace_version(py_version_file, py_version_matcher, f'__version__ = "{version}"')
    node_version_file = ROOT_DIR / "package.json"
    node_version_matcher = re.compile('"version": ".*"')
    _replace_version(node_version_file, node_version_matcher, f'"version": "{version}"')
    setup_py_file = ROOT_DIR / "setup.py"
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


@task
def demo_app(c):
    """Zip demo application to OS specific package for CI"""
    _clean_zip_dir()
    zip_dir = ZIP_DIR / "demoapp"
    zip_dir.mkdir(parents=True)
    zip_name = f"demo-app-{sys.platform}.zip"
    zip_path = zip_dir / zip_name
    demo_app = Path("node", "dynamic-test-app").resolve()
    print(f"Creating zip  in: {zip_path}")
    zip_file = zipfile.ZipFile(zip_path, "w")
    for file in demo_app.glob("**/*.*"):
        file = PurePath(file)
        arc_name = file.relative_to(str(ROOT_DIR))
        zip_file.write(file, arc_name)
    zip_file.close()
    return zip_path
