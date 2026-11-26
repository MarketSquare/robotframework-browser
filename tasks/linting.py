import os
from pathlib import Path

from invoke import task
from invoke.context import Context

from tasks.shared import IN_CI


@task
def lint_python(c, fix=False):
    ruff_cmd_format = [
        "ruff",
        "format",
        "--config",
        "pyproject.toml",
        "Browser/",
        "bootstrap.py",
        "tasks/",
        "utest",
        "browser_batteries",
        ".claude/skills/",
        "tools/",
        "atest/",
    ]
    ruff_cmd_check = [
        "ruff",
        "check",
        "--config",
        "pyproject.toml",
        "Browser/",
        "browser_batteries/",
        "bootstrap.py",
        ".claude/skills/",
        "tools/",
        "atest/",
    ]
    if fix:
        ruff_cmd_check.insert(2, "--fix")
    else:
        ruff_cmd_format.insert(2, "--check")
    print(f"Run ruff format: {ruff_cmd_format}")
    c.run(" ".join(ruff_cmd_format))
    print(f"Run ruff check: {ruff_cmd_check}")
    c.run(" ".join(ruff_cmd_check))
    print("Run mypy:")
    mypy_cmd = [
        "mypy",
        "--exclude",
        ".venv",
        "--exclude",
        r"'Browser/browser\.pyi$'",
        "--config-file",
        "Browser/mypy.ini",
        "Browser/",
        "bootstrap.py",
        "browser_batteries/",
        ".claude/skills/",
        "tools/",
        "atest/library/",
    ]
    c.run(" ".join(mypy_cmd))


@task
def lint_node(c: Context):
    """Lint node files."""
    if IN_CI:
        c.run("npm run format:check")
        c.run("npm run lint:check")
    else:
        c.run("npm run format")
        c.run("npm run lint")
    c.run("npm run typecheck")


@task
def lint_robot(c):
    in_ci = os.getenv("GITHUB_WORKFLOW")
    print(f"Lint Robot files {'in ci' if in_ci else ''}")
    atest_folder = Path("atest/").resolve()
    config_file = Path("pyproject.toml").resolve()
    cmd = [
        "robocop",
        "format",
        "--config",
        str(config_file),
    ]
    if IN_CI:
        cmd.insert(2, "--check")
        cmd.insert(3, "--diff")
    atest_11_tidy_transformer = atest_folder.joinpath(
        "test", "11_tidy_transformer", "network_idle_file.robot"
    )
    atest_resrouces = list(atest_folder.joinpath("test").glob("*.resource"))
    cmd.extend(
        [
            "--exclude",
            str(atest_11_tidy_transformer),
            "--exclude",
            str(atest_resrouces[0]),
            "--exclude",
            str(atest_resrouces[1]),
            str(atest_folder),
        ]
    )
    print(cmd)
    c.run(" ".join(cmd))


@task(lint_python, lint_node, lint_robot)
def lint(c):
    pass
