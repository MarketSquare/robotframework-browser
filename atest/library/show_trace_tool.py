"""Helpers for checking the ``rfbrowser show-trace`` command.

These used to pass a list to ``subprocess.Popen`` together with ``shell=True``.
On POSIX that runs ``/bin/sh -c <first element>`` and drops every remaining
argument, so ``rfbrowser`` was started with no arguments at all: the help check
asserted against the top level command group rather than ``show-trace``, and no
trace viewer was ever started. The processes are now started without a shell so
the arguments reach the command.
"""

import contextlib
import subprocess
import time
from pathlib import Path

import psutil
from os_wrapper import get_enty_command_list
from psutil import NoSuchProcess
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

HELP_TIMEOUT = 30
VIEWER_START_DELAY = 3
VIEWER_WAIT = 60
VIEWER_STOP_TIMEOUT = 10

# The viewer is a long running process started outside Robot Framework's Process
# library, so `Terminate All Processes` does not know about it. Every started
# viewer is tracked here so `Stop Show Trace` can end it even when the test that
# started it failed before it got a handle back.
_started_viewers: list[subprocess.Popen] = []


def run_rfbrowser_show_trace_help() -> str:
    """Return the output of ``rfbrowser show-trace --help``."""
    exec_dir = BuiltIn().get_variable_value("${EXECDIR}")
    command = [*get_enty_command_list(), "show-trace", "--help"]
    logger.info(f"Running: {command}")
    process = subprocess.run(
        command,
        cwd=exec_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=HELP_TIMEOUT,
        check=False,
        text=True,
    )
    logger.info(process.stdout)
    if process.returncode != 0:
        raise AssertionError(
            f"show-trace --help exited with {process.returncode}:\n{process.stdout}"
        )
    return process.stdout


def start_show_trace(zip_file: str) -> tuple[subprocess.Popen, Path]:
    zip_file = Path(zip_file).resolve(strict=True)
    exec_dir = BuiltIn().get_variable_value("${EXECDIR}")
    ouput_dir = BuiltIn().get_variable_value("${OUTPUT_DIR}")
    out_file = Path(ouput_dir, "rfbrower_1.log")
    # The trace file is a positional argument. An earlier version of this helper
    # passed it as "-F", which show-trace has no such option for -- it never
    # surfaced because the shell=True bug meant the arguments were dropped anyway.
    command = [*get_enty_command_list(), "show-trace", str(zip_file)]
    logger.info(f"Running: {command}")
    with open(out_file, "w") as file:
        process = subprocess.Popen(
            command,
            cwd=exec_dir,
            stderr=subprocess.STDOUT,
            stdout=file,
        )
    _started_viewers.append(process)
    logger.info("Give process time to start")
    time.sleep(VIEWER_START_DELAY)
    logger.info(f"Trace viewer output: {out_file.read_text()}")
    if process.poll() is not None:
        raise AssertionError(
            f"show-trace exited with {process.returncode} instead of staying up:\n"
            f"{out_file.read_text()}"
        )
    return process, out_file


def stop_show_trace() -> None:
    """Terminate every trace viewer started in this suite, and its children.

    The viewer spawns npm, node and a chromium browser. Killing only the process
    that `Start Show Trace` returned leaves those running and reparented to init,
    so the whole tree is taken down.
    """
    while _started_viewers:
        parent = _started_viewers.pop()
        try:
            handle = psutil.Process(parent.pid)
        except NoSuchProcess:
            continue
        processes = handle.children(recursive=True)
        processes.append(handle)
        logger.info(f"Stopping trace viewer tree: {[p.pid for p in processes]}")
        for process in processes:
            with contextlib.suppress(NoSuchProcess):
                process.terminate()
        _, alive = psutil.wait_procs(processes, timeout=VIEWER_STOP_TIMEOUT)
        for process in alive:
            with contextlib.suppress(NoSuchProcess):
                process.kill()


def _check_trace_process(process: subprocess.Popen, out_file: Path) -> bool:
    pid = process.pid
    try:
        psutil.pid_exists(pid)
    except NoSuchProcess:
        logger.info(process.stdout)
        raise
    proc = psutil.Process(pid)
    binary = False
    show_trace = False
    trace_zip = False
    for cmd in proc.cmdline():
        logger.info(f"cmd: {cmd}")
        if "rfbrowser" in cmd or "Browser.entry" in cmd:
            binary = True
        if "show-trace" in cmd:
            show_trace = True
        if "trace_1.zip" in cmd:
            trace_zip = True
    if binary and show_trace and trace_zip:
        logger.info("Main process found, check child process")
        node = False
        chromium = False
        for child_proc in proc.children(recursive=True):
            logger.info(child_proc)
            if not child_proc.is_running():
                logger.info(f"Trace file output: {out_file.read_text()}")
            if "node" in child_proc.name().lower():
                logger.info(child_proc.name())
                node = True
            if (
                "chromium" in child_proc.name().lower()
                or "chrome" in child_proc.name().lower()
            ):
                logger.info(child_proc.name())
                chromium = True
        if chromium and node:
            logger.info("Child process found")
            return True
        logger.info("No children")
        return False
    logger.info("Not process found")
    return False


def check_trace_process(process: subprocess.Popen, out_file: Path) -> bool:
    end_time = time.monotonic() + VIEWER_WAIT
    while end_time > time.monotonic():
        if _check_trace_process(process, out_file):
            return True
        logger.info("Sleep 1s and retry.")
        logger.info(f"Trace file output: {out_file.read_text()}")
        time.sleep(1)
    raise ValueError("No valid trace process found")
