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
    ${start_time} =    Get Current Date
    Run Keyword And Expect Error    *    Wait For Condition    Element States    id=not_here    contains    hidden
    Assert Passed Duration    ${start_time}    ${high}
    ${start_time} =    Get Current Date
    Wait For Condition    Element States    id=setdelay    contains    visible    timeout=${high} ms
    Assert Passed Duration    ${start_time}    ${high}
    ${start_time} =    Get Current Date
    Wait For Condition    Element States    id=setdelay    contains    visible
    Assert Passed Duration    ${start_time}    ${low}
    ${start_time} =    Get Current Date
    Wait For Condition    Element States    id=setdelay    contains    visible    timeout=${high} ms
    Assert Passed Duration    ${start_time}    ${high}

Assertion Retry Should Be Between
    [Arguments]    ${low}    ${high}
    ${start_time} =    Get Current Date
    Run Keyword And Expect Error    *    Get Element States    id=not_here    contains    readonly
    Assert Passed Duration    ${start_time}    ${high}
    ${start_time} =    Get Current Date
    Wait For Condition    Element States    id=setdelay    contains    visible    timeout=${high} ms
    Assert Passed Duration    ${start_time}    ${high}

    ${start_time} =    Get Current Date
    Get Element States    id=setdelay    contains    visible
    Assert Passed Duration    ${start_time}    ${low}
    ${start_time} =    Get Current Date
    Wait For Condition    Element States    id=setdelay    contains    visible    timeout=${high} ms
    Assert Passed Duration    ${start_time}    ${high}

Strict Mode Should Be
    [Arguments]    ${status}
    IF    ${status}
        Run Keyword And Expect Error    *strict mode violation*    Get Text    input
    ELSE
        Get Text    input
    END
