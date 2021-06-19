import subprocess
import time
from pathlib import Path

import psutil
from psutil import NoSuchProcess
from robot.libraries.BuiltIn import BuiltIn


def start_show_trace(zip_file: str):
    zip_file = Path(zip_file).resolve(strict=True)
    exec_dir = BuiltIn().get_variable_value("${EXECDIR}")
    ouput_dir = BuiltIn().get_variable_value("${OUTPUT_DIR}")
    out_file = Path(ouput_dir, "rfbrower.log")
    with open(out_file, "w") as file:
        process = subprocess.Popen(
            ["rfbrowser", "show-trace", "-F", str(zip_file)],
            cwd=exec_dir,
            stderr=subprocess.STDOUT,
            stdout=file,
            shell=True
        )
    print("Give process time to start")
    time.sleep(3)
    print(out_file.read_text())
    return process


def _check_trace_process(process: subprocess.Popen):
    pid = process.pid
    try:
        psutil.pid_exists(pid)
    except NoSuchProcess:
        print(process.stdout)
        raise 
    proc = psutil.Process(pid)
    binary = False
    show_trace = False
    file_arg = False
    trace_zip = False
    for cmd in proc.cmdline():
        print(f"cmd: {cmd}")
        if "rfbrowser" in cmd:
            binary = True
        if "show-trace" in cmd:
            show_trace = True
        if "-F" in cmd:
            file_arg = True
        if "trace_1.zip" in cmd:
            trace_zip = True
    if binary and show_trace and file_arg and trace_zip:
        print("Main process found")
        print("Check child process")
        node = False
        chromium = False
        for child_proc in proc.children(recursive=True):
            if child_proc.name().lower() == "node":
                print(child_proc.name())
                node = True
            if child_proc.name().lower() == "chromium":
                print(child_proc.name())
                chromium = True
        if chromium and node:
            print("Child process found")
            return True
        else:
            print("No children")
            return False
    else:
        print("Not process found")
        return False


def check_trace_process(prcess: subprocess.Popen):
    end_time = time.monotonic() + 30
    while end_time > time.monotonic():
        if _check_trace_process(prcess):
            return True
    raise ValueError("No valid trace process found")

