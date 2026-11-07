from types import SimpleNamespace

import pytest

from Browser.browser import Browser


@pytest.mark.parametrize(
    ("auto_delete", "status", "saved"),
    [
        (True, "PASS", False),
        (True, "FAIL", True),
        (True, "SKIP", True),
        (False, "PASS", True),
        (False, "FAIL", True),
    ],
)
def test_trace_ending_with_its_scope_is_saved_unless_passed_and_auto_deleted(
    auto_delete, status, saved
):
    library = SimpleNamespace(auto_delete_passed_tracing=auto_delete)
    assert Browser.saves_trace_at_scope_end(library, status) is saved  # type: ignore[arg-type]
