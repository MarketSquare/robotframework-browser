*** Settings ***
Resource            imports.resource

Suite Teardown      Set Strict Mode    True

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
    ...    *strict mode violation*//input*resolved to 12 elements*
    ...    Get Text    //input

When Strict Is False Should Not Fail
    New Page    ${FORM_URL}
    Set Strict Mode    False
    Get Text    //input

Strict Mode In invokePlaywrightMethodStrict With Frames
    New Page    ${FRAMES_URL}
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *strict mode violation*//iframe*resolved to 2 elements*
    ...    Get Style    //iframe >>> //p    width
    Set Strict Mode    False
    ${width} =    Get Style    //iframe >>> //p    width
    Should End With    ${width}    px

Strict Mode In invokePlaywrightMethodStrict With Frame Element
    New Page    ${FRAMES_URL}
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *strict mode violation*//input*resolved to 2 elements*
    ...    Get Style    id=left >>> //input    width
    Set Strict Mode    False
    ${width} =    Get Style    id=left >>> //input    width
    Should End With    ${width}    px

Stirct Mode In invokePlaywrightMethodStrict Without Frame
    New Page    ${FRAMES_URL}
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *strict mode violation*//iframe*resolved to 2 elements*
    ...    Get Style    //iframe    width
    Set Strict Mode    False
    ${width} =    Get Style    //iframe    width
    Should End With    ${width}    px

Stirct Mode In invokePlaywrightMethodStrict Without Frame And
    New Page    ${FRAMES_URL}
    Set Strict Mode    True
    Run Keyword And Expect Error
    ...    *strict mode violation*//iframe*resolved to 2 elements*
    ...    Click    //iframe
    Set Strict Mode    False
    Click    //iframe
