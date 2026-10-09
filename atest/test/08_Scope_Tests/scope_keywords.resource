*** Settings ***
Resource    ../keywords.resource
Library     scope_logger.py

*** Variables ***
${SERVER_URL} =            http://${SERVER}/
${FRAME_URL} =             framing.html?url=
${IFRAME_PREFIX} =         id=iframe_id >>>
${WAIT_URL_FRAMED} =       ${SERVER_URL}${FRAME_URL}waitfor.html
${WAIT_URL_DIRECT} =       ${SERVER_URL}waitfor.html
${FRAME_LOAD_TIMEOUT} =    10 s

*** Keywords ***
Timeout Should Be
    [Documentation]    Reads the effective browser timeout out of Playwright's own error,
    ...    which names the timeout it used: `Timeout 1000ms exceeded`. That is an exact
    ...    readout rather than a duration to infer a value from, so a stalled CI runner
    ...    cannot change the answer.
    [Arguments]    ${expected_ms}
    Run Keyword And Expect Error
    ...    *Timeout ${expected_ms}ms exceeded*
    ...    Click    id=not_here

Assertion Retry Should Be
    [Documentation]    Asserts the assertion retry budget was honoured, as a lower bound.
    ...    Nothing in the failure names the retry budget the way Playwright names its
    ...    timeout, so a duration is the only reading available - see
    ...    https://github.com/MarketSquare/robotframework-browser/issues/5223. A lower
    ...    bound is the only stall-proof way to take it: the polling loop gives up only
    ...    once the budget is spent, so a loaded runner makes this longer, never shorter.
    ...    Assumes the retry budget is not larger than the browser timeout, which would
    ...    end the loop early.
    [Arguments]    ${expected_ms}
    ${start_time} =    Get Current Date
    Run Keyword And Expect Error    *    Get Element States    id=not_here    contains    readonly
    Assert Retried For At Least    ${start_time}    ${expected_ms}

Strict Mode Should Be
    [Arguments]    ${status}
    IF    ${status}
        Run Keyword And Expect Error    *strict mode violation*    Get Text    input
    ELSE
        Get Text    input
    END

Wait For Framed Page
    [Documentation]    Waits for the iframe's own document. framing.html sets the iframe
    ...    src from a script, so the outer page's load event does not reliably cover the
    ...    frame. Without this a slow frame is indistinguishable from a scope setting that
    ...    did not apply, because both surface as a timeout on the very next keyword.
    ...    The selector is prefix-muted so it reads the same whether or not a selector
    ...    prefix is in scope.
    Wait For Elements State
    ...    !prefix ${IFRAME_PREFIX} id=setdelay
    ...    attached
    ...    ${FRAME_LOAD_TIMEOUT}

Open Framed Page
    [Documentation]    Navigates to the framed page under a timeout of its own, so the
    ...    scope setting under test never governs the navigation.
    Go To    ${WAIT_URL_FRAMED}    timeout=${FRAME_LOAD_TIMEOUT}
    Wait For Framed Page

Ensure Open Framed Page
    Ensure Open Page    ${WAIT_URL_FRAMED}
    Wait For Framed Page
