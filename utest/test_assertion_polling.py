import itertools
import time

from assertionengine import AssertionOperator

from Browser.assertion_engine import with_assertion_polling


class FailsTwiceThenPasses:
    timeout = 10_000
    retry_assertions_for = 5_000

    def __init__(self):
        self.calls = 0

    @with_assertion_polling
    def get_text(self, assertion_operator: AssertionOperator | None = None):
        self.calls += 1
        if self.calls < 3:  # noqa: PLR2004
            raise AssertionError("not yet")
        return "done"


def test_retries_continue_when_wall_clock_jumps_forward(monkeypatch):
    wall_clock = itertools.count(time.time(), 3600)
    monkeypatch.setattr(time, "time", lambda: next(wall_clock))
    keyword = FailsTwiceThenPasses()

    assert keyword.get_text(AssertionOperator["=="]) == "done"
    assert keyword.calls == 3  # noqa: PLR2004
