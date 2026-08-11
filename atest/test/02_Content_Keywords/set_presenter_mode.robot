*** Settings ***
Resource            imports.resource

Suite Setup         Setup
Suite Teardown      Set Presenter Mode    ${ORIGINAL_PRESENTER_MODE}
Test Setup          Set Presenter Mode    False

*** Variables ***
&{CUSTOM_CONFIG} =          duration=1 sec    width=3px    style=solid    color=red
&{EXP_CUSTOM_CONFIG} =      duration=${{datetime.timedelta(seconds=1)}}    width=3px    style=solid    color=red

${DEFAULT_CONFIG} =         ${{{'duration': datetime.timedelta(seconds=2), 'width': '2px', 'style': 'dotted', 'color': 'blue'}}}

*** Test Cases ***
Enable Presenter Mode With True For Default
    [Documentation]
    ...    LOG 2:3    INFO    Highlighted 1 elements for 2000 ms.
    Set Presenter Mode    True
    ${text} =    Get Text    h1
    Test Presenter Mode    &{DEFAULT_CONFIG}

Disable Presenter Mode With False
    [Documentation]
    ...    LOG 2:2    DEBUG    Text received successfully.
    Set Presenter Mode    False
    ${text} =    Get Text    h1
    ${test_set} =    Set Presenter Mode    No
    ${lib} =    Get Library Instance    Browser
    Should Be True    $lib.presenter_mode == False
    ${test_set} =    Set Presenter Mode    False
    Should Be True    $test_set == False

Enable Presenter Mode With Custom Config
    [Documentation]
    ...    LOG 2:3    INFO    Highlighted 1 elements for 1000 ms.
    Set Presenter Mode    ${CUSTOM_CONFIG}
    ${text} =    Get Text    h1
    Test Presenter Mode    &{EXP_CUSTOM_CONFIG}

Enable Presenter Mode with Dict Literal
    [Documentation]
    ...    LOG 2:3    INFO    Highlighted 1 elements for 500 ms.
    Set Presenter Mode    {"duration": "500ms", "width": "1px", "style": "solid", "color": "yellow"}
    Get Text    h1
    Test Presenter Mode    duration=${{datetime.timedelta(seconds=0.5)}}    width=1px    style=solid    color=yellow

Enable Presenter Mode With Dict Literal And Missing Keys
    [Documentation]
    ...    LOG 2:3    INFO    Highlighted 1 elements for 1500 ms.
    Set Presenter Mode    {"duration": "1500ms"}
    Get Text    h1
    Test Presenter Mode
    ...    duration=${{datetime.timedelta(milliseconds=1500)}}
    ...    width=2px
    ...    style=dotted
    ...    color=blue

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
    Should Be Equal    ${lib.presenter_mode}    ${expected_mode}    types=Any
    ${test_set} =    Set Presenter Mode    False
    Should Be Equal    ${test_set}    ${expected_mode}    types=Any

Setup
    Close Page    ALL
    Ensure Open Page    ${LOGIN_URL}
    Save And Disable Presenter Mode

Save And Disable Presenter Mode
    # Save the original presenter mode for the suite and disable it
    ${old_mode} =    Set Presenter Mode    False
    VAR    ${ORIGINAL_PRESENTER_MODE} =    ${old_mode}    scope=SUITE
