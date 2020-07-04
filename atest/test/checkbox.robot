*** Settings ***
Resource          keywords.resource
Test Setup        Open Browser    ${FORM_URL}
Test Teardown     Close Browser

*** Test Cases ***
Checkbox Should Be Checked
    Get Checkbox State    css=[name=can_send_email]    ==    checked

Checkbox Should Not Be Checked
    Get Checkbox State    css=[name=can_send_sms]    ==     UnChecked

Check Checkbox
    ${state}=    Get Checkbox State    css=[name=can_send_sms]    ==    off
    Should Not Be True    ${state}
    Check Checkbox    css=[name=can_send_sms]
    ${state}=    Get Checkbox State    css=[name=can_send_sms]    ==    on
    Should Be True    ${state}

Uncheck Checkbox
    Get Checkbox State    css=[name=can_send_email]    ==    ${True}
    Uncheck Checkbox    css=[name=can_send_email]
    Get Checkbox State    css=[name=can_send_email]    ==    ${False}
