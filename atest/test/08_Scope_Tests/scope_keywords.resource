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
    Waiter Page Set Delay    ${high}
    Select Options By    \#dropdown    text    hidden
    Click With Options    \#submit    noWaitAfter=True
    Run Keyword And Expect Error    *    Wait For Condition    Element States    id=victim    contains    hidden
    Wait For Condition    Element States    id=victim    contains    hidden    timeout=${high} ms

    Waiter Page Set Delay    ${low}
    Select Options By    \#dropdown    text    readonly
    Click With Options    \#submit    noWaitAfter=True
    Wait For Condition    Element States    id=victim    contains    readonly
    Wait For Condition    Element States    id=victim    contains    readonly    timeout=${high} ms

Assertion Retry Should Be Between
    [Arguments]    ${low}    ${high}
    Waiter Page Set Delay    ${high}
    Select Options By    \#dropdown    text    readonly
    Click With Options    \#submit    noWaitAfter=True
    Run Keyword And Expect Error    *    Get Element States    id=victim    contains    readonly
    Wait For Condition    Element States    id=victim    contains    readonly    timeout=${high} ms

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
    Click    id=setdelay
    Take Screenshot    EMBED
