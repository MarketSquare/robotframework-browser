*** Settings ***
Resource        imports.resource

Test Setup      New Page    ${LOGIN_URL}

*** Test Cases ***
Dismiss Alert
    Handle Future Dialogs    action=dismiss
    Click    \#alerts

Accept Alert
    Handle Future Dialogs    action=accept
    Click    \#alerts

Clicking Through Alert Fails
    [Tags]    not-implemented
    # The new close page / context / browser gets broken by this?
    Run Keyword And Expect Error
    ...    Could not find element with selector `#alerts` within timeout.
    ...    Click
    ...    \#alerts

Promptinput Works
    Handle Future Dialogs    action=accept    prompt_input=Some Input String
    Click    \#prompts
    Get Text    \#prompt_result    ==    Some Input String

Dismiss And Promptinput Fails
    Run Keyword And Expect Error    prompt_input is only valid if action is 'accept'    Handle Future Dialogs
    ...    action=dismiss    prompt_input=Some Prompt Input

Verify Dialogue Text With Wrong Text
    ${promise} =    Promise To    Wait For Alert    action=accept    prompt_input=Kala    text=Wrong Text
    Click    id=prompts
    Run Keyword And Expect Error
    ...    Alert text was: "Enter a value" but it should have been: "Wrong Text"
    ...    Wait For    ${promise}
    Get Text    id=prompt_result    ==    Kala

Verify Dialogue Text
    ${promise} =    Promise To    Wait For Alert    action=accept    prompt_input=Kalaa tulee    text=Enter a value
    Click    id=prompts
    Wait For    ${promise}
    Get Text    id=prompt_result    ==    Kalaa tulee

Verify Dialogue Text And Dismiss Dialogue
    ${promise} =    Promise To    Wait For Alert    action=dismiss    prompt_input=Kalaa tulee    text=Enter a value
    Click    id=prompts
    Wait For    ${promise}
    Get Text    id=prompt_result    ==    prompt_not_filled

Verify Alert Text And Dismiss Dialogue
    ${promise} =    Promise To    Wait For Alert    action=dismiss    text=Am an alert
    Click    id=alerts
    Wait For    ${promise}

Verify Alert Text And Accept Dialogue
    ${promise} =    Promise To    Wait For Alert    action=accept
    Click    id=alerts
    ${text} =    Wait For    ${promise}
    Should Be Equal    ${text}    Am an alert

Verify Upper Case Action Dialogue Accept
    ${promise} =    Promise To    Wait For Alert    action=ACCEPT
    Click    id=alerts
    ${text} =    Wait For    ${promise}
    Should Be Equal    ${text}    Am an alert

Verify Upper Case Action Dialogue Dismiss
    ${promise} =    Promise To    Wait For Alert    action=DISMISS    text=Am an alert
    Click    id=alerts
    Wait For    ${promise}

Wait For Alert Times Out
    Evaluate JavaScript    ${None}
    ...    async () => window.setTimeout(() => {alert('Am an alert')}, 100)
    Wait For Alert    accept    timeout=1s
    Evaluate JavaScript    ${None}
    ...    async () => window.setTimeout(() => {alert('Am an alert')}, 800)
    TRY
        Wait For Alert    accept    timeout=0.2s
    EXCEPT    TimeoutError*    type=GLOB
        Log    Got expected timeout error
    ELSE
        Fail    Expected timeout error
    END
