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

Handle Multiple Alerts
    [Setup]    New Page    ${DIALOGS_TWO_URL}
    ${promise} =    Promise To
    ...    Wait For Alerts
    ...    ["accept", "dismiss"]
    ...    [None, None]
    ...    ["First alert!", None]
    ...    5s
    Click    id=alerts
    ${texts} =    Wait For    ${promise}
    Should Be Equal    ${texts}[0]    First alert!
    Should Be Equal    ${texts}[1]    Second alert!
    Length Should Be    ${texts}    2

Handle Multiple Dialogs With Wrong Number Of Arguments
    [Setup]    New Page    ${DIALOGS_TWO_URL}
    TRY
        Wait For Alerts    ["accept"]    ["foobar", "Am an alert"]    ["Accept", None]    5s
    EXCEPT    ValueError: There was not equal amount of items in actions, prompt_inputs and texts lists. actions: 1, prompt_inputs: 2, texts: 2
        Log    Got expected error, all is good.
    END

Handle Multiple Dialogs With Wrong Texts
    [Setup]    New Page    ${DIALOGS_TWO_URL}
    ${promise} =    Promise To
    ...    Wait For Alerts
    ...    ["accept", "dismiss"]
    ...    [None, None]
    ...    [None, "This is WRONG"]
    ...    5s
    Click    id=alerts
    TRY
        Wait For    ${promise}
    EXCEPT    Alert index 2 text was: "Second alert!" but it should have been: "This is WRONG"
        Log    Got expected error, all is good.
    END

Handle Conform And Prompt
    [Setup]    New Page    ${DIALOGS_TWO_URL}
    ${promise} =    Promise To
    ...    Wait For Alerts
    ...    ["dismiss", "accept"]
    ...    [None, "I am a prompt"]
    ...    ["First alert accepted?", None]
    ...    5s
    Click    id=confirmAndPromt
    ${texts} =    Wait For    ${promise}
    Should Be Equal    ${texts}[0]    First alert accepted?
    Should Be Equal    ${texts}[1]    Input in second alert!
    Length Should Be    ${texts}    2
    Get Text    id=confirm    ==    First alert declined!
    Get Text    id=prompt    ==    Second alert input: I am a prompt

Handle Conform And Prompt
    [Setup]    New Page    ${DIALOGS_TWO_URL}
    ${promise} =    Promise To
    ...    Wait For Alerts
    ...    ["accept", "dismiss"]
    ...    [None, "I am a prompt"]
    ...    ["First alert accepted?", None]
    ...    5s
    Click    id=confirmAndPromt
    ${texts} =    Wait For    ${promise}
    Should Be Equal    ${texts}[0]    First alert accepted?
    Should Be Equal    ${texts}[1]    Input in second alert!
    Length Should Be    ${texts}    2
    Get Text    id=confirm    ==    First alert accepted!
    Get Text    id=prompt    ==    Second alert input: no input
