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
    timeout = b.timeout
    retry_assertions_for = b.retry_assertions_for
    strict_mode = b.strict_mode
    selector_prefix = b.selector_prefix

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


def assert_retried_for_at_least(start_time: datetime, min_duration_ms: int) -> None:
    """Asserts an assertion keyword kept retrying for at least its budget.

    A lower bound, deliberately. `with_assertion_polling` gives up only once the
    retry budget (or the browser timeout) is spent, so a loaded CI runner can
    make this longer but never shorter - which an upper bound cannot survive.
    """
    elapsed_ms = int((datetime.now() - start_time).total_seconds() * 1000)
    logger.info(f"Retried for {elapsed_ms}ms (at least {min_duration_ms}ms expected)")
    if elapsed_ms < min_duration_ms:
        raise AssertionError(
            f"Retried for {elapsed_ms}ms, which is less than the "
            f"{min_duration_ms}ms budget the scope should have given it."
        )
