*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${WAIT_URL}

*** Test Cases ***
Promise To With Type Conversion
    ${promise} =    Promise To    Click    id=victim    button=left
    Select Options By    id=dropdown    value    True    enabled
    Click With Options    id=submit    noWaitAfter=True
    Wait For    ${promise}

Promise To Convert Type
    ${promise} =    Promise To    Click With Options    id=clickWithOptions    left    clickCount=4    delay=200 ms
    Go To    ${LOGIN_URL}
    Wait For    ${promise}
    Get Text    id=click_count    ==    4
    Get Text    id=mouse_delay_time    validate    int(value) > 100 and int(value) < 300
    Get Text    id=mouse_button    ==    left

Could Not Find Keyword W Promise To
    [Setup]    NONE
    TRY
        Promise To    Could Not Find Keyword
    EXCEPT    ValueError: Unknown keyword 'Could Not Find Keyword'! 'Promise To' can only be used with Browser keywords.    AS    ${e}
        Log    ${e}
    ELSE
        FAIL    Should have failed
    END

Promise To With *args
    ${promise} =    Promise To
    ...    Click With Options
    ...    id=clickWithOptions
    ...    left
    ...    SHIFT
    ...    ALT
    ...    clickCount=4
    ...    delay=200 ms
    Go To    ${LOGIN_URL}
    Wait For    ${promise}
    Get Text    id=click_count    ==    4
    Get Text    id=mouse_delay_time    validate    int(value) > 100 and int(value) < 300
    Get Text    id=mouse_button    ==    left
    Get Text    id=shift_key    ==    true
    Get Text    id=alt_key    ==    true
