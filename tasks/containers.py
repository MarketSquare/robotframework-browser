from invoke import task
from invoke.context import Context

from tasks.building import build, create_test_app
from tasks.shared import ROOT_DIR
from tasks.testing import clean_atest


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


@task
def docker_copy_output(c: Context):
    """Copy atest output from docker container to host."""
    output = ROOT_DIR / "docker_last_container.txt"
    output.unlink(missing_ok=True)
    c.run(f"docker ps --all --last 1 --format '{{{{.ID}}}}' > {output}")
    with output.open("r") as file:
        container_id = file.read().strip()
    c.run(f"docker cp {container_id}:/home/pwuser/output ./output_docker")
