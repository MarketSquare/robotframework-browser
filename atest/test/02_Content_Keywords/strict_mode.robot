*** Settings ***
Resource    imports.resource

*** Test Cases ***
Set Strict Mode
    ${old_mode} =    Set Strict Mode    False
    Should Be True    ${old_mode}
    ${old_mode} =    Set Strict Mode    True
    Should Not Be True    ${old_mode}
    ${old_mode} =    Set Strict Mode    ${True}
    Should Be True    ${old_mode}

Use Strict Mode
    New Page    ${FORM_URL}
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 12 elements.*
    ...    Get Text    //input
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 12 elements.*
    ...    Get Text    //input    strict=True

When Strict Is False Should Not Fail
    New Page    ${FORM_URL}
    Set Strict Mode    False
    Get Text    //input
    Get Text    //input    strict=False

Strict Mode With Frames
    New Page    ${FRAMES_URL}
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 2 elements.*
    ...    Get Style    //iframe >>> //p    width
    ${width} =    Get Style    //iframe >>> //p    width    strict=False
    Should End With    ${width}    px

Strict Mode With Frame Element
    New Page    ${FRAMES_URL}
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *Error: strict mode violation: selector resolved to 2 elements.*
    ...    Get Style    id=left >>> //input    width
    ${width} =    Get Style    id=left >>> //input    width    strict=False
    Should End With    ${width}    px
