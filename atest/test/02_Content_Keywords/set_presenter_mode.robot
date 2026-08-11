*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Set Presenter Mode    ${ORIGINAL_PRESENTER_MODE}
Test Setup          Set Presenter Mode    False

*** Variables ***
&{CUSTOM_CONFIG} =      duration=3 seconds    width=3px    style=solid    color=red

${DEFAULT_CONFIG} =     ${{{'duration': datetime.timedelta(seconds=2), 'width': '2px', 'style': 'dotted', 'color': 'blue'}}}

*** Test Cases ***
Enable Presenter Mode With True For Default
    [Documentation]
    ...    LOG 2:2    INFO    Stopping coverage
    Set Presenter Mode    True
    ${text} =    Get Text    h1
    Test Presenter Mode    &{DEFAULT_CONFIG}

Disable Presenter Mode With False
    Set Presenter Mode    False
    ${text} =    Get Text    h1
    ${test_set} =    Set Presenter Mode    False
    ${lib} =    Get Library Instance    Browser
    Should Be Equal    ${lib.presenter_mode}    ${False}
    ${test_set} =    Set Presenter Mode    False
    Should Be Equal    ${test_set}    ${False}

Enable Presenter Mode With Custom Config
    Set Presenter Mode    ${CUSTOM_CONFIG}
    ${text} =    Get Text    h1
    Test Presenter Mode    &{CUSTOM_CONFIG}

Enable Presenter Mode with Dict Literal
    Set Presenter Mode    {"duration": "500ms", "width": "1px", "style": "solid", "color": "yellow"}
    Get Text    h1
    Test Presenter Mode    duration=${{datetime.timedelta(seconds=0.5)}}    width=1px    style=solid    color=yellow

Enable Presenter Mode with Dict Literal and Missing Keys
    Set Presenter Mode    {"duration": "1s"}
    Get Text    h1
    Test Presenter Mode    duration=${{datetime.timedelta(seconds=1)}}    width=2px    style=dotted    color=blue

Invalid Config Dictionary Should Fail
    VAR    &{bad_config} =    duration=peter    width=3px
    Run Keyword And Expect Error
    ...    ValueError: Argument 'mode' got value '{'duration': 'peter', 'width': '3px'}' (DotDict) that cannot be converted to HighLightElement or boolean.
    ...    Set Presenter Mode
    ...    ${bad_config}

Invalid Config Dict Literal Should Fail
    Run Keyword And Expect Error
    ...    ValueError: 'Presenter Mode' got value "{'duration': '2sec', 'width': '3px'" (str) that cannot be converted to HighLightElement or boolean.
    ...    Set Presenter Mode
    ...    {'duration': '2sec', 'width': '3px'

*** Keywords ***
Test Presenter Mode
    [Arguments]    &{expected_mode}
    ${lib} =    Get Library Instance    Browser
    Should Be Equal    ${lib.presenter_mode}    ${expected_mode}
    ${test_set} =    Set Presenter Mode    False
    Should Be Equal    ${test_set}    ${expected_mode}

Setup
    Close Page    ALL
    Ensure Open Page    ${LOGIN_URL}
    Save And Disable Presenter Mode

Save And Disable Presenter Mode
    # Save the original presenter mode for the suite and disable it
    ${old_mode} =    Set Presenter Mode    False
    VAR    ${ORIGINAL_PRESENTER_MODE} =    ${old_mode}    scope=SUITE
