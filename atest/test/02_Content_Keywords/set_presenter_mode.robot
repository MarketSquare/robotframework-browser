*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Set Presenter Mode    ${ORIGINAL_PRESENTER_MODE}

*** Variables ***
&{CUSTOM_CONFIG} =      duration=3 seconds    width=3px    style=solid    color=red

*** Test Cases ***
Enable Presenter Mode With True
    ${old_mode} =    Set Presenter Mode    True
    ${text} =    Get Text    h1
    Set Presenter Mode    ${old_mode}

Disable Presenter Mode With False
    ${old_mode} =    Set Presenter Mode    False
    ${text} =    Get Text    h1
    Set Presenter Mode    ${old_mode}

Enable Presenter Mode With Custom Config
    ${old_mode} =    Set Presenter Mode    ${CUSTOM_CONFIG}
    ${text} =    Get Text    h1
    Set Presenter Mode    ${old_mode}

Restore Previous Mode
    Set Presenter Mode    True
    ${previous_mode} =    Set Presenter Mode    False
    Should Be True    ${previous_mode}
    ${previous_mode} =    Set Presenter Mode    ${previous_mode}
    Should Be True    ${previous_mode} == False

Restore Previous Custom Config
    Set Presenter Mode    ${CUSTOM_CONFIG}
    ${previous_mode} =    Set Presenter Mode    False
    Dictionaries Should Be Equal    ${previous_mode}    ${CUSTOM_CONFIG}
    ${previous_mode} =    Set Presenter Mode    ${previous_mode}
    Should Be True    ${previous_mode} == False

Invalid Config Dictionary Should Fail
    VAR    &{bad_config} =    duration=5 seconds    width=3px
    Run Keyword And Expect Error    ValueError: *    Set Presenter Mode    ${bad_config}

*** Keywords ***
Setup
    Close Page    ALL
    Ensure Open Page    ${LOGIN_URL}
    Save And Disable Presenter Mode

Save And Disable Presenter Mode
    # Save the original presenter mode for the suite and disable it
    ${old_mode} =    Set Presenter Mode    False
    VAR    ${ORIGINAL_PRESENTER_MODE} =    ${old_mode}    scope=SUITE
