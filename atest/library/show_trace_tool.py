import subprocess
import time
from pathlib import Path

import psutil
from psutil import NoSuchProcess
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


def run_rfbrowser_help():
    exec_dir = BuiltIn().get_variable_value("${EXECDIR}")
    ouput_dir = BuiltIn().get_variable_value("${OUTPUT_DIR}")
    out_file = Path(ouput_dir, "rfbrower_2.log")
    with open(out_file, "w") as file:
        process = subprocess.Popen(
            ["rfbrowser", "show-trace", "--help"],
            cwd=exec_dir,
            stderr=subprocess.STDOUT,
            stdout=file,
            shell=True,
        )
    time.sleep(2)
    help_text = out_file.read_text()
    logger.info(help_text)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        raise
    return help_text


def start_show_trace(zip_file: str):
    zip_file = Path(zip_file).resolve(strict=True)
    exec_dir = BuiltIn().get_variable_value("${EXECDIR}")
    ouput_dir = BuiltIn().get_variable_value("${OUTPUT_DIR}")
    out_file = Path(ouput_dir, "rfbrower_1.log")
    with open(out_file, "w") as file:
        process = subprocess.Popen(
            ["rfbrowser", "show-trace", "-F", str(zip_file)],
            cwd=exec_dir,
            stderr=subprocess.STDOUT,
            stdout=file,
            shell=True,
        )
    logger.info("Give process time to start")
    time.sleep(3)
    logger.info(f"Trace viewer output: {out_file.read_text()}")
    assert process.returncode is None, (
        "Process should be still running, but it was not."
    )
    return process, out_file


def _check_trace_process(process: subprocess.Popen, out_file: Path):
    pid = process.pid
    try:
        psutil.pid_exists(pid)
    except NoSuchProcess:
        logger.info(process.stdout)
        raise
    proc = psutil.Process(pid)
    binary = False
    show_trace = False
    file_arg = False
    trace_zip = False
    for cmd in proc.cmdline():
        logger.info(f"cmd: {cmd}")
        if "rfbrowser" in cmd:
            binary = True
        if "show-trace" in cmd:
            show_trace = True
        if "-F" in cmd:
            file_arg = True
        if "trace_1.zip" in cmd:
            trace_zip = True
    if binary and show_trace and file_arg and trace_zip:
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


def check_trace_process(prcess: subprocess.Popen, out_file: Path):
    end_time = time.monotonic() + 60
    while end_time > time.monotonic():
        if _check_trace_process(prcess, out_file):
            return True
        logger.info("Sleep 1s and retry.")
        logger.info(f"Trace file output: {out_file.read_text()}")
        time.sleep(1)
    raise ValueError("No valid trace process found")
