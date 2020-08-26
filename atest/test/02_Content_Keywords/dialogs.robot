*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}
Test Teardown     Close Page

*** Test Cases ***
Dismiss Alert
    Handle Future Dialogs    action=dismiss
    Click    \#alerts

Accept Alert
    Handle Future Dialogs    action=accept
    Click    \#alerts

Clicking Through Alert Fails
    Run Keyword And Expect Error    Could not find element with selector `#alerts` within timeout.    Click    \#alerts

Promptinput works
    Handle Future Dialogs    action=accept    prompt_input=Some Input String
    Click    \#prompts
    Get Text    \#prompt_result    ==    Some Input String

Dismiss and Promptinput Fails
    Run Keyword And Expect Error    prompt_input is only valid if action is 'accept'    Handle Future Dialogs    action=dismiss    prompt_input=Some Prompt Input
