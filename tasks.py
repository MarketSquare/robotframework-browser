import os
from pathlib import Path
import re
import shutil

from invoke import task, Exit
from pabot import pabot
import pytest
from robot.libdoc import libdoc

root_dir = Path(os.path.dirname(__file__))
venv_dir = root_dir / ".venv"
atest_output = root_dir / "atest" / "output"
dist_dir = root_dir / "dist"
build_dir = root_dir / "build"


@task
def deps(c):
    c.run("pip install -r Browser/dev-requirements.txt")
    c.run("pip install -r Browser/requirements.txt")
    c.run("yarn")


@task
def clean(c):
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)


@task
def protobuf_python(c):
    gendir = root_dir / "Browser" / "generated"
    if not gendir.exists():
        gendir.mkdir()
        init_path = gendir / "__init__.py"
        c.run(f"touch {init_path}")
    c.run(
        "python -m grpc_tools.protoc -I protobuf --python_out=Browser/generated --grpc_python_out=Browser/generated --mypy_out=Browser/generated protobuf/*.proto"
    )
    genfile = gendir / "playwright_pb2_grpc.py"
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


@task
def protobuf_node(c):
    gendir = root_dir / "node" / "playwright-wrapper" / "generated"
    if not gendir.exists():
        gendir.mkdir()
    protoc_plugin = root_dir / "node_modules" / ".bin" / "grpc_tools_node_protoc_plugin"
    protoc_ts_plugin = root_dir / "node_modules" / ".bin" / "protoc-gen-ts"
    c.run(
        f"yarn run grpc_tools_node_protoc \
		--js_out=import_style=commonjs,binary:{gendir} \
		--grpc_out={gendir} \
		--plugin=protoc-gen-grpc={protoc_plugin} \
		-I ./protobuf \
		protobuf/*.proto"
    )
    c.run(
        f"yarn run grpc_tools_node_protoc \
		--plugin=protoc-gen-ts={protoc_ts_plugin} \
		--ts_out={gendir} \
		-I ./protobuf \
		protobuf/*.proto"
    )


@task(protobuf_python, protobuf_node)
def protobuf(c):
    pass


@task
def node_build(c):
    c.run("yarn build")


@task(protobuf, node_build)
def build(c):
    c.run("python -m Browser.gen_stub")


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


@task(clean_atest)
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
    c.run("mypy --config-file Browser/mypy.ini Browser/ utest/")
    c.run("black --config Browser/pyproject.toml Browser/")
    c.run("flake8 --config Browser/.flake8 Browser/ utest/")
    c.run("isort Browser/")


@task
def lint_node(c):
    c.run("yarn run lint")


@task
def lint_robot(c):
    c.run("python -m robot.tidy --recursive atest/test")


@task(lint_python, lint_node, lint_robot)
def lint(c):
    pass


@task
def docker(c):
    c.run("docker build --tag rfbrowser --file atest/docker/Dockerfile .")


@task(clean_atest)
def docker_test(c):
    c.run(
        "docker run -it --rm --ipc=host --security-opt seccomp=atest/docker/chrome.json -v $(shell pwd)/atest/:/atest rfbrowser robot --loglevel debug --exclude Not-Implemented -d /atest/output /atest/test"
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
