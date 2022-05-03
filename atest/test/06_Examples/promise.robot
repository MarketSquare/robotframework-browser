*** Settings ***
Library     Browser    timeout=5s    retry_assertions_for=3s
Resource    imports.resource

*** Test Cases ***
Issue 1685
    New Page    url=http://www.google.com
    ${promise} =    Promise To    Wait For Response    timeout=2s
    Wait For    ${promise}

Attempt Login With Empty Username And Password
    New Page      https://automation01.emrlab.ca/auth/login.do
    Wait For Elements State    [name*="username"]
    Test to check alert    id=LoginButton    ACCEPT    A username is required.

*** Keywords ***
Test to check alert
    [Arguments]    ${locator}    ${action}    ${text}
    ${promise}    promise to    wait for alert    action=${action}    text=${text}
    click    ${locator}
    wait for    ${promise}    # this is where it fails with  'str' object has no attribute 'name'