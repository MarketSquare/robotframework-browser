from tasks import LcovTotals, _drop_never_loaded_records, _lcov_totals

LOADED = """TN:
SF:node/playwright-wrapper/cookie.ts
DA:1,1
DA:2,0
LF:2
LH:1
end_of_record
"""

NEVER_LOADED = """TN:
SF:node/playwright-wrapper/grpc-service.ts
DA:1,0
DA:2,0
LF:2
LH:0
end_of_record
"""


def test_records_with_no_line_hit_are_dropped():
    assert _drop_never_loaded_records(NEVER_LOADED + LOADED) == LOADED


WITH_BRANCHES = """SF:Browser/browser.py
DA:1,1
LF:10
LH:7
BRDA:3,0,0,1
BRF:4
BRH:1
end_of_record
"""


def test_totals_sum_lines_and_branches_over_records():
    assert _lcov_totals(LOADED + WITH_BRANCHES) == LcovTotals(
        lines_hit=8, lines_found=12, branches_hit=1, branches_found=4
    )
