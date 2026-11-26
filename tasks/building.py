import os
import platform
import shutil
import sys
import zipfile
from pathlib import Path, PurePath

from invoke import task
from invoke.context import Context

from tasks.shared import (
    ATEST_OUTPUT,
    BROWSER_BATTERIES_BIN_DIR,
    BROWSER_BATTERIES_DIR,
    BUILD_DIR,
    COVERAGE_DIR,
    DIST_DIR,
    IN_CI,
    NODE_MODULES,
    PYTHON_SRC_DIR,
    ROOT_DIR,
    SKIP_BROWSER_DOWNLOAD,
    UTEST_OUTPUT,
    WRAPPER_DIR,
    ZIP_DIR,
    clean_zip_dir,
    node_dir,
    node_protobuf_dir,
    npm_deps_timestamp_file,
    python_protobuf_dir,
    sources_changed,
)


def _node_deps(context: Context):
    context.run(
        "npm install --parseable true --progress false",
        env={"PLAYWRIGHT_BROWSERS_PATH": "0"},
    )
    if os.environ.get(SKIP_BROWSER_DOWNLOAD):
        print(f"{SKIP_BROWSER_DOWNLOAD} is set, skipping browser binaries.")
    else:
        context.run(
            "npx --quiet playwright install  --with-deps",
            env={"PLAYWRIGHT_BROWSERS_PATH": "0"},
        )
    npm_deps_timestamp_file.touch()


@task
def deps(c, force=False):
    """Install dependencies for development.

    Python dependencies are synced from uv.lock into the project's .venv. After
    changing the dependencies in pyproject.toml, run `uv lock` first. CI leaves
    out the `watch` group, because it installs wheels only.

    Args:
        force: When set, installs Node dependencies even there is no changes.
    """
    print("Installing Python dependencies.")
    c.run("uv sync --locked" if IN_CI else "uv sync --locked --all-groups")
    if IN_CI:
        shutil.rmtree(str(NODE_MODULES), ignore_errors=True)

    if sources_changed([ROOT_DIR / "./package-lock.json"], npm_deps_timestamp_file):
        print("Installing node dependencies.")
        _node_deps(c)
    elif force:
        print("Forcing to install node dependencies.")
        _node_deps(c)
    else:
        print("no changes in package-lock.json, skipping npm install")


@task
def protobuf(c):
    """Compile grpc protobuf files."""
    if not python_protobuf_dir.exists():
        python_protobuf_dir.mkdir()
        (python_protobuf_dir / "__init__.py").touch()
    if not node_protobuf_dir.exists():
        node_protobuf_dir.mkdir()
    _python_protobuf_gen(c)
    _node_protobuf_gen(c)


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
    protoc_ts_proto_plugin = (
        NODE_MODULES / ".bin" / f"protoc-gen-ts_proto{plugin_suffix}"
    )
    cmd = (
        "npm run grpc_tools_node_protoc -- "
        f"--plugin=protoc-gen-ts_proto={protoc_ts_proto_plugin} "
        f"--ts_proto_out={node_protobuf_dir} "
        "--ts_proto_opt=outputServices=grpc-js,env=node "
        "-I ./protobuf protobuf/*.proto"
    )
    c.run(cmd)


def _gen_stub(c: Context):
    shutil.rmtree("mypy_stub/", ignore_errors=True)
    Path("Browser/browser.pyi").unlink(missing_ok=True)
    c.run("stubgen --output mypy_stub Browser")
    c.run("python -m Browser.gen_stub")


def _remove_shadowing_node_modules(wrapper_dir: Path):
    node_modules = wrapper_dir / "node_modules"
    if node_modules.exists():
        print(
            f"Removing {node_modules}, left by rfbrowser init: it shadows the root node_modules."
        )
        shutil.rmtree(node_modules)


@task(protobuf)
def node_build(c: Context):
    _remove_shadowing_node_modules(WRAPPER_DIR)
    c.run("npm run build")
    shutil.rmtree(WRAPPER_DIR / "static", ignore_errors=True)
    shutil.copytree(node_dir / "playwright-wrapper" / "static", WRAPPER_DIR / "static")
    _gen_stub(c)


@task
def create_test_app(c):
    c.run("npm run build-test-app")


@task(deps, protobuf, node_build, create_test_app)
def build(c: Context):
    _gen_stub(c)


@task
def clean(c):
    """Cleans build and test artifacts, generated code and caches."""
    for target in [
        DIST_DIR,
        BUILD_DIR,
        UTEST_OUTPUT,
        ATEST_OUTPUT,
        ZIP_DIR,
        COVERAGE_DIR,
        BROWSER_BATTERIES_BIN_DIR,
        BROWSER_BATTERIES_DIR / "dist",
        BROWSER_BATTERIES_DIR / "build",
        WRAPPER_DIR,
        python_protobuf_dir,
        node_protobuf_dir,
        Path("./htmlcov"),
        Path("./.mypy_cache"),
        Path("./.ruff_cache"),
        Path("./.pytest_cache"),
    ]:
        shutil.rmtree(target, ignore_errors=True)
    for file in [
        npm_deps_timestamp_file,
        Path("./playwright-log.txt"),
        PYTHON_SRC_DIR / "rfbrowser.log",
        Path("./.coverage"),
        *ROOT_DIR.glob(".coverage.*"),
    ]:
        file.unlink(missing_ok=True)


@task
def run_test_app(c: Context, build=False):
    """Run the Test App in the foreground.

    Args:
        build: Build the Test App first.
    """
    if build:
        create_test_app(c)
    c.run("node node/dynamic-test-app/dist/server.js")


# TODO: should this depend on `create_test_app` ?
@task
def demo_app(c):
    """Zip demo application to OS specific package for CI"""
    clean_zip_dir()
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
