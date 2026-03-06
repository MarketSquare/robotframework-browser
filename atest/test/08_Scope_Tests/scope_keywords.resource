*** Settings ***
Resource    ../keywords.resource
Library     scope_logger.py

*** Variables ***
${SERVER_URL} =         http://${SERVER}/
${FRAME_URL} =          framing.html?url=
${IFRAME_PREFIX} =      id=iframe_id >>>
${WAIT_URL_FRAMED} =    ${SERVER_URL}${FRAME_URL}waitfor.html
${WAIT_URL_DIRECT} =    ${SERVER_URL}waitfor.html

*** Keywords ***
Timeout Should Be Between
    [Arguments]    ${low}    ${high}
    # Add 2000 ms buffer to avoid a race condition on slow CI: if the gRPC/RF overhead between
    # "Click With Options #submit" and "Wait For Condition" exceeds (${high} - global_timeout),
    # the condition may already be met when the wait starts, causing a false pass.
    ${fail_delay} =    Evaluate    ${high} + 2000
    Waiter Page Set Delay    ${fail_delay}
    Select Options By    \#dropdown    text    hidden
    Click With Options    \#submit    noWaitAfter=True
    Run Keyword And Expect Error    *    Wait For Condition    Element States    id=victim    contains    hidden
    Wait For Condition    Element States    id=victim    contains    hidden    timeout=${fail_delay} ms

    Waiter Page Set Delay    ${low}
    Select Options By    \#dropdown    text    readonly
    Click With Options    \#submit    noWaitAfter=True
    Wait For Condition    Element States    id=victim    contains    readonly
    Wait For Condition    Element States    id=victim    contains    readonly    timeout=${high} ms

Assertion Retry Should Be Between
    [Arguments]    ${low}    ${high}
    # Add 2000 ms buffer to avoid a race condition on slow CI: if the gRPC/RF overhead between
    # "Click With Options #submit" and "Get Element States" exceeds (${high} - retry_assertions_for),
    # the condition may already be met when the assertion starts, causing a false pass.
    ${fail_delay} =    Evaluate    ${high} + 2000
    Waiter Page Set Delay    ${fail_delay}
    Select Options By    \#dropdown    text    readonly
    Click With Options    \#submit    noWaitAfter=True
    Run Keyword And Expect Error    *    Get Element States    id=victim    contains    readonly
    Wait For Condition    Element States    id=victim    contains    readonly    timeout=${fail_delay} ms

    Waiter Page Set Delay    ${low}
    Select Options By    \#dropdown    text    hidden
    Click With Options    \#submit    noWaitAfter=True
    Get Element States    id=victim    contains    hidden
    Wait For Condition    Element States    id=victim    contains    hidden    timeout=${high} ms

Strict Mode Should Be
    [Arguments]    ${status}
    IF    ${status}
        Run Keyword And Expect Error    *strict mode violation*    Get Text    input
    ELSE
        Get Text    input
    END

Waiter Page Set Delay
    [Arguments]    ${delay}
    Fill Text    id=delay-setting    ${delay}
    # Use Evaluate JavaScript instead of Click to avoid Playwright actionability-check timeouts
    # (visible, stable, scroll-into-view) that can exceed the global browser timeout, especially
    # when operating inside an iframe on slow CI runners.
    Evaluate JavaScript    id=delay-setting    (el) => el.ownerDocument.defaultView.setDelay()
    Take Screenshot    EMBED
