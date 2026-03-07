from datetime import datetime
from typing import Optional

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from Browser import Browser


def log_all_scopes(
    exp_timeout: float,
    exp_retry_assertions_for: float,
    exp_strict_mode: bool,
    exp_selector_prefix: Optional[str] = None,
):
    b: Browser = BuiltIn().get_library_instance("Browser")
    timeout = b.scope_stack["timeout"].get()
    retry_assertions_for = b.scope_stack["retry_assertions_for"].get()
    strict_mode = b.scope_stack["strict_mode"].get()
    selector_prefix = b.scope_stack["selector_prefix"].get()

    assert timeout == exp_timeout, (
        f"timeout: {timeout} ({type(timeout)}) != {exp_timeout} ({type(exp_timeout)})"
    )
    assert retry_assertions_for == exp_retry_assertions_for, (
        f"retry_assertions_for: {retry_assertions_for} ({type(retry_assertions_for)}) != {exp_retry_assertions_for} ({type(exp_retry_assertions_for)})"
    )
    assert strict_mode == exp_strict_mode, (
        f"strict_mode: {strict_mode} ({type(strict_mode)}) != {exp_strict_mode} ({type(exp_strict_mode)})"
    )
    assert selector_prefix == exp_selector_prefix, (
        f"selector_prefix: {selector_prefix} ({type(selector_prefix)}) != {exp_selector_prefix} ({type(exp_selector_prefix)})"
    )

    logger.info(f"timeout: {timeout}")
    logger.info(f"retry_assertions_for: {retry_assertions_for}")
    logger.info(f"strict_mode: {strict_mode}")
    logger.info(f"selector_prefix: {selector_prefix}")

    return {
        "timeout": timeout,
        "retry_assertions_for": retry_assertions_for,
        "strict_mode": strict_mode,
        "selector_prefix": selector_prefix,
    }


def assert_passed_duration(start_time: datetime, max_duration_ms: int, delta_ms: int = 300) -> None:
    now = datetime.now()
    logger.info(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}, now: {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
    elapsed_ms = int((now - start_time).total_seconds() * 1000)
    logger.info(f"Elapsed time: {elapsed_ms}ms (max allowed: {max_duration_ms + delta_ms}ms)")
    if elapsed_ms >  max_duration_ms + delta_ms:
        browser = BuiltIn().get_library_instance("Browser")
        browser.take_screenshot()
        raise AssertionError(
            f"Elapsed time {elapsed_ms}ms exceeded maximum of {max_duration_ms + delta_ms}ms."
        )
