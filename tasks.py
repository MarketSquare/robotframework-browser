import os
from pathlib import Path
import platform
import re
import shutil

from invoke import task, Exit

try:
    from pabot import pabot
    import pytest
    from robot.libdoc import libdoc
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
    if not python_protobuf_dir.exists():
        python_protobuf_dir.mkdir()
        c.run(f"touch {python_protobuf_dir / '__init__.py'}")
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
		--grpc_out={node_protobuf_dir} \
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


@task(protobuf, node_build)
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
def utest(c):
    status = pytest.main()
    raise Exit()


@task
def utest_watch(c):
    c.run("ptw --ignore ./node_modules --ignore ./.venv")


@task
def clean_atest(c):
    if atest_output.exists():
        shutil.rmtree(atest_output)


@task(clean_atest)
def atest(c):
    _run_robot(
        ["--pythonpath", ".",]
    )


@task(clean_atest)
def atest_global_pythonpath(c):
    _run_robot()


# Running failed tests can't clean be cause the old output.xml is required for parsing which tests failed
@task()
def atest_failed(c):
    _run_robot(["--rerunfailed", "atest/output/output.xml"])


def _run_robot(extra_args=None):
    os.environ["ROBOT_SYSLOG_FILE"] = str(atest_output / "syslog.txt")
    pabot_args = ["--pabotlib", "--verbose"]
    default_args = [
        "--exclude",
        "Not-Implemented",
        "--loglevel",
        "DEBUG",
        "--outputdir",
        str(atest_output),
        "atest/test",
    ]
    pabot.main(pabot_args + (extra_args or []) + default_args)


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
    from Browser import VERSION

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
	    sh -c "ROBOT_SYSLOG_FILE=/app/atest/output/syslog.txt PATH=$PATH:~/.local/bin pabot --verbose --pabotlib --loglevel debug --exclude Not-Implemented --outputdir /app/atest/output /app/atest/test"
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


@task(package)
def release(c):
    c.run("python -m twine upload --repository pypi dist/*")


@task
def version(c, version):
    if not version:
        print("Give version with inv version <version>")
    py_version_file = root_dir / "Browser" / "version.py"
    py_version_matcher = re.compile("VERSION = .*")
    _replace_version(py_version_file, py_version_matcher, f'VERSION = "{version}"')
    node_version_file = root_dir / "package.json"
    node_version_matcher = re.compile('"version": ".*"')
    _replace_version(node_version_file, node_version_matcher, f'"version": "{version}"')
    workflow_file = root_dir / ".github" / "workflows" / "python-package.yml"
    workflow_version_matcher = re.compile("VERSION: .*")
    _replace_version(workflow_file, workflow_version_matcher, f"VERSION: {version}")


def _replace_version(filepath, matcher, version):
    content = filepath.open().read()
    with open(filepath, "w") as out:
        out.write(matcher.sub(version, content))
