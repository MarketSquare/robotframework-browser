# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import contextlib
import os
import re
import subprocess
import sys
from pathlib import Path

import seedir  # type: ignore

from .constant import (
    INSTALLATION_DIR,
    IS_TERMINAL,
    PLAYWRIGHT_BROWSERS_PATH,
    SHELL,
    log,
    write_marker,
)

try:
    import pty

    has_pty = True
except ImportError:
    has_pty = False

ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", flags=re.IGNORECASE)
PROGRESS_MATCHER = re.compile(
    r"(?P<size>\d+(?:\.\d+)*\s\w*B)\s\[\]\s(?P<percent>\d+)(?P<time>%\s.+)"
)
PROGRESS_SIZE = 50


def _walk_install_dir():
    def mask(x: Path) -> bool:  # noqa: PLR0911
        if "index.js" in x.parts:
            return True
        if "package-lock.json" in x.parts:
            return True
        if "package.json" in x.parts:
            return True
        if "node_modules" in x.parts[-1]:
            return True
        if "playwright" in x.parts:
            return True
        if "playwright-core" in x.parts:
            return True
        return "monocart-coverage-reports" in x.parts

    return seedir.seedir(
        INSTALLATION_DIR,
        indent=4,
        mask=mask,
        beyond="content",
        depthlimit=4,
        itemlimit=(None, 5),
    )


def log_install_dir(error_msg=True):
    if error_msg:
        log(
            f"Installation directory `{INSTALLATION_DIR!s}` does not contain the required files for "
            "unknown reason. Investigate the npm output and fix possible problems."
            "\nPrinting contents:\n"
        )
    log(f"\n{_walk_install_dir()}")
    write_marker()


def format_progress_bar(message: str) -> tuple[str, str]:
    progress_match = PROGRESS_MATCHER.search(message)
    if progress_match:
        size = progress_match.group("size")
        percent = progress_match.group("percent")
        time = progress_match.group("time")
        with contextlib.suppress(Exception):
            file_msg = ANSI_ESCAPE.sub(
                "",
                (
                    f"total: {size}, progress: {percent}{time}"
                    if int(percent) % 20 == 0
                    else ""
                ),
            )
            bar = "=" * (int(percent) // (100 // PROGRESS_SIZE))
            message = message.replace(
                " [] ", f" [{bar}{' ' * (PROGRESS_SIZE - len(bar))}] ", 1
            )
    else:
        file_msg = ANSI_ESCAPE.sub("", message)
    return message, file_msg


def _log_progress_update(last_file_msg, message):
    try:
        message, file_msg = format_progress_bar(message)
        if IS_TERMINAL:
            print(message, end="", flush=True)  # noqa: T201
        if file_msg.strip() and last_file_msg.split("%")[0] != file_msg.split("%")[0]:
            log(file_msg.strip("\n"))
            return file_msg
        return last_file_msg
    except Exception as error:
        log(f"Could not log line, suppress error {error}")


def _unix_process_executor_with_bar(command, cwd=None, silent_mode=False):
    if not has_pty:
        return
    master_fd, slave_fd = pty.openpty()
    process = subprocess.Popen(
        command,
        shell=True,
        cwd=cwd,
        stdout=slave_fd,
        stderr=slave_fd,
        stdin=subprocess.PIPE,
        close_fds=True,
    )
    os.close(slave_fd)
    last_file_msg = ""

    while True:
        try:
            output = os.read(master_fd, 1024)
            if not output:  # End of output
                break
            if silent_mode:
                continue
            with contextlib.suppress(UnicodeDecodeError):
                message = output.decode("utf-8", errors="backslashreplace")
            if os.name == "nt":
                message = re.sub(r"[^\x00-\x7f]", r" ", message)
            last_file_msg = _log_progress_update(last_file_msg, message)
        except OSError:
            break
    os.close(master_fd)
    process.wait()

    if process.returncode != 0:
        raise RuntimeError(
            f"Problem installing node dependencies. "
            f"Process returned with exit status {process.returncode}"
        )


def _check_files_and_access():
    if not (INSTALLATION_DIR / "package.json").is_file():
        log(
            f"Installation directory `{INSTALLATION_DIR}` does not contain the required package.json "
            "\nPrinting contents:\n"
        )
        log(f"\n{_walk_install_dir()}")
        raise RuntimeError("Could not find robotframework-browser's package.json")
    if not os.access(INSTALLATION_DIR, os.W_OK):
        sys.tracebacklimit = 0
        raise RuntimeError(
            f"`rfbrowser init` needs write permissions to {INSTALLATION_DIR}"
        )


def _check_npm():
    try:
        subprocess.run(
            ["npm", "-v"], stdout=subprocess.DEVNULL, check=True, shell=SHELL
        )
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        PermissionError,
    ) as exception:
        log(
            "Couldn't execute npm. Please ensure you have node.js and npm installed and in PATH."
            "See https://nodejs.org/ for documentation"
        )
        raise exception


def _process_poller(process: subprocess.Popen, silent_mode: bool):
    while process.poll() is None:
        if process.stdout:
            output = process.stdout.readline().decode("UTF-8")
            log(output, silent_mode)

    if process.returncode != 0:
        raise RuntimeError(
            "Problem installing node dependencies."
            f"Node process returned with exit status {process.returncode}"
        )


def rfbrowser_init(
    skip_browser_install: bool, silent_mode: bool, with_deps: bool, browser: list
):
    log("Installing node dependencies...", silent_mode)
    _check_files_and_access()
    _check_npm()
    log(f"Installing rfbrowser node dependencies at {INSTALLATION_DIR}", silent_mode)
    if skip_browser_install:
        os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
    elif not os.environ.get(PLAYWRIGHT_BROWSERS_PATH):
        os.environ[PLAYWRIGHT_BROWSERS_PATH] = "0"

    process = subprocess.Popen(
        "npm ci --production --parseable true --progress false",
        shell=True,
        cwd=INSTALLATION_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    _process_poller(process, silent_mode)

    if not skip_browser_install:
        cmd = "npx --quiet playwright install"
        browser_as_str = " ".join(browser)
        if browser_as_str:
            browser_as_str = f"{browser_as_str} "
            cmd = f"{cmd} {browser_as_str}"
        if with_deps:
            cmd = f"{cmd.strip(' ')} --with-deps"

        pw_browser_path = os.environ.get(PLAYWRIGHT_BROWSERS_PATH)
        with contextlib.suppress(ValueError):
            pw_browser_path = int(pw_browser_path)  # type: ignore
        install_dir = pw_browser_path if pw_browser_path else INSTALLATION_DIR
        log(
            f"Installing browser {browser_as_str}binaries to {install_dir}",
            silent_mode,
        )
        log(cmd, silent_mode)
        if has_pty:
            _unix_process_executor_with_bar(
                cmd,
                cwd=INSTALLATION_DIR,
                silent_mode=silent_mode,
            )
        else:
            process = subprocess.Popen(
                cmd,
                shell=True,
                cwd=INSTALLATION_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            _process_poller(process, silent_mode)
    log("rfbrowser init completed", silent_mode)
