*** Settings ***
Resource    ../keywords.resource


*** Keywords ***
Timeout Should Be Between
    [Arguments]    ${low}    ${high}
    Waiter Page Set Delay    ${high}
    Select Options By    \#dropdown    text    hidden
    Click    \#submit    noWaitAfter=True
    Run Keyword And Expect Error    *    Wait for Condition    Element States    id=victim    contains    hidden
    Wait For Condition     Element States    id=victim    contains    hidden    timeout=${high} ms

    Waiter Page Set Delay    ${low}
    Select Options By    \#dropdown    text    readonly
    Click    \#submit    noWaitAfter=True
    Wait for Condition    Element States    id=victim    contains    readonly
    Wait For Condition     Element States    id=victim    contains    readonly    timeout=${high} ms

Assertion Retry Should Be Between
    [Arguments]    ${low}    ${high}
    Waiter Page Set Delay    ${high}
    Select Options By    \#dropdown    text    readonly
    Click    \#submit    noWaitAfter=True
    Run Keyword And Expect Error    *    Get Element States    id=victim    contains    readonly
    Wait For Condition     Element States    id=victim    contains    readonly    timeout=${high} ms

    Waiter Page Set Delay    ${low}
    Select Options By    \#dropdown    text    hidden
    Click    \#submit    noWaitAfter=True
    Get Element States    id=victim    contains    hidden
    Wait For Condition     Element States    id=victim    contains    hidden    timeout=${high} ms

Strict Mode should be
    [Arguments]    ${status}
    IF    ${status}
        Run Keyword And Expect Error    *    Get Text    input
    ELSE
        Get Text    input
    END

Waiter Page Set Delay
    [Arguments]    ${delay}
    Fill Text    id=delay-setting    ${delay}
    Click    id=setdelay
    Take Screenshot    EMBED
