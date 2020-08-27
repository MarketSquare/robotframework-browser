*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}
Test Teardown     Close Page

*** Test Cases ***
Dismiss Alert
    Click    \#alerts
    Handle Dialog    action=dismiss

Accept Alert
    Click    \#alerts
    Handle Dialog    action=accept

Clicking Through Alert Fails
    Run Keyword And Expect Error    Could not find element with selector `#alerts` within timeout.    Click    \#alerts

Promptinput works
    Handle Future Dialogs    action=accept    prompt_input=Some Input String
    Click    \#prompts
    Get Text    \#prompt_result    ==    Some Input String

Dismiss and Promptinput Fails
    Run Keyword And Expect Error    prompt_input is only valid if action is 'accept'    Handle Future Dialogs    action=dismiss    prompt_input=Some Prompt Input

Handle Future Dialogs handles many dialogs
    Handle Future Dialogs    accept
    New Page    ${LOGIN_URL}
    Click    \#alerts
    Get Dialog    ==    None
    New Context
    New Page    ${LOGIN_URL}
    Click    \#alerts
    Get Dialog    ==    None
    Fail

Get Dialog asserts content
    Get Dialog
    Fail
