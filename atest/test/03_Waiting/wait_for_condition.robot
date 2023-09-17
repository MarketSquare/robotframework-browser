*** Settings ***
Resource        imports.resource

Suite Setup     Wait For Condition Suite Setup
Test Setup      Wait For Condition Test Setup

*** Test Cases ***
Condition Should Succeed
    Select Options By    \#dropdown    value    attached
    Click With Options    \#submit    noWaitAfter=True
    Wait For Condition    Text    \#victim    ==    victim

Condition Should Fail
    Select Options By    \#dropdown    value    attached
    Click With Options    \#submit    noWaitAfter=True
    Run Keyword And Expect Error
    ...    Text 'victim' (str) should be 'not correct' (str)
    ...    Wait For Condition    Text    \#victim    ==    not correct

Condition Should Fail With Custom Message
    Select Options By    \#dropdown    value    attached
    Click With Options    \#submit    noWaitAfter=True
    Run Keyword And Expect Error
    ...    FooBar
    ...    Wait For Condition    Text    \#victim    ==    not correct    message=FooBar

Condition Should Fail With Timeout
    Select Options By    \#dropdown    value    attached
    Click With Options    \#submit    noWaitAfter=True
    Run Keyword And Expect Error
    ...    Text 'victim' (str) should be 'not correct' (str)
    ...    Wait For Condition    Text    \#victim    ==    not correct    timeout=500ms

Keyword With Same Name Should Not Fail
    [Documentation]    same_keyword.py library also contains Get Title keyword
    Set Library Search Order
    Wait For Condition    Title    ==    ${EMPTY}

Keyword With Same Name Should Not Fail Even With Library Search Order
    [Documentation]    same_keyword.py library also contains Get Title keyword
    Set Library Search Order    same_keyword
    Wait For Condition    Title    ==    ${EMPTY}
    [Teardown]    Set Library Search Order    Browser

Wait For Condition Honors Timeout If It Exceeds Browser Timeout
    Fill Text    \#delay-setting    2000
    Click    \#setdelay
    Select Options By    \#dropdown    value    visible
    Set Browser Timeout    500 ms    Test
    Click With Options    id=submit    noWaitAfter=True
    Wait For Condition    element_states    id=victim    contains    visible    timeout=4 sec

*** Keywords ***
Wait For Condition Test Setup
    New Page    ${WAIT_URL}
    Fill Text    \#delay-setting    700
    Click    \#setdelay

Wait For Condition Suite Setup
    Import Library    ${CURDIR}/../../library/same_keyword.py
