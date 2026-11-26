import os
import shlex
import shutil
import time

from invoke import Exit, task
from invoke.context import Context

from tasks.building import build, create_test_app
from tasks.shared import ROOT_DIR
from tasks.testing import _browser_args, clean_atest

DOCKER_OUTPUT = ROOT_DIR / "output_docker"


@task
def docker_tester(c):
    c.run(
        "docker buildx build --load --tag rfbrowser-tests:latest --file docker/Dockerfile.tests ."
    )


@task(clean_atest, create_test_app, build)
def docker_test(c):
    c.run("mkdir atest/output")
    c.run("chmod -R 777 atest/output")
    c.run(
        """docker run\
        --rm \
        --ipc=host\
        --security-opt seccomp=docker/seccomp_profile.json \
        -v $(pwd)/atest/:/app/atest \
        -v $(pwd)/node/:/app/node/ \
        --workdir /app \
        rfbrowser-tests \
        sh -c "xvfb-run python3 -m invoke atest-robot"
        """
    )


TEST_APP_URL = "http://localhost:7272/dist/"
TEST_APP_START_TIMEOUT = 30


@task
def docker_atest(c: Context, image="tidii:latest", browser=None, suite=None):
    """Run the acceptance tests inside a Browser docker image, as CI does for a PR.

    Starts the Test App in the container, runs the tests with pabot and copies
    the results to output_docker/. The Test App must already be built in
    node/dynamic-test-app/dist, see `inv create-test-app`.

    Args:
        image: The image to test. CI builds tidii from docker/Dockerfile.dev_pr.
        browser: chromium, firefox or webkit, as for `inv atest`.
        suite: Select which suite to run.
    """
    browser_args = _browser_args(browser)
    container = f"rfbrowser-atest-{os.getpid()}"
    c.run(
        shlex.join(
            [
                "docker",
                "run",
                "--detach",
                "--name",
                container,
                "--volume",
                f"{ROOT_DIR / 'atest'}:/home/pwuser/atest",
                "--volume",
                f"{ROOT_DIR / 'node'}:/home/pwuser/node",
                image,
                "sleep",
                "infinity",
            ]
        )
    )
    try:
        _start_test_app(c, container)
        processes = int(c.run(f"docker exec {container} nproc", hide=True).stdout)
        pabot = [
            "docker",
            "exec",
            container,
            "pabot",
            "--processes",
            str(max(processes - 1, 1)),
            "--pabotlib",
            "--pabotlibport",
            "0",
            "--ordering",
            "/home/pwuser/atest/atest_order.data",
            "--artifacts",
            "png,webm,zip",
            "--artifactsinsubfolders",
            "--variable",
            "SERVER:localhost:7272",
            *browser_args,
            *(["--suite", suite] if suite else []),
            "--exclude",
            "no-docker-pr",
            "--loglevel",
            "debug",
            "--outputdir",
            "/home/pwuser/output",
            "/home/pwuser/atest/test",
        ]
        tests = c.run(shlex.join(pabot), warn=True)
        shutil.rmtree(DOCKER_OUTPUT, ignore_errors=True)
        copy = c.run(
            f"docker cp {container}:/home/pwuser/output {DOCKER_OUTPUT}", warn=True
        )
    finally:
        c.run(f"docker rm --force {container}", hide=True, warn=True)
    for step in (tests, copy):
        if step.failed:
            raise Exit(code=step.exited)


def _start_test_app(c: Context, container: str):
    c.run(
        f"docker exec --detach {container} sh -c "
        "'node /home/pwuser/node/dynamic-test-app/dist/server.js > /tmp/test-app.log 2>&1'"
    )
    for _ in range(TEST_APP_START_TIMEOUT):
        if c.run(
            f"docker exec {container} curl --fail --silent {TEST_APP_URL}",
            hide=True,
            warn=True,
        ).ok:
            return
        time.sleep(1)
    c.run(f"docker exec {container} cat /tmp/test-app.log", warn=True)
    raise Exit(f"Test App did not start in {TEST_APP_START_TIMEOUT} s.", code=1)
