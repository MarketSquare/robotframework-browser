*** Settings ***
Resource          imports.resource
Test Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Dismiss Alert
    [Tags]      dialog
    Handle Future Dialogs    action=dismiss
    Click    \#alerts

Dismiss Alert Check Alert Message
    [Tags]      dialog
    Handle Future Dialogs    action=dismiss     expected_dialog_text=Am an alert
    Click    \#alerts

Dismiss Alert Should fail within incorrect dismiss alert message
    [Tags]      dialog
    Handle Future Dialogs    action=dismiss     expected_dialog_text=incorrect alert text
    Click    \#alerts

Accept Alert
    [Tags]      dialog
    Handle Future Dialogs    action=accept
    Click    \#alerts

Accept Alert Check Alert Message
    [Tags]      dialog
    Handle Future Dialogs    action=accept    expected_dialog_text=Am an alert
    Click    \#alerts

Accept Alert Check fail with incorrect accept alert Message
    [Tags]      dialog
    Handle Future Dialogs    action=accept    expected_dialog_text=incorrect alert text
    Click    \#alerts

Clicking Through Alert Fails
    [Tags]    Not-Implemented
    # The new close page / context / browser gets broken by this?
    Run Keyword And Expect Error    Could not find element with selector `#alerts` within timeout.    Click    \#alerts

Promptinput works
    Handle Future Dialogs    action=accept    prompt_input=Some Input String
    Click    \#prompts
    Get Text    \#prompt_result    ==    Some Input String

Dismiss and Promptinput Fails
    Run Keyword And Expect Error    prompt_input is only valid if action is 'accept'    Handle Future Dialogs    action=dismiss    prompt_input=Some Prompt Input
