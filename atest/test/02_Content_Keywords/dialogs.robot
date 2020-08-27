*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}
Test Teardown     Close Page

*** Test Cases ***
Dismiss Future Alert
    Handle Future Dialogs    action=dismiss
    Click    selector=\#alerts

Accept Future Alert
    Handle Future Dialogs    action=accept
    Click    selector=\#alerts

Clicking Through Alert Fails
    Run Keyword And Expect Error    Could not find element with selector `#alerts` within timeout.    Click    \#alerts

Future promptinput works
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
    Click    \#alerts
    Get Dialog    ==    None
    Fail

Handle Future Dialogs can be disabled
    Handle Future Dialogs    accept
    New Page    ${LOGIN_URL}
    Click    \#alerts
    Handle Future Dialogs    ignore
    Run Keyword And Expect Error    Could not find element with selector `#alerts` within timeout.    Click    \#alerts

Get Dialog asserts content
    Get Dialog
    Fail
