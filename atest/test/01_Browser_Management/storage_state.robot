*** Settings ***
Resource          imports.resource
Suite Setup       New Browser

*** Test Cases ***
Save storage state
    New Context
    New Page    ${LOGIN_URL}
    Add Cookies For Storage
    ${STATE_FILE} =    Save Storage State
    Set Suite Variable    ${STATE_FILE}
    File Should Not Be Empty    ${state_file}

Restore Storage State
    New Context    storageState=${STATE_FILE}
    ${cookie}=    Get Cookie    Foo
    Should Be Equal    ${cookie.value}    Bar
    ${cookie}=    Get Cookie    Key
    Should Be Equal    ${cookie.value}    Value

Restore Storage State With Invalid Path
    Run Keyword And Expect Error
    ...    ValueError: storageState argument value '/not/here' is not file, but it should be.
    ...    New Context    storageState=/not/here

Restore Storage State With Invalid File
    Append To File    ${OUTPUT_DIR}/invalid_state_file.json    not valid json
    Run Keyword And Expect Error
    ...    SyntaxError*JSON*
    ...    New Context    storageState=${OUTPUT_DIR}/invalid_state_file.json

*** Keywords ***
Add Cookies For Storage
    ${url} =    Get Url
    Add Cookie    Foo    Bar    url=${url}
    Add Cookie    Key    Value    url=${url}
    Execute JavaScript    localStorage.setItem('bgcolor', 'red');
